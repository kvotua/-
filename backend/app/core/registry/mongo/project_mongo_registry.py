from app.api_v1.projects.schemas import ProjectSchema
from app.core.registry.mongo.mongo_registry import MongoRegistry


class ProjectMongoRegistry(MongoRegistry):
    def get_by_user_id(self, user_id: int) -> ProjectSchema | None:
        project = self.get({"user_id": user_id})
        return ProjectSchema(**project) if project else None
