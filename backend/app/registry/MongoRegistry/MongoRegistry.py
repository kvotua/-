from pymongo.collection import Collection

from ..IRegistry import IRegistry
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class MongoRegistry(IRegistry):
    __collection: Collection

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__collection = collection

    def create(self, data: RegistryData) -> None:
        self.__collection.insert_one(data)

    def read(self, query: RegistryQuery) -> list[RegistryData]:
        return list(self.__collection.find(query))

    def update(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        result = self.__collection.update_many(query, {"$set": data})
        return RegistryResponse(count=result.modified_count)

    def delete(self, query: RegistryQuery) -> RegistryResponse:
        result = self.__collection.delete_many(query)
        return RegistryResponse(count=result.deleted_count)
