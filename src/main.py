"""Main module."""

import uvicorn
from fastapi import FastAPI

from src.core.controllers.registration import registration


def create_app() -> FastAPI:
    """Maker FastAPI."""
    app_ = FastAPI()
    app_.include_router(registration)

    return app_


if __name__ == "__main__":
    """Local test"""
    app = create_app()
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8081,
        log_level="info",
    )
