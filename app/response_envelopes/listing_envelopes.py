from pydantic import BaseModel
from typing import Optional

from models.listing import Listing
from models.meta import Meta

class ListingEnvelope(BaseModel):
    data: Listing
    meta: Optional[Meta]

class ListingsEnvelope(BaseModel):
    data: list[Listing]
    meta: Optional[Meta]