"""Main module."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.core.controllers.auth import auth
from src.core.controllers.clients import clients
from src.core.controllers.depends.utils.connect_db import disconnect_db
from src.core.controllers.locations import location


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Connect and close DB."""
    print("DB connected")
    yield
    await disconnect_db()
    print("DB disconnected")


def create_app() -> FastAPI:
    """Maker FastAPI."""
    app_ = FastAPI(
        lifespan=lifespan,
    )
    app_.include_router(clients)
    app_.include_router(auth)
    app_.include_router(location)

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
