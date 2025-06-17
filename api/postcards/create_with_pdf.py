"""
Core functionality for creating postcards with PDF uploads using the PostGrid API.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, Union, BinaryIO

import httpx

from ...client import PostGridClient
from ._exceptions import PostcardError, PostcardValidationError
from ._responses import PostcardResponse
from ._enums import PostcardSize, MailingClass


async def create_postcard_with_pdf(
    client: PostGridClient,
    *,
    to: Union[str, Dict[str, Any]],
    pdf: Union[str, Path, BinaryIO],
    size: Union[PostcardSize, str] = PostcardSize.NINE_BY_SIX,
    from_contact: Optional[Union[str, Dict[str, Any]]] = None,
    send_date: Optional[Union[datetime, str]] = None,
    express: bool = False,
    description: Optional[str] = None,
    mailing_class: Union[MailingClass, str] = MailingClass.FIRST_CLASS,
    merge_variables: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> PostcardResponse:
    """
    Create a new postcard by uploading a PDF.

    Args:
        client: Authenticated PostGrid client
        to: Either a contact ID or a contact object for the recipient
        pdf: Path to the PDF file or a file-like object containing the PDF
        size: Size of the postcard (6x4, 9x6, or 11x6)
        from_contact: Optional contact ID or object for the sender
        send_date: Optional date when the postcard should be sent
        express: Whether to use express shipping
        description: Optional description for the postcard
        mailing_class: Mailing class (first_class or standard_class)
        merge_variables: Optional variables for template interpolation
        metadata: Optional metadata to attach to the postcard

    Returns:
        PostcardResponse: The created postcard

    Raises:
        PostcardValidationError: If required fields are missing or invalid
        PostcardError: For other API errors
        FileNotFoundError: If the PDF file is not found
    """
    # Prepare the form data
    files = {}
    data: Dict[str, Any] = {
        "size": str(size),
        "express": str(express).lower(),
        "mailingClass": str(mailing_class)
    }

    # Handle the recipient
    if isinstance(to, dict):
        for key, value in to.items():
            data[f"to[{key}]"] = str(value)
    else:
        data["to"] = str(to)

    # Handle the sender if provided
    if from_contact:
        if isinstance(from_contact, dict):
            for key, value in from_contact.items():
                data[f"from[{key}]"] = str(value)
        else:
            data["from"] = str(from_contact)

    # Handle the PDF file
    if isinstance(pdf, (str, Path)):
        pdf_path = Path(pdf)
        if not pdf_path.is_file():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        files["pdf"] = (pdf_path.name, open(pdf_path, "rb"), "application/pdf")
    else:
        # Assume it's a file-like object
        files["pdf"] = ("postcard.pdf", pdf, "application/pdf")

    # Add optional fields if provided
    if send_date:
        data["sendDate"] = send_date.isoformat() if isinstance(send_date, datetime) else send_date
    if description:
        data["description"] = description
    if merge_variables:
        for key, value in merge_variables.items():
            data[f"mergeVariables[{key}]"] = str(value)
    if metadata:
        for key, value in metadata.items():
            data[f"metadata[{key}]"] = str(value)

    try:
        async with client:
            response = await client.post(
                "/postcards",
                data=data,
                files=files
            )
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get('error', {}).get('message', 'Invalid request')
            raise PostcardValidationError(f"Validation error: {error_detail}") from e
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error creating postcard with PDF: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e
    finally:
        # Ensure any opened files are properly closed
        if "pdf" in files and not isinstance(pdf, (str, Path)):
            files["pdf"][1].close()