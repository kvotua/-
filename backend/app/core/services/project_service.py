from uuid import UUID

from app.api_v1.projects.schemas import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from app.core.services.base_service import ServiceBase


class ProjectService(ServiceBase):
    def get_by_user_id(self, user_id: int) -> list[ProjectSchema | None]:
        projects = self.registry.get_by_user_id(user_id)
        return [ProjectSchema(**project) for project in projects] if projects else []

    def get_by_id(self, project_id: UUID) -> ProjectSchema | None:
        """Function to retrieve single project by id"""
        project = self.registry.get_by_id(project_id)
        return ProjectSchema(**project) if project else None

    def create(self, new_project: ProjectCreateSchema) -> str:
        """Function to create a project and return the project's id."""
        project = ProjectSchema(**new_project.model_dump())
        return self.registry.create(project.model_dump(by_alias=True))

    def update(
        self,
        project_id: UUID,
        project_update: ProjectUpdateSchema,
    ) -> int:
        """Function to update a single project and return
        the number of projects matched for this update."""
        return self.registry.update(
            project_id,
            project_update.model_dump(exclude_none=True),
        )

    def delete_by_id(self, project_id: UUID) -> int:
        """Function to delete a single project and
        return the number of projects deleted."""
        return self.registry.delete(project_id)
