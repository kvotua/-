from mongomock.database import Database
from mongomock.mongo_client import MongoClient
from ..IRegistry import IRegistry, IRegistryFactory
from .MongoMockRegistry import MongoMockRegistry
from ..RegistryPermission import RegistryPermission


class MongoMockRegistryFactory(IRegistryFactory):
    """
    Factory class for creating instances of MongoMockRegistry.

    Attributes:
        __client (MongoClient): The MongoDB Mock client.
        __database (Database): The MongoDB Mock database.

    Methods:
        get: Creates an instance of MongoMockRegistry \
            based on the provided name and permissions.
    """

    __client: MongoClient
    __database: Database

    def __init__(self) -> None:
        """
        Initializes a new instance of the MongoMockRegistryFactory class.
        """
        super().__init__()
        self.__client = MongoClient(
            host="mongo",
            port=27017,
        )
        self.__database = self.__client.get_database("backend")

    def get(self, name: str, permissions: RegistryPermission) -> IRegistry:
        """
        Creates an instance of MongoMockRegistry based on the provided name \
            and permissions.

        Args:
            name (str): The name of the collection in the MongoDB Mock database.
            permissions (RegistryPermission): The permissions for the mock registry.

        Returns:
            IRegistry: An instance of MongoRegistry.
        """
        collection = self.__database.get_collection(name)
        return MongoMockRegistry(permissions, collection)
