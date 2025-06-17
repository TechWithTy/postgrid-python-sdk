"""
Core functionality for creating postcards using templates with the PostGrid API.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import PostGridClient
from ._exceptions import PostcardError, PostcardValidationError
from ._responses import PostcardResponse
from ._enums import PostcardSize, MailingClass


async def create_postcard_with_templates(
    client: PostGridClient,
    *,
    to: Union[str, Dict[str, Any]],
    front_template: str,
    back_template: str,
    size: Union[PostcardSize, str] = PostcardSize.SIX_BY_FOUR,
    from_contact: Optional[Union[str, Dict[str, Any]]] = None,
    send_date: Optional[Union[datetime, str]] = None,
    express: bool = False,
    description: Optional[str] = None,
    mailing_class: Union[MailingClass, str] = MailingClass.FIRST_CLASS,
    merge_variables: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, Any]] = None,
    expand: Optional[List[str]] = None
) -> PostcardResponse:
    """
    Create a new postcard using pre-existing templates.

    Args:
        client: Authenticated PostGrid client
        to: Either a contact ID or a contact object for the recipient
        front_template: ID of the template for the front of the postcard
        back_template: ID of the template for the back of the postcard
        size: Size of the postcard (6x4, 9x6, or 11x6)
        from_contact: Optional contact ID or object for the sender
        send_date: Optional date when the postcard should be sent
        express: Whether to use express shipping
        description: Optional description for the postcard
        mailing_class: Mailing class (first_class or standard_class)
        merge_variables: Optional variables for template interpolation
        metadata: Optional metadata to attach to the postcard
        expand: Optional list of fields to expand in the response
               (e.g., ['frontTemplate', 'backTemplate'])

    Returns:
        PostcardResponse: The created postcard

    Raises:
        PostcardValidationError: If required fields are missing or invalid
        PostcardError: For other API errors
    """
    # Prepare the request payload
    payload: Dict[str, Any] = {
        "to": to,
        "frontTemplate": front_template,
        "backTemplate": back_template,
        "size": str(size),
        "express": express,
        "mailingClass": str(mailing_class)
    }

    # Add optional fields if provided
    if from_contact:
        payload["from"] = from_contact
    if send_date:
        payload["sendDate"] = send_date.isoformat() if isinstance(send_date, datetime) else send_date
    if description:
        payload["description"] = description
    if merge_variables:
        payload["mergeVariables"] = merge_variables
    if metadata:
        payload["metadata"] = metadata

    # Prepare query parameters for expansion
    params = {}
    if expand:
        valid_expansions = {'frontTemplate', 'backTemplate'}
        params = {"expand[]": [e for e in expand if e in valid_expansions]}

    try:
        async with client:
            response = await client.post(
                "/postcards",
                json=payload,
                params=params or None
            )
            return PostcardResponse(**response)

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get('error', {}).get('message', 'Invalid request')
            raise PostcardValidationError(f"Validation error: {error_detail}") from e
        else:
            error_detail = e.response.json().get('error', {}).get('message', str(e))
            raise PostcardError(
                f"Error creating postcard with templates: {error_detail}"
            ) from e
    except Exception as e:
        raise PostcardError(f"Unexpected error: {str(e)}") from e