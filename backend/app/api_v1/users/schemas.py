from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(UserBaseSchema):
    id: int


class UserUpdateSchema(UserBaseSchema):
    pass


class UserSchema(UserBaseSchema):
    id: int = Field(alias="_id")
