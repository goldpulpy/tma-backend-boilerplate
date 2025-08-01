"""Authentication middleware."""

import logging
from collections.abc import Awaitable
from typing import Callable, ClassVar

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.shared import jwt

logger = logging.getLogger(__name__)


class AuthenticationMiddleware(BaseHTTPMiddleware):
    """Authentication middleware."""

    # public paths (no authentication)
    AUTH_EXCLUDE_PATHS: ClassVar[set[str]] = {
        "/api/v1/auth/telegram",
        "/health",
        "/docs",
        "/openapi.json",
    }

    def __init__(self, app: ASGIApp) -> None:
        """Initialize authentication middleware."""
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        """Dispatch request."""
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path

        if any(path.startswith(p) for p in self.AUTH_EXCLUDE_PATHS):
            return await call_next(request)

        token = request.cookies.get("token")
        if not token:
            logger.warning("Missing token cookie for path: %s", path)
            return self._unauthorized()

        try:
            data = jwt.verify_auth_token(token)

            user_id = data.get("sub")
            if not user_id or not isinstance(user_id, str):
                logger.warning(
                    "Invalid or missing user_id in token for path: %s",
                    path,
                )
                return self._unauthorized()

            request.state.user_id = int(user_id)

            logger.debug("User authenticated for path: %s", path)

        except (
            jwt.ExpiredSignatureError,
            jwt.DecodeError,
            jwt.InvalidTokenError,
            Exception,
        ):
            logger.exception(
                "Unexpected error verifying token for path %s",
                path,
            )
            return self._unauthorized()

        return await call_next(request)

    @staticmethod
    def _unauthorized() -> Response:
        """Return unauthorized response."""
        return Response(
            content='{"detail": "Unauthorized"}',
            status_code=401,
            media_type="application/json",
        )
