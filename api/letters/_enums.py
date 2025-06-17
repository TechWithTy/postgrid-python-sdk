"""Enums for the PostGrid Letter API.

This module defines constants and enumerations used throughout the
letter request/response models.
"""
from __future__ import annotations

from enum import Enum
from typing import Literal, TypeAlias


class LetterObjectType(str, Enum):
    """PostGrid identifies letters with the object type `letter`."""

    LETTER = "letter"


class LetterStatus(str, Enum):
    """Possible lifecycle states for a letter."""

    DRAFT = "draft"
    QUEUED = "queued"
    PROCESSING = "processing"
    MAILED = "mailed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ColorMode(str, Enum):
    """Print color options."""

    BLACK_WHITE = "black_white"
    COLOR = "color"


class PaperSize(str, Enum):
    """Supported paper sizes."""

    LETTER = "letter"  # 8.5" x 11"
    LEGAL = "legal"    # 8.5" x 14"
    A4 = "a4"          # 210mm x 297mm


class PrintSided(str, Enum):
    """Simplex/Duplex printing."""

    SIMPLEX = "simplex"  # Single-sided
    DUPLEX = "duplex"    # Double-sided


class MailingClass(str, Enum):
    """Mailing class for letters."""

    FIRST_CLASS = "first_class"
    STANDARD_CLASS = "standard_class"


class EnvelopeType(str, Enum):
    """Envelope types for letters."""

    STANDARD_DOUBLE_WINDOW = "standard_double_window"
    FLAT = "flat"


class AddressPlacement(str, Enum):
    """Where to place the address on the letter."""

    TOP_FIRST_PAGE = "top_first_page"
    INSERT_BLANK_PAGE = "insert_blank_page"


class ExtraService(str, Enum):
    """Extra services available for letters."""

    CERTIFIED = "certified"
    REGISTERED = "registered"


class LetterSize(str, Enum):
    """Supported letter sizes."""

    US_LETTER = "us_letter"  # 8.5" x 11"
    US_LEGAL = "us_legal"    # 8.5" x 14"
    A4 = "a4"                # 210mm x 297mm
    POSTCARD = "postcard"     # 4" x 6" or 4.25" x 6"


# Type aliases for better type hints
PerforatedPage: TypeAlias = Literal[1]  # Currently only page 1 can be perforated
