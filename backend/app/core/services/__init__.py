from app.core.registry import project_mongo_registry, user_mongo_registry
from app.core.services.project_service import ProjectService
from app.core.services.user_service import UserService

project_service = ProjectService(project_mongo_registry)
user_service = UserService(user_mongo_registry)
