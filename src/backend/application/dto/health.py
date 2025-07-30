"""Health services status DTO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HealthServiceStatus:
    """Health status."""

    db_connection: bool
