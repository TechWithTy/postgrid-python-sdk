"""Base models for PostGrid API responses."""
from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar('T')

class BaseResponse(BaseModel):
    """Base response model with common fields."""
    id: str
    object: str
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
        
        @classmethod
        def alias_generator(cls, string: str) -> str:
            """Convert field names to camelCase for JSON serialization."""
            parts = iter(string.split("_"))
            return next(parts) + "".join(i.title() for i in parts)


class ListResponse(BaseModel, Generic[T]):
    """Base model for paginated list responses."""
    object: str = "list"
    limit: int
    skip: int
    total_count: int = Field(alias="totalCount")
    data: list[T] = Field(default_factory=list)
    
    class Config:
        """Pydantic config."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
