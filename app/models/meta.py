from pydantic import BaseModel, Field
from typing import Union

from pagination.cursor import Cursor

class Meta(BaseModel):
    next_cursor: Union[str, None] = Field(
        description='Base64 encoded cursor for next page',
        default=None
    )