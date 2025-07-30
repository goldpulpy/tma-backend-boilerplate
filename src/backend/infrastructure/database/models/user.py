"""User database model."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.infrastructure.database.base import Base


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str | None] = mapped_column(String, default=None)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str | None] = mapped_column(String, default=None)
    language_code: Mapped[str | None] = mapped_column(String, default=None)
    photo_url: Mapped[str | None] = mapped_column(String, default=None)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        default=datetime.now,
    )
