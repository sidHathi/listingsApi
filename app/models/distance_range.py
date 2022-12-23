from pydantic import BaseModel, Field

from models.geopoint import Geopoint

default_max_range = 20 # default maximum range for distance-based queries in miles

class DistanceRange(BaseModel):
    point: Geopoint
    minDistance: float = Field(default=0)
    maxDistance: float = Field(default=default_max_range)