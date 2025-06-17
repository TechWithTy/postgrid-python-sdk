"""Base classes and utilities for PostGrid API responses."""
from __future__ import annotations

from datetime import datetime
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field

T = TypeVar('T')


class BaseResponse(BaseModel):
    """Base response model for all PostGrid API responses.
    
    Attributes:
        id: Unique identifier for the resource
        object: Type of the resource (e.g., 'webhook')
        created_at: When the resource was created
        updated_at: When the resource was last updated
    """
    id: str
    object: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    
    class Config:
        """Pydantic config."""
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class ListResponse(BaseModel, Generic[T]):
    """Generic list response model for paginated results.
    
    Attributes:
        data: List of items in the current page
        object: Always 'list'
        count: Total number of items across all pages
        limit: Maximum number of items per page
        skip: Number of items skipped for pagination
    """
    data: list[T]
    object: str = "list"
    count: int
    limit: int
    skip: int = 0
    
    def __len__(self) -> int:
        """Return the number of items in the current page."""
        return len(self.data)
    
    def __getitem__(self, index: int) -> T:
        """Get an item by index."""
        return self.data[index]
    
    def __iter__(self):
        """Iterate over items in the current page."""
        return iter(self.data)
