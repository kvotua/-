from abc import ABC, abstractmethod
from typing import List

from ..RegistryTypes import RegistryData, RegistryQuery


class IRegistryRead(ABC):
    @abstractmethod
    def __call__(self, query: RegistryQuery) -> List[RegistryData]:
        pass
