from pydantic import BaseModel

from .types import AttributeTypeId, RegexStr


class AttributeTypeSchema(BaseModel):
    id: AttributeTypeId
    holder: bool
    attrs: dict[str, RegexStr]
