"""User me endpoints."""

import logging
from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Request, status

from backend.application.use_cases.user.get import IGetUserUseCase
from backend.containers.user.use_cases import UserUseCaseContainer
from backend.domain.exceptions.user import UserNotFoundError
from backend.domain.value_objects.user import UserId
from backend.presentation.api.models.user.me import UserMeResponse
from backend.shared.validators.fastapi import (
    UserIdNotFoundInStateError,
    get_user_id_from_state,
)

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    description="Retrieve the profile information for the authenticated user",
    response_description="User profile information",
    responses={
        200: {
            "description": "User profile retrieved successfully",
            "model": UserMeResponse,
        },
        401: {"description": "Unauthorized"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"},
    },
)
@inject
async def get_me(
    request: Request,
    get_user_use_case: Annotated[
        IGetUserUseCase,
        Depends(
            Provide[UserUseCaseContainer.get],
        ),
    ],
) -> UserMeResponse:
    """Get user profile."""
    try:
        user_id = get_user_id_from_state(request)
        user = await get_user_use_case.execute(UserId(user_id))
        return UserMeResponse.from_entity(user)

    except UserNotFoundError as e:
        logger.exception("User not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        ) from e

    except UserIdNotFoundInStateError as e:
        logger.exception("User id not found in state")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        ) from e

    except Exception as e:
        logger.exception("Error getting user profile")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        ) from e
