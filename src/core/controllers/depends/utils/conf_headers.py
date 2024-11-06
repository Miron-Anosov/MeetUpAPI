"""Setter Http headers."""

from fastapi import Request, Response

from src.core.settings.constants import Headers


def set_response_headers(
    response: Response,
    exp: int | float,
    cached_value: str,
    update: bool = False,
):
    """Set cache headers in the response.

    Args:
        response (Response): HTTP response object.
        exp (int): Expiration time in seconds.
        cached_value (str): Cached data string for ETag.
        update (bool): Whether cache is a hit or miss.
    """
    response.headers[Headers.CACHE_CONTROL] = f"{Headers.CACHE_MAX_AGE}{exp}"
    response.headers[Headers.ETAG] = gen_etag(cached_value)
    response.headers[Headers.X_CACHE] = (
        Headers.X_CACHE_MISS if update is False else Headers.X_CACHE_HIT
    )


def gen_etag(cached_value: str) -> str:
    """Generate ETag from cached value.

    Args:
        cached_value (str): Cached data string.

    Returns:
        str: Weak ETag generated from cached value.
    """
    return f"W/{hash(cached_value)}"


def check_etag(request: Request, response: Response) -> bool:
    """Validate ETag to check cache validity.

    Args:
        request (Request): Incoming request with ETag.
        response (Response): Response containing ETag.

    Returns:
        bool: True if ETag matches, False otherwise.
    """
    return request.headers.get(Headers.IF_NONE_MATCH) == response.headers.get(
        Headers.ETAG
    )
