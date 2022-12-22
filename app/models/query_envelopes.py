from pydantic import BaseModel

from .scrape_query import ScrapeQueryResp
from .meta import Meta

class QueryListEnvelope(BaseModel):
    data: list[ScrapeQueryResp]
    meta: Meta | None

class QueryEnvelope(BaseModel):
    data: ScrapeQueryResp
    meta: Meta | None