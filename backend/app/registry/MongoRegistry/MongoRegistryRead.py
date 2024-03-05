from typing import List

from pymongo.collection import Collection

from ..IRegistry import IRegistryRead
from ..RegistryTypes import RegistryData, RegistryQuery


class MongoRegistryRead(IRegistryRead):
    __collection: Collection

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__collection = collection

    def __call__(self, query: RegistryQuery) -> List[RegistryData]:
        return list(self.__collection.find(query))
