from uuid import UUID

from .exceptions import ProjectNotFoundHTTPException
from .schemas import ProjectSchema
from app.services import project_service


def get_project_by_id(project_id: UUID) -> ProjectSchema:
    project = project_service.get_by_id(project_id)
    if not project:
        raise ProjectNotFoundHTTPException
    return project
