# type: ignore
"""This is the location by auth user module."""

from typing import Annotated

from fastapi import Depends, Form, Header, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.controllers.depends.token import token_is_alive
from src.core.controllers.depends.utils.connect_db import get_crud, get_session
from src.core.controllers.depends.utils.geo import (
    get_near_indexes,
    select_h3_resolution_params,
)
from src.core.controllers.depends.utils.redis_chash import cache_list_location
from src.core.controllers.depends.utils.response_errors import (
    raise_400_bad_req,
)
from src.core.controllers.depends.utils.serialize_and_deserilize import (
    deserialize_data_to_user_obj,
)
from src.core.models.crud import Crud
from src.core.settings.constants import JWT, DescriptionForms, LiterKeys
from src.core.settings.env import settings
from src.core.validators.dto import UsersDataGeo
from src.core.validators.user import UsersCollection


@cache_list_location(
    expire=settings.redis.REDIS_EXP_LOCATION,
    prefix_key=LiterKeys.LOCATION_PREF,
)
async def location_near_auth_user(
    token: Annotated[dict, Depends(token_is_alive)],
    crud: Annotated["Crud", Depends(get_crud)],
    session: Annotated["AsyncSession", Depends(get_session)],
    request: Request,
    response: Response,
    radius: Annotated[
        int | float,
        Query(description=DescriptionForms.RADIUS),
    ] = 1,
    exact: Annotated[
        bool,
        Query(description=DescriptionForms.EXACT),
    ] = False,
    sex: Annotated[
        str | None,
        Form(
            description="User's sex.",
            min_length=1,
            max_length=1,
            pattern=r"^[MF]$",
            default_value="M",
        ),
    ] = None,
    first_name: Annotated[
        str | None,
        Form(
            description="User's name.",
            min_length=2,
            max_length=15,
            pattern=r"^[a-zA-Z0-9_]+$",
        ),
    ] = None,
    last_name: Annotated[
        str | None,
        Form(
            description="User's name.",
            min_length=2,
            max_length=15,
            pattern=r"^[a-zA-Z0-9_]+$",
        ),
    ] = None,
    sort_by_created: bool | None = None,
    if_none_match: str | None = Header(default=None),
) -> UsersCollection:
    """Get location by auth user."""
    if radius:

        users_geo_data = UsersDataGeo()

        radius = 150_000 if exact and radius > 150_000 else radius
        # TODO затычка  что  база не упала,
        #  для 300 кm создается большой запрос с таким разрешением.

        h3_params = select_h3_resolution_params(radius, exact)
        users_geo_data.field_name = h3_params.field_name
        users_geo_data.exact = exact

        auth_location = await crud.locations.get_h3_index_by_resolution(
            auth_id=token.get(JWT.PAYLOAD_SUB_KEY),
            field_h3_index=h3_params.field_name,
            session=session,
        )

        if auth_location:

            users_geo_data.auth_location = auth_location

            h3_indexes = get_near_indexes(
                user_location=auth_location,
                radius=radius,
                h3_params=h3_params,
            )

            users_geo_data.loc_data = await crud.locations.near_location(
                user_id=token.get(JWT.PAYLOAD_SUB_KEY),
                field_h3_index=h3_params.field_name,
                h3_indexes=h3_indexes,
                session=session,
            )

            extract_user_id = [
                user_data.user_id for user_data in users_geo_data.loc_data
            ]

            filters = {}
            if sex:
                filters["sex"] = sex
            if first_name:
                filters["first_name"] = first_name
            if last_name:
                filters["last_name"] = last_name

            users_geo_data.users_data = await crud.users.get_user_by_filers(
                users_id=extract_user_id,
                filters=filters,
                sort_by_created=sort_by_created,
                session=session,
            )

            users_obj: UsersCollection = deserialize_data_to_user_obj(
                users_data=users_geo_data
            )

            return users_obj

    return raise_400_bad_req()
