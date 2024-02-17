from pydantic import BaseModel


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(UserBaseSchema):
    id: str


class UserUpdateSchema(UserBaseSchema):
    pass


class UserSchema(UserBaseSchema):
    id: str
