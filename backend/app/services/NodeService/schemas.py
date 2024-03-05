from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class NodeCreateSchema(BaseModel):
    parent: str


class NodeUpdateSchema(BaseModel):
    parent: Optional[str] = None


class NodeSchema(BaseModel):
    parent: str | None
    id: str = Field(default_factory=lambda: str(uuid4()))
    children: list[str] = []


class NodeTreeSchema(BaseModel):
    id: str
    children: list["NodeTreeSchema"]
