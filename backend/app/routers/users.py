from typing import Annotated

from app.schemas.User import UserCreateSchema, UserSchema
from app.services.exceptions import UserExistError, UserNotFoundError, NotAllowedError
from fastapi import APIRouter, Depends, status, HTTPException
from app.services import service_factory, UserService

from .dependencies import get_user_id_by_init_data
from .exceptions import HTTPExceptionSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPExceptionSchema},
        status.HTTP_403_FORBIDDEN: {"model": HTTPExceptionSchema},
        status.HTTP_404_NOT_FOUND: {"model": HTTPExceptionSchema},
    },
)
def user_get(
    initiator_id: Annotated[str, Depends(get_user_id_by_init_data)],
    user_id: str,
    user_service: Annotated[UserService, Depends(service_factory.get_user_service)],
):
    try:
        return user_service.try_get_by_id(initiator_id, user_id)
    except UserNotFoundError:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, "The user with this ID was not found"
        )
    except NotAllowedError:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have permission to receive this user"
        )


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_409_CONFLICT: {"model": HTTPExceptionSchema},
    },
)
def user_add(
    user: UserCreateSchema,
    user_service: Annotated[UserService, Depends(service_factory.get_user_service)],
) -> None:
    try:
        user_service.create(user)
    except UserExistError:
        raise HTTPException(status.HTTP_409_CONFLICT, "User already exist")
