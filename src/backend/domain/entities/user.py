"""User entity."""

from dataclasses import dataclass

from backend.domain.value_objects.user import (
    FirstName,
    LanguageCode,
    LastName,
    PhotoUrl,
    UserId,
    Username,
)


@dataclass(frozen=True)
class User:
    """User entity."""

    id: UserId
    username: Username
    first_name: FirstName
    last_name: LastName
    language_code: LanguageCode
    photo_url: PhotoUrl
