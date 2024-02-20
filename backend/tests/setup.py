from app.registry.MongoMockRegistry import MongoMockRegistryFactory
from app.services.ServiceFactory import ServiceFactory
from fastapi.testclient import TestClient
from app.routers.dependencies import get_project_service, get_user_service
from app.main import app


test_client = TestClient(app)

mock_registry_factory = MongoMockRegistryFactory()
mock_service_factory = ServiceFactory(mock_registry_factory)


app.dependency_overrides[get_project_service] = mock_service_factory.get_project_service
app.dependency_overrides[get_user_service] = mock_service_factory.get_user_service


API_V1 = "/api/v1"

USERS = API_V1 + "/users"
PROJECTS = API_V1 + "/projects"

USER = USERS + "/{user_id}"
PROJECT = PROJECTS + "/{project_id}"
PROJECT_BY_USER = PROJECTS + "/by/user/{user_id}"
