"""User database model."""

from datetime import datetime

from sqlalchemy import TIMESTAMP, BigInteger, Column, String

from backend.infrastructure.database.base import Base


class UserModel(Base):
    """User model."""

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)
    username = Column(String, default=None)
    first_name = Column(String, nullable=False)
    last_name = Column(String, default=None)
    language_code = Column(String, default=None)
    photo_url = Column(String, default=None)
    created_at = Column(TIMESTAMP, default=datetime.now)
