from enum import StrEnum

class PostcardStatus(StrEnum):
    """Possible status values for a Postcard in PostGrid."""
    DRAFT = "draft"
    RENDERED = "rendered"
    TRANSFORMED = "transformed"
    PRINTED = "printed"
    MAILED = "mailed"
    IN_TRANSIT = "in_transit"
    PROCESSED = "processed"
    RETURNED = "returned"
    FAILED = "failed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    READY = "ready"

class AddressStatus(StrEnum):
    """Possible address validation statuses."""
    CORRECTED = "corrected"
    VALID = "valid"
    INVALID = "invalid"

class MailingClass(StrEnum):
    """Mailing class options."""
    FIRST_CLASS = "first_class"
    STANDARD_CLASS = "standard_class"

class PostcardSize(StrEnum):
    """Available postcard sizes."""
    SIX_BY_FOUR = "6x4"
    NINE_BY_SIX = "9x6"
    ELEVEN_BY_SIX = "11x6"

class ObjectType(StrEnum):
    """Object types in PostGrid API."""
    POSTCARD = "postcard"
    CONTACT = "contact"