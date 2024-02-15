from pydantic import BaseModel, Field


class UserBaseSchema(BaseModel):
    pass


class UserCreateSchema(UserBaseSchema):
    id: int = Field(serialization_alias="_id", validation_alias="id")


class UserUpdateSchema(UserBaseSchema):
    pass


class UserSchema(UserBaseSchema):
    id: int = Field(alias="_id")
