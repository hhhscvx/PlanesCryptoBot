from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    API_ID: int
    API_HASH: str

    RELOGIN_DELAY: list[int] = [5, 7]

    USE_PROXY_FROM_FILE: bool = False

    WORKDIR: str = "sessions/"


settings = Settings()
