from app.registry import IRegistry

from ..exceptions import NodeCannotBeDeletedError, NodeNotFoundError, NotAllowedError
from ..ProjectService.ProjectService import IProjectService
from ..UserService.schemas import UserId
from ..UserService.UserService import IUserService
from .INodeService import INodeService
from .schemas import (
    NodeCreateSchema,
    NodeId,
    NodeSchema,
    NodeTreeSchema,
    NodeUpdateSchema,
)


class NodeService(INodeService):
    """
    A service class for managing node-related operations.
    """

    __registry: IRegistry
    __user_service: IUserService
    __project_service: IProjectService

    def __init__(
        self,
        registry: IRegistry,
    ) -> None:
        """
        Initialize the NodeService with registry

        Args:
            registry (IRegistry): the registry used for node operations
        """
        self.__registry = registry

    def inject_dependencies(
        self, user_service: IUserService, project_service: IProjectService
    ) -> None:
        """
        injects dependencies

        Args:
            user_service (IUserService): service for interacting with users
            project_service (IProjectService): service for interacting with projects
        """
        self.__user_service = user_service
        self.__project_service = project_service

    async def try_get(self, initiator_id: UserId, node_id: NodeId) -> NodeSchema:
        """
        try get node

        Args:
            initiator_id (str): user id
            node_id (str): id of node

        Returns:
        NodeSchema: dict representation of node stored in database

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when operation is performed by user who does not \
            own the project node belongs to
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """

        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)
        return await self.__get(node_id)

    async def try_update(
        self, initiator_id: UserId, node_id: NodeId, node_update: NodeUpdateSchema
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
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ValueError: raised when node has no parent
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)

        if node_update.parent is not None:
            await self.__reparent(node_id, node_update.parent)

    async def try_get_tree(
        self, initiator_id: UserId, node_id: NodeId
    ) -> NodeTreeSchema:
        """
        Try get subtree preresentation of a node and subnodes

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Returns:
            NodeTreeSchema: tree representation of a node and subnodes

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
                they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)

        node_tree = await self.__get_tree(node_id)
        return node_tree

    async def try_delete(self, initiator_id: UserId, node_id: NodeId) -> None:
        """
        try delete

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Raises:
            NodeCannotBeDeleted: raised when attempting to delete root node
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, node_id)

        node = await self.__get(node_id)
        if node.parent is None:
            raise NodeCannotBeDeletedError()
        await self.delete(node_id)

    async def create(self, initiator_id: UserId, new_node: NodeCreateSchema) -> str:
        """
        create node

        Args:
            initiator_id (str): id of a user
            new_node (NodeCreateSchema): new node data

        Returns:
            str: id of a new node

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised if user tries to add a new node to a project they \
            do not own
            NodeNotFoundError: raised when there is no node with id provided \
            by new_node
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node

        """
        await self.__user_service.user_exist_validation(initiator_id)
        await self.__check_initiator_permission(initiator_id, new_node.parent)

        node = NodeSchema(**new_node.model_dump())
        parent = await self.__get(new_node.parent)
        parent.children.append(node.id)

        self.__registry.create(node.model_dump())
        self.__registry.update({"id": parent.id}, parent.model_dump())

        return node.id

    async def create_root(self) -> NodeId:
        """create root node for project

        Returns:
            str: id of a freshly created node
        """
        node = NodeSchema(parent=None)
        self.__registry.create(node.model_dump())
        return node.id

    async def exist(self, node_id: NodeId) -> bool:
        """
        check if node exist

        Args:
            node_id (str): id of a node to check

        Returns:
            bool: bool result depicting existence of a node
        """
        nodes = self.__registry.read({"id": node_id})
        return len(nodes) > 0

    async def __get(self, node_id: NodeId) -> NodeSchema:
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

    async def __get_root_node_id(self, node_id: NodeId) -> NodeId:
        """
        get root node id of a given node

        Args:
            node_id (str): id of node whose root you are seeking

        Returns:
            str: id of root node

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        while node.parent is not None:
            node = await self.__get(node.parent)
        return node.id

    async def __get_tree(self, node_id: NodeId) -> NodeTreeSchema:
        """
        Get tree representation of node and subnodes

        Args:
            node_id (str): id of a node

        Returns:
            NodeTreeSchema: tree representaion of a node and subnodes

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        tree_root = NodeTreeSchema(id=node_id, children=[])
        nodes_to_process = [tree_root]
        while len(nodes_to_process) > 0:
            current_tree_node = nodes_to_process.pop()
            current_node = await self.__get(current_tree_node.id)
            for child_node_id in current_node.children:
                current_tree_node.children.append(
                    NodeTreeSchema(id=child_node_id, children=[])
                )
            nodes_to_process.extend(current_tree_node.children)
        return tree_root

    async def delete(self, node_id: NodeId) -> None:
        """
        Deletes node

        Args:
            node_id (str): id of a node to be deleted

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        if node.parent is not None:
            parent = await self.__get(node.parent)
            parent.children.remove(node_id)
            self.__registry.update({"id": parent.id}, parent.model_dump())

        children = [node_id]
        while len(children) > 0:
            node_id = children.pop()
            try:
                node = await self.__get(node_id)
            except NodeNotFoundError:
                continue
            children.extend(node.children)
            self.__registry.delete({"id": node_id})

    async def __reparent(self, node_id: NodeId, new_parent_id: NodeId) -> None:
        """
        change parent of node with new_parent_id

        Args:
            node_id (str): node to change parent id
            new_parent_id (str): new parent id

        Raises:
            ValueError: raised when node has no parent
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = await self.__get(node_id)
        parent = await self.__get(new_parent_id)
        if node.parent is None:
            raise ValueError()
        old_parent = await self.__get(node.parent)

        old_parent.children.remove(node.id)
        parent.children.append(node.id)
        node.parent = parent.id

        self.__registry.update({"id": node.id}, node.model_dump())
        self.__registry.update({"id": parent.id}, parent.model_dump())
        self.__registry.update({"id": old_parent.id}, old_parent.model_dump())

    async def __check_initiator_permission(
        self, initiator_id: UserId, node_id: NodeId
    ) -> None:
        """
        Check if initiator can manipulate with node pointed by node_id

        Args:
            initiator_id (str): id of user who initiates action
            node_id (str): id of node which will be used

        Raises:
            NotAllowedError: raised when initiator can't performe actions with node
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        root_node_id = await self.__get_root_node_id(node_id)
        project = await self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()
