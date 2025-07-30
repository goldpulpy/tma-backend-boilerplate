"""User repository implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from backend.domain.entities.user import User
from backend.domain.repositories.user import IUserRepository

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from backend.domain.value_objects.user import UserId


class UserRepository(IUserRepository):
    """User repository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize the user repository."""
        self.session = session

    async def find_by_id(self, user_id: UserId) -> User | None:
        """Find a user by their ID."""
        return await self.session.get(User, user_id)

    async def save(self, user: User) -> User:
        """Save a user."""
        self.session.add(user)
        await self.session.commit()
        return user

    async def delete(self, user_id: UserId) -> None:
        """Delete a user."""
        await self.session.delete(user_id)
