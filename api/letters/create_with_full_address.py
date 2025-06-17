"""Create a new letter in PostGrid with full contact information.

This module provides functionality to create a new letter order using full contact
information for both sender and recipient, rather than just contact IDs.
"""
from __future__ import annotations

from typing import Any, Optional, Union

from ...client import PostGridClient
from .._exceptions import PostGridError
from ._enums import AddressPlacement, ColorMode, MailingClass
from ._exceptions import LetterCreateError
from ._requests import Address, LetterCreateRequest
from ._responses import LetterResponse


async def create_letter_with_full_address(
    client: PostGridClient,
    *,
    # Recipient details
    to_address: dict[str, Any],
    # Sender details
    from_address: dict[str, Any],
    # Content
    html: Optional[str] = None,
    template_id: Optional[str] = None,
    pdf_url: Optional[str] = None,
    # Address options
    address_placement: Union[AddressPlacement, str] = AddressPlacement.TOP_FIRST_PAGE,
    # Print options
    color: Union[bool, ColorMode] = False,
    double_sided: bool = False,
    perforated_page: Optional[int] = None,
    # Envelope options
    extra_service: Optional[str] = None,
    envelope_id: Optional[str] = None,
    return_envelope_id: Optional[str] = None,
    # Delivery options
    send_date: Optional[str] = None,
    express: bool = False,
    mailing_class: Union[MailingClass, str] = MailingClass.FIRST_CLASS,
    # Metadata
    description: Optional[str] = None,
    merge_variables: Optional[dict[str, Any]] = None,
    metadata: Optional[dict[str, str]] = None,
    size: Optional[str] = None,
) -> LetterResponse:
    """Create a new letter order with full contact information.

    Args:
        client: An authenticated PostGrid client instance.
        to_address: Dictionary containing recipient's address details.
        from_address: Dictionary containing sender's address details.
        html: Raw HTML content for the letter.
        template_id: ID of a PostGrid template to use.
        pdf_url: URL to a PDF to use as letter content.
        address_placement: Where to place the address.
        color: Whether to print in color (costs more).
        double_sided: Whether to print on both sides of the paper.
        perforated_page: Page number to perforate.
        extra_service: Extra service like "certified" or "registered".
        envelope_id: ID of a custom envelope.
        return_envelope_id: ID of a return envelope.
        send_date: When to send the letter (ISO 8601 format).
        express: Whether to use express shipping.
        mailing_class: Mailing class ("first_class" or "standard").
        description: Internal description of the letter.
        merge_variables: Variables for template rendering.
        metadata: Custom metadata (key-value pairs).
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

    # Convert string enums if needed
    if isinstance(address_placement, str):
        address_placement = AddressPlacement(address_placement.lower())
    if isinstance(color, bool):
        color = ColorMode.COLOR if color else ColorMode.BLACK_WHITE
    if isinstance(mailing_class, str):
        mailing_class = MailingClass(mailing_class.lower())

    # Create address objects
    try:
        to_contact = Address(**to_address)
        from_contact = Address(**from_address)
    except Exception as e:
        raise ValueError(f"Invalid address format: {str(e)}") from e

    # Prepare the request data
    request_data = LetterCreateRequest(
        to=to_contact,
        from_address=from_contact,
        html=html,
        template_id=template_id,
        pdf=pdf_url,
        color=color,
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
        merge_variables=merge_variables or {},
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