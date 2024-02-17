from typing import Annotated, List

from fastapi import APIRouter, status, Depends, HTTPException

from .dependences import get_user_by_init_data, get_project_by_id
from app.schemas.Project import (
    ProjectSchema,
    ProjectCreateSchema,
    ProjectUpdateSchema,
)
from app.schemas.User import UserSchema
from app.services import project_service, user_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def project_get(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
) -> ProjectSchema:
    """Get information about the project"""
    return project


@router.get(
    "/by/user/id/{user_id}",
    status_code=status.HTTP_200_OK,
)
def project_get_user(
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
) -> List[ProjectSchema]:
    """Get user's projects"""
    return project_service.get_by_user_id(user.id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def project_add(
    project_create: ProjectCreateSchema,
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
) -> None:
    """Create a project"""
    if not user_service.exist(project_create.user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return project_service.create(project_create)


# TODO: сделать через patch
@router.put(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
)
def update_project(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    project_update: ProjectUpdateSchema,
) -> None:
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
) -> None:
    """Delete a project. Returns 1 if deletion has occurred, otherwise returns 0"""
    project_service.delete_by_id(project_id=project.id)
