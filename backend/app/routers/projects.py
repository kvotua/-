from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException

from .dependences import get_user_by_init_data, get_project_by_id
from app.schemas.Project import ProjectSchema, ProjectCreateSchema, ProjectUpdateSchema

from app.schemas.User import UserSchema
from app.services import project_service, user_service
from .exceptions import Error

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def project_get(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
):
    return project


@router.get(
    "/by/user/id/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ProjectSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def project_get_user(
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
):
    return project_service.get_by_user_id(user.id)


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    response_model=ProjectCreateSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def project_add(
    project_create: ProjectCreateSchema,
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
):
    if not user_service.exist(project_create.user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return project_service.create(project_create)


# TODO: сделать через patch
@router.put(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def update_project(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
    project_update: ProjectUpdateSchema,
):
    return project_service.update(
        project_id=project.id,
        project_update=project_update,
    )


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    response_model=int,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def project_delete(
    project: Annotated[ProjectSchema, Depends(get_project_by_id)],
):
    return project_service.delete_by_id(project_id=project.id)
