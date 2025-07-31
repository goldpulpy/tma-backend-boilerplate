"""Web App init data validation."""

import logging
from datetime import datetime

from aiogram.utils.web_app import (
    WebAppInitData,
    WebAppUser,
    safe_parse_webapp_init_data,
)

from backend.shared import config

logger = logging.getLogger(__name__)


class WebAppInitDataValidationError(Exception):
    """Web App init data validation error."""


def validate_init_data(init_data: str) -> WebAppInitData:
    """Validate Web App init data request."""
    if not config.app.is_production:
        logger.debug("Skipping validation in development environment")
        return WebAppInitData(
            user=WebAppUser(
                id=1,
                first_name="developer",
            ),
            auth_date=datetime.now().astimezone(),
            hash="developer",
        )

    try:
        return safe_parse_webapp_init_data(
            config.app.bot_token,
            init_data,
        )

    except Exception as e:
        msg = "Invalid init_data"
        raise WebAppInitDataValidationError(
            msg,
        ) from e


def validate_user_presence(web_app_init_data: WebAppInitData) -> WebAppUser:
    """Validate that user is present in init_data."""
    if not web_app_init_data.user:
        msg = "User is not found in init_data"
        logger.error(msg)
        raise WebAppInitDataValidationError(msg) from None

    return web_app_init_data.user
