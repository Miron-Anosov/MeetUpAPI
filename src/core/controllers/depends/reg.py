"""Dependent for new users."""

import uuid
from typing import TYPE_CHECKING, Annotated, Optional

import pydantic
from fastapi import Depends, Form

from src.core.controllers.depends.utils.connect_db import get_crud, get_session
from src.core.controllers.depends.utils.hash_password import hash_pwd
from src.core.controllers.depends.utils.response_errors import (
    raise_400_bad_req,
    valid_password_or_error_422,
)
from src.core.controllers.locations import location

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.core.models.crud import Crud


async def new_user(
    crud: Annotated["Crud", Depends(get_crud)],
    session: Annotated["AsyncSession", Depends(get_session)],
    first_name: Annotated[
        str,
        Form(
            description="Author's name.",
            min_length=2,
            max_length=15,
            pattern=r"^[a-zA-Z0-9_]+$",
        ),
    ],
    last_name: Annotated[
        str,
        Form(
            description="Author's name.",
            min_length=2,
            max_length=15,
            pattern=r"^[a-zA-Z0-9_]+$",
        ),
    ],
    email: Annotated[
        pydantic.EmailStr,
        Form(
            description="User's email.",
        ),
    ],
    password: Annotated[
        str,
        Form(
            min_length=8,
            max_length=64,
            description="User's secret.",
        ),
    ],
    password_control: Annotated[
        str,
        Form(
            min_length=8,
            max_length=64,
            description="User's secret for check both.",
        ),
    ],
    sex: Annotated[
        str,
        Form(
            description="User's sex.",
            min_length=1,
            max_length=1,
            pattern=r"^[MF]$",
            default_value="M",
        ),
    ],
    avatar: Annotated[
        bytes | None,
        Form(
            description="User's avatar.",
            max_length=1024 * 1024,
        ),
    ] = None,
    latitude: Annotated[
        float,
        Form(
            description="User's latitude.",
            ge=-90,
            le=90,
        ),
    ] = 0,
    longitude: Annotated[
        float,
        Form(
            description="User's longitude.",
            ge=-180,
            le=180,
        ),
    ] = 0,
) -> Optional[bool]:
    """Create a new user from form data.

    Returns:
        JSONResponse: Confirmation of user creation or error message
    """
    valid_password_or_error_422(pwd=password, pwd2=password_control)

    password_hash: bytes = hash_pwd(password)

    new_uuid = uuid.uuid4().hex

    new_auth = dict(
        user_id=new_uuid,
        hashed_password=password_hash.decode(),
        email=email,
    )

    new_location = dict(
        user_id=new_uuid,
        location=(latitude, longitude),
    )

    creating_user = dict(
        id=new_uuid,
        first_name=first_name,
        last_name=last_name,
        sex=sex,
        avatar_path="",  # TODO gen path
    )

    try:
        async with session.begin():

            await crud.users.insert_new_client(
                session=session,
                new_user=creating_user,
            )

            await session.flush()

            await crud.auth.insert_auth_user(
                session=session,
                auth_user=new_auth,
            )

            await crud.locations.insert_location(
                session=session, location=new_location
            )

        return True
    except Exception as e:
        print(f"Registration failed: {e}")
        raise_400_bad_req()
        await session.close()
        return None
