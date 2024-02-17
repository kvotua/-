from typing import Annotated, List

from fastapi import APIRouter, status, Depends, Header

from .dependences import get_project_by_id
from .schemas import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from ..users.dependences import get_user_by_id
from ..users.exceptions import UserNotFoundHTTPException
from ..users.schemas import UserSchema
from app.services import project_service, user_service
from app.auth.user_validate import validate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def project_get(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
) -> ProjectSchema:
    """Get information about the project"""
    validate(user_web_data)
    return project


@router.get(
    "/by/user/id/{user_id}",
    status_code=status.HTTP_200_OK,
)
def project_get_user(
    user: Annotated[UserSchema, Depends(get_user_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
) -> List[ProjectSchema]:
    validate(user_web_data)
    """Get user's projects"""
    return project_service.get_by_user_id(user.id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def project_add(
    project_create: ProjectCreateSchema,
    user_web_data: Annotated[str | None, Header()] = None,
) -> None:
    """Create a project"""
    validate(user_web_data)
    if not user_service.exist(project_create.user_id):
        raise UserNotFoundHTTPException
    return project_service.create(project_create)


# TODO: сделать через patch
@router.put(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
)
def update_project(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    project_update: ProjectUpdateSchema,
    user_web_data: Annotated[str | None, Header()] = None,
) -> None:
    validate(user_web_data)
    """Change the project. Returns 1 if the change has occurred, otherwise returns 0"""
    project_service.update(
        project_id=project.id,
        project_update=project_update,
    )


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
)
def project_delete(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
) -> None:
    validate(user_web_data)
    """Delete a project. Returns 1 if deletion has occurred, otherwise returns 0"""
    project_service.delete_by_id(project_id=project.id)
