from pydantic import BaseModel

from ..models.listing import Listing
from ..models.meta import Meta

class ListingEnvelope(BaseModel):
    data: Listing
    meta: Meta | None

class ListingsEnvelope(BaseModel):
    data: list[Listing]
    meta: Meta | None