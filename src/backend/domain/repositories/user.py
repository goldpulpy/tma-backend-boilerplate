"""User repository."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.domain.entities.user import User
    from backend.domain.value_objects.user import UserId


class IUserRepository(ABC):
    """User repository interface."""

    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> User | None:
        """Find a user by their ID."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user."""

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Delete a user."""
