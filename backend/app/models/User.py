from pydantic import BaseModel, Field


class User(BaseModel):
    id: int = Field(alias="_id")
