from __future__ import annotations

from pydantic import BaseModel, Field, validator
from typing import Any, Union
from starlette.datastructures import MultiDict
from fastapi import Request

from models.distance_range import DistanceRange
from models.geopoint import Geopoint
from constants import MILES_TO_METERS

class SortingOptions(BaseModel):
    fieldName: str = Field(description='name of field to sort')
    order: int = Field(description='sorting order: 1 for ascending, -1 for descending', default=1)
    startVal: Any = Field(
        description='start value for cursor',
        default=None
    )
    # for location/distance based sorting
    distanceRange: Union[DistanceRange, None] = Field(
        description='for location sorting - point from which to measure distance along with range bound for search',
        default=None
    )

    def to_mongo_sort(self) -> Union[dict[str, Any], None]:
        if self.fieldName == 'distance':
            return None
        return { '_id': 1, self.fieldName: self.order }
    
    def to_location_query(self) -> Union[dict[str, Any], None]:
        if self.fieldName != 'distance' or self.distanceRange is None:
            return None
        
        center_point: Geopoint = self.distanceRange.point
        query: dict[str, Any] =  {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [center_point.long, center_point.lat]
                },
                '$minDistance': self.distanceRange.minDistance * MILES_TO_METERS,
                '$maxDistance': self.distanceRange.maxDistance * MILES_TO_METERS
            }
        }

        return query

    @validator('order')
    def validate_order(cls, v):
        if v is not None and v not in [1, -1]:
            raise ValueError('must be in [-1, 1]')
        return v

    @classmethod
    def from_request(cls, request: Request) -> Union[SortingOptions, None]:
        query_params: MultiDict = MultiDict(request.query_params)
        sort_by: Union[str, None] = query_params.pop('sortBy')
        order: Union[int, None] = query_params.pop('order')
        nearest_point_lat: Union[float, None] = query_params.pop('distanceFromLat')
        nearest_point_long: Union[float, None] = query_params.pop('distanceFromLong')
        max_distance: Union[float, None] = query_params.pop('maxDistance')

        opts: dict[str, Any] = {}
        if sort_by is None:
            return None
        if sort_by == 'distance':
            if nearest_point_lat is None or nearest_point_long is None:
                return None
            distance_range: DistanceRange = DistanceRange(
                point=Geopoint(lat=nearest_point_lat, long=nearest_point_long)
            )
            if max_distance is not None:
                distance_range.maxDistance = max_distance
            opts['distanceRange'] = distance_range

        opts['fieldName'] = sort_by
        opts['startVal'] = None
        if order is not None:
            opts['order'] = order

        return cls.parse_obj(opts)
