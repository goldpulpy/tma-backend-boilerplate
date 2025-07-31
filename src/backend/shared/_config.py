"""Config module."""

from enum import Enum
from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Environment enum."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class BaseConfig(BaseSettings):
    """Base config class."""

    model_config = SettingsConfigDict(extra="ignore", frozen=True)


class APPConfig(BaseConfig):
    """APP config class."""

    host: str = "0.0.0.0"  # noqa: S104
    port: int = Field(default=5000, ge=1, le=65535)
    bot_token: str
    allowed_origins: str
    environment: Environment = Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        """Check if the environment is production."""
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if the environment is development."""
        return self.environment == Environment.DEVELOPMENT

    @property
    def allowed_origins_list(self) -> list[str]:
        """Allowed origins list."""
        return [
            origin.strip()
            for origin in self.allowed_origins.split(",")
            if origin.strip()
        ]


class JWTConfig(BaseConfig):
    """JWT config class."""

    secret: str = Field(min_length=32)
    issuer: str = "backend"
    expiry_days: int = 1
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        extra="ignore",
        frozen=True,
    )


class DBConfig(BaseConfig):
    """DB config class."""

    host: str = "localhost"
    port: int = Field(default=5432, ge=1, le=65535)
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
        frozen=True,
    )

    @property
    def url(self) -> str:
        """DB URL."""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Config:
    """Global application config."""

    app: ClassVar[APPConfig] = APPConfig()  # type: ignore[call-arg]
    jwt: ClassVar[JWTConfig] = JWTConfig()  # type: ignore[call-arg]
    db: ClassVar[DBConfig] = DBConfig()  # type: ignore[call-arg]


config = Config()
