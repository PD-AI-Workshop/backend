from pydantic_settings import BaseSettings, SettingsConfigDict

from tests.core.enums.user_role import UserRole


class AdminSettings(BaseSettings):
    ID: int
    EMAIL: str
    IS_ACTIVE: bool
    IS_SUPERUSER: bool
    IS_VERIFIED: bool
    USERNAME: str
    PASSWORD: str
    ROLE: UserRole


class APITestSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="./tests/.env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_nested_delimiter='.'
    )

    API_BASE_URL: str
    TIMEOUT: int
    TEST_ENTITIES_COUNT: int

    ADMIN: AdminSettings


settings = APITestSettings()
