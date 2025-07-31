"""Database container."""

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.shared import config


class DatabaseContainer(containers.DeclarativeContainer):
    """Database container."""

    engine: providers.Singleton[AsyncEngine] = providers.Singleton(
        create_async_engine,
        config.db.url,
        future=True,
        pool_size=20,
        max_overflow=30,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    session_factory: providers.Singleton[async_sessionmaker[AsyncSession]] = (
        providers.Singleton(
            async_sessionmaker,
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    )
