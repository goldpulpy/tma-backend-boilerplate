"""Ensure user use case."""

from abc import ABC, abstractmethod
from collections.abc import Callable

from backend.application.services.uow import IUnitOfWork
from backend.domain.entities.user import User


class IEnsureUserUseCase(ABC):
    """Ensure user use case interface."""

    @abstractmethod
    async def execute(self, user: User) -> User:
        """Ensure user."""


class EnsureUserUseCase(IEnsureUserUseCase):
    """Ensure user use case."""

    def __init__(
        self,
        uow_factory: Callable[[], IUnitOfWork],
    ) -> None:
        """Initialize EnsureUserUseCase."""
        self._uow_factory = uow_factory

    async def execute(self, user: User) -> User:
        """Ensure user."""
        async with self._uow_factory() as uow:
            await uow.users.save(user)

        return user
