"""Constants"""
from fastapi import status


class DetailError:
    """Default Error model to response."""

    CONTENT = {
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
    }



class HTTPResponseNewUser:
    """Swagger Docs."""

    responses = dict()
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )
    responses[status.HTTP_422_UNPROCESSABLE_ENTITY] = (
        ResponseError.RESPONSES.get(status.HTTP_422_UNPROCESSABLE_ENTITY)
    )

    responses[status.HTTP_400_BAD_REQUEST] = ResponseError.RESPONSES.get(
        status.HTTP_400_BAD_REQUEST
    )

class Response500:
    """Swagger Docs."""

    responses = dict()
    responses[status.HTTP_500_INTERNAL_SERVER_ERROR] = (
        ResponseError.RESPONSES.get(status.HTTP_500_INTERNAL_SERVER_ERROR)
    )

class MimeTypes:
    """МIME types constants."""

    APPLICATION_JSON = "application/json"


class ClientsRouts:
    """Registration routes."""

    TAG = "Clients"
    CREATE_CLIENT_PATH = "/clients/create"
    MACH_POST_PATH = "/clients/{id}/match"


class AllClientsRoutes:
    """All clients routes."""
    TAG = "AllClients"
    ALL_CLIENTS = "/list"



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
    MESSAGE_SERVER_ERROR = "An error occurred."
    MESSAGE_ENV_FILE_INCORRECT_OR_NOT_EXIST = "~/.env  incorrect or not exist"
    MESSAGE_NO_REFERRALS_FOUND = "No referrals found"
    MESSAGE_USER_NOT_FOUND = "User not found"
    MESSAGE_IF_EMAIL_ALREADY_EXIST = (
        "Registration failed. Please check your information."
    )


class H3Index:
    """H3 Index constants."""
    TABLE_NAME = 'locations'
    GEOMETRY_TYPE = 'POINT'
    SRID = 4326
    POSTGRESQL_INDEX_TYPE = 'gist'
    POSTGRESQL_GEOGRAPHY_OPS = 'geography_ops'
    H3_RESOLUTION_MIN = 4
    H3_RESOLUTION_MAX = 8

    FIELD_ID = 'id'
    FIELD_CREATOR = 'creator'
    FIELD_LOCATION = 'location'
    FIELD_LATITUDE = 'latitude'
    FIELD_LONGITUDE = 'longitude'
    H3_RESOLUTION_8 = 8
    H3_RESOLUTION_7 = 7
    H3_RESOLUTION_6 = 6
    H3_RESOLUTION_5 = 5
    H3_DIAMETER_8 = 461.354684
    H3_DIAMETER_7 = 1220.629759
    H3_DIAMETER_6 = 3229.482772
    H3_DIAMETER_5 = 8544.408276
    H3_MAX_DIAMETER_8 = 10000
    H3_MAX_DIAMETER_7 = 20000
    H3_MAX_DIAMETER_6 = 40000
    H3_MAX_DIAMETER_5 = 50000
    FIELD_H3_INDEX = "h3_index{}"

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

    TAG = "AUTH"
    LOGIN_PATH = "/auth/login"
    LOGOUT_PATH = "/auth/logout"
    TOKEN_PATH = "/auth/token"


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
