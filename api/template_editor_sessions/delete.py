
from ...client import PostGridClient
from ._exceptions import (
    TemplateEditorSessionError,
    TemplateEditorSessionNotFoundError,
    TemplateEditorSessionValidationError,
)
from ._responses import DeleteTemplateEditorSessionResponse


async def delete_template_editor_session(
    client: PostGridClient,
    session_id: str
) -> DeleteTemplateEditorSessionResponse:
    """Delete a template editor session.
    
    Args:
        client: Authenticated PostGrid client
        session_id: ID of the session to delete
        
    Returns:
        DeleteTemplateEditorSessionResponse: Confirmation of deletion
        
    Raises:
        TemplateEditorSessionValidationError: If session ID is invalid
        TemplateEditorSessionNotFoundError: If session doesn't exist
        TemplateEditorSessionError: If the API request fails
    """
    if not session_id or not session_id.startswith("template_editor_session_"):
        raise TemplateEditorSessionValidationError("Invalid session ID format")

    try:
        response = await client.delete(f"/template_editor_sessions/{session_id}")
        
        if response.status_code == 404:
            raise TemplateEditorSessionNotFoundError(f"Template editor session {session_id} not found")
            
        response.raise_for_status()
        return DeleteTemplateEditorSessionResponse(**response.json())
        
    except TemplateEditorSessionNotFoundError:
        raise
    except Exception as e:
        raise TemplateEditorSessionError(f"Failed to delete template editor session: {str(e)}") from e