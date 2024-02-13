from abc import ABC, abstractmethod
from uuid import UUID

from app.core.registry.base_registry import RegistryBase


class ServiceBase(ABC):
    def __init__(self, registry: RegistryBase):
        self.registry = registry

    @abstractmethod
    def get_by_id(self, object_id: UUID | int):
        pass

    @abstractmethod
    def create(self, new_object: dict):
        pass

    @abstractmethod
    def delete_by_id(self, object_id: UUID | int):
        pass

    @abstractmethod
    def update(self, object_id: UUID | int, new_values):
        pass
