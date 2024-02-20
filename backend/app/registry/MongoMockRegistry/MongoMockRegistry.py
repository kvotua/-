from typing import List
from ..RegistryPermission import RegistryPermission
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery
from ..IRegistry import IRegistry
from mongomock.collection import Collection


class MongoMockRegistry(IRegistry):
    """
    Implementation of IRegistry interface for interacting with MongoDB.
    """

    __collection: Collection

    def __init__(self, permissions: RegistryPermission, collection: Collection) -> None:
        """
        Initializes a new instance of the MongoMockRegistry class.

        Args:
            permissions (RegistryPermission): The permissions for the registry.
            collection (Collection): The MongoDB Mock collection to interact with.
        """
        super().__init__(permissions)
        self.__collection = collection

    def create(self, data: RegistryData) -> None:
        self.__collection.insert_one(data)

    def read(self, query: RegistryQuery) -> List[RegistryData]:
        return list(self.__collection.find(query))

    def update(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        result = self.__collection.update_many(query, {"$set": data})
        return RegistryResponse(count=result.modified_count)

    def delete(self, query: RegistryQuery) -> RegistryResponse:
        result = self.__collection.delete_many(query)
        return RegistryResponse(count=result.deleted_count)
