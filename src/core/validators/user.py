"""User model validator."""

import pydantic


class User(pydantic.BaseModel):
    """**Model  user details**.

     - `id`: str: Identification of user.
    - `name`: User's name.
    """

    id: str = pydantic.Field(
        description="Identification of user.",
    )
    name: str = pydantic.Field(
        ...,
        description="User's name.",
        min_length=2,
        max_length=15,
    )
    sex: str = pydantic.Field(
        pattern=r"[MF]",
    )
    location: tuple[float, float]

    avatar_path: str

    model_config = pydantic.ConfigDict(
        title="User",
        from_attributes=True,
    )


class UsersLocation(pydantic.BaseModel):
    """Validate model for profile of user."""

    id: str
    name: str
    users: list[User | None]

    model_config = pydantic.ConfigDict(title="User's nearby users")
