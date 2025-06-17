class TemplateEditorSessionError(Exception):
    """Base exception for template editor session errors."""
    pass

class TemplateEditorSessionNotFoundError(TemplateEditorSessionError):
    """Raised when a template editor session is not found."""
    pass

class TemplateEditorSessionValidationError(TemplateEditorSessionError):
    """Raised when template editor session validation fails."""
    pass