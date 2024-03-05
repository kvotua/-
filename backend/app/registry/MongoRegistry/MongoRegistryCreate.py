from pymongo.collection import Collection

from ..IRegistry import IRegistryCreate
from ..RegistryTypes import RegistryData


class MongoRegistryCreate(IRegistryCreate):
    __collection: Collection

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__collection = collection

    def __call__(self, data: RegistryData) -> None:
        self.__collection.insert_one(data)
