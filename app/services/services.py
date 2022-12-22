from .listing_service import ListingService
from .city_service import CityService
from .query_service import QueryService

from pymongo.database import Database

class Services:
    def __init__(self, db: Database) -> None:
        self.listing_service = ListingService(db)
        self.query_service = QueryService(db)
        self.city_service = CityService()
