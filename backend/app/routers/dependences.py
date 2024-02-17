import hashlib
import hmac
import json
from typing import Annotated
from urllib.parse import unquote
from uuid import UUID

from app.config import settings
from app.schemas.Project import ProjectSchema
from app.schemas.User import UserSchema
from app.services import project_service, user_service
from fastapi import Depends, Header, HTTPException, status

secret_key = hmac.new(
    "WebAppData".encode("utf-8"), settings.bot_key.encode("utf-8"), hashlib.sha256
).digest()


def get_user_by_init_data(user_init_data: Annotated[str, Header()]) -> None:
    user_id = 0
    if settings.mode != "local":
        init_data_dict = parse_to_dict(user_init_data)
        verify(init_data_dict)
        user_id = json.loads(init_data_dict["user"])["id"]
    return user_service.get_by_id(str(user_id))


def get_project_by_id(
    project_id: UUID, user: Annotated[UserSchema, Depends(get_user_by_init_data)]
) -> ProjectSchema:
    project = project_service.get_by_id(project_id)
    if not project:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return project


def parse_to_dict(init_data: str) -> dict[str, str]:
    chunks = unquote(init_data).split("&")
    chunk_dict = dict()
    for chunk in chunks:
        splitted = chunk.split("=")
        if len(splitted) != 2:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED)
        chunk_dict[splitted[0]] = splitted[1]
    return chunk_dict


def verify(init_data_dict: dict[str, str]) -> None:
    hash = init_data_dict.get("hash", None)
    if hash is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
    pairs = [f"{key}={value}" for key, value in init_data_dict.items() if key != "hash"]
    pairs.sort()
    data_paired = "\n".join(pairs)
    self_hashed = hmac.new(
        secret_key, data_paired.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    if hash != self_hashed:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)
