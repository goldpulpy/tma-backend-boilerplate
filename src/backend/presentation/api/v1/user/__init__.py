"""User API endpoints."""

from fastapi import APIRouter

from .me import router as me_router

router = APIRouter(prefix="/user", tags=["User"])
router.include_router(me_router)
