from abc import ABC, abstractproperty

from .IRegistryCreate import IRegistryCreate
from .IRegistryDelete import IRegistryDelete
from .IRegistryRead import IRegistryRead
from .IRegistryUpdate import IRegistryUpdate


class IRegistry(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractproperty
    def create(self) -> IRegistryCreate:
        pass

    @abstractproperty
    def read(self) -> IRegistryRead:
        pass

    @abstractproperty
    def update(self) -> IRegistryUpdate:
        pass

    @abstractproperty
    def delete(self) -> IRegistryDelete:
        pass
