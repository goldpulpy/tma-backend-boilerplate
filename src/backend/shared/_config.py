"""Config module"""
import time
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Environment enum"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"


class BaseConfig(BaseSettings):
    """Base config class"""
    model_config = SettingsConfigDict(
        extra="ignore",
        frozen=True
    )


class APPConfig(BaseConfig):
    """APP config class"""
    bot_token: str
    allowed_origin: str
    environment: Environment

    @property
    def is_production(self) -> bool:
        """Check if the environment is production"""
        return self.environment == Environment.PRODUCTION

    @property
    def is_development(self) -> bool:
        """Check if the environment is development"""
        return self.environment == Environment.DEVELOPMENT


class JWTConfig(BaseConfig):
    """JWT config class"""
    secret: str
    algorithm: str = "HS256"

    model_config = SettingsConfigDict(
        env_prefix="JWT_",
        extra="ignore",
        frozen=True
    )


class DBConfig(BaseConfig):
    """DB config class"""
    host: str
    port: int
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        extra="ignore",
        frozen=True
    )

    @property
    def url(self) -> str:
        """DB URL"""
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Config(BaseConfig):
    """Application config class"""
    app: APPConfig = APPConfig()
    jwt: JWTConfig = JWTConfig()
    db: DBConfig = DBConfig()


time.tzset()
config = Config()
