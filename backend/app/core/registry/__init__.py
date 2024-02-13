from app.core.config import settings
from app.core.registry.db_helper import mongo_db_helper
from app.core.registry.mongo.project_mongo_registry import ProjectMongoRegistry
from app.core.registry.mongo.user_mongo_registry import UserMongoRegistry

database = mongo_db_helper.get_database(settings.mongo_db.db_name)

user_mongo_registry = UserMongoRegistry(
    database.get_collection(settings.mongo_db.users_collection_name)
)
project_mongo_registry = ProjectMongoRegistry(
    database.get_collection(settings.mongo_db.projects_collection_name)
)
