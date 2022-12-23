from pydantic import BaseModel
from typing import Union

from models.listing import Listing
from models.meta import Meta

class ListingEnvelope(BaseModel):
    data: Listing
    meta: Union[Meta, None]

class ListingsEnvelope(BaseModel):
    data: list[Listing]
    meta: Union[Meta, None]