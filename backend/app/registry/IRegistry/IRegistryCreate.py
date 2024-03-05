from abc import ABC, abstractmethod

from ..RegistryTypes import RegistryData


class IRegistryCreate(ABC):
    @abstractmethod
    def __call__(self, data: RegistryData) -> None:
        pass
