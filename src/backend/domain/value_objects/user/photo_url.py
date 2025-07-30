"""User photo URL value object."""

from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse


@dataclass(frozen=True)
class PhotoUrl:
    """User photo URL value object."""

    value: Optional[str] = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value:
            if not isinstance(self.value, str):
                raise TypeError("Photo URL must be a string")

            parsed = urlparse(self.value)
            if parsed.scheme != "https" or not parsed.netloc:
                raise ValueError("Photo URL must be a valid HTTPS URL")

            if not self.value.startswith("https://t.me/i/userpic/"):
                raise ValueError(
                    "Photo URL must be a valid Telegram userpic URL",
                )

    def __str__(self) -> str:
        """Return the string representation of the photo URL."""
        return self.value or ""

    def __repr__(self) -> str:
        """Return the string representation of the photo URL."""
        return f"PhotoUrl({self.value})"
