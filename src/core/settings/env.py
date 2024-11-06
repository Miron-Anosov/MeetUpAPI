"""Configuration .env."""

from datetime import timedelta

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


class RedisEnv(EnvironmentSetting):
    """Class give common environments params for Redis."""

    REDIS_HOST: str
    REDIS_DB_BROKER: int
    REDIS_DB_BACKEND: int
    REDIS_PORT: int
    REDIS_PASSWORD: str
    REDIS_USER: str
    REDIS_LIMIT_REQUESTS: int
    REDIS_EXP_REQUESTS_DAYS: int
    REDIS_EXP_LOCATION: int

    @property
    def exp_in_days(self) -> int:
        """Set the expiration time."""
        return int(
            timedelta(days=self.REDIS_EXP_REQUESTS_DAYS).total_seconds()
        )

    @property
    def redis_url_broker(self):
        """Generate and return the Redis URL."""
        return (
            f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@"
            f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_BROKER}"
        )

    @property
    def redis_url_backend(self):
        """Generate and return the Redis URL."""
        return (
            f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@"
            f"{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB_BACKEND}"
        )


class S3Env(EnvironmentSetting):
    """S3 environment."""

    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET: str
    ENDPOINT_URL: str
    DOMAIN_URL: str


class WatterMark(EnvironmentSetting):
    """Class for handling water mark."""

    POSTFIX: str = Field(default="_watermarked.jpg")
    RGB: str = Field(default="RGB")
    JPEG: str = Field(default="JPEG")
    RGBA: str = Field(default="RGBA")
    WATERMARK_TEXT: str = Field(default="Watermark")
    FONT_SIZE: int = Field(default=60)
    OPACITY: int = Field(default=128)


class EmailEnv(EnvironmentSetting):
    """Email env configuration."""

    SMTP_USER: str
    SMTP_HOST: str
    SMTP_PASSWORD: str
    SMTP_PORT: int


class GunicornENV(EnvironmentSetting):
    """Conf Gunicorn."""

    WORKERS: int
    BUILD: str
    LOG_LEVEL: str
    WSGI_APP: str
    WORKER_CLASS: str
    TIMEOUT: int
    ACCESSLOG: str
    ERRORLOG: str


class Settings:
    """Common settings for environments."""

    def __init__(self) -> None:
        """Initialize the settings by loading environment variables."""
        self.jwt = JWTToken()
        self.db = DataBaseEnvConf()
        self.redis = RedisEnv()
        self.s3 = S3Env()
        self.wm = WatterMark()
        self.email = EmailEnv()
        self.gunicorn = GunicornENV()


settings = Settings()
