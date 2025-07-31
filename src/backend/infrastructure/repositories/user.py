"""User repository implementation."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sqlalchemy import delete

from backend.domain.exceptions.user import UserNotFoundError
from backend.domain.repositories.user import IUserRepository
from backend.infrastructure.database.adapters.user import UserAdapter
from backend.infrastructure.database.models.user import UserModel

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from backend.domain.entities.user import User
    from backend.domain.value_objects.user import UserId

logger = logging.getLogger(__name__)


class UserRepository(IUserRepository):
    """User repository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository."""
        self._session = session

    async def find_by_id(self, user_id: UserId) -> User | None:
        """Find a user by their ID."""
        user_model = await self._session.get(UserModel, user_id.value)
        return UserAdapter.to_entity(user_model) if user_model else None

    async def save(self, user: User) -> User:
        """Save a user."""
        user_model = UserAdapter.to_model(user)

        existing_user = await self.find_by_id(user.id)

        if existing_user:
            persistent_model = await self._session.merge(user_model)
            logger.debug("User ID=%s already exists, updating", user.id)
        else:
            self._session.add(user_model)
            persistent_model = user_model
            logger.debug("User ID=%s not found, creating", user.id)

        await self._session.flush()
        await self._session.refresh(persistent_model)

        return UserAdapter.to_entity(persistent_model)

    async def delete(self, user_id: UserId) -> None:
        """Delete a user."""
        stmt = delete(UserModel).where(UserModel.id == user_id.value)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise UserNotFoundError(user_id)

        logger.debug("User ID=%s deleted", user_id)

        await self._session.flush()
