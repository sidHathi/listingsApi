from pydantic import BaseModel

from .geoarea import Geoarea

class CityInfo(BaseModel):
    area: Geoarea | None
    subdivisions: dict[str, Geoarea]