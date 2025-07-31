"""User last name value object."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LastName:
    """User last name value object."""

    value: str | None = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value is None:
            return

        if not isinstance(self.value, str):
            msg = "Last name must be a string"
            raise TypeError(msg)

        if not self.value.strip():
            msg = "Last name cannot be empty"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the string representation of the last name."""
        return self.value or ""

    def __repr__(self) -> str:
        """Return the string representation of the last name."""
        return f"LastName({self.value})"
