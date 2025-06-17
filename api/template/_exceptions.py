"""
Custom exceptions for the PostGrid Template API.

This module defines exceptions specific to template operations
in the PostGrid API.
"""
from __future__ import annotations

from ......client import PostGridAPIError


class TemplateError(PostGridAPIError):
    """Base exception for all template-related errors."""
    pass


class TemplateNotFoundError(TemplateError):
    """Raised when a template cannot be found."""
    def __init__(self, template_id: str, message: str | None = None) -> None:
        self.template_id = template_id
        msg = message or f"Template with ID '{template_id}' not found"
        super().__init__(msg)


class TemplateUpdateError(TemplateError):
    """Raised when a template update fails."""
    def __init__(self, template_id: str, message: str | None = None) -> None:
        self.template_id = template_id
        msg = message or f"Failed to update template with ID '{template_id}'"
        super().__init__(msg)


class TemplateDeleteError(TemplateError):
    """Raised when a template deletion fails."""
    def __init__(self, template_id: str, message: str | None = None) -> None:
        self.template_id = template_id
        msg = message or f"Failed to delete template with ID '{template_id}'"
        super().__init__(msg)


class TemplateListError(TemplateError):
    """Raised when listing templates fails."""
    def __init__(self, message: str | None = None) -> None:
        msg = message or "Failed to list templates"
        super().__init__(msg)


class TemplateCreateError(TemplateError):
    """Raised when template creation fails."""
    def __init__(self, message: str | None = None) -> None:
        msg = message or "Failed to create template"
        super().__init__(msg)
