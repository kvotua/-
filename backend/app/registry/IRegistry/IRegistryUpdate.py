from abc import ABC, abstractmethod

from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class IRegistryUpdate(ABC):
    @abstractmethod
    def __call__(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        pass
