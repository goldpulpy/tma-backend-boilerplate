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


def create_auth_token(sub: str) -> tuple[str, datetime, datetime]:
    """Create a JWT token.

    Returns:
        tuple[str, datetime, datetime]: JWT token, created at, expires at

    """
    try:
        created_at = datetime.now().astimezone()
        expires_at = created_at + timedelta(days=config.jwt.expiry_days)

        jwt_token = encode(
            {
                "sub": sub,
                "exp": int(expires_at.timestamp()),
                "iat": int(created_at.timestamp()),
                "nbf": int(created_at.timestamp()),
                "iss": config.jwt.issuer,
            },
            config.jwt.secret,
            algorithm=config.jwt.algorithm,
        )

    except Exception:
        logger.exception("Failed to create JWT token")
        raise

    else:
        return jwt_token, created_at, expires_at


def verify_auth_token(token: str) -> dict:
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
