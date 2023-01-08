from pydantic import BaseModel, Field, json
import uuid
from datetime import datetime
from typing import Optional

from models.object_id import ObjectId
from models.db_location import DBLocation

json.ENCODERS_BY_TYPE[ObjectId]=str

class Listing(BaseModel):
    id: ObjectId = Field(
        default_factory=ObjectId, 
        alias='_id', 
        description='object id'
    )
    url: str = Field(description='listing url')
    providerName: str = Field(description='name of provider website')
    name: str = Field(description='name of listing')
    location: DBLocation = Field(description='location object')
    reType: str = Field(description='type of listing')
    bedrooms: list[int] = Field(description='range of bedrooms available in listing [min, max]')
    price: int = Field(description='price of listing in dollars')
    shortestLease: int = Field(description='length of shortest available lease for listing')
    pets: bool = Field(description='are pets allowed in this listing')
    transit: bool = Field(description='is the listing close to transit?')
    scrapeTime: datetime
    pageRank: Optional[int]= Field(description='How high up on the listing provider website did the listing appear', default=None)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {
            ObjectId: lambda v: str(v),
        }