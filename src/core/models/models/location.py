"""Location table for User."""

import h3
from geoalchemy2 import Geography
from sqlalchemy import UUID, BigInteger, Column, ForeignKey, Index, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.models.base import BaseModel
from src.core.settings.constants import LocationH3


class LocationORM(BaseModel):
    """Location table for User."""

    __tablename__ = LocationH3.TABLE_NAME

    id: Mapped[id] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID,
        ForeignKey("users.id"),
        nullable=False,
    )

    location = Column(
        Geography(geometry_type=LocationH3.GEOMETRY_TYPE, srid=LocationH3.SRID)
    )

    h3_index_8: Mapped[id] = mapped_column(BigInteger)
    h3_index_7: Mapped[id] = mapped_column(BigInteger)
    h3_index_6: Mapped[id] = mapped_column(BigInteger)
    h3_index_5: Mapped[id] = mapped_column(BigInteger)
    h3_index_4: Mapped[id] = mapped_column(BigInteger)

    __table_args__ = (
        Index(
            "idx_location_gist",
            location,
            postgresql_using=LocationH3.POSTGRESQL_INDEX_TYPE,
        ),
    )

    def update_h3_indexes(self, latitude, longitude):
        """Update h3 indexes."""
        for res in range(
            LocationH3.H3_RESOLUTION_MIN, LocationH3.H3_RESOLUTION_MAX + 1
        ):

            h3_index = h3.latlng_to_cell(latitude, longitude, res)
            setattr(
                self, LocationH3.FIELD_H3_INDEX.format(res), int(h3_index, 16)
            )
