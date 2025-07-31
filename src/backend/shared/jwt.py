"""JWT utils."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta

from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidTokenError,
    decode,
    encode,
)

from backend.shared import config

logger = logging.getLogger(__name__)


def create_jwt(sub: str) -> str:
    """Create a JWT token."""
    now = datetime.now().astimezone()
    payload: dict[str, str | int] = {
        "sub": sub,
        "exp": int((now + timedelta(minutes=15)).timestamp()),
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
    }

    try:
        return encode(
            payload,
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )
    except Exception:
        logger.exception("Failed to create JWT token")
        raise


def verify_jwt(token: str) -> dict:
    """Verify a JWT token and return its payload."""
    try:
        return decode(
            token,
            config.jwt.secret,
            algorithms=[config.jwt.algorithm],
        )
    except ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise
    except DecodeError:
        logger.warning("JWT decode error (invalid format)")
        raise
    except InvalidTokenError:
        logger.warning("Invalid JWT token")
        raise
    except Exception:
        logger.exception("Unexpected error during JWT verification")
        raise
