"""DTO cache model."""

from typing import Any, Callable, Iterable, Optional

from pydantic import BaseModel


class Cache(BaseModel):
    """DTO cache model."""

    pref_key: str
    exp: int | float
    fun: Callable
    return_type_ob: Any
    id_pers: Optional[int | str] = None
    req: Optional[Any] = None
    cache_key: str | None = None


class H3Parameters(BaseModel):
    """H3parameter model."""

    resolution: int
    diameter: float
    field_name: str


class UsersDataGeo(BaseModel):
    """Geographic model."""

    auth_location: int | None = None

    loc_data: Iterable | None = None
    users_data: Iterable | None = None
    field_name: str | None = None
    exact: bool | None = None


class LocationData(BaseModel):
    """Location model."""

    lat: float
    lon: float
    distance: float | None = None


class LocationTemp(BaseModel):
    """Location temp model."""

    lat_auth: float | None = None
    lon_auth: float | None = None
    lat_user: float | None = None
    lon_user: float | None = None
    h3_str_auth: str | None = None
    h3_str_user: str | None = None
