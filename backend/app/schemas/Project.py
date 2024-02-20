from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: Optional[str]


class ProjectSchema(ProjectCreateSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))
    owner_id: str
