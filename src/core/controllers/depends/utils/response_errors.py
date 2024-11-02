"""Common Raise HTTPException."""

import uuid
from typing import Optional

from fastapi import HTTPException, status

from src.core.settings.constants import MessageError
from src.core.validators.error import ErrorMessage


def http_exception(
    status_code: int,
    error_type: str,
    error_message: str,
    headers: dict[str, str] | None = None,
) -> HTTPException:
    """Return HTTPException.

    Args:
        - status_code (int): HTTP status.
        - error_type (str): Type error.
        - error_message (str): Message error.
        - headers (dict[str, str] | None): If it is requirement.
    Raise:
        - HTTPException

    """
    return HTTPException(
        status_code=status_code,
        detail=ErrorMessage(
            error_type=error_type,
            error_message=error_message,
        ).model_dump(),
        headers=headers,
    )


def raise_400_bad_req(
    status_code=status.HTTP_400_BAD_REQUEST,
    error_type=MessageError.TYPE_ERROR_INVALID_REG,
    error_message=MessageError.MESSAGE_IF_EMAIL_ALREADY_EXIST,
):
    """Raise error for failed registration."""
    raise http_exception(
        status_code=status_code,
        error_type=error_type,
        error_message=error_message,
    )


def valid_password_or_error_422(pwd: str, pwd2: str) -> None:
    """Check the given password.

    Args:
        pwd (str): The password as a string.
        pwd2 (str): The control password as a string.

    Raises:
        HTTPException: If `pwd` is not same as `pwd2`.,
        raises HTTP 422 with an error message.
    """
    try:
        if pwd != pwd2:
            raise ValueError
    except ValueError:
        raise http_exception(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_type=MessageError.INVALID_ID_ERR,
            error_message=MessageError.INVALID_ID_ERR_MESSAGE,
        )
