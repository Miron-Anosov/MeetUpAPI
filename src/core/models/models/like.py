"""SQLAlchemy FollowersORM model."""

from sqlalchemy import UUID, BigInteger, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.models.base import BaseModel


class LikesORM(BaseModel):
    """Likes ORM model."""

    __tablename__ = "likes"

    like_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    owner_like_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    target_like_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    __table_args__ = (
        Index(
            "unique_like_idx", "owner_like_id", "target_like_id", unique=True
        ),
    )
