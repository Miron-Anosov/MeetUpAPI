"""Depends for new users."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.core.controllers.depends.utils.connect_db import get_crud, get_session

if TYPE_CHECKING:
    from fastapi.responses import JSONResponse
    from sqlalchemy.ext.asyncio import AsyncSession

    from src.core.models.crud import Crud


async def login_user_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    crud: Annotated["Crud", Depends(get_crud)],
    session: Annotated["AsyncSession", Depends(get_session)],
) -> "JSONResponse":
    """Check user in DB than create tokens."""
    pass
