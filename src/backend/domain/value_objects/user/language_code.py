"""User language code value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageCode:
    """User language code value object."""

    value: str

    def __post_init__(self) -> None:
        """Validate the user language code."""
        if not isinstance(self.value, str):
            raise TypeError("Language code must be a string")

        if len(self.value) != 2:
            raise ValueError("Language code must be 2 characters long")

        if not self.value.isalpha():
            raise ValueError("Language code must be alphabetic")

    def __str__(self) -> str:
        """Return the string representation of the language code."""
        return self.value

    def __repr__(self) -> str:
        """Return the string representation of the language code."""
        return f"LanguageCode({self.value})"
