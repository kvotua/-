from pymongo.collection import Collection

from ..IRegistry import (
    IRegistry,
    IRegistryCreate,
    IRegistryDelete,
    IRegistryRead,
    IRegistryUpdate,
)
from .MongoRegistryCreate import MongoRegistryCreate
from .MongoRegistryDelete import MongoRegistryDelete
from .MongoRegistryRead import MongoRegistryRead
from .MongoRegistryUpdate import MongoRegistryUpdate


class MongoRegistry(IRegistry):
    __create: IRegistryCreate
    __read: IRegistryRead
    __update: IRegistryUpdate
    __delete: IRegistryDelete

    def __init__(self, collection: Collection) -> None:
        super().__init__()
        self.__create = MongoRegistryCreate(collection)
        self.__read = MongoRegistryRead(collection)
        self.__update = MongoRegistryUpdate(collection)
        self.__delete = MongoRegistryDelete(collection)

    @property
    def create(self) -> IRegistryCreate:
        return self.__create

    @property
    def read(self) -> IRegistryRead:
        return self.__read

    @property
    def update(self) -> IRegistryUpdate:
        return self.__update

    @property
    def delete(self) -> IRegistryDelete:
        return self.__delete
