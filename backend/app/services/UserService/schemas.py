from pydantic import BaseModel


class UserCreateSchema(BaseModel):
    id: str


class UserSchema(UserCreateSchema):
    pass
