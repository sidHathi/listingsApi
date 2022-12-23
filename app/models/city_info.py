from pydantic import BaseModel
from typing import Union

from models.geoarea import Geoarea

class CityInfo(BaseModel):
    area: Union[Geoarea, None]
    subdivisions: dict[str, Geoarea]