"""User last name value object."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class LastName:
    """User last name value object."""

    value: Optional[str] = None

    def __post_init__(self) -> None:
        """Post init."""
        if self.value:
            if not isinstance(self.value, str):
                raise TypeError("Last name must be a string")

            if not self.value.strip():
                raise ValueError("Last name cannot be empty")

    def __str__(self) -> str:
        """Return the string representation of the last name."""
        return self.value or ""

    def __repr__(self) -> str:
        """Return the string representation of the last name."""
        return f"LastName({self.value})"
