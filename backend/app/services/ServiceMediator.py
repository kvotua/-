from app.registry import IRegistryFactory

from .NodeService import INodeService
from .NodeService.NodeService import NodeService
from .ProjectService import IProjectService
from .ProjectService.ProjectService import ProjectService
from .UserService import IUserService
from .UserService.UserService import UserService


class ServiceMediator:
    __registry_factory: IRegistryFactory
    __user_service: UserService
    __project_service: ProjectService
    __node_service: NodeService

    def __init__(self, registry_factory: IRegistryFactory) -> None:
        self.__registry_factory = registry_factory
        self.instantiate_user_service()
        self.instantiate_project_service()
        self.instantiate_node_service()
        self.inject_dependencies()

    def inject_dependencies(self) -> None:
        self.__project_service.inject_dependencies(
            self.__user_service, self.__node_service
        )
        self.__node_service.inject_dependencies(
            self.__user_service, self.__project_service
        )

    def instantiate_user_service(self) -> None:
        users_registry = self.__registry_factory.get("users")
        self.__user_service = UserService(users_registry)

    def instantiate_project_service(self) -> None:
        project_registry = self.__registry_factory.get("projects")
        self.__project_service = ProjectService(project_registry)

    def instantiate_node_service(self) -> None:
        node_registry = self.__registry_factory.get("nodes")

        self.__node_service = NodeService(node_registry)

    def get_user_service(self) -> IUserService:
        return self.__user_service

    def get_project_service(self) -> IProjectService:
        return self.__project_service

    def get_node_service(self) -> INodeService:
        return self.__node_service
