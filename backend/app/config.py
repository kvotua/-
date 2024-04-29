from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    mode: str = "local"
    bot_key: str = ""
    storage: str = "storage"


settings = Setting()
