from pymongo.collection import Collection

from ..IRegistry import IRegistryDelete
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryQuery


class MongoRegistryDelete(IRegistryDelete):
    __collection: Collection

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__collection = collection

    def __call__(self, query: RegistryQuery) -> RegistryResponse:
        result = self.__collection.delete_many(query)
        return RegistryResponse(count=result.deleted_count)
