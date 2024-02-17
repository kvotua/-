from abc import ABC, abstractmethod
from .IRegistry import IRegistry
from ..RegistryPermission import RegistryPermission


class IRegistryFactory(ABC):
    @abstractmethod
    def get(self, name: str, permissions: RegistryPermission) -> IRegistry:
        pass
