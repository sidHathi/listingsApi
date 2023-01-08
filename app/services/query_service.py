from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.results import UpdateResult, InsertOneResult
from fastapi import HTTPException
from typing import Any, Optional

from models.scrape_query import ScrapeQuery, ScrapeQueryResp
from models.object_id import ObjectId
from pagination.cursor import Cursor

class QueryService:
    def __init__(self, db: Database, col_name: str):
        self.query_col: Collection = db[col_name]


    def get_all_queries(self, cursor: Cursor) -> list[ScrapeQueryResp]:
        filters: dict[str, Any] = {}
        start: Optional[str] = cursor.startId
        page_size: int = cursor.pageSize
        if start is not None and ObjectId.is_valid(start):
            start_id: ObjectId = ObjectId(start)
            filters['_id'] = { '$gte': start_id }

        queries: list[ScrapeQueryResp] = list(map(
            ScrapeQueryResp.parse_obj,
            self.query_col.find(filters).sort('_id', 1).limit(page_size + 1)
        ))

        return queries


    def get_one_query(self, id: str) -> ScrapeQueryResp:
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=400,
                detail='invalid object ID'
            )

        object_id: ObjectId = ObjectId(id)
        query: ScrapeQueryResp = ScrapeQueryResp.parse_obj(
            self.query_col.find_one({'_id': object_id})
        )
        if query is None:
            raise HTTPException(
                status_code=404,
                detail='no matching queries found'
            )

        return query


    def create_new_query(self, new_query: ScrapeQuery) -> ScrapeQueryResp:
        insertion_doc: dict[str, Any] = new_query.to_insertion_doc()
        res: InsertOneResult = self.query_col.insert_one(insertion_doc)

        if not res.acknowledged:
            raise HTTPException(status_code=422, detail='insertion failed')
        
        insertion_doc['_id'] = res.inserted_id
        return ScrapeQueryResp.parse_obj(insertion_doc)
    
    
    def update_query(self, id: str, query_updates: ScrapeQuery) -> ScrapeQueryResp:
        if not ObjectId.is_valid(id):
            raise HTTPException(
                status_code=400,
                detail='invalid object ID'
            )

        object_id: ObjectId = ObjectId(id)
        update_doc: dict[str, Any] = {
            '$set':
            query_updates.to_insertion_doc()
        }
        res: UpdateResult = self.query_col.update_one(
            {'_id' : object_id},
            update_doc
        )

        if not res.acknowledged:
            raise HTTPException(status_code=422, detail='insertion failed')
        elif res.matched_count < 1:
            raise HTTPException(status_code=404, detail='No queries matching id')

        return ScrapeQueryResp.parse_obj(update_doc['$set'])

