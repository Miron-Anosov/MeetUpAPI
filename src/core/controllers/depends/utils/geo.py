"""Geo utilities."""

import math

import h3
from geopy.distance import distance

from src.core.settings.constants import LocationH3
from src.core.validators.dto import H3Parameters, LocationData, LocationTemp


def select_h3_resolution_params(radius: float, exact: bool) -> H3Parameters:
    """Choice params H3 by radius."""
    if exact:
        return H3Parameters(
            resolution=LocationH3.H3_RESOLUTION_8,
            diameter=LocationH3.H3_MAX_DIAMETER_8,
            field_name=LocationH3.FIELD_H3_INDEX.format(
                LocationH3.H3_RESOLUTION_8
            ),
        )

    if radius <= LocationH3.H3_MAX_DIAMETER_8:
        return H3Parameters(
            resolution=LocationH3.H3_RESOLUTION_8,
            diameter=LocationH3.H3_MAX_DIAMETER_8,
            field_name=LocationH3.FIELD_H3_INDEX.format(
                LocationH3.H3_RESOLUTION_8
            ),
        )

    elif radius <= LocationH3.H3_MAX_DIAMETER_7:
        return H3Parameters(
            resolution=LocationH3.H3_RESOLUTION_7,
            diameter=LocationH3.H3_MAX_DIAMETER_7,
            field_name=LocationH3.FIELD_H3_INDEX.format(
                LocationH3.H3_RESOLUTION_7
            ),
        )

    elif radius <= LocationH3.H3_MAX_DIAMETER_6:
        return H3Parameters(
            resolution=LocationH3.H3_RESOLUTION_6,
            diameter=LocationH3.H3_MAX_DIAMETER_6,
            field_name=LocationH3.FIELD_H3_INDEX.format(
                LocationH3.H3_RESOLUTION_6
            ),
        )

    else:
        return H3Parameters(
            resolution=LocationH3.H3_RESOLUTION_5,
            diameter=LocationH3.H3_MAX_DIAMETER_5,
            field_name=LocationH3.FIELD_H3_INDEX.format(
                LocationH3.H3_RESOLUTION_5
            ),
        )


def get_near_indexes(
    user_location: int,
    radius: int | float,
    h3_params: H3Parameters,
) -> list[int]:
    """Return H3 indexes near location."""
    center_cell = h3.int_to_str(user_location)
    ring_size = math.ceil(radius / h3_params.diameter)
    neighbor_cells = h3.grid_disk(center_cell, ring_size)

    h3_indexes = [int(cell, 16) for cell in neighbor_cells]
    h3_indexes.append(user_location)

    return h3_indexes


def get_location_params_by_auth_user(
    auth_location: int | None,
    user_location: int | None,
    exact: bool | None,
) -> LocationData:
    """Get location params to auth user."""
    if auth_location and user_location:
        loc_temp = LocationTemp()
        loc_temp.h3_str_auth = h3.int_to_str(auth_location)
        loc_temp.h3_str_user = h3.int_to_str(user_location)

        loc_temp.lat_auth, loc_temp.lon_auth = h3.cell_to_latlng(
            loc_temp.h3_str_auth
        )
        loc_temp.lat_user, loc_temp.lon_user = h3.cell_to_latlng(
            loc_temp.h3_str_user
        )

        return LocationData(
            lat=loc_temp.lat_user,
            lon=loc_temp.lon_user,
            distance=(
                exact_circle_distance(coordinates=loc_temp)
                if exact
                else greate_circle_distance(coordinates=loc_temp)
            ),
        )
    raise ValueError("Data location is not valid.")


def greate_circle_distance(coordinates: LocationTemp) -> float:
    """Return greate-circle distance."""
    return h3.great_circle_distance(
        latlng1=(coordinates.lat_auth, coordinates.lon_auth),
        latlng2=(coordinates.lat_user, coordinates.lon_user),
        unit="km",
    )


def exact_circle_distance(coordinates: LocationTemp) -> float:
    """Return exact circle distance."""
    return (
        distance(
            (coordinates.lat_auth, coordinates.lon_auth),
            (coordinates.lat_user, coordinates.lon_user),
        ).m
        / 1000
    )
