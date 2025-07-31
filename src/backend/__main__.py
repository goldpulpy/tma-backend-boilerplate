"""Main entry point for the application."""

import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from backend.containers import Container
from backend.containers.services import ServiceContainer
from backend.presentation import api
from backend.presentation.api import docs, health, middlewares, state
from backend.shared import config
from backend.shared.slowapi import rate_limit_handler

logging.basicConfig(
    level=logging.INFO if config.app.is_production else logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

# Wire all containers
container = Container()
container.user_use_case().wire(packages=[api])
container.service_use_case().wire(packages=[api])

app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None if config.app.is_production else "/openapi.json",
)

app.state = state.AppState()
app.state.limiter = ServiceContainer.limiter()

app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
app.add_middleware(middlewares.AuthenticationMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.app.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.include_router(health.router)

if config.app.is_development:
    docs.setup_scalar(app)


if __name__ == "__main__":
    logger.info(
        "Starting the application in %s mode",
        config.app.environment.value,
    )
    uvicorn.run(app, host=config.app.host, port=config.app.port)
