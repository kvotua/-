import os

from pymongo import MongoClient
from pymongo.database import Database

from ..IRegistry import IRegistry, IRegistryFactory
from .MongoRegistry import MongoRegistry


class MongoRegistryFactory(IRegistryFactory):
    __mongo_client: MongoClient
    __database: Database

    def __init__(self, mongo_client: MongoClient | None = None) -> None:
        super().__init__()
        if mongo_client is not None:
            self.__mongo_client = mongo_client
        else:
            username = os.getenv("MONGO_USERNAME")
            password = os.getenv("MONGO_PASSWORD")
            self.__mongo_client = MongoClient(
                f"mongodb://{username}:{password}@mongo:27017"
            )
        self.__database = self.__mongo_client.get_database("registries")

    def get(self, name: str) -> IRegistry:
        collection = self.__database.get_collection(name)
        return MongoRegistry(collection)
