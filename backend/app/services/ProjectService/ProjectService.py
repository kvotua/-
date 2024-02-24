from app.registry import IRegistry
from .schemas import (
    ProjectCreateSchema,
    ProjectSchema,
    ProjectUpdateSchema,
)
from ..NodeService.schemas import NodeCreateSchema

from ..exceptions import (
    ProjectNotFoundError,
    NotAllowedError,
    NodeNotFoundError,
)
from .IProjectService import IProjectService

from ..NodeService import INodeService
from ..UserService import IUserService


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
            user_service (UserService): The service to communicate with users.
        """
        self.__registry = registry

    def inject_dependencies(
        self, user_service: IUserService, node_service: INodeService
    ) -> None:
        self.__user_service = user_service
        self.__node_service = node_service

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
            UserNotFoundError: If the initiator or the user with the specified ID is
                not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
        """
        self.__user_service.user_exist_validation(initiator_id)
        self.__user_service.user_exist_validation(user_id)
        if initiator_id != user_id:
            raise NotAllowedError()
        return self._get_by_user_id(user_id)

    def try_get(self, initiator_id: str, project_id: str) -> ProjectSchema:
        """
        Attempt to retrieve a specific project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to retrieve.

        Returns:
            ProjectSchema: The project information.

        Raises:
            UserNotFoundError: If the initiator or the project with the specified ID
                is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
        """
        self.__user_service.user_exist_validation(initiator_id)
        try:
            project = self._get(project_id)
        except ProjectNotFoundError:
            raise NotAllowedError()
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        return project

    def create(self, initiator_id: str, new_project: ProjectCreateSchema) -> str:
        """
        Create a new project.

        Parameters:
            initiator_id (str): The ID of the user who owns the project.
            new_project (ProjectCreateSchema): The schema representing the new project
                to create.

        Raises:
            UserNotFoundError: If the owner of the project is not found.
        """
        self.__user_service.user_exist_validation(initiator_id)
        node_id = self.__node_service.create(
            initiator_id, NodeCreateSchema(parent=None, children=[])
        )
        project = ProjectSchema(
            **new_project.model_dump(), owner_id=initiator_id, core_node_id=node_id
        )
        self.__registry.create(project.model_dump())
        return project.id

    def try_update(
        self, initiator_id: str, project_id: str, project_update: ProjectUpdateSchema
    ) -> None:
        """
        Attempt to update a project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to update.
            project_update (ProjectUpdateSchema): The schema representing the updates
                to apply.

        Raises:
            UserNotFoundError: If the initiator of the update is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        self.__user_service.user_exist_validation(initiator_id)
        try:
            project = self._get(project_id)
        except ProjectNotFoundError:
            raise NotAllowedError()
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        self._update(project_id, project_update)

    def try_delete(self, initiator_id: str, project_id: str) -> None:
        """
        Attempt to delete a project.

        Parameters:
            initiator_id (str): The ID of the initiator performing the operation.
            project_id (str): The ID of the project to delete.

        Raises:
            UserNotFoundError: If the initiator of the deletion is not found.
            NotAllowedError: If the initiator is not allowed to perform the operation.
            ProjectNotFoundError: If the project with the specified ID is not found.
        """
        self.__user_service.user_exist_validation(initiator_id)
        try:
            project = self._get(project_id)
        except ProjectNotFoundError:
            raise NotAllowedError()
        if initiator_id != project.owner_id:
            raise NotAllowedError()
        self._delete(project_id)

    def _delete(self, project_id: str) -> None:
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

    def _update(self, project_id: str, project_update: ProjectUpdateSchema) -> None:
        """
        Update a project.

        Parameters:
            project_id (str): The ID of the project to update.
            project_update (ProjectUpdateSchema): The schema representing the updates
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

    def _get(self, project_id: str) -> ProjectSchema:
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

    def _get_by_user_id(self, user_id: str) -> list[ProjectSchema]:
        """
        Retrieve projects associated with a user.

        Parameters:
            user_id (str): The ID of the user whose projects to retrieve.

        Returns:
            list[ProjectSchema]: A list of projects associated with the user.

        Raises:
            UserNotFoundError: If the user with the specified ID is not found.
        """
        projects = self.__registry.read({"owner_id": user_id})
        return [ProjectSchema(**project) for project in projects]

    def try_get_by_core_node_id(self, initiator_id: str, node_id: str) -> ProjectSchema:
        if not self.__node_service.exist(node_id):
            raise NodeNotFoundError()
        project = self.__registry.read({"core_node_id": node_id})
        if len(project) < 1:
            raise ProjectNotFoundError()
        project_schema = ProjectSchema(**project[0])
        if project_schema.owner_id != initiator_id:
            raise NotAllowedError()
        return project_schema
