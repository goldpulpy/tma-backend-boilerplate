"""User photo URL value object."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class PhotoUrl:
    """User photo URL value object."""

    value: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value is None:
            return

        if not isinstance(self.value, str):
            msg = "Photo URL must be a string"
            raise TypeError(msg)

        parsed = urlparse(self.value)
        if parsed.scheme != "https" or not parsed.netloc:
            msg = "Photo URL must be a valid HTTPS URL"
            raise ValueError(msg)

        if not self.value.startswith("https://t.me/i/userpic/"):
            msg = "Photo URL must be a valid Telegram userpic URL"
            raise ValueError(
                msg,
            )

    def __str__(self) -> str:
        """Return the string representation of the photo URL."""
        return self.value or ""

    def __repr__(self) -> str:
        """Return the string representation of the photo URL."""
        return f"PhotoUrl({self.value})"
