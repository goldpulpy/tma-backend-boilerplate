"""Slowapi utilities."""

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded


async def rate_limit_handler(
    request: Request,  # noqa: ARG001
    exc: Exception,
) -> Response:
    """Rate limit handler."""
    if isinstance(exc, RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too many requests",
                "detail": f"Rate limit exceeded: {exc.detail}",
            },
        )

    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )
