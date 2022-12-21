from pydantic import BaseModel, Field
from .cursor import Cursor

class Meta(BaseModel):
    next_cursor: str | None = Field(
        description='Base64 encoded cursor for next page',
        default=None
    )