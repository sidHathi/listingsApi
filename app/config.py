from pydantic import BaseSettings

class Settings(BaseSettings):
    atlas_uri: str
    db_name: str
    listings_collection_name: str = 'listings'
    migrations_collection_name: str = 'migrationRecords'
    queries_collection_name: str = 'queryList'
    google_maps_api_key: str