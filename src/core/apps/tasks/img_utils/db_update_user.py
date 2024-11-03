"""Add path avatar to user_table."""

from src.core.controllers.depends.utils.connect_db import (
    get_crud,
    get_session,
    init_engine,
)


async def add_path_to_user(
    file_path: str,
    user_id: str,
) -> None:
    """Add path avatar to user_table."""
    crud = get_crud()
    engine = await init_engine()
    async with engine.get_scoped_session() as session:

        async with session.begin():
            await crud.users.update_path_avatar(
                path=file_path, user_ud=user_id, session=session
            )

        await session.close()
