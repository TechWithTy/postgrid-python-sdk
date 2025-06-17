"""
Enums for PostGrid Template API operations.

This module contains enumerations used in the PostGrid Template API
for type safety and validation.
"""
from enum import Enum


class TemplateObjectType(str, Enum):
    """Object types for PostGrid Template API responses."""
    TEMPLATE = "template"