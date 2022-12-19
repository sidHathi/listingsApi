from uuid import UUID

from pydantic import BaseModel, Field

class Meta(BaseModel):
    requestId: UUID = Field(description="UUID identifying the request")