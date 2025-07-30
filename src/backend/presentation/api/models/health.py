"""Health check models."""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    timestamp: int
