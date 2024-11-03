"""Users CRUD methods."""

from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models.user import UserORM


class Users:
    """CRUD operations for user management."""

    @staticmethod
    async def insert_new_client(
        new_user: dict,
        session: AsyncSession,
        user_table: type[UserORM] = UserORM,
    ):
        """Add a new user to the database."""
        stmt = user_table(**new_user)
        session.add(stmt)

    # TODO добавляем логирование и обработку ошибок.

    @staticmethod
    async def update_path_avatar(
        path: str,
        user_ud: str,
        session: AsyncSession,
        user_table: type[UserORM] = UserORM,
    ):
        """Add path avatar to the database by user ID."""
        await session.execute(
            update(user_table)
            .where(user_table.id == user_ud)
            .values(avatar_path=path)
        )

    # TODO добавляем логирование и обработку ошибок.
