from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from .mongo_location import MongoLocation

class Listing(BaseModel):
    _id: UUID = Field(description='object uuid')
    url: str = Field(description='listing url')
    providerName: str = Field(description='name of provider website')
    name: str = Field(description='name of listing')
    location: MongoLocation = Field(description='location object')
    reType: str = Field(description='type of listing')
    bedrooms: list[int] = Field(description='range of bedrooms available in listing [min, max]')
    price: int = Field(description='price of listing in dollars')
    shortestLease: int = Field(description='length of shortest available lease for listing')
    pets: bool = Field(description='are pets allowed in this listing')
    transit: bool = Field(description='is the listing close to transit?')
    scrapeTime: datetime