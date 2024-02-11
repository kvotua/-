from pydantic import BaseModel, Field


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None)
