"""User ID value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    """User ID value object."""

    value: int

    def __post_init__(self) -> None:
        """Post-init validation."""
        if not isinstance(self.value, int):
            msg = "User ID must be an integer"
            raise TypeError(msg)

        if self.value < 0:
            msg = "User ID must be positive"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the string representation of the user ID."""
        return str(self.value)

    def __repr__(self) -> str:
        """Return the string representation of the user ID."""
        return f"UserId({self.value})"
