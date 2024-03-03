from .UserService import UserService
from .ProjectService import ProjectService
from app.registry import RegistryPermission, IRegistryFactory


class ServiceFactory:
    __registry_factory: IRegistryFactory
    __user_service: UserService
    __project_service: ProjectService

    def __init__(self, registry_factory: IRegistryFactory) -> None:
        self.__registry_factory = registry_factory
        self.instantiate_user_service()
        self.instantiate_project_service()

    def instantiate_user_service(self) -> None:
        users_registry = self.__registry_factory.get(
            "users",
            RegistryPermission(
                canCreate=True, canRead=True, canUpdate=True, canDelete=True
            ),
        )
        self.__user_service = UserService(users_registry)

    def instantiate_project_service(self) -> None:
        project_registry = self.__registry_factory.get(
            "projects",
            RegistryPermission(
                canCreate=True, canRead=True, canUpdate=True, canDelete=True
            ),
        )
        user_service_read_only = UserService(
            self.__registry_factory.get(
                "users",
                RegistryPermission(
                    canRead=True,
                ),
            )
        )
        self.__project_service = ProjectService(
            project_registry, user_service_read_only
        )

    def get_user_service(self) -> UserService:
        return self.__user_service

    def get_project_service(self) -> ProjectService:
        return self.__project_service
