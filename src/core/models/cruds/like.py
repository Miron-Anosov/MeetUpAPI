"""Like CRUD methods."""

from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models.like import LikesORM
from src.core.settings.constants import IntKeys


class Like:
    """CRUD operations for user management."""

    @staticmethod
    async def insert_new_match(
        target_user: str,
        owner_like: str,
        session: AsyncSession,
        like_table: type[LikesORM] = LikesORM,
    ):
        """Add a new match."""
        stmt = like_table(owner_like_id=owner_like, target_like_id=target_user)

        session.add(stmt)

    # TODO добавляем логирование и обработку ошибок.

    @staticmethod
    async def select_match(
        target_user: str,
        owner_like: str,
        session: AsyncSession,
        like_table: type[LikesORM] = LikesORM,
    ) -> bool:
        """Check if a match exists."""
        stmt = select(func.count()).where(
            or_(
                and_(
                    like_table.owner_like_id == owner_like,
                    like_table.target_like_id == target_user,
                ),
                and_(
                    like_table.owner_like_id == target_user,
                    like_table.target_like_id == owner_like,
                ),
            )
        )
        result = await session.scalar(stmt)

        return True if result == IntKeys.MATCH else False

    # TODO добавляем логирование и обработку ошибок.
