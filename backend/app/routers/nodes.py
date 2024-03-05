from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.services import NodeService
from app.services.exceptions import (
    NodeCannotBeDeletedError,
    NodeNotFoundError,
    NotAllowedError,
    UserNotFoundError,
)
from app.services.NodeService.schemas import (
    NodeCreateSchema,
    NodeSchema,
    NodeTreeSchema,
    NodeUpdateSchema,
)

from .dependencies import get_node_service, get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/nodes", tags=["Nodes"])


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
) -> NodeSchema:
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
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant see this node")


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
) -> NodeTreeSchema:
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
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant get this tree")


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
def node_add(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_create: NodeCreateSchema,
) -> str:
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
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant create this node")


@router.patch(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    response_model=str,
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
) -> None:
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
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant update this node")


@router.delete(
    path="/{node_id}",
    status_code=status.HTTP_200_OK,
    response_model=str,
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPExceptionSchema},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def delete_node(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    node_service: Annotated[NodeService, Depends(get_node_service)],
    node_id: str,
) -> None:
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
    except NotAllowedError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "You cant delete this node")
    except NodeCannotBeDeletedError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Can't delete root node")
