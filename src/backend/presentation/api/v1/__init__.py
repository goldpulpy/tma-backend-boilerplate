"""V1 Routes."""

from fastapi import APIRouter

from backend.presentation.api.v1.auth import router as auth_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
