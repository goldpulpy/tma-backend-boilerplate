"""Authentication endpoints."""

from fastapi import APIRouter

from backend.presentation.api.v1.auth.telegram import router as telegram_router

router = APIRouter(prefix="/auth", tags=["Authentication"])

router.include_router(telegram_router)
