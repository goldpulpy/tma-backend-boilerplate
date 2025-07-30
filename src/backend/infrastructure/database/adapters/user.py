"""User database adapter."""

from backend.domain.entities.user import User
from backend.domain.value_objects.user import (
    FirstName,
    LanguageCode,
    LastName,
    PhotoUrl,
    UserId,
    Username,
)
from backend.infrastructure.database.models.user import UserModel


class UserAdapter:
    """User database adapter."""

    @staticmethod
    def to_entity(user: UserModel) -> User:
        """Convert a user model to an entity."""
        return User(
            id=UserId(user.id),
            username=Username(user.username),
            first_name=FirstName(user.first_name),
            last_name=LastName(user.last_name),
            language_code=LanguageCode(user.language_code),
            photo_url=PhotoUrl(user.photo_url),
        )

    @staticmethod
    def to_model(user: User) -> UserModel:
        """Convert an entity to a model."""
        return UserModel(
            id=user.id.value,
            username=user.username.value,
            first_name=user.first_name.value,
            last_name=user.last_name.value,
            language_code=user.language_code.value,
            photo_url=user.photo_url.value,
        )
