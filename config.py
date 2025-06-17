"""Configuration for the PostGrid API client."""
from __future__ import annotations

from functools import lru_cache

from pydantic import BaseSettings, Field, HttpUrl


class PostGridConfig(BaseSettings):
    """Configuration for the PostGrid API client.

    Loads configuration from environment variables with the following precedence:
    1. Environment variables
    2. .env file
    3. Default values
    """

    api_key: str = Field(..., env="POSTGRID_API_KEY")
    base_url: HttpUrl = Field(
        default="https://api.postgrid.com/print-mail/v1/",
        env="POSTGRID_BASE_URL"
    )
    timeout: int = Field(
        default=30,
        description="Request timeout in seconds",
        env="POSTGRID_TIMEOUT"
    )
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed requests",
        env="POSTGRID_MAX_RETRIES"
    )
    rate_limit: int = Field(
        default=50,
        description="Maximum number of requests per minute",
        env="POSTGRID_RATE_LIMIT"
    )

    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_config() -> PostGridConfig:
    """Get the PostGrid configuration.

    Returns:
        PostGridConfig: The PostGrid configuration.
    """
    return PostGridConfig()
