from app.auth.exceptions import UserValidationErrorHTTPException
from app.auth.functions.user import hash_validate
from app.core.config import settings


def validate(user_init_data: str | None) -> None:
    """either returns true or raises UserValidationError"""
    if settings.mode == "local":
        return
    if user_init_data is None:
        raise UserValidationErrorHTTPException
    if not hash_validate(user_init_data):
        raise UserValidationErrorHTTPException
