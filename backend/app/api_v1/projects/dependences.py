from uuid import UUID

from app.api_v1.projects.exceptions import ProjectNotFoundHTTPException
from app.api_v1.projects.schemas import ProjectSchema
from app.core.services import project_service


def get_project_by_id(project_id: UUID) -> ProjectSchema:
    project = project_service.get_by_id(project_id)
    if not project:
        raise ProjectNotFoundHTTPException
    return project
