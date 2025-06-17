"""Progress a test letter to the next status in its lifecycle.

This module provides functionality to progress a test letter through its
status lifecycle for testing webhooks and other integrations.
"""
from ...client import PostGridClient
from .._exceptions import PostGridError
from ._exceptions import InvalidProgressionError
from ._responses import LetterResponse


async def progress_test_letter(
    client: PostGridClient,
    letter_id: str,
) -> LetterResponse:
    """Progress a test letter to the next status in its lifecycle.
    
    This endpoint is only available for test letters and is used to simulate
    the progression of a letter through its status lifecycle for testing
    webhooks and other integrations.

    Args:
        client: An authenticated PostGrid client instance.
        letter_id: The ID of the test letter to progress.

    Returns:
        The updated letter response.

    Raises:
        PostGridAPIError: If the API returns an error.
        InvalidProgressionError: If the letter cannot be progressed further.
        ValueError: If the letter_id is invalid.
    """
    if not letter_id or not isinstance(letter_id, str) or not letter_id.startswith("letter_"):
        raise ValueError("Invalid letter_id. Must be a string starting with 'letter_'.")

    try:
        response = await client.post(
            f"letters/{letter_id}/progressions",
            response_model=LetterResponse,
        )
        return response
    except PostGridError as e:
        if "invalid_progression_error" in str(e).lower():
            # Try to get the current status to provide a better error message
            try:
                letter = await client.get(f"letters/{letter_id}", response_model=LetterResponse)
                raise InvalidProgressionError(
                    letter_id=letter_id,
                    current_status=letter.status,
                    message=str(e),
                ) from e
            except PostGridError:
                # If we can't get the current status, raise the original error
                raise InvalidProgressionError(
                    letter_id=letter_id,
                    current_status="unknown",
                    message=str(e),
                ) from e
        raise