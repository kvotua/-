from typing import NewType

from pydantic import BaseModel

UserId = NewType("UserId", str)


class UserCreateSchema(BaseModel):
    id: UserId


class UserSchema(UserCreateSchema):
    pass
