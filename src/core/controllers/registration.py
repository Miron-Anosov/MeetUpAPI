"""Registration routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from src.core.controllers.depends.reg import new_user
from src.core.settings.constants import (
    HTTPResponseNewUser,
    MimeTypes,
    ClientsRouts,
)
from src.core.validators.status_ok import Status


def create_reg_route() -> APIRouter:
    """Create registration router.

    Returns:
        APIRouter: Router with registration routes.
    """
    return APIRouter(tags=[ClientsRouts.TAG])


registration: APIRouter = create_reg_route()


@registration.post(
    path=ClientsRouts.CREATE_CLIENT_PATH,
    status_code=status.HTTP_201_CREATED,
    response_model=Status,
    responses=HTTPResponseNewUser.responses,
)
async def create_client(
    successful: Annotated[bool, Depends(new_user)]
) -> JSONResponse:
    """Handle new client registration.

    Args:
        successful (bool): Indicates if user creation succeeded.

    Returns:
        JSONResponse: Response with registration status.
    """
    return JSONResponse(
        content=Status(result=successful).model_dump(),
        status_code=status.HTTP_201_CREATED,
        media_type=MimeTypes.APPLICATION_JSON,
    )