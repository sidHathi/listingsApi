import uvicorn

from fastapi import FastAPI
from pymongo import MongoClient
from dotenv import dotenv_values

from .listings_controller import router as listings_router

config = dotenv_values('.env')

app = FastAPI()

def check_env():
    assert config['ATLAS_URI'] is not None
    assert config['DB_NAME'] is not None
    assert config['LISTINGS_COLLECTION_NAME'] is not None

@app.on_event('startup')
def startup_db_client():
    check_env()

    app.mongodb_client = MongoClient(config['ATLAS_URI'])
    app.database = app.mongodb_client[config['DB_NAME']]
    print('connected to db')

@app.on_event('shutdown')
def shutdown_db_client():
    app.mongodb_client.close()

@app.get('/')
def hello_world():
    return {"message": "hello world"}

app.include_router(listings_router, prefix='/listings')

if __name__ == '__main__':
    uvicorn.run('app:app', port=5000, log_level='info')