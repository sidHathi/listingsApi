from enum import Enum
from typing import Any, cast
from pydantic import BaseModel
from geopy.geocoders import Nominatim
from geopy import Location
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError, GeocoderParseError

from models.geoarea import Geoarea
from models.city_info import CityInfo
from enums.supported_city import SupportedCity

class CityService:
    def get_cities_list(self) -> list[str]:
        return [city.value for city in SupportedCity]

    def get_city_radius(self, city: SupportedCity) -> float:
        # returns square mileage of city in miles

        if city == SupportedCity.boston:
            return 60
        if city == SupportedCity.newYork:
            return 120
        if city == SupportedCity.seattle:
            return 80
        if city == SupportedCity.sanFran:
            return 100

        # unsupported in python <3.10 tragically
        # match(city):
        #     case SupportedCity.boston:
        #         return 60
        #     case SupportedCity.newYork:
        #         return 120
        #     case SupportedCity.seattle:
        #         return 80
        #     case SupportedCity.sanFran:
        #         return 100

    def get_cities_detail(self) -> dict[str: CityInfo]:
        cityAreas: dict[SupportedCity, Geoarea] = {}
        for city in SupportedCity:
            cityName: str = city.value
            try:
                geocoder = Nominatim(user_agent='listings_api')
                geocode = RateLimiter(geocoder.geocode, min_delay_seconds=1, return_value_on_exception=None)
                location = geocode(cityName)
                assert location is not None
                cast(Location, location)
                area: Geoarea = Geoarea(lat=location.latitude, long=location.longitude, radius=self.get_city_radius(city))
                cityAreas[city] = area
            except (GeocoderTimedOut, GeocoderUnavailable, GeocoderServiceError, GeocoderParseError, AssertionError) as e:
                print('location parse failed')
                print(e)
                cityAreas[city] = None
        citiesInfo: list[CityInfo] = []
        for city in SupportedCity:
            citiesInfo.append(CityInfo(name=city.value, location=cityAreas[city], subdivisions={}))
        return citiesInfo
