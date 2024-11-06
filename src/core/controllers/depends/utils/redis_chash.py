# type: ignore
"""Cache module for caching API responses with Redis."""

import hashlib
from functools import update_wrapper, wraps
from typing import Any, Callable

from fastapi import Request, Response
from fastapi.dependencies.utils import get_typed_return_annotation
from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from starlette.status import HTTP_304_NOT_MODIFIED

from src.core.controllers.depends.utils.conf_headers import (
    check_etag,
    set_response_headers,
)
from src.core.controllers.depends.utils.response_errors import raise_http_429
from src.core.controllers.depends.utils.serialize_and_deserilize import (
    deserialize_data,
    serialize_data,
)
from src.core.controllers.depends.utils.token_from import (
    get_user_id_from_token,
)
from src.core.settings.constants import IntKeys, LiterKeys, TypeEncoding
from src.core.settings.env import settings


def singleton(func: Callable) -> Callable:
    """Singleton pattern decorator for caching instances.

    Args:
        func (Callable): The function to wrap with singleton pattern.

    Returns:
        Callable: Wrapped function with singleton pattern.
    """
    instance: dict[str, Any] = {}

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        if ins_func := instance.get(func.__name__):
            return ins_func
        new_instance = await func(*args, **kwargs)
        instance[func.__name__] = new_instance
        return new_instance

    return wrapper


@singleton
async def setup_redis(
    url: str = settings.redis.redis_url_broker,
    encoding: str = TypeEncoding.UTF8,
    decode_responses: bool = True,
) -> Redis:
    """Initialize Redis client.

    Args:
        url (str): Redis connection URL.
        encoding (str): Character encoding used for responses.
        decode_responses (bool): Flag for decoding responses.

    Returns:
        Redis: Redis client instance.
    """
    try:
        return await aioredis.from_url(
            url=url,
            encoding=encoding,
            decode_responses=decode_responses,
        )
    except aioredis.RedisError as e:
        raise e


async def close_redis(client: Redis) -> None:
    """Close the Redis connection.

    Args:
        client (Redis): Redis client instance to close.

    Raises:
        RedisError: If closing the connection fails.
    """
    try:
        await client.close()
    except aioredis.RedisError as e:
        raise e


async def init_redis() -> Redis:
    """Return initialized Redis client.

    Returns:
        Redis: Initialized Redis client.
    """
    return await setup_redis()


def gen_hash_from_req(req: Request) -> str:
    """Gen hash from request params."""
    data_to_cache = get_user_id_from_token(request=req)

    req_params = req.query_params.items()

    return hashlib.md5(
        f"{data_to_cache}{req_params if req_params else ''}".encode()
    ).hexdigest()


def gen_key(prefix_key: str, req: Request | None = None) -> str:
    """Generate cache key from request parameters.

    Args:
        prefix_key (str): Prefix for cache key.
        req (Request): Request parameters.

    Returns:
        str: Generated cache key.
    """
    keys = [prefix_key]

    if req:
        keys.append(gen_hash_from_req(req=req))
    return ":".join(keys)


async def get_cache(cache_key: str) -> str | None:
    """Retrieve cached data from Redis by key.

    Args:
        cache_key (str): Key to retrieve data from Redis.

    Returns:
        str | None: Cached data if available, else None.
    """
    redis_client: Redis = await setup_redis()
    try:
        return await redis_client.get(cache_key)
    except aioredis.RedisError as e:
        raise e


async def set_cache(cache_key, value, ex) -> None:
    """Store data in Redis with expiration time.

    Args:
        cache_key (str): Key to store data under.
        value (Any): Data to store in Redis.
        ex (int): Expiration time in seconds.

    Raises:
        RedisError: If storage fails.
    """
    redis_client: Redis = await setup_redis()
    try:

        await redis_client.set(
            name=cache_key,
            value=value,
            ex=ex,
        )

    except aioredis.RedisError as e:
        raise e


async def get_cache_ttl(cache_key: str) -> int:
    """Retrieve TTL (time-to-live) for a cache key.

    Args:
        cache_key (str): The key for which TTL is requested.

    Returns:
    int: Remaining time in seconds. Returns -1 if the key has no expiration,
             and -2 if the key does not exist.
    """
    redis_client: Redis = await setup_redis()
    try:
        ttl = await redis_client.ttl(cache_key)
        return ttl
    except aioredis.RedisError as e:
        raise e


async def select_request_and_response(**kwargs) -> tuple[Request, Response]:
    """Select request and response from keyword arguments.

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        tuple[Request, Response]: Selected request and response objects.
    """
    request: Request = kwargs.get(LiterKeys.REQUEST)
    response: Response = kwargs.get(LiterKeys.RESPONSE)
    return request, response


def cache_count_limit_http_request_for_positive_response(
    expire_in_day: int,
    prefix_key: str,
    match_limits: int,
) -> Callable:
    """Cache decorator for match POST.

    If func return True  count limit += 1 else limit == limit.
    """

    def _decorator(function: Callable) -> Callable:

        @wraps(function)
        async def _wrapper(*args: Any, **kwargs: Any):
            request, response = await select_request_and_response(**kwargs)

            cache_key = gen_key(prefix_key=prefix_key, req=request)
            cached_value = await get_cache(cache_key=cache_key)

            if cached_value and int(cached_value) >= match_limits:
                raise_http_429()

            func_volume = await function(*args, **kwargs)

            if func_volume:
                limit_volume = (
                    IntKeys.FIRST_MATCH + int(cached_value)
                    if cached_value
                    else IntKeys.FIRST_MATCH
                )
                await set_cache(
                    cache_key=cache_key, value=limit_volume, ex=expire_in_day
                )

            return func_volume

        update_wrapper(_wrapper, function)

        return _wrapper

    return _decorator


def cache_list_location(expire: int, prefix_key: str) -> Callable:
    """Cache decorator for POST api/location."""

    def _decorator(function: Callable) -> Callable:
        return_type = get_typed_return_annotation(function)

        @wraps(function)
        async def _wrapper(*args: Any, **kwargs: Any):
            request, response = await select_request_and_response(**kwargs)

            cache_key = gen_key(prefix_key=prefix_key, req=request)

            cached_value = await get_cache(cache_key=cache_key)

            if cached_value is None:
                data_response = await function(*args, **kwargs)

                cached_value = serialize_data(data_response)

                await set_cache(
                    cache_key=cache_key, value=cached_value, ex=expire
                )
                set_response_headers(response, expire, cached_value)

                return data_response

            else:
                exp = await get_cache_ttl(cache_key=cache_key)

                set_response_headers(
                    response=response,
                    exp=exp,
                    cached_value=cached_value,
                    update=True,
                )

                if check_etag(request=request, response=response):
                    return Response(status_code=HTTP_304_NOT_MODIFIED)

                data_response = deserialize_data(
                    data=cached_value, return_type=return_type
                )

                return data_response

        return _wrapper

    return _decorator
