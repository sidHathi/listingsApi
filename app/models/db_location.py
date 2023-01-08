from pydantic import BaseModel, Field
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError, GeocoderParseError
from geopy.geocoders import GoogleV3
from geopy import Location
from geopy.extra.rate_limiter import RateLimiter
from typing import cast, Optional
from config import Settings
from dotenv import load_dotenv

load_dotenv()
settings = Settings()

class DBLocation(BaseModel):
    '''
    data format used by the scraper to store location info
    '''
    lat: float = Field(description='latitude')
    long: float = Field(description='longitude')
    address: str = Field(description='address string')

    def to_geopy(self) -> Optional[Location]:
        try:
            if settings.google_maps_api_key is None:
                raise ValueError('No API key specified')
            
            geocoder = GoogleV3(api_key=settings.google_maps_api_key)
            geocode = RateLimiter(geocoder.reverse, min_delay_seconds=1, return_value_on_exception=None)
            location = geocode((self.lat, self.long))
            if location is None:
                return None
            else:
                return cast(Location, location)
        except (GeocoderTimedOut, GeocoderParseError, GeocoderUnavailable, GeocoderServiceError) as e:
            print(e)
            print('location cast failed')
            return None