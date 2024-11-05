# type: ignore
"""Serialize and deserialize module."""

from typing import cast

from src.core.controllers.depends.utils.geo import (
    get_location_params_by_auth_user,
)
from src.core.validators.dto import LocationData, UsersDataGeo
from src.core.validators.user import User, Users


def deserialize_data_to_user_obj(users_data: "UsersDataGeo") -> "Users":
    """Deserialize data to Users object."""
    users: list[User] = []

    for user, loc in zip(users_data.users_data, users_data.loc_data):
        geo: LocationData = get_location_params_by_auth_user(
            auth_location=users_data.auth_location,
            user_location=getattr(loc, users_data.field_name),
            exact=users_data.exact,
        )
        if geo.distance > 0 or users_data.exact:
            user_model = make_model(user, geo)
            users.append(user_model)

    return Users(users=users)


def make_model(user, geo) -> "User":
    """Maker User."""
    return User(
        id=str(user.id),
        firstname=user.first_name,
        lastname=user.last_name,
        sex=user.sex,
        lat=geo.lat,
        lon=geo.lon,
        distance=geo.distance,
        avatar_path=user.avatar_path,
    )
