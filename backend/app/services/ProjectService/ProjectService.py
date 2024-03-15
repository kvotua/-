from app.registry import IRegistry

from ..exceptions import (
    NodeNotFoundError,
    NotAllowedError,
    ProjectNotFoundError,
    UserNotFoundError,
)
from ..NodeService import INodeService
from ..UserService import IUserService
from .IProjectService import IProjectService
from .schemas import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema


class ProjectService(IProjectService):
    """
    A service class for managing project-related operations.
    """

    __registry: IRegistry
    __user_service: IUserService
    __node_service: INodeService

    def __init__(
        self,
        registry: IRegistry,
    ) -> None:
        """
        Initialize the ProjectService with a registry.

        Parameters:
            registry (IRegistry): The registry to use for project operations.
        """
        self.__registry = registry

    def inject_dependencies(
        self, user_service: IUserService, node_service: INodeService
    ) -> None:
        """
        Inject dependencies necessary for the service to work.

        Args:
            user_service (IUserService): Service for interacting with users
            node_service (INodeService): Service for interacting with projects
        """
        self.__user_service = user_service
        self.__node_service = node_service

    def user_exist_validation(self, user_id: str) -> None:
        self.__user_service.user_exist_validation(user_id)

    def try_get_by_user_id(
        self, initiator_id: str, user_id: str
    ) -> list[ProjectSchema]:
        """
        Attempt to retrieve projects associated with a user.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            user_id (str): The ID of the user whose projects to retrieve.

        Returns:
            list[ProjectSchema]: A list of projects associated with the user.

        Raises:
            UserNotFoundError: If the initiator or the user with the specified ID is \
                not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            WrongInitiatorError: if the initiator does not exist.
        """
        self.__user_service.user_exist_validation(initiator_id)
        project = self.__get_by_user_id(user_id)
        if initiator_id != user_id:
            raise NotAllowedError()
        return project

    def try_get(self, initiator_id: str, project_id: str) -> ProjectSchema:
        """
        Attempt to retrieve a specific project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to retrieve.

        Returns:
            ProjectSchema: The project information.

        Raises:
            ProjectNotFoundError: If the initiator or the project \
                with the specified ID is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            WrongInitiatorError: if the initiator does not exist.
        """
        self.__user_service.user_exist_validation(initiator_id)
        project = self.__get(project_id)
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        return project

    def create(
        self, initiator_id: str, new_project: ProjectCreateSchema
    ) -> ProjectSchema:
        """
        Create a new project.

        Parameters:
            initiator_id (str): The ID of the user who owns the project.
            new_project (ProjectCreateSchema): The schema representing the new project
                to create.

        Raises:
            WrongInitiatorError: if the initiator does not exist.
        """
        self.user_exist_validation(initiator_id)
        node_id = self.__node_service.create_root()
        project = ProjectSchema(
            **new_project.model_dump(), owner_id=initiator_id, core_node_id=node_id
        )
        self.__registry.create(project.model_dump())
        return project

    def try_update(
        self, initiator_id: str, project_id: str, project_update: ProjectUpdateSchema
    ) -> None:
        """
        Attempt to update a project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to update.
            project_update (ProjectUpdateSchema): The schema representing the updates \
                to apply.

        Raises:
            WrongInitiatorError: If the initiator of the update is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        self.__user_service.user_exist_validation(initiator_id)
        project = self.__get(project_id)
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        self.__update(project_id, project_update)

    def try_delete(self, initiator_id: str, project_id: str) -> None:
        """
        Attempt to delete a project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to delete.

        Raises:
            WrongInitiatorError: If the initiator of the deletion is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        self.__user_service.user_exist_validation(initiator_id)
        project = self.__get(project_id)
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        self.__delete(project_id)
        self.__node_service.delete(project.core_node_id)

    def try_get_by_core_node_id(self, initiator_id: str, node_id: str) -> ProjectSchema:
        """
        Get project info by core node ID.

        Args:
            initiator_id (str): ID of user which retrieves info
            node_id (str): ID of core node of the project

        Raises:
            NodeNotFoundError: if node with ID not exist
            ProjectNotFoundError: if project with this node as root not exist
            NotAllowedError: if user can't get this project

        Returns:
            ProjectSchema: _description_
        """
        if not self.__node_service.exist(node_id):
            raise NodeNotFoundError()
        project = self.__registry.read({"core_node_id": node_id})
        if len(project) < 1:
            raise ProjectNotFoundError()
        project_schema = ProjectSchema(**project[0])
        if project_schema.owner_id != initiator_id:
            raise NotAllowedError()
        return project_schema

    def get_by_root_node_id(self, node_id: str) -> ProjectSchema:
        """
        get project using it's root node

        Args:
            node_id (str): id of a root node

        Returns:
            ProjectSchema: dict representation of a project

        Raises:
            NodeNotFoundError: raised when node with given id does not exist
            ProjectNotFoundError: raised when there is no project that has given node \
                as a root node
        """
        if not self.__node_service.exist(node_id):
            raise NodeNotFoundError()
        project = self.__registry.read({"core_node_id": node_id})
        if len(project) < 1:
            raise ProjectNotFoundError()
        project_schema = ProjectSchema(**project[0])
        return project_schema

    def __delete(self, project_id: str) -> None:
        """
        Delete a project.

        Parameters:
            project_id (str): The ID of the project to delete.

        Raises:
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        response = self.__registry.delete({"id": project_id})
        if response.count < 1:
            raise ProjectNotFoundError()

    def __update(self, project_id: str, project_update: ProjectUpdateSchema) -> None:
        """
        Update a project.

        Parameters:
            project_id (str): The ID of the project to update.
            project_update (ProjectUpdateSchema): The schema representing the updates \
                to apply.

        Raises:
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        response = self.__registry.update(
            {"id": project_id},
            project_update.model_dump(exclude_none=True),
        )
        if response.count < 1:
            raise ProjectNotFoundError()

    def __get(self, project_id: str) -> ProjectSchema:
        """
        Retrieve a project.

        Parameters:
            project_id (str): The ID of the project to retrieve.

        Returns:
            ProjectSchema: The project information.

        Raises:
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        projects = self.__registry.read({"id": project_id})
        if len(projects) < 1:
            raise ProjectNotFoundError()
        return ProjectSchema(**projects[0])

    def __get_by_user_id(self, user_id: str) -> list[ProjectSchema]:
        """
        Retrieve projects associated with a user.

        Parameters:
            user_id (str): The ID of the user whose projects to retrieve.

        Returns:
            list[ProjectSchema]: A list of projects associated with the user.

        Raises:
            UserNotFoundError: If the user with the specified ID is not found.
        """
        if not self.__user_service.exist(user_id):
            raise UserNotFoundError()
        projects = self.__registry.read({"owner_id": user_id})
        return [ProjectSchema(**project) for project in projects]
