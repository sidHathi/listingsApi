from pydantic import BaseModel, Field
from typing import Any

from .db_location import DBLocation
from .object_id import ObjectId
from .db_location import DBLocation

class ScrapeQuery(BaseModel):
    name: str = Field(
        description='name of new scraping query'
    )
    location: DBLocation = Field(
        description='location around which to begin query'
    )
    reType: str = Field(
        description='type of listings to scrape for'
    )
    bedrooms: int = Field(
        description='number of bedrooms to scrape for'
    )
    priceRange: list[int] = Field(
        description='price range of listings [min, max]'
    )
    leaseDuration: int = Field(
        description='duration of rental terms'
    )
    pets: bool = Field(
        description='scrape for listings that require pets'
    )
    transit: bool = Field(
        description='scrape for listings near transit'
    )

    def to_insertion_doc(self) -> dict[str, Any]:
        insertion_doc: dict[str, Any] = self.dict()
        leaseTerm: str = 'longTerm'
        
        if self.leaseDuration <= 2:
            leaseTerm = 'monthToMonth'
        elif self.leaseDuration <= 6:
            leaseTerm= 'shortTerm'

        insertion_doc['leaseTerm'] = leaseTerm
        return insertion_doc


class ScrapeQueryResp(ScrapeQuery):
    id: ObjectId = Field(
        default_factory=ObjectId, 
        alias='_id',
        description='object id'
    )
    location: str = Field(
        description='name of location around which to begin query'
    )
    reType: str = Field(
        description='type of listings to scrape for'
    )
    bedrooms: int = Field(
        description='number of bedrooms to scrape for'
    )
    priceRange: list[int] = Field(
        description='price range of listings [min, max]'
    )
    leaseDuration: int = Field(
        description='duration of rental terms'
    )
    leaseTerm: str = Field(
        description='keyword description for lease duration'
    )
    pets: bool = Field(
        description='scrape for listings that require pets'
    )
    transit: bool = Field(
        description='scrape for listings near transit'
    )
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True #required for the _id 
        json_encoders = {
            ObjectId: lambda v: str(v),
        }

