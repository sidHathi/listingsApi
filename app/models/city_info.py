from pydantic import BaseModel
from typing import Optional

from models.geoarea import Geoarea

class CityInfo(BaseModel):
    '''
    Defines a city using a geographic region and a name indexed 
    dictionary of subdivisions/neighborhoods within the city
    '''

    area: Optional[Geoarea]
    subdivisions: dict[str, Geoarea]