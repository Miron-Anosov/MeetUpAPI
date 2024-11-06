# type: ignore
"""Serialize and deserialize module."""
import json
from typing import Any, Type, cast

import pydantic
from fastapi.responses import JSONResponse

from src.core.controllers.depends.utils.geo import (
    get_location_params_by_auth_user,
)
from src.core.validators.dto import LocationData, UsersDataGeo
from src.core.validators.user import User, UsersCollection


def deserialize_data_to_user_obj(
    users_data: "UsersDataGeo",
) -> "UsersCollection":
    """Deserialize data to UsersCollection object."""
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

    return UsersCollection(users=users)


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


def deserialize_data(data: Any, return_type: Type[pydantic.BaseModel]) -> Any:
    """Convert JSON string to Pydantic model.

    Args:
        data (str): JSON string to deserialize.
        return_type (Type[pydantic.BaseModel]): Target model type.

    Returns:
        pydantic.BaseModel: Deserialized data model.
    """
    try:
        if isinstance(data, str):
            return return_type(**json.loads(data))
        if isinstance(data, pydantic.BaseModel):
            return return_type(**data.model_dump())

        raise pydantic.ValidationError

    except pydantic.ValidationError as e:
        raise e


def serialize_data(data: Any) -> str:
    """Convert Pydantic model to JSON string.

    Args:
        data (pydantic.BaseModel): Data model to serialize.

    Returns:
        str: Serialized JSON string of the model.
    """
    try:
        if isinstance(data, pydantic.BaseModel):
            return data.model_dump_json()

        if isinstance(data, dict):
            return json.dumps(data)

        if isinstance(data, JSONResponse):
            return json.dumps(str(data.body))

        raise pydantic.ValidationError

    except pydantic.ValidationError as e:
        raise e
