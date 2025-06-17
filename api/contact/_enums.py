"""Enumerations for PostGrid API types and statuses."""
from enum import Enum

class AddressStatus(str, Enum):
    """Status of an address verification."""
    VERIFIED = "verified"
    UNVERIFIED = "unverified"
    FAILED = "failed"

class ContactObjectType(str, Enum):
    """Type of contact object in PostGrid."""
    INDIVIDUAL = "individual"
    COMPANY = "company"
    BOTH = "both"

class VerificationStatus(str, Enum):
    """Status of a verification process."""
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class DeliveryStatus(str, Enum):
    """Status of mail delivery."""
    PROCESSING = "processing"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    RETURNED = "returned_to_sender"
    FAILED = "failed"

class MailType(str, Enum):
    """Type of mail piece."""
    POSTCARD = "postcard"
    LETTER = "letter"
    CHECK = "check"
    SELF_MAILER = "self_mailer"
    PACKAGE = "package"