from typing import Annotated

from app.schemas.Project import ProjectCreateSchema, ProjectSchema, ProjectUpdateSchema

from app.services.exceptions import (
    UserNotFoundError,
    ProjectNotFoundError,
    NotAllowedError,
)
from fastapi import APIRouter, Depends, status, HTTPException

from .dependencies import get_user_id_by_init_data, get_project_service
from .exceptions import HTTPExceptionSchema
from app.services import ProjectService

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/{project_id}",
    response_model=ProjectSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def project_get(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.try_get(initiator_id, project_id)
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have permission to view this project"
        )


@router.get(
    "/by/user/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=list[ProjectSchema],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def project_get_user(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    user_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.try_get_by_user_id(initiator_id, user_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to view this user's projects",
        )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def project_add(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    project_create: ProjectCreateSchema,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        return project_service.create(initiator_id, project_create)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The user with this ID was not found"
        )


@router.patch(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def update_project(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    project_update: ProjectUpdateSchema,
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        project_service.try_update(initiator_id, project_id, project_update)
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to update this project",
        )
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "The user with this ID was not found",
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )


@router.delete(
    path="/{project_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def project_delete(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    project_id: str,
    project_service: Annotated[ProjectService, Depends(get_project_service)],
):
    try:
        project_service.try_delete(initiator_id, project_id)
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "You do not have permission to delete this project",
        )
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "The user with this ID was not found",
        )
    except ProjectNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A project with this ID does not exist"
        )
