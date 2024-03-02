import os

from pymongo import MongoClient
from pymongo.database import Database

from ..IRegistry import IRegistry, IRegistryFactory
from ..RegistryPermission import RegistryPermission
from .MongoRegistry import MongoRegistry


class MongoRegistryFactory(IRegistryFactory):
    """
    Factory class for creating instances of MongoRegistry.

    Attributes:
        __client (MongoClient): The MongoDB client.
        __database (Database): The MongoDB database.

    Methods:
        get: Creates an instance of MongoRegistry \
            based on the provided name and permissions.
    """

    __client: MongoClient
    __database: Database

    def __init__(self) -> None:
        """
        Initializes a new instance of the MongoRegistryFactory class.
        """
        super().__init__()
        username = os.getenv("MONGO_USERNAME")
        password = os.getenv("MONGO_PASSWORD")
        self.__client = MongoClient(f"mongodb://{username}:{password}@mongo:27017")
        self.__database = self.__client.get_database("backend")

    def get(self, name: str, permissions: RegistryPermission) -> IRegistry:
        """
        Creates an instance of MongoRegistry based on the provided name and permissions.

        Args:
            name (str): The name of the collection in the MongoDB database.
            permissions (RegistryPermission): The permissions for the registry.

        Returns:
            IRegistry: An instance of MongoRegistry.
        """
        collection = self.__database.get_collection(name)
        return MongoRegistry(permissions, collection)
