"""Standardized REST API Request and Response Schemas."""
from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class APIErrorDetails(BaseModel):
    code: str
    message: str
    field: Optional[str] = None


class APIResponseEnvelope(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    error: Optional[APIErrorDetails] = None
    meta: Optional[dict[str, Any]] = None


class PaginationMeta(BaseModel):
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)
    total_items: int = Field(ge=0)
    total_pages: int = Field(ge=0)


class PaginatedAPIResponse(BaseModel, Generic[T]):
    success: bool = True
    data: List[T] = []
    meta: PaginationMeta
    error: Optional[APIErrorDetails] = None
