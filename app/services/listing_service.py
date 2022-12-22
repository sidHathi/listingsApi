from dotenv import dotenv_values
from pymongo.database import Database
from pymongo.collection import Collection
from fastapi import HTTPException
from typing import Any

from ..models.listing import Listing
from ..models.object_id import ObjectId
from ..models.db_query import DBQuery
from ..models.cursor import Cursor
from ..models.sorting_options import SortingOptions

config = dotenv_values('.env')

class ListingService:
    def __init__(self, db: Database) -> None:
        self.listings_col: Collection = db[config['LISTINGS_COLLECTION_NAME']]

    def _query_by_distance(self, cursor: Cursor, query: DBQuery | None) -> list[Listing]:
        if cursor.sorting_options is None or cursor.sorting_options.distanceRange is None:
            return []
        
        page_size = cursor.pageSize
        query_dict: dict[str, Any] = {}
        if query is not None:
            query_dict = query.to_filter_dict()
        query_dict['location'] = cursor.sorting_options.to_location_query()
        if cursor.previousIds is not None:
            query_dict['_id'] = { '$nin': cursor.previousIds }

        print(query_dict)
        listings: list[Listing] = list(map(
            Listing.parse_obj, 
            self.listings_col.find(query_dict).limit(page_size + 1)
        ))
        return listings
    
    def _query_by_field(self, cursor: Cursor, query: DBQuery | None) -> list[Listing]:
        start: str | None = cursor.startId
        page_size: int = cursor.pageSize
        query_dict: dict[str, Any] = {}
        if query is not None:
            query_dict = query.to_filter_dict()
        if start is not None and ObjectId.is_valid(start):
            start_id: ObjectId = ObjectId(start)
            query_dict['_id'] = { '$gte': start_id }

        sort_fields: list[Any] = [('_id', 1)]
        if cursor.sorting_options is not None and cursor.sorting_options.order is not None:
            order: int = cursor.sorting_options.order
            fieldName: str = cursor.sorting_options.fieldName
            startVal = cursor.sorting_options.startVal
            sort_fields = [
                (fieldName, order),
                ('_id', 1)
            ]
            if startVal is not None:
                if fieldName not in query_dict:
                    query_dict[fieldName] = {}
                if order == -1:
                    query_dict[fieldName]['$lte'] = startVal
                else:
                    query_dict[fieldName]['$gte'] = startVal

        listings: list[Listing] = list(map(
            Listing.parse_obj, 
            self.listings_col.find(query_dict).sort(sort_fields).limit(page_size + 1)
        ))
        return listings


    def get_all_listings(self, cursor: Cursor) -> list[Listing]:
        if cursor.sorting_options is not None and cursor.sorting_options.fieldName == 'distance':
            return self._query_by_distance(cursor, None)
        return self._query_by_field(cursor, None)

    def get_one_listing(self, id: str) -> Listing:
        listing: Listing = Listing.parse_obj(self.listings_col.find_one({'_id': ObjectId(id)}))

        if listing is None:
            raise HTTPException(status_code=404, detail='listing not found')
        return listing

    def get_listings_for_query(self, query: DBQuery, cursor: Cursor) -> list[Listing]:
        if cursor.sorting_options is not None and cursor.sorting_options.fieldName == 'distance':
            return self._query_by_distance(cursor, query)
        return self._query_by_field(cursor, query)