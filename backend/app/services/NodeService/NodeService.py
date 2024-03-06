from app.registry import IRegistry

from ..exceptions import NodeCannotBeDeletedError, NodeNotFoundError, NotAllowedError
from ..ProjectService.ProjectService import IProjectService
from ..UserService.UserService import IUserService
from .INodeService import INodeService
from .schemas import NodeCreateSchema, NodeSchema, NodeTreeSchema, NodeUpdateSchema


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

    def try_get(self, initiator_id: str, node_id: str) -> NodeSchema:
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

        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self.__get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        return self.__get(node_id)

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
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ValueError: raised when node has no parent
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self.__get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        if node_update.parent is not None:
            self.__reparent(node_id, node_update.parent)

    def __reparent(self, node_id: str, new_parent_id: str) -> None:
        """
        change parent of node with new_parent_id

        Args:
            node_id (str): node to change parent id
            new_parent_id (str): new parent id

        Raises:
            ValueError: raised when node has no parent
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = self.__get(node_id)
        parent = self.__get(new_parent_id)
        if node.parent is None:
            raise ValueError()
        old_parent = self.__get(node.parent)

        old_parent.children.remove(node.id)
        parent.children.append(node.id)
        node.parent = parent.id

        self.__registry.update({"id": node.id}, node.model_dump())
        self.__registry.update({"id": parent.id}, parent.model_dump())
        self.__registry.update({"id": old_parent.id}, old_parent.model_dump())

    def try_get_tree(self, initiator_id: str, node_id: str) -> NodeTreeSchema:
        """
        try get tree preresentation of a project

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Returns:
            NodeTreeSchema: tree representation of a project

        Raises:
            UserNotFoundError: raises when user with given id does not exist
            NotAllowedError: raised when user tries to update node from project \
            they do not own
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node


        """
        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self.__get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        node_tree = self.__get_tree(node_id)
        return node_tree

    def try_delete(self, initiator_id: str, node_id: str) -> None:
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
        self.__user_service.user_exist_validation(initiator_id)
        node = self.__get(node_id)
        if node.parent is None:
            raise NodeCannotBeDeletedError()
        root_node_id = self.__get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        self.__delete(node_id)

    def create(self, initiator_id: str, new_node: NodeCreateSchema) -> str:
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
        self.__user_service.user_exist_validation(initiator_id)
        root_node_id = self.__get_root_node_id(new_node.parent)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()
        if not self.exist(new_node.parent):
            raise NodeNotFoundError()

        node = NodeSchema(**new_node.model_dump())
        parent = self.__get(new_node.parent)
        parent.children.append(node.id)

        self.__registry.create(node.model_dump())
        self.__registry.update({"id": parent.id}, parent.model_dump())

        return node.id

    def create_root(self) -> str:
        """create root node for project

        Returns:
            str: id of a freshly created node
        """
        node = NodeSchema(parent=None)
        self.__registry.create(node.model_dump())
        return node.id

    def exist(self, node_id: str) -> bool:
        """
        check if node exist

        Args:
            node_id (str): id of a node to check

        Returns:
            bool: bool result depicting existence of a node
        """
        nodes = self.__registry.read({"id": node_id})
        return len(nodes) > 0

    def __get(self, node_id: str) -> NodeSchema:
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

    def __get_root_node_id(self, node_id: str) -> str:
        """
        get root node id of a given node

        Args:
            node_id (str): id of node whose root you are seeking

        Returns:
            str: id of root node

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node = self.__get(node_id)
        while node.parent is not None:
            node = self.__get(node.parent)
        return node.id

    def __get_tree(self, node_id: str) -> NodeTreeSchema:
        """
        get tree representation of project

        Args:
            node_id (str): id of a ROOT node

        Returns:
            NodeTreeSchema: tree representaion of a project

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """
        node_id = self.__get_root_node_id(node_id)
        node = self.__get(node_id)
        node_tree = NodeTreeSchema(id=node.id, children=list())
        for child in node.children:
            child_node = self.__get(child)
            child_node_tree = NodeTreeSchema(id=child_node.id, children=list())
            if len(child_node.children) > 0:
                child_node_tree.children.append(self.__get_tree(child_node.id))
            node_tree.children.append(child_node_tree)
        return node_tree

    def __delete(self, node_id: str) -> None:
        """
        Deletes node

        Args:
            node_id (str): id of a node to be deleted

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """

        node = self.__get(node_id)
        for child in node.children:
            self.__delete(child)

        response = self.__registry.delete({"id": node.id})
        if response.count < 1:
            raise NodeNotFoundError()
