from app.main import app
from app.registry.MongoMockRegistry import MongoMockRegistryFactory
from app.routers.dependencies import get_project_service, get_user_service
from app.services.ServiceMediator import ServiceMediator

from .api import ClientApi

client = ClientApi(app)

mock_registry_factory = MongoMockRegistryFactory()
mock_service_factory = ServiceMediator(mock_registry_factory)


app.dependency_overrides[get_project_service] = mock_service_factory.get_project_service
app.dependency_overrides[get_user_service] = mock_service_factory.get_user_service
