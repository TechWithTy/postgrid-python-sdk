# _exceptions.py
class PostGridTrackerError(Exception):
    """Base exception for PostGrid Tracker related errors"""
    pass

class PostGridTrackerNotFoundError(PostGridTrackerError):
    """Raised when a tracker is not found"""
    pass

class PostGridTrackerAPIError(PostGridTrackerError):
    """Raised when there's an error from the PostGrid API"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"PostGrid API error {status_code}: {detail}")