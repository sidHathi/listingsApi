from pydantic import BaseModel
from typing import Union

from models.geoarea import Geoarea

class CityInfo(BaseModel):
    '''
    Defines a city using a geographic region and a name indexed 
    dictionary of subdivisions/neighborhoods within the city
    '''

    area: Union[Geoarea, None]
    subdivisions: dict[str, Geoarea]