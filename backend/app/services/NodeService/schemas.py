from typing import NewType, Optional
from uuid import uuid4

from pydantic import BaseModel, Field

NodeId = NewType("NodeId", str)


class NodeCreateSchema(BaseModel):
    parent: NodeId


class NodeUpdateSchema(BaseModel):
    parent: Optional[NodeId] = None


class NodeSchema(BaseModel):
    parent: NodeId | None
    id: NodeId = Field(default_factory=lambda: NodeId(str(uuid4())))
    children: list[NodeId] = []


class NodeTreeSchema(BaseModel):
    id: NodeId
    children: list["NodeTreeSchema"]
