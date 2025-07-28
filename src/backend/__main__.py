"""Main entry point for the application"""
import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.presentation import api
from backend.presentation.api import docs
from backend.containers import Container
from backend.shared import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

container = Container()
container.wire(packages=[api])


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None if config.app.is_production else "/openapi.json",
)


app.container = container
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.app.allowed_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
if config.app.is_development:
    docs.setup_scalar(app)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
