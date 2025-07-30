"""Unit of Work pattern implementation for transaction management."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from types import TracebackType

    from backend.domain.repositories.user import IUserRepository


class IUnitOfWork(ABC):
    """Unit of Work interface."""

    users: IUserRepository

    @abstractmethod
    async def __aenter__(self) -> IUnitOfWork:
        """Enter async context manager."""

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""

    @abstractmethod
    async def commit(self) -> None:
        """Commit transaction."""

    @abstractmethod
    async def rollback(self) -> None:
        """Rollback transaction."""
