from pydantic import BaseModel

from ...AttributeService.schemas.types import AttributeTypeId
from .NodeId import NodeId


class NodeTreeSchema(BaseModel):
    id: NodeId
    type_id: AttributeTypeId
    holder: bool
    attrs: dict[str, str]
    children: list["NodeTreeSchema"]
