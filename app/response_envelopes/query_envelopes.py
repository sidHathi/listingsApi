from pydantic import BaseModel
from typing import Union

from models.scrape_query import ScrapeQueryResp
from models.meta import Meta

class QueryListEnvelope(BaseModel):
    data: list[ScrapeQueryResp]
    meta: Union[Meta, None]

class QueryEnvelope(BaseModel):
    data: ScrapeQueryResp
    meta: Union[Meta, None]