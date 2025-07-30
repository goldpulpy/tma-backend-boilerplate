"""User username value object."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Username:
    """User username value object."""

    value: Optional[str] = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value:
            if not isinstance(self.value, str):
                raise TypeError("Username must be a string")

            if not self.value.strip():
                raise ValueError("Username cannot be empty")

    def __repr__(self) -> str:
        """Return the string representation of the username."""
        return f"Username({self.value})"
