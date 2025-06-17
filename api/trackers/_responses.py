from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime
from ._enums import SortBy, SortOrder

class TrackerCreateRequest(BaseModel):
    redirect_url_template: Optional[HttpUrl] = Field(
        None, 
        description="URL template for redirection with template variables"
    )
    url_expire_after_days: Optional[int] = Field(
        None,
        ge=1,
        le=365,
        description="Number of days until the tracking URL expires"
    )

class TrackerUpdateRequest(BaseModel):
    redirect_url_template: Optional[HttpUrl] = None
    url_expire_after_days: Optional[int] = Field(
        None,
        ge=1,
        le=365
    )

class TrackerListRequest(BaseModel):
    limit: int = Field(10, ge=1, le=100)
    skip: int = Field(0, ge=0)
    sort_by: Optional[SortBy] = None
    sort_order: SortOrder = SortOrder.DESC