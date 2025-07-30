"""Database health check service."""

from abc import ABC, abstractmethod


class IDatabaseHealthCheckService(ABC):
    """Database health check service."""

    @abstractmethod
    async def check_connection(self) -> bool:
        """Check the database connection."""
        raise NotImplementedError
