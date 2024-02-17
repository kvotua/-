from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DataBaseSettings(BaseModel):
    pass


class MongoDBSettings(DataBaseSettings):
    host: str = "mongo"
    port: int = 27017
    uuid_representation: str = "standard"
    db_name: str = "backend"
    users_collection_name: str = "users"
    projects_collection_name: str = "projects"


class Setting(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    mode: str = "local"
    bot_key: str = ""
    mongo_db: DataBaseSettings = MongoDBSettings()


settings = Setting()
