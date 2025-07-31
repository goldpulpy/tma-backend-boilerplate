"""SQLAlchemy implementation of Unit of Work pattern."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from typing_extensions import Self

from backend.application.services.uow import IUnitOfWork
from backend.infrastructure.repositories.user import UserRepository

if TYPE_CHECKING:
    from types import TracebackType

    from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(IUnitOfWork):
    """SQLAlchemy implementation of Unit of Work."""

    def __init__(self, session_factory: Callable[[], AsyncSession]) -> None:
        """Initialize the SQLAlchemy unit of work."""
        self._session_factory = session_factory
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> Self:
        """Enter async context manager."""
        self._session = self._session_factory()

        self.users = UserRepository(self._session)

        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit async context manager."""
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            if self._session:
                await self._session.close()

    async def commit(self) -> None:
        """Commit transaction."""
        if self._session:
            await self._session.commit()

    async def rollback(self) -> None:
        """Rollback transaction."""
        if self._session:
            await self._session.rollback()
