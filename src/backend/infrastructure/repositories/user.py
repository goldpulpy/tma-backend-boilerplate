"""User repository implementation."""

from __future__ import annotations

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

        self._session.add(user_model)
        await self._session.flush()

        await self._session.refresh(user_model)
        return UserAdapter.to_entity(user_model)

    async def delete(self, user_id: UserId) -> None:
        """Delete a user."""
        stmt = delete(UserModel).where(UserModel.id == user_id.value)
        result = await self._session.execute(stmt)

        if result.rowcount == 0:
            raise UserNotFoundError(user_id)

        await self._session.flush()
