"""Registration routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.controllers.depends.match import match_post
from src.core.controllers.depends.reg import new_user
from src.core.settings.constants import (
    ClientsRouts,
    HTTPResponseAuthClients,
    HTTPResponseClients,
    MimeTypes,
)
from src.core.validators.match import Match
from src.core.validators.status_ok import Status


def create_reg_route() -> APIRouter:
    """Create clients router.

    Returns:
        APIRouter: Router with registration routes.
    """
    return APIRouter(tags=[ClientsRouts.TAG])


clients: APIRouter = create_reg_route()


@clients.post(
    path=ClientsRouts.CREATE_CLIENT_PATH,
    status_code=status.HTTP_201_CREATED,
    response_model=Status,
    responses=HTTPResponseClients.responses,
)
async def create_client(
    successful: Annotated[bool, Depends(new_user)]
) -> JSONResponse:
    """Handle new client registration."""
    return JSONResponse(
        content=Status(result=successful).model_dump(),
        status_code=status.HTTP_201_CREATED,
        media_type=MimeTypes.APPLICATION_JSON,
    )


@clients.post(
    path=ClientsRouts.MATCH_POST_PATH,
    status_code=status.HTTP_201_CREATED,
    response_model=Match,
    responses=HTTPResponseAuthClients.responses,
)
async def mach_post(
    successful: Annotated[bool, Depends(match_post)]
) -> JSONResponse:
    """Handle for match post."""
    pass
