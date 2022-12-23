from pydantic import BaseModel
from typing import Union

from models.city_info import CityInfo
from models.meta import Meta
from enums.supported_city import SupportedCity

class CityListEnvelope(BaseModel):
    data: list[str]
    meta: Union[Meta, None]

class CitiesDetailEnvelope(BaseModel):
    data: dict[str, CityInfo]
    meta: Union[Meta, None]

class CityDetailEnvelope(BaseModel):
    data: CityInfo
    meta: Union[Meta, None]