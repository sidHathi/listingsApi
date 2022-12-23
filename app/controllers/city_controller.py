from fastapi import APIRouter, Request, Path

from response_envelopes.city_envelopes import CitiesDetailEnvelope, CityListEnvelope, CityDetailEnvelope
from models.city_info import CityInfo
from services.city_service import CityService
from models.error import Error


router = APIRouter()


@router.get(
    '/',
    response_model=CityListEnvelope,
    responses={
        200: {'model': CityListEnvelope, 'description': 'Success'}
    }
)
def get_cities_list(request: Request):
    city_service: CityService = request.app.services.city_service

    cities_list: list[str] = city_service.get_cities_list()
    return CityListEnvelope(data=cities_list)


@router.get(
    '/detail',
    response_model=CitiesDetailEnvelope,
    responses={
        200: {'model': CitiesDetailEnvelope, 'description': 'Success'}
    }
)
def get_cities_detail(request: Request):
    city_service: CityService = request.app.services.city_service

    cities_detail: dict[str, CityInfo] = city_service.get_cities_detail()
    return CitiesDetailEnvelope(data=cities_detail)
