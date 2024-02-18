from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from .dependences import get_user_by_init_data
from app.schemas.User import UserSchema, UserCreateSchema
from app.services import user_service
from .exceptions import Error

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_404_NOT_FOUND: {"model": Error},
    },
)
def user_get(
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
):
    return user


@router.post(
    path="/",
    response_model=UserCreateSchema,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": Error},
        status.HTTP_409_CONFLICT: {"model": Error},
    },
)
def user_add(user: UserCreateSchema) -> None:
    if user_service.exist(user.id):
        return JSONResponse(
            content=Error(message="User ID already exist").model_dump(),
            status_code=status.HTTP_409_CONFLICT,
            media_type="application/json",
        )
    user_service.create(user)
