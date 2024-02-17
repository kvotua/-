from typing import Annotated

from fastapi import APIRouter, status, Depends, Header

from app.api_v1.projects.dependences import get_project_by_id
from app.api_v1.projects.schemas import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from app.api_v1.users.dependences import get_user_by_id
from app.api_v1.users.exceptions import UserNotFoundHTTPException
from app.api_v1.users.schemas import UserSchema
from app.core.services import project_service, user_service
from app.auth.user_validate import validate

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
)
def project_get(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
):
    """Get information about the project"""
    validate(user_web_data)
    return project


@router.get(
    "/by/user/id/{user_id}",
    response_model=list[ProjectSchema | None],
    status_code=status.HTTP_200_OK,
)
def project_get_user(
    user: Annotated[UserSchema, Depends(get_user_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
):
    validate(user_web_data)
    """Get user's projects"""
    return project_service.get_by_user_id(user.id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
)
def project_add(
    project_create: ProjectCreateSchema,
    user_web_data: Annotated[str | None, Header()] = None,
):
    """Create a project"""
    validate(user_web_data)
    if not user_service.exist(project_create.user_id):
        raise UserNotFoundHTTPException
    return project_service.create(project_create)


# TODO: сделать через patch
@router.put(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=int,
)
def update_project(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    project_update: ProjectUpdateSchema,
    user_web_data: Annotated[str | None, Header()] = None,
):
    validate(user_web_data)
    """Change the project. Returns 1 if the change has occurred, otherwise returns 0"""
    return project_service.update(
        project_id=project.id,
        project_update=project_update,
    )


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=int,
)
def project_delete(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
):
    validate(user_web_data)
    """Delete a project. Returns 1 if deletion has occurred, otherwise returns 0"""
    return project_service.delete_by_id(project_id=project.id)
