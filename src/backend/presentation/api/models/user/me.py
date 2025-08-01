"""User me API models."""

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from backend.domain.entities.user import User


class UserMeResponse(BaseModel):
    """User me response."""

    id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    language_code: str | None = None

    @classmethod
    def from_entity(cls, user: User) -> UserMeResponse:
        """Create a UserMeResponse from a User entity."""
        return cls(
            id=user.id.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            username=user.username.value,
            photo_url=user.photo_url.value,
            language_code=user.language_code.value,
        )
