from fastapi import APIRouter, Request
from dotenv import dotenv_values
from pymongo import MongoClient

from .models.listing_envelopes import ListingEnvelope, ListingsEnvelope
from .models.listing import Listing
from .models.error import Error

config = dotenv_values('.env')

router = APIRouter()

@router.get(
    '/',
    response_model=ListingsEnvelope,
    responses={
        200: {'model': ListingsEnvelope, 'description': 'Success'}
    })
async def get_all_listings(request: Request):
    listings_col: str = config['LISTINGS_COLLECTION_NAME']
    assert listings_col is not None

    listings = list(map(Listing.parse_obj, request.app.database[listings_col].find()))
    print(listings)
    return ListingsEnvelope(data=listings)
