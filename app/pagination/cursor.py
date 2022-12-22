from __future__ import annotations

from pydantic import BaseModel
from base64 import urlsafe_b64decode, urlsafe_b64encode
from json import dumps, loads
from typing import Any
from fastapi import Request
from starlette.datastructures import MultiDict

from .sorting_options import SortingOptions
from ..models.geopoint import Geopoint
from ..models.db_location import DBLocation

default_page_size=20

class Cursor(BaseModel):
    startId: str | None
    previousIds: list[str] | None
    pageSize: int = default_page_size
    sorting_options: SortingOptions | None


    def encode(self) -> str:
        return urlsafe_b64encode(dumps(self.dict()).encode())
    

    def get_next_cursor(self, next_start: dict[str, Any], last_page_docs: list[BaseModel]) -> Cursor:
        new_sorting_opts: SortingOptions = self.sorting_options
        previous_ids: list[str] | None = self.previousIds
        if previous_ids is None:
            previous_ids = []
        if self.sorting_options is not None:
            if self.sorting_options.fieldName == 'distance' and self.sorting_options.distanceRange is not None:
                point: Geopoint = self.sorting_options.distanceRange.point
                last_location: dict[str, Any] = next_start['location']
                if 'lat' in last_location and 'long' in last_location:
                    new_sorting_opts.distanceRange.minDistance = point.distance(
                        Geopoint(lat=last_location['lat'], long=last_location['long'])
                    )
                    previous_ids = [*previous_ids, *list(map(
                        lambda doc: doc.dict()['id'],
                        last_page_docs
                    ))]
            else:
                new_sorting_opts.startVal = next_start[self.sorting_options.fieldName]

        return Cursor(
            startId=str(next_start['id']), 
            pageSize=self.pageSize,
            sorting_options=new_sorting_opts,
            previousIds=list(map(str, previous_ids))
        )
    

    @classmethod
    def decode(cls, encoded: str) -> Cursor:
        data: dict[str, Any] = loads(urlsafe_b64decode(encoded).decode())
        return cls.parse_obj(data)
    

    @classmethod
    def from_request(cls, request: Request) -> Cursor:
        query_params: MultiDict = MultiDict(request.query_params)
        query_cursor: str | None = query_params.pop('cursor')
        page_size_override: str | None = query_params.pop('pageSize')
        sort_key: str | None = query_params.pop('sortBy')

        cursor: Cursor = cls(startId=None, pageSize=default_page_size)
        if query_cursor is not None:
            cursor = cls.decode(query_cursor)
            return cursor
        if page_size_override is not None:
            cursor.pageSize = int(page_size_override)
        if sort_key is not None:
            cursor.sorting_options = SortingOptions.from_request(request)
        
        return cursor