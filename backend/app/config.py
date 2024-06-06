from pydantic_settings import BaseSettings


class Setting(BaseSettings):
    mode: str = "local"
    bot_key: str = ""


settings = Setting()
