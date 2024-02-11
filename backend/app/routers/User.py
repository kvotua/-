from fastapi import APIRouter
from app.entities import users
from app.schemas import UserNew
from app.models import User

router = APIRouter(prefix="/users")


@router.get("/{id}/", response_model=User)
def user_get(id: int):
    return users.get_by_id(id)


@router.post("/add/")
def user_add(user: UserNew):
    return users.add(user)
