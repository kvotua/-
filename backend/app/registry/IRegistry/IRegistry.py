from abc import ABC, abstractmethod
from typing import Any, List
from ..RegistryPermissionException import RegistryPermissionException
from ..RegistryPermission import RegistryPermission
from ..RegistryResponse import RegistryResponse
from ..RegistryTypes import RegistryData, RegistryQuery


class IRegistry(ABC):
    __permissions: RegistryPermission

    def __init__(self, permissions: RegistryPermission) -> None:
        super().__init__()
        self.__permissions = permissions

    def __getattribute__(self, __name: str) -> Any:
        if __name == "create" and not self.permissions.canCreate:
            raise RegistryPermissionException()
        if __name == "read" and not self.permissions.canRead:
            raise RegistryPermissionException()
        if __name == "update" and not self.permissions.canUpdate:
            raise RegistryPermissionException()
        if __name == "delete" and not self.permissions.canDelete:
            raise RegistryPermissionException()
        return super().__getattribute__(__name)

    @property
    def permissions(self) -> RegistryPermission:
        return self.__permissions

    @abstractmethod
    def create(self, data: RegistryData) -> None:
        pass

    @abstractmethod
    def read(self, query: RegistryQuery) -> List[RegistryData]:
        pass

    @abstractmethod
    def update(self, query: RegistryQuery, data: RegistryData) -> RegistryResponse:
        pass

    @abstractmethod
    def delete(self, query: RegistryQuery) -> RegistryResponse:
        pass
