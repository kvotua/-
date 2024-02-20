from .ServiceFactory import ServiceFactory
from app.registry import registry_factory
from .UserService import UserService
from .ProjectService import ProjectService

service_factory = ServiceFactory(registry_factory)

__all__ = ["UserService", "ProjectService", "service_factory"]
