"""Create a new letter in PostGrid using a PDF file.

This module provides functionality to create a new letter order by uploading a PDF file
that will be stamped and mailed by PostGrid.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Optional, Union, BinaryIO

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterCreateError
from ._requests import LetterCreateRequest
from ._responses import LetterResponse


async def create_letter_with_pdf(
    client: PostGridClient,
    *,
    to: Union[str, dict[str, Any]],
    from_address: Union[str, dict[str, Any]],
    pdf_file: Union[str, Path, BinaryIO],
    color: bool = False,
    address_placement: str = "top_first_page",
    double_sided: bool = False,
    perforated_page: Optional[int] = None,
    extra_service: Optional[str] = None,
    envelope_id: Optional[str] = None,
    return_envelope_id: Optional[str] = None,
    send_date: Optional[str] = None,
    description: Optional[str] = None,
    express: bool = False,
    metadata: Optional[dict[str, str]] = None,
    mailing_class: str = "first_class",
    merge_variables: Optional[dict[str, Any]] = None,
    size: Optional[str] = None,
) -> LetterResponse:
    """Create a new letter order in PostGrid using a PDF file.

    Args:
        client: An authenticated PostGrid client instance.
        to: Either a contact ID string or a dictionary with address details.
        from_address: Either a contact ID string or a dictionary with address details.
        pdf_file: Path to a PDF file, file-like object, or URL to a PDF.
        color: Whether to print in color (costs more).
        address_placement: Where to place the address ("top_first_page" or "insert_blank_page").
        double_sided: Whether to print on both sides of the paper.
        perforated_page: Page number to perforate (currently only 1 is supported).
        extra_service: Extra service like "certified" or "registered".
        envelope_id: ID of a custom envelope.
        return_envelope_id: ID of a return envelope.
        send_date: When to send the letter (ISO 8601 format).
        description: Internal description of the letter.
        express: Whether to use express shipping.
        metadata: Custom metadata (key-value pairs, max 20 keys, 500 chars each).
        mailing_class: Mailing class ("first_class" or "standard").
        merge_variables: Variables for template rendering (if template is used).
        size: Letter size (e.g., "us_letter", "a4").

    Returns:
        The created letter details.

    Raises:
        ValueError: If input validation fails.
        LetterCreateError: If the API returns an error.
    """
    # Prepare the form data
    form_data = {
        "to": to if isinstance(to, str) else str(to),
        "from": from_address if isinstance(from_address, str) else str(from_address),
        "addressPlacement": address_placement,
        "doubleSided": str(double_sided).lower(),
        "color": str(color).lower(),
        "express": str(express).lower(),
        "mailingClass": mailing_class,
    }

    # Add optional fields if provided
    if perforated_page is not None:
        form_data["perforatedPage"] = str(perforated_page)
    if extra_service:
        form_data["extraService"] = extra_service
    if envelope_id:
        form_data["envelope"] = envelope_id
    if return_envelope_id:
        form_data["returnEnvelope"] = return_envelope_id
    if send_date:
        form_data["sendDate"] = send_date
    if description:
        form_data["description"] = description
    if size:
        form_data["size"] = size

    # Add metadata and merge variables
    if metadata:
        for key, value in metadata.items():
            form_data[f"metadata[{key}]"] = str(value)
    
    if merge_variables:
        for key, value in merge_variables.items():
            form_data[f"mergeVariables[{key}]"] = str(value)

    # Handle the PDF file
    files = {}
    if isinstance(pdf_file, (str, Path)):
        # It's a file path
        pdf_path = Path(pdf_file)
        if not pdf_path.is_file():
            raise ValueError(f"PDF file not found: {pdf_path}")
        files["pdf"] = (pdf_path.name, open(pdf_path, "rb"), "application/pdf")
    elif hasattr(pdf_file, "read"):
        # It's a file-like object
        files["pdf"] = ("document.pdf", pdf_file, "application/pdf")
    else:
        # Assume it's a URL
        form_data["pdf"] = str(pdf_file)

    try:
        response = await client.post(
            "letters",
            data=form_data,
            files=files if files else None,
            response_model=LetterResponse,
        )
        return response
    except PostGridError as e:
        raise LetterCreateError(f"Failed to create letter with PDF: {str(e)}") from e
    finally:
        # Make sure to close any file handles we opened
        if files and "pdf" in files:
            files["pdf"][1].close()