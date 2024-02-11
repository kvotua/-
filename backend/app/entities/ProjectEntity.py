from pymongo.collection import Collection
from fastapi import HTTPException, status
from app.models import Project
from app.schemas import ProjectNew, ProjectUpdate
from uuid import UUID
from app.config import project_do_not_exist


class ProjectEntity:
    projects_collection: Collection

    def __init__(self, collection: Collection) -> None:
        self.projects_collection = collection

    def get_by_id(self, id: UUID) -> Project:
        project = self.projects_collection.find_one({"_id": id})
        if project is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=project_do_not_exist
            )
        return Project(**project)

    def add(self, project: ProjectNew) -> str:

        project_db = Project(**project.model_dump())

        self.projects_collection.insert_one(project_db.model_dump(by_alias=True))
        return project_db.id

    def edit(self, id: UUID, project_u: ProjectUpdate) -> None:

        result = self.projects_collection.update_one(
            {"_id": id}, {"$set": project_u.model_dump(exclude_none=True)}
        )

        if result.matched_count < 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=project_do_not_exist
            )

    def delete(self, id: UUID) -> None:
        if self.exist(id):
            self.projects_collection.find_one_and_delete({"_id": id})
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=project_do_not_exist
            )

    def exist(self, id: UUID) -> bool:
        return self.projects_collection.find_one({"_id": id}) is not None
