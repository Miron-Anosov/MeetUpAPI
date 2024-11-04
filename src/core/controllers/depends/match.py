"""This is the match module."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Path
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import IntegrityError

from src.core.apps.tasks.tasks import background_task_send_email
from src.core.controllers.depends.token import token_is_alive
from src.core.controllers.depends.utils.connect_db import get_crud, get_session
from src.core.controllers.depends.utils.response_errors import (
    raise_http_401,
    valid_id_or_error_422,
)
from src.core.settings.constants import JWT

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.core.models.crud import Crud


async def match_post(
    token: Annotated[dict, Depends(token_is_alive)],
    crud: Annotated["Crud", Depends(get_crud)],
    session: Annotated["AsyncSession", Depends(get_session)],
    target_user_id: str = Path(
        ..., description="The ID of the target user to match", alias="id"
    ),
) -> bool:
    """Match post dependency."""
    valid_id_or_error_422(id_data=target_user_id)

    try:

        type_token = token.pop(JWT.TOKEN_TYPE_FIELD)

        if type_token == JWT.TOKEN_TYPE_ACCESS:
            auth_user = token.pop(JWT.PAYLOAD_SUB_KEY)

            if auth_user == target_user_id:
                return False

            async with session.begin():
                await crud.likes.insert_new_match(
                    target_user=target_user_id,
                    owner_like=auth_user,
                    session=session,
                )

            is_match = await crud.likes.select_match(
                target_user=target_user_id,
                owner_like=auth_user,
                session=session,
            )

            if is_match:

                id_users: tuple[str, str] = target_user_id, auth_user

                emails = await crud.auth.get_emails_by_id(
                    session=session,
                    users=id_users,
                )

                names = await crud.users.get_user_names(
                    id_users=id_users,
                    session=session,
                )

                background_task_send_email(emails=emails, names=names)

                return True

            else:

                return True

        raise InvalidTokenError

    except InvalidTokenError as e:
        print(e)
        raise_http_401()
        return False

    except IntegrityError:
        # TODO logger  если уже есть уникальная пара значений
        return True
