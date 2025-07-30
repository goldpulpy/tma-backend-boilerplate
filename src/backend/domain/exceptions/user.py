"""User exceptions."""


class UserNotFoundError(Exception):
    """User not found exception."""


class UserAlreadyExistsError(Exception):
    """User already exists exception."""


class UserInvalidError(Exception):
    """User invalid exception."""
