from abc import ABC, abstractmethod

from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class IRegistry(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def create(self, data: RegistryData) -> None:
        pass

    @abstractmethod
    def read(self, query: RegistryQuery) -> list[RegistryData]:
        pass

    @abstractmethod
    def update(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        pass

    @abstractmethod
    def delete(self, query: RegistryQuery) -> RegistryResponse:
        pass
