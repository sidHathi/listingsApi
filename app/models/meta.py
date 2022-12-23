from pydantic import BaseModel, Field
from typing import Optional

from pagination.cursor import Cursor

class Meta(BaseModel):
    next_cursor: Optional[str] = Field(
        description='Base64 encoded cursor for next page',
        default=None
    )