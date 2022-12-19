from pydantic import BaseModel, Field
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError, GeocoderParseError
from geopy import Nominatim
from geopy import Location
from geopy.extra.rate_limiter import RateLimiter
from typing import cast

class MongoLocation(BaseModel):
    lat: float = Field(description='latitude')
    long: float = Field(description='longitude')
    address: str = Field(description='address string')

    def to_geopy(self) -> Location | None:
        try:
            geocoder = Nominatim(user_agent='listings_api')
            geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1, return_value_on_exception=None)
            location = geocode.reverse((self.lat, self.long))
            if location is None:
                return None
            else:
                return cast(Location, location)
        except (GeocoderTimedOut, GeocoderParseError, GeocoderUnavailable, GeocoderServiceError) as e:
            print(e)
            print('location cast failed')
            return None