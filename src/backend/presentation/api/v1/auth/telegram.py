"""Telegram authentication endpoints."""

import logging
from datetime import datetime, timedelta
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

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
from backend.presentation.api.models.auth.telegram import (
    TelegramAuthRequest,
    TelegramAuthResponse,
)
from backend.shared import config
from backend.shared.jwt import create_jwt
from backend.shared.validators.webapp import (
    WebAppInitDataValidationError,
    validate_init_data,
    validate_user_presence,
)

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = ServiceContainer.limiter()


@router.post(
    "/telegram",
    status_code=status.HTTP_200_OK,
    summary="Telegram authentication endpoint",
    description="Authenticate via Telegram Mini App init_data",
    response_description="Telegram authentication response",
)
@limiter.limit("1/second")
@inject
async def telegram_auth(
    request: Request,  # noqa: ARG001
    auth_request: TelegramAuthRequest,
    ensure_user_use_case: Annotated[
        IEnsureUserUseCase,
        Depends(
            Provide[UserUseCaseContainer.ensure],
        ),
    ],
) -> JSONResponse:
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

        created_at = datetime.now().astimezone()
        expires_at = created_at + timedelta(days=config.jwt.expiry_days)

        jwt_token = create_jwt(
            {
                "sub": str(user.id.value),
                "exp": int(expires_at.timestamp()),
                "iat": int(created_at.timestamp()),
                "nbf": int(created_at.timestamp()),
                "iss": config.jwt.issuer,
            },
        )

        logger.debug(
            "Created JWT token (exp=%s, iat=%s, iss=%s)",
            int(expires_at.timestamp()),
            int(created_at.timestamp()),
            config.jwt.issuer,
        )

        json_response = JSONResponse(
            content=TelegramAuthResponse(
                status="success",
                message="Telegram authentication successful",
                created_at=int(created_at.timestamp()),
                expires_at=int(expires_at.timestamp()),
            ).model_dump(),
        )

        json_response.set_cookie(
            key="access_token",
            value=jwt_token,
            httponly=True,
            samesite="none" if config.app.is_production else "lax",
            secure=config.app.is_production,
        )

        logger.debug("Set access_token httpOnly cookie")

    except WebAppInitDataValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        ) from e

    except Exception as e:
        logger.exception("Error authenticating via Telegram")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e

    else:
        return json_response
