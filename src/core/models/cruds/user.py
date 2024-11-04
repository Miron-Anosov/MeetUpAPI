"""Users CRUD methods."""

from typing import Optional

from sqlalchemy import Sequence, select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
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

    @staticmethod
    async def get_user(
        id_user: str,
        session: AsyncSession,
        user_table: type[UserORM] = UserORM,
    ) -> Optional["UserORM"]:
        """Fetch a user by ID."""
        stmt = select(user_table).where(user_table.id == id_user)
        try:
            return await session.scalar(stmt)
        except (SQLAlchemyError, IntegrityError) as e:
            print(e)
            return None

    # TODO добавляем логирование и обработку ошибок.

    @staticmethod
    async def get_user_names(
        id_users: tuple,
        session: AsyncSession,
        user_table: type[UserORM] = UserORM,
    ):
        """Fetch user's names by ID."""
        stmt = select(user_table.first_name).where(user_table.id.in_(id_users))
        result = await session.execute(stmt)
        names = result.scalars().all()
        return names
