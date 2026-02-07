from typing import Any
from pydantic import BaseModel, Field


class Page(BaseModel):
    items: list[Any]
    total: int
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
