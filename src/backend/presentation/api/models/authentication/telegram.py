"""Telegram authentication models."""

from datetime import datetime

from pydantic import BaseModel


class TelegramAuthRequest(BaseModel):
    """Telegram authentication request."""

    init_data: str


class TelegramAuthResponse(BaseModel):
    """Telegram authentication response."""

    status: str
    message: str
    created_at: datetime
    expires_at: datetime
