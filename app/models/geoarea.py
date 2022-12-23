from pydantic import BaseModel
from typing import Any

from constants import EARTH_RADIUS

class Geoarea(BaseModel):
    lat: float
    long: float
    radius: float

    def to_mongo_filter(self) -> dict[str, Any]:
        return {
            '$geoWithin': {
                '$centerSphere': [
                    [ self.long, self.lat ],
                    self.radius/EARTH_RADIUS
                ]
            }
        }