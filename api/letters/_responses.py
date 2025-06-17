"""Pydantic response models for the PostGrid Letter API.

This module defines the response models that map to the PostGrid API responses
for letter-related operations. These models are used to parse and validate
the API responses and provide type hints for the response data.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from ._enums import (
    AddressPlacement,
    ColorMode,
    EnvelopeType,
    ExtraService,
    LetterObjectType,
    LetterStatus,
    MailingClass,
    PaperSize,
    PerforatedPage,
    PrintSided,
)


class AddressResponse(BaseModel):
    """Address object returned by PostGrid.
    
    Represents a postal address with validation and formatting.
    """

    id: str = Field(..., description="Unique identifier for the address")
    name: str = Field(..., description="Recipient or sender name")
    company_name: str | None = Field(None, description="Company name")
    line1: str = Field(..., description="First line of the address")
    line2: str | None = Field(None, description="Second line of the address")
    city: str = Field(..., description="City or locality")
    province_or_state: str = Field(..., alias="state", description="State or province code")
    postal_or_zip: str = Field(..., alias="postal_code", description="Postal or ZIP code")
    country: str = Field(..., description="ISO 3166-1 alpha-2 country code")
    phone_number: str | None = Field(None, description="Contact phone number")
    email: str | None = Field(None, description="Contact email address")
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "adr_1234567890abcdef",
                "name": "John Doe",
                "company_name": "Acme Inc.",
                "line1": "123 Main St",
                "line2": "Apt 4B",
                "city": "New York",
                "state": "NY",
                "postal_code": "10001",
                "country": "US",
                "phone_number": "+12125551234",
                "email": "john@example.com"
            }
        }
    )


class LetterBaseResponse(BaseModel):
    """Common fields shared by all letter responses.
    
    Contains the core metadata and status information for a letter.
    """

    id: str = Field(..., description="Unique identifier for the letter")
    object: LetterObjectType = Field(..., description="Type of the object (always 'letter')")
    status: LetterStatus = Field(..., description="Current status of the letter")
    description: str | None = Field(None, description="User-provided description")
    color: ColorMode = Field(..., description="Print color mode")
    paper_size: PaperSize = Field(..., description="Paper size used for the letter")
    print_sided: PrintSided = Field(..., description="Single or double-sided printing")
    mailing_class: MailingClass = Field(..., description="Mailing class (first_class or standard_class)")
    envelope_type: EnvelopeType = Field(..., description="Type of envelope used")
    address_placement: AddressPlacement = Field(..., description="Where the address is placed on the letter")
    
    # Content information
    template_id: str | None = Field(None, description="ID of the template used, if any")
    pdf_url: HttpUrl | None = Field(None, description="URL to the PDF content, if available")
    
    # Tracking and status
    tracking_events: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of tracking events for the letter"
    )
    expected_delivery_date: date | None = Field(
        None,
        description="Estimated delivery date (if available)"
    )
    
    # Timestamps
    send_date: date | None = Field(None, description="Date the letter was/will be sent")
    created_at: datetime = Field(..., description="When the letter was created")
    updated_at: datetime = Field(..., description="When the letter was last updated")
    mailed_at: datetime | None = Field(None, description="When the letter was mailed")
    delivered_at: datetime | None = Field(None, description="When the letter was delivered")
    
    # Metadata
    metadata: dict[str, str] | None = Field(
        None,
        description="Custom metadata associated with the letter"
    )
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "letter_1234567890abcdef",
                "object": "letter",
                "status": "mailed",
                "description": "Monthly invoice",
                "color": "black_white",
                "paper_size": "letter",
                "print_sided": "simplex",
                "mailing_class": "first_class",
                "envelope_type": "standard_double_window",
                "address_placement": "top_first_page",
                "template_id": "tmpl_1234567890abcdef",
                "send_date": "2023-06-15",
                "expected_delivery_date": "2023-06-20",
                "created_at": "2023-06-14T10:30:00Z",
                "updated_at": "2023-06-15T08:15:00Z",
                "mailed_at": "2023-06-15T08:15:00Z",
                "metadata": {"invoice_id": "INV-2023-001"}
            }
        }
    )


class LetterResponse(LetterBaseResponse):
    """Complete letter object with all details.
    
    This model represents a full letter response from the PostGrid API,
    including the complete recipient and sender address information.
    """

    to: AddressResponse = Field(..., description="Recipient address details")
    from_address: AddressResponse = Field(
        ...,
        alias="from",
        description="Sender/return address details"
    )
    
    # Content URLs
    url: HttpUrl | None = Field(
        None,
        description="[DEPRECATED] Use pdf_url instead. URL to the rendered PDF"
    )
    pdf_url: HttpUrl | None = Field(
        None,
        description="URL to download the final rendered PDF"
    )
    thumbnails: list[dict[str, str]] = Field(
        default_factory=list,
        description="Thumbnail URLs for the letter pages"
    )
    
    # Additional details
    pages: int = Field(..., description="Number of pages in the letter")
    price_cents: int | None = Field(
        None,
        description="Price of the letter in cents"
    )
    price_currency: str = Field(
        "USD",
        description="Currency code for the price (ISO 4217)"
    )
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "id": "letter_1234567890abcdef",
                "object": "letter",
                "status": "mailed",
                "to": {
                    "id": "adr_1234567890abcdef",
                    "name": "John Doe",
                    "line1": "123 Main St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "US"
                },
                "from": {
                    "id": "adr_0987654321abcdef",
                    "name": "Acme Inc.",
                    "line1": "456 Business Ave",
                    "city": "San Francisco",
                    "state": "CA",
                    "postal_code": "94105",
                    "country": "US"
                },
                "pdf_url": "https://api.postgrid.com/v1/letters/letter_1234567890abcdef/pdf",
                "pages": 2,
                "price_cents": 199,
                "price_currency": "USD"
            }
        }
    )


class LetterListResponse(BaseModel):
    """Paginated list of letters with metadata.
    
    This model represents a paginated response containing a list of letters
    along with pagination metadata.
    """

    data: list[LetterResponse] = Field(
        ...,
        description="List of letter objects"
    )
    total: int = Field(
        ...,
        ge=0,
        description="Total number of letters matching the filter criteria"
    )
    limit: int = Field(
        ...,
        ge=1,
        le=100,
        description="Maximum number of items returned per page"
    )
    offset: int = Field(
        ...,
        ge=0,
        description="Number of items skipped in the result set"
    )
    has_more: bool = Field(
        ...,
        description="Whether there are more items available beyond the current page"
    )
    
    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "data": [
                    {
                        "id": "letter_1234567890abcdef",
                        "object": "letter",
                        "status": "mailed",
                        "created_at": "2023-06-14T10:30:00Z"
                    }
                ],
                "total": 1,
                "limit": 10,
                "offset": 0,
                "has_more": False
            }
        }
    )
