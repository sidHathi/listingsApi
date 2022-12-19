from pydantic import BaseModel

from .listing import Listing
from .meta import Meta

class ListingEnvelope(BaseModel):
    data: Listing
    meta: Meta | None

class ListingsEnvelope(BaseModel):
    data: list[Listing]
    meta: Meta | None