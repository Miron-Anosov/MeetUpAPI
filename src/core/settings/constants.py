"""Constants."""

from pathlib import Path
from typing import Any, Collection

from fastapi import status


class DetailError:
    """Default Error model to response."""

    CONTENT: dict[str, Any] = {
        "application/json": {
            "example": {
                "detail": {
                    "result": False,
                    "error_type": "String",
                    "error_message": "String",
                }
            }
        }
    }


class ResponseError:
    """Swagger Docs Errors."""

    RESPONSES = {
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Not authenticated",
            "content": DetailError.CONTENT,
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "Forbidden",
            "content": DetailError.CONTENT,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Not Found",
            "content": DetailError.CONTENT,
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "description": "Validation Error",
            "content": DetailError.CONTENT,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Invalid credentials",
            "content": DetailError.CONTENT,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Bad Request",
            "content": DetailError.CONTENT,
        },
        status.HTTP_429_TOO_MANY_REQUESTS: {
            "description": "Not Found",
            "content": DetailError.CONTENT,
        },
    }


class HTTPResponseClients:
    """Swagger Docs."""

    responses: dict[str, Any] = dict()
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY] = (
        ResponseError.RESPONSES.get(status.HTTP_422_UNPROCESSABLE_ENTITY)
    )

    responses[status.HTTP_400_BAD_REQUEST] = ResponseError.RESPONSES.get(
        status.HTTP_400_BAD_REQUEST
    )


class HTTPResponseAuthClients:
    """Swagger Docs."""

    responses: dict[str, Any] = dict()
    responses[status.HTTP_401_UNAUTHORIZED] = ResponseError.RESPONSES.get(
        status.HTTP_401_UNAUTHORIZED
    )
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY] = (
        ResponseError.RESPONSES.get(status.HTTP_422_UNPROCESSABLE_ENTITY)
    )


class HTTPResponseMatch:
    """Http Response Match."""

    responses: dict[str, Any] = dict()
    responses[status.HTTP_401_UNAUTHORIZED] = ResponseError.RESPONSES.get(
        status.HTTP_401_UNAUTHORIZED
    )
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY] = (
        ResponseError.RESPONSES.get(status.HTTP_422_UNPROCESSABLE_ENTITY)
    )
    responses[status.HTTP_429_TOO_MANY_REQUESTS] = ResponseError.RESPONSES.get(
        status.HTTP_429_TOO_MANY_REQUESTS
    )


class Response500:
    """Swagger Docs."""

    responses = dict()
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )


class ResponsesAuthUser:
    """Swagger Docs."""

    responses = dict()
    responses[status.HTTP_401_UNAUTHORIZED] = ResponseError.RESPONSES.get(
        status.HTTP_401_UNAUTHORIZED
    )
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )


class ResponsesLocationUser:
    """Swagger Docs."""

    responses_304: dict[str, Collection[str]] | None = {
        status.HTTP_304_NOT_MODIFIED: {
            "description": "Not Modified",
            "content": {},
        },
    }

    responses = dict()
    responses[status.HTTP_401_UNAUTHORIZED] = ResponseError.RESPONSES.get(
        status.HTTP_401_UNAUTHORIZED
    )
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )

    responses[status.HTTP_304_NOT_MODIFIED] = responses_304
    responses[status.HTTP_404_NOT_FOUND] = ResponseError.RESPONSES.get(
        status.HTTP_404_NOT_FOUND
    )


class MimeTypes:
    """МIME types constants."""

    APPLICATION_JSON = "application/json"


class ClientsRouts:
    """Registration routes."""

    TAG = "Clients"
    CREATE_CLIENT_PATH = "/clients/create"
    MATCH_POST_PATH = "/clients/{id}/match"


class MessageError:
    """STATIC ERROR DATA."""

    INVALID_EMAIL_OR_PWD = "Invalid email or password"
    INVALID_TOKEN_ERR = "Invalid token."
    INVALID_ID_ERR = "Invalid ID."
    INVALID_ID_ERR_MESSAGE = "Type ID is not correct."
    INVALID_ID_ERR_MESSAGE_404 = "ID is not exist."
    INVALID_TOKEN_ERR_MESSAGE = "Please repeat authentication."
    INVALID_REF_TOKEN_ERR_MESSAGE = "Token is not exist."
    TYPE_ERROR_INVALID_AUTH = "Invalid auth."
    TYPE_ERROR_INVALID_REG = "Invalid registration."
    TYPE_ERROR_INTERNAL_SERVER_ERROR = "Internal server error."
    TYPE_ERROR_404 = "HTTP_404_NOT_FOUND"
    TYPE_ERROR_500 = "HTTP_500_INTERNAL_SERVER_ERROR"
    TYPE_ERROR_429 = "429 Too Many Requests"
    MESSAGE_429_LIMIT = "Message 429 Limit request."
    MESSAGE_SERVER_ERROR = "An error occurred."
    MESSAGE_ENV_FILE_INCORRECT_OR_NOT_EXIST = "~/.env  incorrect or not exist"
    MESSAGE_USER_NOT_FOUND = "User not found"
    MESSAGE_IF_EMAIL_ALREADY_EXIST = (
        "Registration failed. Please check your information."
    )


class LocationH3:
    """H3 Index constants."""

    TABLE_NAME = "locations"
    GEOMETRY_TYPE = "POINT"
    SRID = 4326
    POSTGRESQL_INDEX_TYPE = "gist"
    POSTGRESQL_GEOGRAPHY_OPS = "geography_ops"
    H3_RESOLUTION_MIN = 3
    H3_RESOLUTION_MAX = 9

    FIELD_ID = "id"
    FIELD_CREATOR = "creator"
    FIELD_LOCATION = "location"
    FIELD_LATITUDE = "latitude"
    FIELD_LATITUDE_INDEX = 0
    FIELD_LONGITUDE = "longitude"
    FIELD_LONGITUDE_INDEX = 1

    H3_RESOLUTION_9 = 9
    H3_RESOLUTION_8 = 8
    H3_RESOLUTION_7 = 7
    H3_RESOLUTION_6 = 6
    H3_RESOLUTION_5 = 5
    H3_RESOLUTION_4 = 4
    H3_RESOLUTION_3 = 3

    H3_MAX_DIAMETER_9 = 100
    H3_MAX_DIAMETER_8 = 2000
    H3_MAX_DIAMETER_7 = 3000
    H3_MAX_DIAMETER_6 = 5000
    H3_MAX_DIAMETER_5 = 6000
    H3_MAX_DIAMETER_4 = 8000
    H3_MAX_DIAMETER_3 = 15000

    FIELD_H3_INDEX = "h3_index_{}"


class JWT:
    """STATIC JWT DATA."""

    DESCRIPTION_PYDANTIC_ACCESS_TOKEN = (
        "Authorization: Bearer JWT access-token. It'll set at "
    )
    DESCRIPTION_PYDANTIC_REFRESH_TOKEN = "Set-cookie: JWT refresh_token"
    DESCRIPTION_PYDANTIC_TOKEN_TYPE = "Bearer"
    DESCRIPTION_PYDANTIC_TITLE = "Token"
    DESCRIPTION_PYDANTIC_EXPIRE_REFRESH = "expires_refresh"
    PAYLOAD_EXPIRE_KEY = "exp"
    PAYLOAD_IAT_KEY = "iat"
    PAYLOAD_SUB_KEY = "sub"
    PAYLOAD_USERNAME_KEY = "username"
    TOKEN_TYPE_FIELD = "type"
    TOKEN_TYPE_ACCESS = "access_token"
    TOKEN_TYPE_REFRESH = "refresh_token"


class AuthRoutes:
    """Authorization routes."""

    TAG = "Authorization"
    LOGIN_PATH = "/auth/login"
    LOGOUT_PATH = "/auth/logout"
    TOKEN_PATH = "/auth/token"


class LocationRoutes:
    """Authorization routes."""

    TAG = "Location"
    GET_USERS_PATH_BY_AUTH_USER = "/list"
    GET_CALCULATED_DISTANCE_PATH = "/distance"


class Headers:
    """STATIC HEADERS DATA."""

    WWW_AUTH_BEARER = {"WWW-Authenticate": "Bearer"}
    WWW_AUTH_BEARER_LOGOUT = {"WWW-Authenticate": 'Bearer realm="logout"'}
    AUTHORIZATION = {"Authorization": ""}
    WWW_AUTH_BEARER_EXPIRED = {
        "WWW-Authenticate": 'Bearer realm="Refresh token expired"'
    }
    CACHE_CONTROL = "Cache-Control"
    CACHE_MAX_AGE = "max-age="
    ETAG = "ETag"
    X_CACHE = "X-Cache"
    X_CACHE_MISS = "MISS"
    X_CACHE_HIT = "HIT"
    IF_NONE_MATCH = "if-none-match"


class CommonConfSettings:
    """Common configurate."""

    ENV_FILE_NAME = ".env"
    EXTRA_IGNORE = "ignore"

    ENV = Path(__file__).parent.parent.parent.parent / ENV_FILE_NAME


class JWTconf:
    """Conf for settings."""

    ALGORITHM = "RS256"
    ENV_PREFIX = "JWT_"
    ACCESS_EXPIRE_MINUTES = 15
    REFRESH_EXPIRE_DAYS = 30
    REFERRAL_EXPIRE_DAYS = 100
    PRIVATE_KEY = "private_key"
    PUBLIC_KEY = "public_key"


class IntKeys:
    """Index keys."""

    AUTH_USER_FOR_EMAIL = 0
    TARGET_USER_FOR_EMAIL = 1
    MATCH = 2
    FIRST_MATCH = 1


class LiterKeys:
    """Litter KEYS."""

    REQUEST = "request"
    RESPONSE = "response"
    # GET = "GET"
    # POST = "POST"
    # DELETE = "DELETE"
    AUTH_HEADER = "authorization"
    AUTH_HEADER_PREF_BEARER = 7
    LOCATION_PREF = "api/location_list"


class TypeEncoding:
    """STATIC ENCODING DATA."""

    UTF8 = "utf-8"


class DescriptionForms:
    """Description forms."""

    EXACT = (
        "Specifies whether to use exact distances. "
        "If true, precise distance calculations are applied;"
        " if false, approximate values are used, suited for map"
        " visualizations with varying zoom levels."
    )

    RADIUS = (
        "Sets the radius with H3 resolution level 9 as the highest precision,"
        " with a maximum effective diameter "
        "of approximately 100 meters (H3_MAX_DIAMETER_9 = 100). Additional "
        "resolutions are also available with the following "
        "maximum diameters: 2,000 meters for level 8, 3,000 meters "
        "for level 7, 5,000 meters for level 6, 6,000 meters for level 5, "
        "8,000 meters for level 4, and 15,000 meters for level 3. "
        "These thresholds can be adjusted for production as needed. "
        "When 'EXACT' is applied, the default resolution "
        "is set to the highest available (level 9), with a maximum "
        "range constraint of 300 km (or 150 km when interpreted as radius). "
        "The unit of measurement is currently set to meters."
    )
