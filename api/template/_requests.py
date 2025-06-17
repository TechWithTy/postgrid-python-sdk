"""
Pydantic request models for the PostGrid Template API.

This module contains Pydantic models for validating and serializing
request data for template operations.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, ClassVar
from typing_extensions import Literal
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from typing import Optional

class TemplateMetadata(BaseModel):
    """Metadata model for template operations."""
    updated: Optional[bool] = Field(
        None,
        description="Indicates if the template was updated"
    )
    
    model_config = {
        "populate_by_name": True,
        "extra": "allow"
    }


class TemplateUpdateRequest(BaseModel):
    """Request model for updating a template."""
    html: str = Field(
        ...,
        description="The HTML content for the template"
    )
    description: Optional[str] = Field(
        None,
        description="A description for the template"
    )
    metadata: Optional[dict[str, Any]] = Field(
        None,
        description="Custom metadata for the template"
    )
    
    @model_validator(mode='before')
    @classmethod
    def validate_metadata(cls, data: Any) -> Any:
        """Convert metadata to the correct format if needed."""
        if not isinstance(data, dict):
            return data
            
        if 'metadata' in data and isinstance(data['metadata'], dict):
            # Convert metadata keys to use dot notation for API compatibility
            metadata = data['metadata']
            if any('.' in key for key in metadata.keys()):
                return data
                
            # Convert nested metadata to dot notation
            new_metadata = {}
            for key, value in metadata.items():
                if isinstance(value, dict):
                    for k, v in value.items():
                        new_metadata[f"{key}.{k}"] = v
                else:
                    new_metadata[key] = value
            data['metadata'] = new_metadata
            
        return data
    
    model_config = ConfigDict(populate_by_name=True, extra="forbid")


class TemplateDeleteRequest(BaseModel):
    """Request model for deleting a template.
    
    This is an empty model since template deletion only requires the template ID.
    """
    model_config = {
        "extra": "forbid"
    }
