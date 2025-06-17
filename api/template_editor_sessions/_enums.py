from enum import Enum

class TemplateEditorSessionStatus(str, Enum):
    """Status of a template editor session."""
    ACTIVE = "active"
    EXPIRED = "expired"
    DELETED = "deleted"