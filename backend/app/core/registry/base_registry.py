from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class RegistryBase(ABC):

    @abstractmethod
    def get(self, field_name: str, value: Any, skip: int = 0, limit: int = 5):
        pass

    @abstractmethod
    def get_by_id(self, object_id: int | UUID):
        pass

    @abstractmethod
    def create(self, new_object: dict):
        pass

    @abstractmethod
    def update(self, object_id: int | UUID, new_values: dict):
        pass

    @abstractmethod
    def delete(self, object_id: int | UUID):
        pass

    @abstractmethod
    def exist(self, object_id: int | UUID):
        pass
