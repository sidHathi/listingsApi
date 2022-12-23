from pydantic import BaseModel
from typing import Optional

from models.city_info import CityInfo
from models.meta import Meta
from enums.supported_city import SupportedCity

class CityListEnvelope(BaseModel):
    data: list[str]
    meta: Optional[Meta]

class CitiesDetailEnvelope(BaseModel):
    data: dict[str, CityInfo]
    meta: Optional[Meta]

class CityDetailEnvelope(BaseModel):
    data: CityInfo
    meta: Optional[Meta]