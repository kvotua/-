from typing import NewType, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from ..NodeService.schemas import NodeId
from ..UserService.schemas import UserId

ProjectId = NewType("ProjectId", str)


class ProjectCreateSchema(BaseModel):
    name: str


class ProjectUpdateSchema(BaseModel):
    name: Optional[str]


class ProjectSchema(ProjectCreateSchema):
    id: ProjectId = Field(default_factory=lambda: ProjectId(str(uuid4())))
    core_node_id: NodeId
    owner_id: UserId
