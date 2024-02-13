from app.api_v1.users.exceptions import UserNotFoundHTTPException
from app.api_v1.users.schemas import UserSchema
from app.core.services import user_service


def get_user_by_id(user_id: int) -> UserSchema:
    user = user_service.get_by_id(user_id)
    if not user:
        raise UserNotFoundHTTPException
    return user
