"""Get user use case."""

import logging
from abc import ABC, abstractmethod
from typing import Callable

from backend.application.services.uow import IUnitOfWork
from backend.domain.entities.user import User
from backend.domain.exceptions.user import UserNotFoundError
from backend.domain.value_objects.user import UserId

logger = logging.getLogger(__name__)


class IGetUserUseCase(ABC):
    """Get user use case."""

    @abstractmethod
    async def execute(self, user_id: UserId) -> User:
        """Get user."""


class GetUserUseCase(IGetUserUseCase):
    """Get user use case."""

    def __init__(self, uow_factory: Callable[[], IUnitOfWork]) -> None:
        """Initialize get user use case."""
        self.uow_factory = uow_factory

    async def execute(self, user_id: UserId) -> User:
        """Get user.

        Args:
            user_id: User id

        Returns:
            User: User entity

        Raises:
            UserNotFoundError: If user not found

        """
        async with self.uow_factory() as uow:
            logger.debug("Getting user with id %s", user_id)

            user = await uow.users.find_by_id(user_id)
            if not user:
                msg = f"User with id {user_id.value} not found"
                logger.error(msg)
                raise UserNotFoundError(msg)

            return user
