"""User language code value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageCode:
    """User language code value object."""

    value: str

    def __post_init__(self) -> None:
        """Validate the user language code."""
        if not isinstance(self.value, str):
            msg = "Language code must be a string"
            raise TypeError(msg)

        if len(self.value) != 2:
            msg = "Language code must be 2 characters long"
            raise ValueError(msg)

        if not self.value.isalpha():
            msg = "Language code must be alphabetic"
            raise ValueError(msg)

    def __str__(self) -> str:
        """Return the string representation of the language code."""
        return self.value

    def __repr__(self) -> str:
        """Return the string representation of the language code."""
        return f"LanguageCode({self.value})"
