"""Users CRUD methods."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models.auth import AuthORM


class AuthUsers:
    """CRUD operations for authentication users."""

    @staticmethod
    async def insert_auth_user(
        session: AsyncSession,
        auth_user: dict,
        table_auth: type[AuthORM] = AuthORM,
    ) -> None:
        """Add a new user to the database."""
        session.add(table_auth(**auth_user))
