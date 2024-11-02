"""Location CRUD methods."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.models.models.location import LocationORM
from src.core.settings.constants import LocationH3


class Locations:
    """CRUD operations for user management."""

    @staticmethod
    async def insert_location(
        location: dict,
        session: AsyncSession,
        location_table: type[LocationORM] = LocationORM,
    ) -> None:
        """Create a new location by user id."""
        latitude = location[LocationH3.FIELD_LOCATION][
            LocationH3.FIELD_LATITUDE_INDEX
        ]
        longitude = location[LocationH3.FIELD_LOCATION][
            LocationH3.FIELD_LONGITUDE_INDEX
        ]

        location[LocationH3.FIELD_LOCATION] = f"POINT({longitude} {latitude})"

        new_location = location_table(**location)

        new_location.update_h3_indexes(latitude=latitude, longitude=longitude)

        session.add(new_location)
