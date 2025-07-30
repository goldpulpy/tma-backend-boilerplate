"""Main entry point for the application."""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from backend.containers import Container
from backend.presentation import api
from backend.presentation.api import docs, health
from backend.shared import config
from backend.shared.slowapi import rate_limit_handler

logging.basicConfig(
    level=logging.INFO if config.app.is_production else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


container = Container()
container.wire(packages=[api])


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None if config.app.is_production else "/openapi.json",
)

app.state.limiter = Container.service.limiter()  # type: ignore[attr-defined]
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)


app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(health.router)

if config.app.is_development:
    docs.setup_scalar(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)  # noqa: S104
