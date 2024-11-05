# type: ignore
"""This is the match module."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, Path, Request, Response
from jwt.exceptions import InvalidTokenError
from sqlalchemy.exc import IntegrityError

from src.core.apps.tasks.tasks import background_task_send_email
from src.core.controllers.depends.token import token_is_alive
from src.core.controllers.depends.utils.connect_db import get_crud, get_session
from src.core.controllers.depends.utils.redis_chash import (
    cache_count_limit_http_request_for_positive_response,
)
from src.core.controllers.depends.utils.response_errors import (
    raise_http_401,
    valid_id_or_error_422,
)
from src.core.settings.constants import JWT
from src.core.settings.env import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.core.models.crud import Crud


@cache_count_limit_http_request_for_positive_response(
    expire_in_day=settings.redis.exp_in_days,
    prefix_key="match_post",
    match_limits=settings.redis.REDIS_LIMIT_REQUESTS,
)
async def match_post(
    request: Request,
    response: Response,
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

        if token.get(JWT.TOKEN_TYPE_FIELD) != JWT.TOKEN_TYPE_ACCESS:
            raise InvalidTokenError()

        if token.get(JWT.PAYLOAD_SUB_KEY) == target_user_id:
            return False

        async with session.begin():
            await crud.likes.insert_new_match(
                target_user=target_user_id,
                owner_like=token.get(JWT.PAYLOAD_SUB_KEY),
                session=session,
            )

        is_match = await crud.likes.select_match(
            target_user=target_user_id,
            owner_like=token.get(JWT.PAYLOAD_SUB_KEY),
            session=session,
        )

        if is_match:

            id_users: tuple[str, str] = target_user_id, token.get(
                JWT.PAYLOAD_SUB_KEY
            )

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

    except InvalidTokenError as e:
        print(e)
        raise_http_401()
        return False

    except IntegrityError as e:
        print(e, response, request)
        # TODO logger  target_user_id is not exist
        return True
