from aiogram.types import WebAppInfo

from config_reader import config


def get_webapp() -> WebAppInfo:
    return WebAppInfo(url=f"{config.APP_BASE_URL}")
