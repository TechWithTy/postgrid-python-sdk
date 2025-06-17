"""Create template editor session functionality for PostGrid API."""
"""Create template editor session functionality for PostGrid API."""
from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from app.core.third_party_integrations.postgrid.client import PostGridClient
from app.core.third_party_integrations.postgrid.api.template_editor_sessions._exceptions import (
    TemplateEditorSessionError,
    TemplateEditorSessionValidationError,
)
from app.core.third_party_integrations.postgrid.api.template_editor_sessions._requests import (
    CreateTemplateEditorSessionRequest,
)
from app.core.third_party_integrations.postgrid.api.template_editor_sessions._responses import (
    TemplateEditorSessionResponse,
)


async def create_template_editor_session(
    client: PostGridClient,
    metadata: dict[str, Any] | None = None,
) -> TemplateEditorSessionResponse:
    """Create a new template editor session in PostGrid.

    Args:
        client: Authenticated PostGrid client instance
        metadata: Optional metadata to associate with the session
        
    Returns:
        TemplateEditorSessionResponse: The created template editor session

    Raises:
        TemplateEditorSessionValidationError: If request validation fails
        TemplateEditorSessionError: If the API request fails
        
    Example:
        ```python
        response = await create_template_editor_session(
            client=postgrid_client,
            metadata={"key": "value"}
        )
        print(f"Created session URL: {response.url}")
        ```
    """
    try:
        # Validate request data
        request_data = CreateTemplateEditorSessionRequest(metadata=metadata or {})
        
        # Make API request
        response = await client.post(
            "/template_editor_sessions",
            json=request_data.dict(exclude_none=True)
        )
        response.raise_for_status()
        
        # Parse and return response
        return TemplateEditorSessionResponse(**response.json())
        
    except ValidationError as e:
        raise TemplateEditorSessionValidationError(
            f"Invalid template editor session data: {str(e)}"
        ) from e
    except Exception as e:
        raise TemplateEditorSessionError(
            f"Failed to create template editor session: {str(e)}"
        ) from e