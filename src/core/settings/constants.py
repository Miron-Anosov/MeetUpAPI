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
