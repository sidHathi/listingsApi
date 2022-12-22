from fastapi import APIRouter, Request, Path, Body, Query
from dotenv import dotenv_values
from uuid import UUID
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Any

from ..models.listing_envelopes import ListingEnvelope, ListingsEnvelope
from ..models.listing import Listing
from ..models.error import Error
from ..models.db_query import DBQuery
from ..models.cursor import default_page_size, Cursor
from ..models.meta import Meta
from ..services.listing_service import ListingService


config = dotenv_values('.env')

router = APIRouter()

@router.get(
    '/',
    response_model=ListingsEnvelope,
    responses={
        200: {'model': ListingsEnvelope, 'description': 'Success'}
    }
)
async def get_all_listings(
    request: Request
):
    cursor = Cursor.from_request(request)

    listing_service: ListingService = request.app.services.listing_service
    listings: list[Listing] = listing_service.get_all_listings(
        cursor=cursor
    )

    next_cursor: str = ""
    if len(listings) > cursor.pageSize:
        next_start: dict[str, Any] = listings[-1].dict()
        listings: list[Listing] = listings[:-1]
        next_cursor = cursor.get_next_cursor(next_start=next_start, last_page_docs=listings).encode()

    request_meta: Meta = Meta(next_cursor=next_cursor)
    return ListingsEnvelope(data=listings, meta=request_meta)


@router.get(
    '/{id}',
    response_model=ListingEnvelope,
    responses={
        200: {'model': ListingEnvelope, 'description': 'Success'},
        400: {'model': Error, 'description': 'Bad request'},
        404: {'model': Error, 'description': "Resource not found"}
    }
)
def get_one_listing(request: Request, id: str = Path()):
    listing_service: ListingService = request.app.services.listing_service
    listing: Listing = listing_service.get_one_listing(id)

    return ListingEnvelope(data=listing)


@router.post(
    '/search',
    response_model=ListingsEnvelope,
    responses={
        200: {'model': ListingsEnvelope, 'description': 'Success'},
        400: {'model': Error, 'description': 'Bad request'},
    }
)
def search_listings(
    request: Request,
    query: DBQuery = Body(),
    cursor: str | None = Query(
        description='pagination cursor (absence indicates first page)',
        default=None
    )
):
    cursor: Cursor = Cursor.from_request(request)

    listing_service: ListingService = request.app.services.listing_service
    listings: list[Listing] = listing_service.get_listings_for_query(
        query=query,
        cursor=cursor
    )

    next_cursor: str = ""
    if len(listings) > cursor.pageSize:
        next_start: dict[str, Any] = listings[-1].dict()
        listings: list[Listing] = listings[:-1]
        next_cursor = cursor.get_next_cursor(next_start=next_start, last_page_docs=listings).encode()

    request_meta: Meta = Meta(next_cursor=next_cursor)
    return ListingsEnvelope(data=listings, meta=request_meta)
