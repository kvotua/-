from abc import ABC

from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings


class DatabaseHelper(ABC):
    pass


class MongoDBHelper(DatabaseHelper):
    def __init__(
        self,
        host: str,
        port: int,
        uuid_representation: str,
    ) -> None:
        self.mongo_client = MongoClient(
            host=host,
            port=port,
            uuidRepresentation=uuid_representation,
        )

    def get_database(self, database_name: str = settings.mongo_db.db_name) -> Database:
        """
        Get a pymongo.database.Database with the given name and options.
        Useful for creating a pymongo.database.Database.
        """
        return self.mongo_client.get_database(database_name)


mongo_db_helper = MongoDBHelper(
    host=settings.mongo_db.host,
    port=settings.mongo_db.port,
    uuid_representation=settings.mongo_db.uuid_representation,
)
