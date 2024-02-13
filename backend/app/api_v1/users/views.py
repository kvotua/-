from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api_v1.users.dependences import get_user_by_id
from app.api_v1.users.exceptions import UserAlreadyExistHTTPException
from app.api_v1.users.schemas import UserSchema, UserCreateSchema
from app.core.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    path="/{user_id}",
    response_model=UserSchema,
    status_code=status.HTTP_200_OK,
)
def user_get(user: Annotated[UserSchema, Depends(get_user_by_id)]):
    return user


@router.post(
    path="/",
    response_model=str,
    status_code=status.HTTP_201_CREATED,
)
def user_add(user: UserCreateSchema):
    if user_service.exist(user.id):
        raise UserAlreadyExistHTTPException
    return user_service.create(user)
