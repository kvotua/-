from pydantic import BaseModel, Field


class UserNew(BaseModel):
    id: int = Field(alias="_id")
