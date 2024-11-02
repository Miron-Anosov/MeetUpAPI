"""Location routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from geopy.distance import distance

from src.core.controllers.depends.get_location_by_auth_user import (
    location_near_auth_user,
)
from src.core.settings.constants import (
    LocationRoutes,
    Response500,
    ResponsesAuthUser,
)
from src.core.validators.distance import DistanceRequest, DistanceResponse
from src.core.validators.user import UsersLocation


def create_location_route() -> APIRouter:
    """Create location route.

    Return:
    - APIRouter
    """
    return APIRouter(
        tags=[LocationRoutes.TAG],
    )


location: APIRouter = create_location_route()


@location.get(
    path=LocationRoutes.GET_USERS_PATH_BY_AUTH_USER,
    status_code=status.HTTP_200_OK,
    response_model=UsersLocation,
    responses=ResponsesAuthUser.responses,
)
async def get_locations_near_auth_user(
    users: Annotated["JSONResponse", Depends(location_near_auth_user)],
) -> "JSONResponse":
    """**Get locations of users near authenticated user**."""
    return users


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
