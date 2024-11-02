"""Users CRUD methods."""

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
