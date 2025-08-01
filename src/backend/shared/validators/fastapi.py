"""FastAPI validators."""

from fastapi import Request


class UserIdNotFoundInStateError(Exception):
    """User id not found error."""


def get_user_id_from_state(request: Request) -> int:
    """Get user id from request.

    Returns:
        int: User id

    Raises:
        UserIdNotFoundInStateError: If user id is not found in request state

    """
    user_id = request.state.user_id
    if not user_id:
        msg = "User id not found"
        raise UserIdNotFoundInStateError(msg)

    return user_id
