import hashlib
import hmac
from urllib.parse import unquote
from app.config import settings


"""tmp value while there is no way to get telegram bot key from, well, telegram bot"""
secret_key = hmac.new(
    "WebAppData".encode("utf-8"), settings.bot_key.encode("utf-8"), hashlib.sha256
).digest()


def hash_validate(user_init_data: str) -> bool:
    """Through multitude of inconcivable actions
    compares hash that was send by telegram
    with hashed user data"""
    chunks = unquote(user_init_data).split("&")
    chunk_dict = dict()
    for chunk in chunks:
        pair = chunk.split("=")
        if len(pair) != 2:
            return False
        chunk_dict[pair[0]] = pair[1]
    hash = chunk_dict.pop("hash", None)
    if hash is None:
        return False
    pairs = [f"{key}={value}" for key, value in chunk_dict.items()]
    pairs.sort()
    data_paired = "\n".join(pairs)

    self_hashed = hmac.new(
        secret_key, data_paired.encode("utf-8"), hashlib.sha256
    ).hexdigest()

    return hash == self_hashed
