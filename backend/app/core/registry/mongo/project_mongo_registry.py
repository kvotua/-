from app.core.registry.mongo.mongo_registry import MongoRegistry


class ProjectMongoRegistry(MongoRegistry):
    def get_by_user_id(self, user_id: int) -> list | None:
        project = self.get("user_id", user_id)
        return list(project) if project else None
