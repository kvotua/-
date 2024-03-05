from abc import ABC, abstractmethod

from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryQuery


class IRegistryDelete(ABC):
    @abstractmethod
    def __call__(self, query: RegistryQuery) -> RegistryResponse:
        pass
