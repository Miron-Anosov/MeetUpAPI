"""Main module."""

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.apps.app_celery import check_redis_connection
from src.core.controllers.auth import auth
from src.core.controllers.clients import clients
from src.core.controllers.depends.utils.connect_db import disconnect_db
from src.core.controllers.depends.utils.redis_chash import (
    close_redis,
    init_redis,
)
from src.core.controllers.locations import location
from src.core.settings.env import settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Connect and close DB."""
    print("DB connected")
    redis = await init_redis()
    check_redis_connection()
    yield
    await disconnect_db()
    await close_redis(client=redis)
    print("DB disconnected")


def create_app() -> FastAPI:
    """Maker FastAPI."""
    app_ = FastAPI(
        lifespan=lifespan,
        root_path=settings.webconf.PREFIX_API,
    )

    app_.add_middleware(
        CORSMiddleware,  # noqa
        allow_origins=settings.webconf.allowed_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
