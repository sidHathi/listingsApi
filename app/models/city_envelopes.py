from pydantic import BaseModel

from .city_info import CityInfo
from .meta import Meta
from ..enums.supported_city import SupportedCity

class CityListEnvelope(BaseModel):
    data: list[str]
    meta: Meta | None

class CitiesDetailEnvelope(BaseModel):
    data: dict[str, CityInfo]
    meta: Meta | None

class CityDetailEnvelope(BaseModel):
    data: CityInfo
    meta: Meta | None