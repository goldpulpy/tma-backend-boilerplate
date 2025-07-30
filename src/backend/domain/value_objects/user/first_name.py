"""User first name value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class FirstName:
    """User first name value object."""

    value: str

    def __post_init__(self) -> None:
        """Validate the user first name."""
        if not isinstance(self.value, str):
            raise TypeError("First name must be a string")

        if not self.value.strip():
            raise ValueError("First name cannot be empty")

    def __str__(self) -> str:
        """Return the string representation of the user first name."""
        return self.value

    def __repr__(self) -> str:
        """Return the string representation of the user first name."""
        return f"FirstName({self.value})"
