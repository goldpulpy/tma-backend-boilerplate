"""Middlewares for the API."""

from .authentication import AuthenticationMiddleware

__all__ = ["AuthenticationMiddleware"]
