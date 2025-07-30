"""Database health check service."""

import asyncio
import logging

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.application.services.health.db import IDatabaseHealthCheckService

logger = logging.getLogger(__name__)


class DatabaseHealthCheckService(IDatabaseHealthCheckService):
    """Database health check service."""

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self.session_factory = session_factory

    async def check_connection(self, timeout: float = 5.0) -> bool:
        """Check database connection."""
        logger.debug("Checking database connection...")
        try:
            async with asyncio.timeout(timeout):
                async with self.session_factory() as session:
                    result = await session.execute(text("SELECT 1"))
                    value = result.scalar()
                    is_ok = value == 1
                    logger.debug("Database health check result: %s", is_ok)
                    return is_ok

        except (SQLAlchemyError, ConnectionError) as e:
            logger.error("Database health check failed: %s", e)
            return False
        except Exception as e:
            logger.error(
                "Unexpected error during database health check: %s",
                e,
            )
            return False
