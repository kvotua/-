from abc import ABC, abstractmethod
from .schemas import (
    ProjectCreateSchema,
    ProjectSchema,
    ProjectUpdateSchema,
)


class IProjectService(ABC):
    @abstractmethod
    def try_get_by_user_id(
        self, initiator_id: str, user_id: str
    ) -> list[ProjectSchema]:
        pass

    @abstractmethod
    def try_get(self, initiator_id: str, project_id: str) -> ProjectSchema:
        pass

    @abstractmethod
    def create(self, initiator_id: str, new_project: ProjectCreateSchema) -> str:
        pass

    @abstractmethod
    def try_update(
        self, initiator_id: str, project_id: str, project_update: ProjectUpdateSchema
    ) -> None:
        pass

    @abstractmethod
    def try_delete(self, inititator_id: str, project_id: str) -> None:
        pass

    @abstractmethod
    def try_get_by_core_node_id(
        self, inittiator_id: str, node_id: str
    ) -> ProjectSchema:
        pass
