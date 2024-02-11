from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Project(BaseModel):
    id: UUID = Field(default=uuid4(), alias="_id")
    user_id: int
    name: str
