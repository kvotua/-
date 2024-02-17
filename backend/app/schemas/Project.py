from pydantic import BaseModel, Field
from uuid import uuid4


class ProjectBaseSchema(BaseModel):
    name: str
    user_id: str


class ProjectCreateSchema(ProjectBaseSchema):
    pass


class ProjectUpdateSchema(ProjectBaseSchema):
    pass


class ProjectSchema(ProjectBaseSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
