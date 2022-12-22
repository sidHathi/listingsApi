from pydantic import BaseModel

from ..models.scrape_query import ScrapeQueryResp
from ..models.meta import Meta

class QueryListEnvelope(BaseModel):
    data: list[ScrapeQueryResp]
    meta: Meta | None

class QueryEnvelope(BaseModel):
    data: ScrapeQueryResp
    meta: Meta | None