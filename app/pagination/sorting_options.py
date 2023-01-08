from __future__ import annotations

from pydantic import BaseModel, Field, validator
from typing import Any, Optional
from starlette.datastructures import MultiDict
from fastapi import Request

from models.distance_range import DistanceRange
from models.geopoint import Geopoint
from constants import MILES_TO_METERS

class SortingOptions(BaseModel):
    '''
    Model that contains the sorting fields/ordering for list results.
    Customizations are included to enable geographic sorting
    '''

    fieldName: str = Field(description='name of field to sort')
    order: int = Field(description='sorting order: 1 for ascending, -1 for descending', default=1)
    startVal: Any = Field(
        description='start value for cursor',
        default=None
    )
    # for location/distance based sorting
    distanceRange: Optional[DistanceRange] = Field(
        description='for location sorting - point from which to measure distance along with range bound for search',
        default=None
    )


    # builds a sort dictionary for use in a mongo query
    def to_mongo_sort(self) -> Optional[dict[str, Any]]:
        if self.fieldName == 'distance':
            return None
        return { '_id': 1, self.fieldName: self.order }
    

    # builds a bounded location query
    def to_location_query(self) -> Optional[dict[str, Any]]:
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


    # constructs an instance from the request's query params
    @classmethod
    def from_request(cls, request: Request) -> Optional[SortingOptions]:
        query_params: MultiDict = MultiDict(request.query_params)
        sort_by: Optional[str] = query_params.pop('sortBy')
        order: Optional[int] = query_params.pop('order')
        nearest_point_lat: Optional[float] = query_params.pop('distanceFromLat')
        nearest_point_long: Optional[float] = query_params.pop('distanceFromLong')
        max_distance: Optional[float] = query_params.pop('maxDistance')

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
