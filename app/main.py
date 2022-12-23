from fastapi import FastAPI, Request
from pymongo import MongoClient
from pymongo.database import Database

from controllers.listing_controller import router as listings_router
from controllers.city_controller import router as cities_router
from controllers.query_controller import router as queries_router
from services.services import Services
from config import Settings

app = FastAPI()

settings = Settings()

def check_env():
    assert settings.atlas_uri is not None
    assert settings.db_name is not None
    assert settings.listings_collection_name is not None

@app.on_event('startup')
def startup_db_client():
    check_env()

    print('attempting connection')
    app.mongodb_client: MongoClient = MongoClient(settings.atlas_uri)
    app.database: Database = app.mongodb_client[settings.db_name]
    print('connected to db')

    app.services: Services = Services(app.database, settings)

@app.on_event('shutdown')
def shutdown_db_client():
    app.mongodb_client.close()

@app.middleware("http")
def manage_context(request: Request, call_next: callable):
    if not (hasattr(app, 'mongodb_client') and hasattr(app, 'database') and hasattr(app, 'services')):
        startup_db_client()

    return call_next(request)

@app.get('/')
def hello_world():
    return {"message": "hello world"}

@app.get('/ip')
def get_client(request: Request):
    return request.client

app.include_router(listings_router, prefix='/listings')
app.include_router(cities_router, prefix='/cities')
app.include_router(queries_router, prefix='/queries')
