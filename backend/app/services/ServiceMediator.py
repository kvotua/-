from app.registry import IRegistryFactory

from .AttributeService import IAttributeService
from .AttributeService.AttributeService import AttributeService
from .NodeService import INodeService
from .NodeService.NodeService import NodeService
from .ProjectService import IProjectService
from .ProjectService.ProjectService import ProjectService
from .TemplateService.ITemplateService import ITemplateService
from .TemplateService.TemplateService import TemplateService
from .UserService import IUserService
from .UserService.UserService import UserService


class ServiceMediator:
    __registry_factory: IRegistryFactory
    __user_service: UserService
    __project_service: ProjectService
    __node_service: NodeService
    __template_service: TemplateService
    __attribute_service: AttributeService
    __dependencies_injected: bool = False

    def __init__(self, registry_factory: IRegistryFactory) -> None:
        self.__registry_factory = registry_factory
        self.__instantiate_user_service()
        self.__instantiate_project_service()
        self.__instantiate_node_service()
        self.__instantiate_template_service()
        self.__instantiate_attribute_service()

    async def get_user_service(self) -> IUserService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__user_service

    async def get_project_service(self) -> IProjectService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__project_service

    async def get_node_service(self) -> INodeService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__node_service

    async def get_template_service(self) -> ITemplateService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__template_service

    async def get_attribute_service(self) -> IAttributeService:
        if not self.__dependencies_injected:
            await self.__inject_dependencies()
            self.__dependencies_injected = True
        return self.__attribute_service

    async def __inject_dependencies(self) -> None:
        await self.__project_service.inject_dependencies(
            self.__user_service,
            self.__node_service,
        )
        await self.__node_service.inject_dependencies(
            self.__user_service,
            self.__project_service,
            self.__template_service,
            self.__attribute_service,
        )
        await self.__attribute_service.inject_dependencies()
        await self.__template_service.inject_dependencies(
            self.__node_service,
        )

    def __instantiate_user_service(self) -> None:
        users_registry = self.__registry_factory.get("users")
        self.__user_service = UserService(users_registry)

    def __instantiate_project_service(self) -> None:
        project_registry = self.__registry_factory.get("projects")
        self.__project_service = ProjectService(project_registry)

    def __instantiate_node_service(self) -> None:
        node_registry = self.__registry_factory.get("nodes")
        self.__node_service = NodeService(node_registry)

    def __instantiate_template_service(self) -> None:
        template_registry = self.__registry_factory.get("templates")
        self.__template_service = TemplateService(template_registry)

    def __instantiate_attribute_service(self) -> None:
        attribute_registry = self.__registry_factory.get("attributes")
        type_registry = self.__registry_factory.get("types")
        self.__attribute_service = AttributeService(type_registry, attribute_registry)
