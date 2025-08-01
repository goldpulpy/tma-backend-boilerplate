"""V1 Routes."""

from fastapi import APIRouter

from .auth import router as auth_router
from .user import router as user_router

router = APIRouter(prefix="/v1")

router.include_router(auth_router)
router.include_router(user_router)
