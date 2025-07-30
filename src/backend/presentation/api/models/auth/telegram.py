"""Telegram authentication models."""

from pydantic import BaseModel


class TelegramAuthRequest(BaseModel):
    """Telegram authentication request."""

    init_data: str


class TelegramAuthResponse(BaseModel):
    """Telegram authentication response."""

    status: str
    message: str
    created_at: int
    expires_at: int
