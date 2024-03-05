from pymongo.collection import Collection

from ..IRegistry import IRegistryUpdate
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class MongoRegistryUpdate(IRegistryUpdate):
    __collection: Collection

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__collection = collection

    def __call__(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        result = self.__collection.update_many(query, {"$set": data})
        return RegistryResponse(count=result.modified_count)
