from pydantic import BaseModel
from typing import Optional

from models.scrape_query import ScrapeQueryResp
from models.meta import Meta

class QueryListEnvelope(BaseModel):
    data: list[ScrapeQueryResp]
    meta: Optional[Meta]

class QueryEnvelope(BaseModel):
    data: ScrapeQueryResp
    meta: Optional[Meta]