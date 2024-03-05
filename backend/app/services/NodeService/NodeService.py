from app.registry import IRegistry

from ..exceptions import NodeCannotBeDeletedError, NodeNotFoundError, NotAllowedError
from ..ProjectService.ProjectService import IProjectService
from ..UserService.UserService import IUserService
from .INodeService import INodeService
from .schemas import NodeCreateSchema, NodeSchema, NodeTreeSchema, NodeUpdateSchema


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
            NotAllowedError: raised when user tries to update node from project \
            they do not own
        """

        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self._get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

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
            NotAllowedError: raised when user tries to update node from project \
            they do not own
        """
        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self._get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        if node_update.parent is not None:
            self._reparent(node_id, node_update.parent)

    def _reparent(self, node_id: str, new_parent_id: str) -> None:
        node = self._get(node_id)
        parent = self._get(new_parent_id)
        if node.parent is None:
            raise ValueError()
        old_parent = self._get(node.parent)

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

        Raises:
            NotAllowedError: raised when user tries to get representation \
            of a project they do not own

        Returns:
            NodeTreeSchema: tree representation of a project
        """
        self.__user_service.user_exist_validation(initiator_id)

        root_node_id = self._get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        node_tree = self._get_tree(node_id)
        return node_tree

    def try_delete(self, initiator_id: str, node_id: str) -> None:
        """
        try to delete node

        Args:
            initiator_id (str): user id
            node_id (str): node id

        Raises:
            NodeCannotBeDeleted: raised when attempting to delete root node
            NotAllowedError: raised when user attempts to delete node from \
            project they do not own
        """
        self.__user_service.user_exist_validation(initiator_id)
        node = self._get(node_id)
        if node.parent is None:
            raise NodeCannotBeDeletedError()
        root_node_id = self._get_root_node_id(node_id)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()

        self._delete(node_id)

    def create(self, initiator_id: str, new_node: NodeCreateSchema) -> str:
        """
        create node

        Args:
            initiator_id (str): id of a user
            new_node (NodeCreateSchema): new node data

        Raises:
            NotAllowedError: raised if user tries to add a new node to a project they \
            do not own,DOES NOT TRIGGERS WHEN CREATING NEW PROJECT
            NodeNotFoundError: raised when there is no node with provided by \
            new_node parent id

        Returns:
            str: node id
        """
        self.__user_service.user_exist_validation(initiator_id)
        root_node_id = self._get_root_node_id(new_node.parent)
        project = self.__project_service.get_by_root_node_id(root_node_id)
        if project.owner_id != initiator_id:
            raise NotAllowedError()
        if not self.exist(new_node.parent):
            raise NodeNotFoundError()

        node = NodeSchema(**new_node.model_dump())
        if node.parent is None:
            raise ValueError()
        parent = self._get(node.parent)
        parent.children.append(node.id)

        self.__registry.create(node.model_dump())
        self.__registry.update({"id": parent.id}, parent.model_dump())

        return node.id

    def create_root(self) -> str:
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

    def _get_root_node_id(self, node_id: str) -> str:
        """
        get root node id of a given node

        Args:
            node_id (str): id of node whose root you are seeking

        Returns:
            str: id of root node
        """
        node = self._get(node_id)
        while node.parent is not None:
            node = self._get(node.parent)
        return node.id

    def _get_tree(self, node_id: str) -> NodeTreeSchema:
        """
        get tree representation of project

        Args:
            node_id (str): id of a ROOT node

        Returns:
            NodeTreeSchema: tree representaion of a project
        """
        node_id = self._get_root_node_id(node_id)
        node = self._get(node_id)
        node_tree = NodeTreeSchema(id=node.id, children=list())
        for child in node.children:
            child_node = self._get(child)
            child_node_tree = NodeTreeSchema(id=child_node.id, children=list())
            if len(child_node.children) > 0:
                child_node_tree.children.append(self._get_tree(child_node.id))
            node_tree.children.append(child_node_tree)
        return node_tree

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
        Deletes node

        Args:
            node_id (str): id of a node to be deleted

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
        """

        node = self._get(node_id)
        for child in node.children:
            self._delete(child)

        response = self.__registry.delete({"id": node.id})
        if response.count < 1:
            raise NodeNotFoundError()
