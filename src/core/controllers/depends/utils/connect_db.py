"""Get db session and CRUDs."""

from typing import TYPE_CHECKING, Annotated

from fastapi import Depends

from src.core.models.crud import create_crud_helper
from src.core.models.engine import get_engine
from src.core.settings.env import settings

if TYPE_CHECKING:
    from src.core.models.crud import Crud
    from src.core.models.engine import HelperDB


def get_crud() -> "Crud":
    """Return CRUD worker."""
    return create_crud_helper()


async def init_engine():
    """Initialize the engine and connect to the database."""
    return await get_engine(
        url=settings.db.get_url_database, echo=settings.db.ECHO
    )


async def disconnect_db():
    """Disconnect db."""
    connect = await get_engine(
        url=settings.db.get_url_database, echo=settings.db.ECHO
    )
    await connect.async_engine.dispose()


async def get_session(engine: Annotated["HelperDB", Depends(init_engine)]):
    """Return db session."""
    async with engine.get_scoped_session() as session:
        yield session
        await session.close()
