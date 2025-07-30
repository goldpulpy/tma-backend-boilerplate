"""Health use case."""

import logging
from abc import ABC, abstractmethod

from backend.application.dtos.health import HealthServiceStatus
from backend.application.services.health.db import IDatabaseHealthCheckService

logger = logging.getLogger(__name__)


class IHealthCheckUseCase(ABC):
    """Health check use case."""

    @abstractmethod
    async def execute(self) -> HealthServiceStatus:
        """Execute the health check."""
        raise NotImplementedError


class HealthCheckUseCase(IHealthCheckUseCase):
    """Health check use case implementation."""

    def __init__(
        self,
        database_health_check_service: IDatabaseHealthCheckService,
    ) -> None:
        self.db_health_check = database_health_check_service

    async def execute(self) -> HealthServiceStatus:
        """Execute the health check."""
        logger.debug("Executing health check...")

        # Health check
        db_conn_ok = await self.db_health_check.check_connection()

        return HealthServiceStatus(db_connection=db_conn_ok)
