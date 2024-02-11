from pydantic import BaseModel


class ProjectNew(BaseModel):
    user_id: int
    name: str
