"""User username value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Username:
    """User username value object."""

    value: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value:
            if not isinstance(self.value, str):
                msg = "Username must be a string"
                raise TypeError(msg)

            if not self.value.strip():
                msg = "Username cannot be empty"
                raise ValueError(msg)

    def __repr__(self) -> str:
        """Return the string representation of the username."""
        return f"Username({self.value})"
