from typing import Annotated
from app.services.NodeService.schemas import (
    NodeCreateSchema,
    NodeSchema,
    NodeTreeSchema,
    NodeUpdateSchema,
)
from app.services import NodeService
from app.services.exceptions import NodeNotFoundError, UserNotFoundError
from fastapi import APIRouter, Depends, status, HTTPException
from .dependencies import get_user_id_by_init_data, get_node_service
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/nodes", tags=["nodes"])


@router.get(
    "/{node_id}",
    response_model=NodeSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def node_get(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: str,
):
    try:
        return node_service.try_get(initiator_id, node_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )


@router.get(
    "/tree/{node_id}",
    response_model=NodeTreeSchema,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def node_get_tree(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: str,
):
    try:
        return node_service.try_get_tree(initiator_id, node_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=str,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def project_add(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_create: NodeCreateSchema,
):
    try:
        return node_service.create(initiator_id, node_create)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )


@router.patch(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def update_node(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_update: NodeUpdateSchema,
    node_id: str,
):
    try:
        node_service.try_update(initiator_id, node_id, node_update)

    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A user with this ID does not exist"
        )

    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )


@router.delete(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def delete_node(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: str,
):
    try:
        node_service.try_delete(initiator_id, node_id)

    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "The user with this ID was not found",
        )
    except NodeNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "A node with this id does not exist"
        )
