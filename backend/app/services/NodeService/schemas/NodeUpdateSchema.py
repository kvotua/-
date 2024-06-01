from typing import Optional

from pydantic import BaseModel

from .NodeId import NodeId


class NodeUpdateSchema(BaseModel):
    parent: Optional[NodeId] = None
    position: int
