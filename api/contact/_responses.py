# app/core/third_party_integrations/postgrid/api/route/_responses.py
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import  Optional, Literal

from pydantic import BaseModel, Field

# Enums for response statuses
class VerificationStatus(str, Enum):
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    PENDING = "pending"
    FAILED = "failed"

class ContactObjectType(str, Enum):
    CONTACT = "contact"

# Address Models
class AddressVerification(BaseModel):
    success: bool
    errors: list[dict[str, str]] | None = None
    verified_components: dict[str, str | bool] | None = Field(
        default=None,
        alias="verifiedComponents",
    )
    
    class Config:
        allow_population_by_field_name = True

class AddressResponse(BaseModel):
    id: str
    object: Literal["address"] = "address"
    status: str
    description: Optional[str] = None
    address_line1: str = Field(..., alias="addressLine1")
    address_line2: Optional[str] = Field(None, alias="addressLine2")
    city: str
    province_or_state: str = Field(..., alias="provinceOrState")
    postal_or_zip: str = Field(..., alias="postalOrZip")
    country_code: str = Field(..., alias="countryCode")
    country: str
    verification: Optional[AddressVerification] = None
    metadata: dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# Contact Models
class ContactResponse(BaseModel):
    id: str
    object: ContactObjectType = Field(default=ContactObjectType.CONTACT)
    first_name: str | None = Field(None, alias="firstName")
    last_name: str | None = Field(None, alias="lastName")
    company_name: str | None = Field(None, alias="companyName")
    email: str | None = None
    phone_number: str | None = Field(None, alias="phoneNumber")
    job_title: str | None = Field(None, alias="jobTitle")
    description: str | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
    address: AddressResponse | None = None
    verification_status: VerificationStatus | None = Field(
        None, alias="verificationStatus"
    )
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ContactListResponse(BaseModel):
    data: list[ContactResponse]
    object: Literal["list"] = "list"
    limit: int
    skip: int
    total_count: int = Field(..., alias="totalCount")
    
    class Config:
        allow_population_by_field_name = True


class ContactDeleteResponse(BaseModel):
    """Response model for contact deletion."""
    id: str
    object: Literal["contact"] = "contact"
    deleted: bool = True
    
    class Config:
        allow_population_by_field_name = True