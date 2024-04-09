from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field

from ...TemplateService.schemas.TemplateId import TemplateId
from .NodeId import NodeId


class NodeCreateSchema(BaseModel):
    parent: NodeId
    template_id: TemplateId


class NodeUpdateSchema(BaseModel):
    parent: Optional[NodeId] = None


class NodeSchema(BaseModel):
    parent: NodeId | None
    id: NodeId = Field(default_factory=lambda: NodeId(str(uuid4())))
    children: list[NodeId] = []


class NodeTreeSchema(BaseModel):
    id: NodeId
    children: list["NodeTreeSchema"]
