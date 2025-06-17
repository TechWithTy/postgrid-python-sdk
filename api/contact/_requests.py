"""
Pydantic request models for PostGrid Contact API.

This module defines the request schemas for creating and updating contacts
in the PostGrid API, including support for single-line address contacts.
"""
from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, validator

class ContactAddress(BaseModel):
    address_line1: str = Field(..., alias="addressLine1")
    address_line2: str | None = Field(None, alias="addressLine2")
    city: str
    province_or_state: str = Field(..., alias="provinceOrState")
    postal_or_zip: str = Field(..., alias="postalOrZip")
    country_code: str = Field("CA", alias="countryCode")

    model_config = {
        "populate_by_name": True,
        "extra": "forbid"
    }

class ContactCreateRequest(BaseModel):
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    company_name: str | None = Field(None, alias="companyName")
    email: str | None = None
    phone_number: str | None = Field(None, alias="phoneNumber")
    job_title: str | None = Field(None, alias="jobTitle")
    description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    skip_verification: bool = Field(False, alias="skipVerification")
    force_verified_status: bool = Field(False, alias="forceVerifiedStatus")
    secret: bool = Field(
        False,
        description="If true, the contact will be marked as secret and PII will be redacted"
    )

    # Address fields - can be provided directly or as an Address object
    address_line1: str | None = Field(None, alias="addressLine1")
    address_line2: str | None = Field(None, alias="addressLine2")
    city: str | None = None
    province_or_state: str | None = Field(None, alias="provinceOrState")
    postal_or_zip: str | None = Field(None, alias="postalOrZip")
    country_code: str = Field("CA", alias="countryCode")
    
    @validator('first_name', 'company_name')
    def validate_required_fields(
        cls,
        v: str | None,
        values: dict[str, Any],
        **kwargs: Any,
    ) -> str | None:
        """Ensure either first_name or company_name is provided."""
        field = kwargs.get('field').name
        other_field = 'company_name' if field == 'first_name' else 'first_name'

        if not v and not values.get(other_field):
            raise ValueError(f'Either {field} or {other_field} must be provided')
        return v

    model_config = {
        "populate_by_name": True,
        "extra": "forbid"
    }
        
class SingleLineContactCreateRequest(ContactCreateRequest):
    """Model for creating a contact with a single-line address.

    PostGrid will automatically parse and verify the address. This model
    enforces that only address_line1 is provided, while other address
    components are explicitly set to None to prevent confusion.
    """
    address_line1: str = Field(..., alias="addressLine1")

    # Remove individual address components to avoid confusion
    address_line2: None = None
    city: None = None
    province_or_state: None = None
    postal_or_zip: None = None

    model_config = {
        "populate_by_name": True,
        "extra": "forbid"
    }
