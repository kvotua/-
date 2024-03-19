from abc import ABC, abstractmethod

from ..UserService.schemas import UserId
from .schemas import (
    NodeCreateSchema,
    NodeId,
    NodeSchema,
    NodeTreeSchema,
    NodeUpdateSchema,
)


class INodeService(ABC):
    @abstractmethod
    def try_get(self, initiator_id: UserId, node_id: NodeId) -> NodeSchema:
        pass

    @abstractmethod
    def try_update(
        self, initiator_id: UserId, node_id: NodeId, node_update: NodeUpdateSchema
    ) -> None:
        pass

    @abstractmethod
    def try_get_tree(self, initiator_id: UserId, node_id: NodeId) -> NodeTreeSchema:
        pass

    @abstractmethod
    def try_delete(self, initiator_id: UserId, node_id: NodeId) -> None:
        pass

    @abstractmethod
    def create(self, initiator_id: UserId, new_node: NodeCreateSchema) -> str:
        pass

    @abstractmethod
    def create_root(self) -> str:
        pass

    @abstractmethod
    def exist(self, node_id: NodeId) -> bool:
        pass

    @abstractmethod
    def delete(self, node_id: NodeId) -> None:
        pass
