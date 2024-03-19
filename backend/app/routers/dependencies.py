import hashlib
import hmac
import json
from json import JSONDecodeError
from typing import Annotated
from urllib.parse import unquote

from fastapi import Header, HTTPException, status

from app.config import settings
from app.services import service_mediator
from app.services.NodeService import INodeService
from app.services.ProjectService import IProjectService
from app.services.UserService import IUserService
from app.services.UserService.schemas import UserId

secret_key = hmac.new(
    "WebAppData".encode("utf-8"), settings.bot_key.encode("utf-8"), hashlib.sha256
).digest()


def get_user_service() -> IUserService:
    return service_mediator.get_user_service()


def get_project_service() -> IProjectService:
    return service_mediator.get_project_service()


def get_node_service() -> INodeService:
    return service_mediator.get_node_service()


def get_user_id_by_init_data(user_init_data: Annotated[str, Header()]) -> UserId:
    init_data_dict = parse_to_dict(user_init_data)
    if settings.mode != "local" and not verify(init_data_dict):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token")
    try:
        user_id = json.loads(init_data_dict["user"])["id"]
    except JSONDecodeError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
        )
    return UserId(user_id)


def parse_to_dict(init_data: str) -> dict[str, str]:
    chunks = unquote(init_data).split("&")
    chunk_dict = dict()
    for chunk in chunks:
        splitted = chunk.split("=")
        if len(splitted) != 2:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
            )
        chunk_dict[splitted[0]] = splitted[1]
    return chunk_dict


def verify(init_data_dict: dict[str, str]) -> bool:
    hash = init_data_dict.get("hash", None)
    if hash is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid Telegram token format"
        )
    pairs = [f"{key}={value}" for key, value in init_data_dict.items() if key != "hash"]
    pairs.sort()
    data_paired = "\n".join(pairs)
    self_hashed = hmac.new(
        secret_key, data_paired.encode("utf-8"), hashlib.sha256
    ).hexdigest()
    return hash == self_hashed
