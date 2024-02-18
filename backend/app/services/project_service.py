from app.schemas.Project import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from app.registry import IRegistry


class ProjectService:
    __registry: IRegistry

    def __init__(self, registry: IRegistry) -> None:
        self.__registry = registry

    def get_by_user_id(self, user_id: str) -> list[ProjectSchema]:
        projects = self.__registry.read({"user_id": user_id})
        return [ProjectSchema(**project) for project in projects]

    def get_by_id(self, project_id: str) -> ProjectSchema | None:
        """Function to retrieve single project by id"""
        projects = self.__registry.read({"id": project_id})
        if len(projects) == 0:
            return None
        return ProjectSchema(**projects[0])

    def create(self, new_project: ProjectCreateSchema) -> None:
        """Function to create a project and return the project's id."""
        project = ProjectSchema(**new_project.model_dump())
        self.__registry.create(project.model_dump(by_alias=True))

    def update(
        self,
        project_id: str,
        project_update: ProjectUpdateSchema,
    ) -> int:
        """Function to update a single project and return
        the number of projects matched for this update."""
        response = self.__registry.update(
            {"id": project_id},
            project_update.model_dump(exclude_none=True),
        )
        return response.count

    def delete_by_id(self, project_id: str) -> int:
        """Function to delete a single project and
        return the number of projects deleted."""
        response = self.__registry.delete({"id": project_id})
        return response.count
