"""Configuration .env."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.core.settings.constants import CommonConfSettings, JWTconf


class EnvironmentSetting(BaseSettings):
    """EnvironmentSettingMix uses type mode."""

    model_config = SettingsConfigDict(
        env_file=CommonConfSettings.ENV,
        extra=CommonConfSettings.EXTRA_IGNORE,
    )


class JWTToken(EnvironmentSetting):
    """Class for handling JWT settings."""

    jwt_private: str = Field(default=JWTconf.PRIVATE_KEY)
    jwt_public: str = Field(default=JWTconf.PUBLIC_KEY)
    algorithm: str = JWTconf.ALGORITHM
    access_token_expire_minutes: int = Field(
        default=JWTconf.ACCESS_EXPIRE_MINUTES
    )
    refresh_token_expire_days: int = Field(default=JWTconf.REFRESH_EXPIRE_DAYS)
    referral_token_expire_days: int = Field(
        default=JWTconf.REFRESH_EXPIRE_DAYS
    )


class DataBaseEnvConf(EnvironmentSetting):
    """Configuration for production environments."""

    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    ECHO: bool
    POOL_TIMEOUT: int
    POOL_SIZE_SQL_ALCHEMY_CONF: int
    MAX_OVERFLOW: int
    MODE: str

    @property
    def get_url_database(self) -> str:
        """Return the database URL for SQLAlchemy."""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


class Settings:
    """Common settings for environments."""

    def __init__(self) -> None:
        """Initialize the settings by loading environment variables."""
        self.jwt = JWTToken()
        self.db = DataBaseEnvConf()


settings = Settings()
