from app.registry import IRegistry
from .schemas import (
    NodeSchema,
    NodeCreateSchema,
    NodeUpdateSchema,
    NodeTreeSchema,
)

from ..exceptions import NodeNotFoundError
from .INodeService import INodeService
from ..ProjectService.ProjectService import IProjectService
from ..UserService.UserService import IUserService


class NodeService(INodeService):
    __registry: IRegistry
    __user_service: IUserService
    __project_service: IProjectService

    def __init__(
        self,
        registry: IRegistry,
    ) -> None:
        self.__registry = registry

    def inject_dependencies(
        self, user_service: IUserService, project_service: IProjectService
    ) -> None:
        self.__user_service = user_service
        self.__project_service = project_service

    def try_get(self, initiator_id: str, node_id: str) -> NodeSchema:
        """
        try to get node

        Args:
            initiator_id (str): id of user
            node_id (str): node id

        Raises:
            UserNotFoundError: raises when user with given id does not exist

        Returns:
            NodeSchema: dict representation of node
        """
        self.__user_service.user_exist_validation(initiator_id)
        return self._get(node_id)

    def try_update(
        self, initiator_id: str, node_id: str, node_update: NodeUpdateSchema
    ) -> None:
        """
        update node

        Args:
            initiator_id (str): user id
            node_id (str): id of a node
            node_update (NodeUpdateSchema): dict representation of data \
                used to update node

        Raises:
            UserNotFoundError: raises when user with given id does not exist
        """
        self.__user_service.user_exist_validation(initiator_id)
        self._update(node_id, node_update)

    def try_get_tree(self, initiator_id: str, node_id: str) -> NodeTreeSchema:
        """
        try to get tree representation of a node and it's children

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Raises:
            UserNotFoundError: raises when user with given id does not exist

        Returns:
            NodeTreeSchema: dict representation of node and it's children
        """
        self.__user_service.user_exist_validation(initiator_id)
        node = self._get(node_id)
        node_tree = NodeTreeSchema(id=node.id, children=list())
        for child in node.children:
            child_node = self._get(child)
            child_node_tree = NodeTreeSchema(id=child_node.id, children=list())
            if len(child_node.children) > 0:
                child_node_tree.children.append(
                    self.try_get_tree(initiator_id, child_node.id)
                )
            node_tree.children.append(child_node_tree)
        return node_tree

    def try_delete(self, initiator_id: str, node_id: str) -> None:
        """
        try to delete node

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Raises:
            UserNotFoundError: raises when user with given id does not exist
        """
        self.__user_service.user_exist_validation(initiator_id)
        self._delete(node_id)

    def create(self, initiator_id: str, new_node: NodeCreateSchema) -> str:
        """
        create node

        Args:
            owner_id (str): user id
            new_node (NodeCreateSchema): data nedeed to create new node

        Raises:
            UserNotFoundError: raises when user with given id does not exist

        Returns:
            str: node id
        """
        self.__user_service.user_exist_validation(initiator_id)
        node = NodeSchema(**new_node.model_dump())
        self.__registry.create(node.model_dump())
        return node.id

    def exist(self, node_id: str) -> bool:
        nodes = self.__registry.read({"id": node_id})
        return len(nodes) < 0

    def _get(self, node_id: str) -> NodeSchema:
        """
        get node directly from database

        Args:
            node_id (str): node id

        Raises:
            NodeNotFoundError: raised when node with given id does not exist

        Returns:
            NodeSchema: dict representation of node
        """
        nodes = self.__registry.read({"id": node_id})
        if len(nodes) < 1:
            raise NodeNotFoundError()
        return NodeSchema(**nodes[0])

    def _update(self, node_id: str, node_update: NodeUpdateSchema) -> None:
        """
        update node directly from database

        Args:
            node_id (str): node id
            node_update (NodeUpdateSchema): data needed to update node

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        response = self.__registry.update(
            {"id": node_id}, node_update.model_dump(exclude_none=True)
        )
        if response.count < 1:
            raise NodeNotFoundError()

    def _delete(self, node_id: str) -> None:
        """
        delete node directly from database

        Args:
            node_id (str): node id

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        response = self.__registry.delete({"id": node_id})
        if response.count < 1:
            raise NodeNotFoundError()
