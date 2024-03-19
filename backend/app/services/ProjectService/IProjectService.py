from abc import ABC, abstractmethod

from ..NodeService.schemas import NodeId
from ..UserService.schemas import UserId
from .schemas import ProjectCreateSchema, ProjectId, ProjectSchema, ProjectUpdateSchema


class IProjectService(ABC):
    @abstractmethod
    def try_get_by_user_id(
        self, initiator_id: UserId, user_id: UserId
    ) -> list[ProjectSchema]:
        pass

    @abstractmethod
    def try_get(self, initiator_id: UserId, project_id: ProjectId) -> ProjectSchema:
        pass

    @abstractmethod
    def create(
        self, initiator_id: UserId, new_project: ProjectCreateSchema
    ) -> ProjectSchema:
        pass

    @abstractmethod
    def try_update(
        self,
        initiator_id: UserId,
        project_id: ProjectId,
        project_update: ProjectUpdateSchema,
    ) -> None:
        pass

    @abstractmethod
    def try_delete(self, initiator_id: UserId, project_id: ProjectId) -> None:
        pass

    @abstractmethod
    def get_by_root_node_id(self, node_id: NodeId) -> ProjectSchema:
        pass
