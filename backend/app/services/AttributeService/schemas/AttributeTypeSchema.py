from pydantic import BaseModel

from .types import AttributeTypeId, RegexStr


class AttributeTypeSchema(BaseModel):
    id: AttributeTypeId
    attrs: dict[str, RegexStr]
