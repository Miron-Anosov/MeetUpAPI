"""Core ORM module."""

from src.core.models.cruds.auth import AuthUsers
from src.core.models.cruds.location import Locations
from src.core.models.cruds.user import Users


class Crud:
    """Interface for combined CRUD operations."""

    def __init__(
        self,
        user_crud: Users,
        auth_crud: AuthUsers,
        location_crud: Locations,
    ) -> None:
        """Initialize Crud with CRUD instances."""
        self.users = user_crud
        self.auth = auth_crud
        self.locations = location_crud


def create_crud_helper() -> Crud:
    """Initialize and return a Crud instance with models.

    Returns:
        Crud: Initialized Crud instance.
    """
    return Crud(
        location_crud=Locations(),
        user_crud=Users(),
        auth_crud=AuthUsers(),
    )
