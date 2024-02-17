from pymongo import MongoClient
from pymongo.database import Database
from ..IRegistry import IRegistry, IRegistryFactory
from .MongoRegistry import MongoRegistry
from ..RegistryPermission import RegistryPermission


class MongoRegistryFactory(IRegistryFactory):
    __client: MongoClient
    __database: Database

    def __init__(self) -> None:
        super().__init__()
        self.__client = MongoClient(
            host="mongo",
            port=27017,
            uuidRepresentation="standard",
        )
        self.__database = self.__client.get_database("backend")

    def get(self, name: str, permissions: RegistryPermission) -> IRegistry:
        collection = self.__database.get_collection(name)
        return MongoRegistry(permissions, collection)
