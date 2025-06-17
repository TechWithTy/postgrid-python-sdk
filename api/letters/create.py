"""Create a new letter in PostGrid.

This module provides functionality to create a new letter order using HTML content
or a template with merge variables.
"""
from __future__ import annotations

from typing import Any, Optional, Union

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import LetterCreateError
from ._requests import LetterCreateRequest
from ._responses import LetterResponse


async def create_letter(
    client: PostGridClient,
    *,
    to: Union[str, dict[str, Any]],
    from_address: Union[str, dict[str, Any]],
    html: Optional[str] = None,
    template_id: Optional[str] = None,
    pdf_url: Optional[str] = None,
    merge_variables: Optional[dict[str, Any]] = None,
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
    size: Optional[str] = None,
) -> LetterResponse:
    """Create a new letter order in PostGrid.

    Args:
        client: An authenticated PostGrid client instance.
        to: Either a contact ID string or a dictionary with address details.
        from_address: Either a contact ID string or a dictionary with address details.
        html: Raw HTML content for the letter (required if not using template_id or pdf_url).
        template_id: ID of a PostGrid template to use (alternative to html).
        pdf_url: URL to a PDF to use as letter content (alternative to html/template).
        merge_variables: Variables for template rendering.
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
        size: Letter size (e.g., "us_letter", "a4").

    Returns:
        The created letter details.

    Raises:
        ValueError: If input validation fails.
        LetterCreateError: If the API returns an error.
    """
    # Validate that we have exactly one content source
    if sum(1 for x in [html, template_id, pdf_url] if x) != 1:
        raise ValueError("Exactly one of html, template_id, or pdf_url must be provided")

    # Prepare the request data
    request_data = LetterCreateRequest(
        to=to if isinstance(to, dict) else {"id": to},
        from_address=from_address if isinstance(from_address, dict) else {"id": from_address},
        html=html,
        template_id=template_id,
        pdf=pdf_url,
        merge_variables=merge_variables or {},
        color="color" if color else "black_white",
        address_placement=address_placement,
        double_sided=double_sided,
        perforated_page=perforated_page,
        extra_service=extra_service,
        envelope_id=envelope_id,
        return_envelope_id=return_envelope_id,
        send_date=send_date,
        description=description,
        express=express,
        metadata=metadata or {},
        mailing_class=mailing_class,
        size=size,
    )

    try:
        response = await client.post(
            "letters",
            data=request_data.model_dump(by_alias=True, exclude_none=True),
            response_model=LetterResponse,
        )
        return response
    except PostGridError as e:
        raise LetterCreateError(f"Failed to create letter: {str(e)}") from e