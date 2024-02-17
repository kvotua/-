from typing import Annotated

from fastapi import APIRouter, Depends, status, Header

from .dependences import get_user_by_id
from .exceptions import UserAlreadyExistHTTPException
from .schemas import UserSchema, UserCreateSchema
from app.services import user_service
from app.auth.user_validate import validate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    status_code=status.HTTP_200_OK,
)
def user_get(
    user: Annotated[UserSchema, Depends(get_user_by_id)],
    user_web_data: Annotated[str | None, Header()] = None,
) -> UserSchema:
    validate(user_web_data)
    return user


@router.post(
    path="/",
    status_code=status.HTTP_201_CREATED,
)
def user_add(user: UserCreateSchema) -> None:
    if user_service.exist(user.id):
        raise UserAlreadyExistHTTPException
    user_service.create(user)
