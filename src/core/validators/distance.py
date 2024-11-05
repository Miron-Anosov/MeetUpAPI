"""User model validator."""

import pydantic


class DistanceRequest(pydantic.BaseModel):
    """Model for getting distance between two locations."""

    location_a: tuple[float, float]
    location_b: tuple[float, float]

    model_config = pydantic.ConfigDict(
        title="Get distance between two locations",
        json_schema_extra={
            "example": {
                "location_a": (55.7558, 37.6173),
                "location_b": (59.9343, 30.3351),
            }
        },
    )


class DistanceResponse(pydantic.BaseModel):
    """Model representing the distance in kilometers."""

    kilometers: float

    model_config = pydantic.ConfigDict(title="Distance model")
