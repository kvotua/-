from abc import ABC, abstractmethod
from .schemas import (
    NodeSchema,
    NodeCreateSchema,
    NodeUpdateSchema,
    NodeTreeSchema,
)


class INodeService(ABC):

    @abstractmethod
    def try_get(self, initiator_id: str, node_id: str) -> NodeSchema:
        pass

    @abstractmethod
    def try_update(
        self, initiator_id: str, node_id: str, node_update: NodeUpdateSchema
    ) -> None:
        pass

    @abstractmethod
    def try_get_tree(self, initiator_id: str, node_id: str) -> NodeTreeSchema:
        pass

    @abstractmethod
    def try_delete(self, initiator_id: str, node_id: str) -> None:
        pass

    @abstractmethod
    def create(self, initiator_id: str, new_node: NodeCreateSchema) -> str:
        pass

    @abstractmethod
    def exist(self, node_id: str) -> bool:
        pass
