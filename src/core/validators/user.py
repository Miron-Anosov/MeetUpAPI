"""User model validator."""

import pydantic


class User(pydantic.BaseModel):
    """User model for api/list.

    The User model stores essential details about a user,
    including two distance fields that provide flexible distance
    data depending on filtering requirements:

    distance_exact: Represents an exact distance value, useful when
    precise measurements are necessary for specific filters.
    distance_for_map: Represents distance data optimized for mapping
    applications. This value can be tailored based on different map
    resolutions, allowing for efficient rendering where nearby users
    with nearly zero distances may be hidden as the resolution increases.
    """

    id: str
    firstname: str
    lastname: str
    sex: str
    lat: float
    lon: float
    distance: float
    avatar_path: str

    model_config = pydantic.ConfigDict(
        title="User",
        from_attributes=True,
    )


class UsersCollection(pydantic.BaseModel):
    """User model for api/list.

    The UsersCollection model validates a collection of user profiles,
    with each user profile containing either precise or map-oriented
    distance data.
    The choice of distance representation (exact or map-optimized)
    allows the model to adapt to different filtering scenarios,
    balancing between accuracy and efficient
    map rendering at various resolutions.
    """

    users: list[User | None]

    model_config = pydantic.ConfigDict(title="User's nearby users_data")
