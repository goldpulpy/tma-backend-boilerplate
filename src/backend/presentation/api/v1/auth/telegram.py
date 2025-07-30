"""Telegram authentication endpoints."""

import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, status

from backend.application.use_cases.user.ensure import IEnsureUserUseCase
from backend.containers import Container
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
from backend.shared.validators.webapp import (
    WebAppInitDataValidationError,
    validate_init_data,
    validate_user_presence,
)

logger = logging.getLogger(__name__)
router = APIRouter()
limiter = Container.service.limiter()


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
            Annotated[
                IEnsureUserUseCase,
                Provide[Container.use_case.user.ensure],
            ],
        ),
    ],
) -> TelegramAuthResponse:
    """Authenticate via Telegram Mini App init_data."""
    try:
        web_app_init_data = validate_init_data(auth_request.init_data)
        web_app_user = validate_user_presence(web_app_init_data)

        user = User(
            id=UserId(web_app_user.id),
            first_name=FirstName(web_app_user.first_name),
            last_name=LastName(web_app_user.last_name),
            username=Username(web_app_user.username),
            photo_url=PhotoUrl(web_app_user.photo_url),
            language_code=LanguageCode(web_app_user.language_code),
        )

        await ensure_user_use_case.execute(user)

        return TelegramAuthResponse(
            status="success",
            message="Telegram authentication successful",
            created_at=1,
            expires_at=1,
        )

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
