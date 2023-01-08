from __future__ import annotations

from pydantic import BaseModel, Field
from geopy.distance import great_circle

from constants import MILES_TO_METERS

class Geopoint(BaseModel):
    lat: float =  Field(description='latitude')
    long: float = Field(description='longitude')

    # get distance between two points in meters
    def distance(self, other: Geopoint):
        return float(great_circle(
            (self.lat, self.long),
            (other.lat, other.long)
        ).miles)
