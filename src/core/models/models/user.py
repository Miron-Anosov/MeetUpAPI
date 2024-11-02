"""SQLAlchemy UserORM model."""
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.models.base import BaseModel



class UserORM(BaseModel):
    """User ORM model."""

    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    avatar_path: Mapped[str] = mapped_column()
