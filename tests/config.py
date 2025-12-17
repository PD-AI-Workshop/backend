from pydantic_settings import BaseSettings, SettingsConfigDict


class APITestSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./tests/.env", env_file_encoding="utf-8")

    API_BASE_URL: str
    TIMEOUT: int


settings = APITestSettings()
