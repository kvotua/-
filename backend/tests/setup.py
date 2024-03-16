from mongomock import MongoClient

from app.main import app
from app.registry.MongoRegistry import MongoRegistryFactory
from app.routers.dependencies import (
    get_node_service,
    get_project_service,
    get_user_service,
)
from app.services.ServiceMediator import ServiceMediator

from .api import ClientApi

client = ClientApi(app)

mock_registry_factory = MongoRegistryFactory(MongoClient())
mock_service_factory = ServiceMediator(mock_registry_factory)


app.dependency_overrides[get_project_service] = mock_service_factory.get_project_service
app.dependency_overrides[get_user_service] = mock_service_factory.get_user_service
app.dependency_overrides[get_node_service] = mock_service_factory.get_node_service
