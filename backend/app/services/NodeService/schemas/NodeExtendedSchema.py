from ...AttributeService.schemas.types import AttributeTypeId
from .NodeSchema import NodeSchema


class NodeExtendedSchema(NodeSchema):
    type_id: AttributeTypeId
    holder: bool
    attrs: dict[str, str]
