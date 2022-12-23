from services.listing_service import ListingService
from services.city_service import CityService
from services.query_service import QueryService
from config import Settings

from pymongo.database import Database

class Services:
    def __init__(self, db: Database, app_settings: Settings) -> None:
        self.listing_service = ListingService(db, app_settings.listings_collection_name)
        self.query_service = QueryService(db, app_settings.queries_collection_name)
        self.city_service = CityService()
