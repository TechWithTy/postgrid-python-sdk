"""Pydantic request models for the PostGrid Letter API."""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator, model_validator

from ._enums import (
    AddressPlacement,
    ColorMode,
    EnvelopeType,
    ExtraService,
    MailingClass,
    PaperSize,
    PerforatedPage,
    PrintSided,
)


class Address(BaseModel):
    """Address model for letter recipients and senders."""

    name: str = Field(..., description="Recipient or sender name", min_length=1, max_length=100)
    company_name: str | None = Field(None, max_length=100)
    address_line1: str = Field(..., description="Address line 1", min_length=1, max_length=200, alias="line1")
    address_line2: str | None = Field(None, description="Address line 2", max_length=200, alias="line2")
    city: str = Field(..., min_length=1, max_length=100)
    province_or_state: str = Field(..., min_length=1, max_length=100, alias="state")
    postal_or_zip: str = Field(..., min_length=1, max_length=20, alias="postal_code")
    country: str = Field("US", description="ISO 3166-1 alpha-2 country code", min_length=2, max_length=2)
    phone_number: str | None = Field(None, max_length=20)
    email: str | None = Field(None, max_length=100)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str | None) -> str | None:
        if v and "@" not in v:
            raise ValueError("Invalid email format")
        return v

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class LetterMetadata(BaseModel):
    """Custom metadata for letters (max 20 keys, 500 chars per value)."""

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @model_validator(mode="after")
    def validate_metadata_size(self) -> "LetterMetadata":
        if len(self.model_dump(exclude_unset=True)) > 20:
            raise ValueError("Metadata cannot exceed 20 key-value pairs")
        for k, v in self.model_dump(exclude_unset=True).items():
            if v and len(str(v)) > 500:
                raise ValueError(f"Metadata value for '{k}' exceeds 500 character limit")
        return self


class LetterCreateRequest(BaseModel):
    """Model for creating a letter with all PostGrid API options."""

    # Required fields
    to: Address = Field(..., description="Recipient address")
    from_address: Address = Field(..., alias="from", description="Return address")
    
    # Content (one of these is required)
    html: str | None = Field(
        None,
        description="Raw HTML content (if not using template)",
        min_length=1,
        max_length=100_000,
    )
    template_id: str | None = Field(
        None,
        description="PostGrid template ID to use instead of raw HTML",
        min_length=1,
        max_length=100,
    )
    pdf: HttpUrl | None = Field(
        None,
        description="URL to a PDF to use as the letter content (max 50MB)",
    )
    
    # Template rendering
    merge_variables: dict[str, Any] | None = Field(
        None,
        description="Variables for template rendering (if using template)",
        max_length=100,
    )
    
    # Print options
    color: ColorMode = Field(
        ColorMode.BLACK_WHITE,
        description="Print color mode (color costs more)",
    )
    paper_size: PaperSize = Field(
        PaperSize.LETTER,
        description="Output paper size (affects pricing)",
    )
    print_sided: PrintSided = Field(
        PrintSided.SIMPLEX,
        description="Single or double sided printing (duplex costs more)",
    )
    
    # Mailing options
    mailing_class: MailingClass = Field(
        MailingClass.STANDARD_CLASS,
        description="Mailing class (first_class is faster but more expensive)",
    )
    envelope_type: EnvelopeType = Field(
        EnvelopeType.STANDARD_DOUBLE_WINDOW,
        description="Type of envelope to use",
    )
    address_placement: AddressPlacement = Field(
        AddressPlacement.TOP_FIRST_PAGE,
        description="Where to place the recipient address",
    )
    perforated_page: PerforatedPage | None = Field(
        None,
        description="Page number to add perforation (only page 1 supported)",
    )
    extra_services: list[ExtraService] = Field(
        default_factory=list,
        description="Additional mailing services (certified, registered, etc.)",
    )
    
    # Scheduling
    send_date: date | None = Field(
        None,
        description="Date to mail the letter (must be in the future, defaults to next business day)",
    )
    
    # Metadata
    description: str | None = Field(
        None,
        description="Internal description (not visible to recipient)",
        max_length=200,
    )
    metadata: LetterMetadata | None = Field(
        None,
        description="Custom metadata (max 20 key-value pairs, 500 chars each)",
    )
    
    # Advanced options
    double_sided_custom_margin: float | None = Field(
        None,
        ge=0.25,
        le=1.5,
        description="Custom margin in inches for double-sided printing (0.25-1.5)",
    )
    
    # Validation
    @model_validator(mode="after")
    def validate_send_date(self) -> "LetterCreateRequest":
        if self.send_date and self.send_date < date.today():
            raise ValueError("Send date must be in the future")
        return self
        
    @model_validator(mode="after")
    def validate_extra_services(self) -> "LetterCreateRequest":
        if self.extra_services and len(self.extra_services) != len(set(self.extra_services)):
            raise ValueError("Duplicate extra services not allowed")
        return self

    @model_validator(mode="after")
    def validate_content(self) -> "LetterCreateRequest":
        """Ensure exactly one content source is provided."""
        content_sources = [
            bool(self.html),
            bool(self.template_id),
            bool(self.pdf),
        ]
        if sum(content_sources) != 1:
            raise ValueError(
                "Exactly one of 'html', 'template_id', or 'pdf' must be provided"
            )
        return self

    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class LetterUpdateRequest(BaseModel):
    """Update mutable fields of a letter before it is processed.
    
    Only fields that can be updated after creation are included here.
    """
    
    description: str | None = Field(
        None,
        description="Internal description (not visible to recipient)",
        max_length=200,
    )
    metadata: LetterMetadata | None = Field(
        None,
        description="Custom metadata (replaces all existing metadata)",
    )
    send_date: date | None = Field(
        None,
        description=(
            "New send date (must be in the future and before original send date, "
            "if the letter hasn't been sent yet)"
        ),
    )
    
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
    
    @model_validator(mode="after")
    def validate_send_date(self) -> "LetterUpdateRequest":
        if self.send_date and self.send_date < date.today():
            raise ValueError("New send date must be in the future")
        return self


class LetterListRequest(BaseModel):
    """Filter and pagination parameters for listing letters."""
    
    # Pagination
    limit: int = Field(
        10,
        ge=1,
        le=100,
        description="Number of records to return (1-100)",
    )
    offset: int = Field(
        0,
        ge=0,
        description="Number of records to skip for pagination",
    )
    
    # Filters
    status: str | None = Field(
        None,
        description=(
            "Filter by status (draft, queued, processing, mailed, delivered, "
            "cancelled, failed)"
        ),
    )
    created_after: datetime | None = Field(
        None,
        description="Filter by creation date (ISO 8601 format)",
    )
    created_before: datetime | None = Field(
        None,
        description="Filter by creation date (ISO 8601 format)",
    )
    send_date_after: date | None = Field(
        None,
        description="Filter by scheduled send date (YYYY-MM-DD)",
    )
    send_date_before: date | None = Field(
        None,
        description="Filter by scheduled send date (YYYY-MM-DD)",
    )
    
    # Sorting
    sort_by: Literal["created_at", "send_date"] = Field(
        "created_at",
        description="Field to sort results by",
    )
    sort_order: Literal["asc", "desc"] = Field(
        "desc",
        description="Sort order (ascending or descending)",
    )
    
    model_config = ConfigDict(extra="forbid")
    
    @model_validator(mode="after")
    def validate_date_ranges(self) -> "LetterListRequest":
        if self.created_after and self.created_before and self.created_after > self.created_before:
            raise ValueError("'created_after' must be before 'created_before'")
            
        if self.send_date_after and self.send_date_before and self.send_date_after > self.send_date_before:
            raise ValueError("'send_date_after' must be before 'send_date_before'")
            
        return self
