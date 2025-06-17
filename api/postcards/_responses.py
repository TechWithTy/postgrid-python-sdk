from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Dict, Any, List
from datetime import datetime

from ._enums import PostcardStatus, MailingClass, ObjectType, AddressStatus

class ContactResponse(BaseModel):
    """Contact information in the response."""
    id: str = Field(..., description="Unique identifier for the contact")
    object: ObjectType = Field(ObjectType.CONTACT, description="Type of the object")
    firstName: Optional[str] = Field(None, description="First name of the contact")
    lastName: Optional[str] = Field(None, description="Last name of the contact")
    addressLine1: Optional[str] = Field(None, description="First line of the address")
    addressLine2: Optional[str] = Field(None, description="Second line of the address")
    addressStatus: Optional[AddressStatus] = Field(None, description="Status of the address validation")
    city: Optional[str] = Field(None, description="City name")
    provinceOrState: Optional[str] = Field(None, description="Province or state code")
    postalOrZip: Optional[str] = Field(None, description="Postal or ZIP code")
    country: Optional[str] = Field(None, description="Country name")
    countryCode: Optional[str] = Field(None, description="ISO 3166-1 alpha-2 country code")

class PostcardResponse(BaseModel):
    """Response model for a postcard."""
    id: str = Field(..., description="Unique identifier prefixed with postcard_")
    object: ObjectType = Field(ObjectType.POSTCARD, description="Type of the object")
    status: PostcardStatus = Field(..., description="Current status of the postcard")
    imbStatus: Optional[str] = Field(None, description="Intelligent-Mail barcode status")
    live: bool = Field(..., description="Whether this is a live mode postcard")
    description: Optional[str] = Field(None, description="Description of the postcard")
    sendDate: datetime = Field(..., description="Scheduled send date")
    size: str = Field(..., description="Size of the postcard (6x4, 9x6, or 11x6)")
    to: ContactResponse = Field(..., description="Recipient contact information")
    from_contact: Optional[ContactResponse] = Field(
        None,
        alias="from",
        description="Sender contact information"
    )
    frontHTML: Optional[str] = Field(None, description="HTML for the front of the postcard")
    backHTML: Optional[str] = Field(None, description="HTML for the back of the postcard")
    frontTemplate: Optional[str] = Field(None, description="Template ID for the front")
    backTemplate: Optional[str] = Field(None, description="Template ID for the back")
    uploadedPDF: Optional[HttpUrl] = Field(None, description="URL to the uploaded PDF")
    url: Optional[HttpUrl] = Field(None, description="URL to preview the postcard")
    mailingClass: MailingClass = Field(..., description="Mailing class used")
    mergeVariables: Optional[Dict[str, Any]] = Field(None, description="Merge variables used")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    createdAt: datetime = Field(..., description="Creation timestamp")
    updatedAt: datetime = Field(..., description="Last update timestamp")

class PostcardListResponse(BaseModel):
    """Response model for listing postcards."""
    data: List[PostcardResponse] = Field(..., description="List of postcards")
    object: str = Field(..., description="Type of the response")
    next_url: Optional[HttpUrl] = Field(None, description="URL for the next page of results")
    previous_url: Optional[HttpUrl] = Field(None, description="URL for the previous page of results")
    count: int = Field(..., description="Total number of postcards available")