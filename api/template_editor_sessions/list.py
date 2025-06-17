
from ...client import PostGridClient
from ._exceptions import (
    TemplateEditorSessionError,
    TemplateEditorSessionValidationError,
)
from ._responses import (
    ListTemplateEditorSessionsResponse,
    TemplateEditorSessionResponse,
)


async def list_template_editor_sessions(
    client: PostGridClient,
    limit: int = 10,
    skip: int = 0
) -> ListTemplateEditorSessionsResponse:
    """List all template editor sessions.
    
    Args:
        client: Authenticated PostGrid client
        limit: Maximum number of sessions to return (1-100)
        skip: Number of sessions to skip for pagination
        
    Returns:
        ListTemplateEditorSessionsResponse: List of template editor sessions
        
    Raises:
        TemplateEditorSessionValidationError: If limit or skip are invalid
        TemplateEditorSessionError: If the API request fails
    """
    if limit < 1 or limit > 100:
        raise TemplateEditorSessionValidationError("Limit must be between 1 and 100")
    if skip < 0:
        raise TemplateEditorSessionValidationError("Skip must be >= 0")

    try:
        params = {"limit": limit, "skip": skip}
        response = await client.get(
            "/template_editor_sessions",
            params=params
        )
        response.raise_for_status()
        
        data = response.json()
        return ListTemplateEditorSessionsResponse(
            data=[TemplateEditorSessionResponse(**item) for item in data.get("data", [])],
            count=len(data.get("data", []))
        )
    except Exception as e:
        raise TemplateEditorSessionError(f"Failed to list template editor sessions: {str(e)}") from e