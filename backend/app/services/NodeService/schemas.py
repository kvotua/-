from pydantic import BaseModel, Field
from uuid import uuid4


class NodeCreateSchema(BaseModel):
    parent: str | None = None
    children: list[str] = []


class NodeUpdateSchema(BaseModel):
    parent: str | None
    children: list[str] | None


class NodeSchema(NodeCreateSchema):
    id: str = Field(default_factory=lambda: str(uuid4()))


class NodeTreeSchema(BaseModel):
    id: str
    children: list["NodeTreeSchema"]
