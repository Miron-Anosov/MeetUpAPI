"""Location CRUD methods."""

from collections.abc import Iterable

from geoalchemy2.types import Geometry
from sqlalchemy import func, select
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

    @staticmethod
    async def get_location_auths_user(
        user_id: str,
        session: AsyncSession,
        location_table: type[LocationORM] = LocationORM,
    ):
        """Get users_data location by user id."""
        result = await session.execute(
            select(
                func.ST_X(
                    location_table.location.cast(
                        Geometry(geometry_type="POINT", srid=4326)
                    )
                ),
                func.ST_Y(
                    location_table.location.cast(
                        Geometry(geometry_type="POINT", srid=4326)
                    )
                ),
            ).where(location_table.user_id == user_id)
        )
        longitude, latitude = result.first()

        return longitude, latitude

    @staticmethod
    async def get_h3_index_by_resolution(
        auth_id: str,
        field_h3_index: str,
        session: AsyncSession,
        location_table: type["LocationORM"] = LocationORM,
    ) -> int | None:
        """Get h3 index by user id."""
        user_location = await session.scalar(
            select(getattr(location_table, field_h3_index)).where(
                location_table.user_id == auth_id
            )
        )

        return user_location

    @staticmethod
    async def near_location(
        user_id: str,
        field_h3_index: str,
        session: AsyncSession,
        h3_indexes: list,
        location_table: type["LocationORM"] = LocationORM,
    ) -> Iterable["LocationORM"]:
        """Return nearest h3 index by user id."""
        nearby_locations = await session.execute(
            select(
                location_table.user_id,
                getattr(location_table, field_h3_index),
            ).where(
                getattr(location_table, field_h3_index).in_(h3_indexes),
                location_table.user_id != user_id,
            )
        )

        return nearby_locations.all()
