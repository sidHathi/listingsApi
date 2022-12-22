from pydantic import BaseModel, Field
from typing import Any

from .geoarea import Geoarea

class DBQuery(BaseModel):
    provider: str | None = Field(
        description='Listing provider name', 
        default=None
    )
    name: str | None = Field(
        description='Search string - matched against listing names',
        default=None
    )
    location: Geoarea | None = Field(
        description='Geographic area within which to search for listings',
        default=None
    )
    reType: str | None = Field(
        description='type of listing',
        example='apartment',
        default=None
    )
    bedrooms: int | None = Field(
        description='number of bedrooms desired in listing',
        default=None
    )
    price: list[int] | None = Field(
        description='[Min, max] price range',
        default=None
    )
    leaseTerm: int | None = Field(
        description='desired lease term',
        default=None
    )
    pets: bool | None = Field(
        description='only get leasings that allow pets',
        default=None
    )
    transit: bool | None = Field(
        description='only get listings close to transit',
        default=None
    )

    def to_filter_dict(self, overrides: dict[str, Any] | None = None) -> dict[str, Any]:
        query_dict: dict[str, Any] = {}

        if self.provider is not None:
            query_dict['providerName'] = self.provider
        if self.name is not None:
            query_dict['name'] = self.name
        if self.location is not None:
            query_dict['location'] = self.location.to_mongo_filter()
        if self.reType is not None:
            query_dict['reType'] = self.reType
        if self.bedrooms is not None:
            query_dict['bedrooms'] = {
                '$elemMatch': {
                    '$lte': self.bedrooms,
                    '$gte': self.bedrooms
                }
            }
        if self.price is not None and len(self.price) >= 2:
            query_dict['price'] = {
                '$gte': self.price[0],
                '$lte': self.price[1]
            }
        if self.leaseTerm is not None:
            query_dict['shortestLease'] = {
                '$lte': self.leaseTerm
            }
        if self.pets is not None:
            query_dict['pets'] = self.pets
        if self.transit is not None:
            query_dict['transit'] = self.transit

        if overrides is not None:
            for key, val in overrides.items():
                query_dict[key] = val

        return query_dict
