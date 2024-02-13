from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class ProjectBaseSchema(BaseModel):
    name: str
    user_id: int


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: UUID = Field(default=uuid4(), alias="_id")
