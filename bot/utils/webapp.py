from aiogram.types import WebAppInfo

from config_reader import config


def get_webapp() -> WebAppInfo:
    protocol = "https" if config.MODE != "local" else "http"
    return WebAppInfo(url=f"{protocol}://{config.SERVER_NAME}")
