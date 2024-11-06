"""UsersCollection CRUD methods."""

from sqlalchemy import Sequence, bindparam, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models.auth import AuthORM


class AuthUsers:
    """CRUD operations for authentication users_data."""

    @staticmethod
    async def insert_auth_user(
        session: AsyncSession,
        auth_user: dict,
        table_auth: type[AuthORM] = AuthORM,
    ) -> None:
        """Add a new user to the database."""
        session.add(table_auth(**auth_user))

    @staticmethod
    async def login_user(
        email: str,
        session: AsyncSession,
        auth_user: type[AuthORM] = AuthORM,
    ):
        """Authenticate a user by email."""
        try:
            user: AuthORM | None = await session.scalar(
                statement=(
                    select(auth_user).where(
                        auth_user.email == bindparam("email")
                    )
                ),
                params={"email": email},
            )

            if user:
                return user.hashed_password, user.user_id

            return None, None

        except SQLAlchemyError as e:
            print(e)
            return None, None

    @staticmethod
    async def get_emails_by_id(
        session: AsyncSession,
        users: tuple[str, str],
        table_auth: type[AuthORM] = AuthORM,
    ):
        """Return emails users_data by ID."""
        stmt = select(table_auth.email).where(table_auth.user_id.in_(users))

        result = await session.execute(stmt)

        emails = result.scalars().all()
        return emails
