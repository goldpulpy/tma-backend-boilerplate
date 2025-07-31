"""FastAPI app state."""

from __future__ import annotations

from typing import TYPE_CHECKING

from starlette.datastructures import State

if TYPE_CHECKING:
    from slowapi import Limiter


class AppState(State):
    """App state."""

    limiter: Limiter
    user_id: int | None
