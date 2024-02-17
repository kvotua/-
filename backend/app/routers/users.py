from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from .dependences import get_user_by_init_data
from app.schemas.User import UserSchema, UserCreateSchema
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
)
def user_get(
    user: Annotated[UserSchema, Depends(get_user_by_init_data)],
) -> UserSchema:
    return user


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def user_add(user: UserCreateSchema) -> None:
    if user_service.exist(user.id):
        raise HTTPException(status.HTTP_409_CONFLICT)
    user_service.create(user)
