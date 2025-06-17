"""Async client for interacting with the PostGrid API."""
from __future__ import annotations

import asyncio
import logging
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, TypeVar, cast

import aiohttp
from pydantic import BaseModel, ValidationError

from .api._exceptions import (
    PostGridAPIError,
    PostGridAuthenticationError,
    PostGridValidationError,
)
from .config import get_config

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)
FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def handle_errors(func: FuncT) -> FuncT:
    """Handle common API errors and retry logic.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function with error handling.
    """
    @wraps(func)
    async def wrapper(self: PostGridClient, *args: Any, **kwargs: Any) -> Any:
        config = get_config()
        last_exception: Exception | None = None

        for attempt in range(config.max_retries + 1):
            try:
                # Check rate limiting before making the request
                await self._check_rate_limit()
                # Make the request
                return await func(self, *args, **kwargs)
            except aiohttp.ClientResponseError as e:
                last_exception = e
                if e.status == 401:
                    raise PostGridAuthenticationError("Invalid API key") from e
                if e.status == 429:
                    retry_after = int(e.headers.get("Retry-After", 5))
                    logger.warning(
                        "Rate limited. Retrying after %s seconds", retry_after
                    )
                    await asyncio.sleep(retry_after)
                    continue
                if e.status >= 500:
                    logger.warning(
                        "Server error, retrying... (attempt %s/%s)",
                        attempt + 1, config.max_retries
                    )
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                    continue
                if e.status >= 400:
                    try:
                        error_data = e.json() if e.text else {}
                        raise PostGridValidationError(
                            error_data.get("error", {}).get("message", str(e)),
                            status_code=e.status,
                            errors=error_data.get("error", {}).get("errors"),
                        ) from e
                    except ValueError:
                        raise PostGridAPIError(
                            f"Request failed with status {e.status}: {e.message}",
                            status_code=e.status,
                        ) from e
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                logger.warning(
                    "Network error, retrying... (attempt %s/%s)",
                    attempt + 1, config.max_retries
                )
                if attempt < config.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                continue
                # If we've exhausted all retries
        if last_exception:
            if isinstance(last_exception, PostGridAPIError):
                raise last_exception
            raise PostGridAPIError("Max retries exceeded") from last_exception

        raise PostGridAPIError("Request failed after multiple retries")

    return cast(FuncT, wrapper)


class PostGridClient:
    """Async client for interacting with the PostGrid API."""
    
    _instance: "PostGridClient" | None = None
    
    def __new__(cls) -> "PostGridClient":
        """Ensure only one instance of the client exists (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self: PostGridClient) -> None:
        """Initialize the PostGrid client with configuration."""
        if self._initialized:
            return
            
        self._config = get_config()
        self._session: aiohttp.ClientSession | None = None
        self._rate_limit_remaining = self._config.rate_limit
        self._rate_limit_reset = datetime.utcnow()
        self._rate_lock = asyncio.Lock()
        self._initialized = True
        
    async def __aenter__(self: PostGridClient) -> PostGridClient:
        """Async context manager entry."""
        await self.start()
        return self
        
    async def __aexit__(self, *exc_info: Any) -> None:
        """Async context manager exit."""
        await self.close()
    
    async def start(self) -> None:
        """Initialize the client session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                base_url=str(self._config.base_url),
                headers={
                    "x-api-key": self._config.api_key,
                    "Content-Type": "application/json",
                },
                timeout=aiohttp.ClientTimeout(total=self._config.timeout),
            )
    
    async def close(self) -> None:
        """Close the client session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def _check_rate_limit(self: PostGridClient) -> None:
        """Check and handle rate limits."""
        async with self._rate_lock:
            now = datetime.utcnow()
            
            # Reset the request count and update the window start time
            if now >= self._rate_limit_reset:
                self._rate_limit_remaining = self._config.rate_limit
                self._rate_limit_reset = now + timedelta(minutes=1)
            
            # If we've hit the limit, sleep until the window resets
            if self._rate_limit_remaining <= 0:
                sleep_time = (self._rate_limit_reset - now).total_seconds()
                if sleep_time > 0:
                    logger.warning("Rate limit reached. Sleeping for %s seconds", sleep_time)
                    await asyncio.sleep(sleep_time)
                self._rate_limit_remaining = self._config.rate_limit
                self._rate_limit_reset = datetime.utcnow() + timedelta(minutes=1)
            
            self._rate_limit_remaining -= 1
    
    @handle_errors
    async def _request(
        self: PostGridClient,
        method: str,
        endpoint: str,
        response_model: type[T] | None = None,
        **kwargs: Any,
    ) -> T | dict[str, Any]:
        """Make an HTTP request to the PostGrid API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            response_model: Pydantic model to validate response against
            **kwargs: Additional arguments to pass to aiohttp
            
        Returns:
            Parsed response data
        """
        if self._session is None:
            await self.start()
            
        url = endpoint if endpoint.startswith("http") else f"{self._config.base_url}{endpoint}"
        
        async with self._session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            
            # Update rate limit headers if present
            if "X-RateLimit-Remaining" in response.headers:
                self._rate_limit_remaining = int(response.headers["X-RateLimit-Remaining"])
            if "X-RateLimit-Reset" in response.headers:
                self._rate_limit_reset = datetime.fromtimestamp(
                    int(response.headers["X-RateLimit-Reset"])
                )
            
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                data = await response.json()
                if response_model:
                    try:
                        return response_model.parse_obj(data)
                    except ValidationError as e:
                        logger.error("Failed to validate response: %s", e)
                        raise PostGridValidationError(
                            "Invalid response format from API",
                            errors=e.errors(),
                        ) from e
                return data
            
            text = await response.text()
            return {"text": text}
    
    @handle_errors
    async def get(self, endpoint: str, response_model: type[T] | None = None, **kwargs: Any) -> T | dict[str, Any]:
        """Make a GET request."""
        return await self._request("GET", endpoint, response_model, **kwargs)
    
    @handle_errors
    async def post(self, endpoint: str, response_model: type[T] | None = None, **kwargs: Any) -> T | dict[str, Any]:
        """Make a POST request."""
        return await self._request("POST", endpoint, response_model, **kwargs)
    
    @handle_errors
    async def put(self, endpoint: str, response_model: type[T] | None = None, **kwargs: Any) -> T | dict[str, Any]:
        """Make a PUT request."""
        return await self._request("PUT", endpoint, response_model, **kwargs)
    
    @handle_errors
    async def delete(self, endpoint: str, **kwargs: Any) -> bool:
        """Make a DELETE request."""
        await self._request("DELETE", endpoint, **kwargs)
        return True