# type: ignore
"""Location routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from geopy.distance import distance

from src.core.controllers.depends.get_users_near_auth import (
    location_near_auth_user,
)
from src.core.settings.constants import (
    LocationRoutes,
    MimeTypes,
    Response500,
    ResponsesAuthUser,
)
from src.core.validators.distance import DistanceRequest, DistanceResponse
from src.core.validators.user import Users


def create_location_route() -> APIRouter:
    """Create location route.

    Return:
    - APIRouter
    """
    return APIRouter(
        tags=[LocationRoutes.TAG],
    )


location: APIRouter = create_location_route()


@location.post(
    path=LocationRoutes.GET_USERS_PATH_BY_AUTH_USER,
    status_code=status.HTTP_200_OK,
    response_model=Users,
    responses=ResponsesAuthUser.responses,
)
async def get_locations_near_auth_user(
    users: Annotated[Users, Depends(location_near_auth_user)],
) -> "JSONResponse":
    """**Get locations of users_data near authenticated user**."""
    return JSONResponse(
        content=users.model_dump(),
        status_code=status.HTTP_201_CREATED,
        media_type=MimeTypes.APPLICATION_JSON,
    )


@location.post(
    path=LocationRoutes.GET_CALCULATED_DISTANCE_PATH,
    status_code=status.HTTP_200_OK,
    response_model=DistanceResponse,
    responses=Response500.responses,
)
async def get_distance(locations: DistanceRequest) -> "DistanceResponse":
    """**Get distance between two locations**."""
    return DistanceResponse(
        kilometers=distance(locations.location_a, locations.location_b).km
    )
