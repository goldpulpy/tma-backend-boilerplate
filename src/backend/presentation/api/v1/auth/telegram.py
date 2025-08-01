"""Telegram authentication endpoints."""

import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    status,
)

from backend.application.use_cases.user.ensure import IEnsureUserUseCase
from backend.containers.services import ServiceContainer
from backend.containers.user.use_cases import UserUseCaseContainer
from backend.domain.entities.user import User
from backend.domain.value_objects.user import (
    FirstName,
    LanguageCode,
    LastName,
    PhotoUrl,
    UserId,
    Username,
)
from backend.presentation.api.models.authentication.telegram import (
    TelegramAuthRequest,
    TelegramAuthResponse,
)
from backend.shared import config
from backend.shared.jwt import create_auth_token
from backend.shared.validators.webapp import (
    WebAppInitDataValidationError,
    validate_init_data,
    validate_user_presence,
)

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = ServiceContainer.limiter()


def set_auth_cookie(response: Response, token: str) -> None:
    """Set authentication cookie with proper security settings."""
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        samesite="none" if config.app.is_production else "lax",
        secure=config.app.is_production,
        max_age=config.jwt.expiry_days * 24 * 60 * 60,
    )


@router.post(
    "/telegram",
    status_code=status.HTTP_200_OK,
    summary="Telegram authentication endpoint",
    description="Authenticate via Telegram Mini App init_data",
    response_description="Telegram authentication response",
    responses={
        200: {
            "description": "Authentication successful",
            "model": TelegramAuthResponse,
        },
        401: {"description": "Invalid Telegram authentication data"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Internal server error"},
    },
)
@limiter.limit("1/second")
@inject
async def telegram_auth(
    request: Request,  # noqa: ARG001
    response: Response,
    auth_request: TelegramAuthRequest,
    ensure_user_use_case: Annotated[
        IEnsureUserUseCase,
        Depends(
            Provide[UserUseCaseContainer.ensure],
        ),
    ],
) -> TelegramAuthResponse:
    """Authenticate via Telegram Mini App init_data."""
    try:
        web_app_init_data = validate_init_data(auth_request.init_data)
        web_app_user = validate_user_presence(web_app_init_data)

        logger.debug("Validated web_app_user: %s", web_app_user)

        user = User(
            id=UserId(web_app_user.id),
            first_name=FirstName(web_app_user.first_name),
            last_name=LastName(web_app_user.last_name),
            username=Username(web_app_user.username),
            photo_url=PhotoUrl(web_app_user.photo_url),
            language_code=LanguageCode(web_app_user.language_code),
        )

        logger.debug("Ensuring user %s", user.id.value)
        await ensure_user_use_case.execute(user)

        jwt_token, created_at, expires_at = create_auth_token(
            str(user.id.value),
        )

        logger.debug(
            "Created JWT token (sub=%s, exp=%s, iat=%s, iss=%s)",
            str(user.id.value),
            expires_at,
            created_at,
            config.jwt.issuer,
        )

        set_auth_cookie(response, jwt_token)
        logger.debug("Set token httpOnly cookie")

        return TelegramAuthResponse(
            status="success",
            message="Telegram authentication successful",
            created_at=created_at,
            expires_at=expires_at,
        )

    except WebAppInitDataValidationError as e:
        logger.warning("Invalid Telegram init_data: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication data",
        ) from e

    except Exception as e:
        logger.exception("Error authenticating via Telegram")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
