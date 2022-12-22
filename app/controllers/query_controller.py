from fastapi import APIRouter, Path, Body, Request, Query

from ..services.query_service import QueryService
from ..models.scrape_query import ScrapeQuery, ScrapeQueryResp
from ..models.query_envelopes import QueryEnvelope, QueryListEnvelope
from ..models.error import Error
from ..models.meta import Meta
from ..models.cursor import default_page_size, Cursor


router = APIRouter()


@router.get(
    '/',
    response_model=QueryListEnvelope,
    responses={
        200: {'model': QueryListEnvelope, 'description': 'Success'}
    }
)
def get_all_queries(
    request: Request
):
    cursor = Cursor.from_request(request)

    query_service: QueryService = request.app.services.query_service
    queries: list[ScrapeQueryResp] = query_service.get_all_queries(cursor)

    next_cursor: str = ""
    if len(queries) > cursor.pageSize:
        next_start = queries[-1].dict()
        queries = queries[:-1]
        next_cursor = cursor.get_next_cursor(next_start=next_start, last_page_docs=queries)
    request_meta: Meta = Meta(next_cursor=next_cursor)
    return QueryListEnvelope(data=queries, meta=request_meta)


@router.get(
    '/{id}',
    response_model=QueryEnvelope,
    responses={
        200: {'model': QueryEnvelope, 'description': 'Success'},
        400: {'model': Error, 'description': 'Bad request'},
        404: {'model': Error, 'description': 'Resource not found'}
    }
)
def get_one_query(request: Request, id: str = Path()):
    query_service: QueryService = request.app.services.query_service
    query = query_service.get_one_query(id)

    return QueryEnvelope(data=query)


@router.post(
    '/',
    response_model=QueryEnvelope,
    responses={
        200: {'model': QueryEnvelope, 'description': 'Success'},
        400: {'model': Error, 'description': 'Bad request'},
        404: {'model': Error, 'description': 'Resource not found'},
        422: {'model': Error, 'description': 'Database error'}
    }
)
def create_new_query(request: Request, query: ScrapeQuery = Body()):
    query_service: QueryService = request.app.services.query_service
    new_query: ScrapeQueryResp = query_service.create_new_query(query)

    return QueryEnvelope(data=new_query)


@router.put(
    '/{id}',
    response_model=QueryEnvelope,
    responses={
        200: {'model': QueryEnvelope, 'description': 'Success'},
        400: {'model': Error, 'description': 'Bad request'},
        404: {'model': Error, 'description': 'Resource not found'},
        422: {'model': Error, 'description': 'Database error'}
    }
)
def update_query(request: Request, id: str = Path(), query: ScrapeQuery = Body()):
    query_service: QueryService = request.app.services.query_service
    updated_query: ScrapeQueryResp = query_service.update_query(id, query)

    return QueryEnvelope(data=updated_query)
