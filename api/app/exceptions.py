from fastapi import HTTPException, status
from typing import TypedDict


class Error(HTTPException):
    status_code: int
    detail: str = "Undefined error"
    field: str | None = None
    exception: Exception | None = None

    def __init__(
        self, detail=None, field=None, exception=None, status_code=None, key=None, **options
    ):
        self.field = field
        self.exception = exception
        self.options = options
        self._key = key

        if status_code:
            self.status_code = status_code

        assert self.status_code
        super().__init__(self.status_code, detail=detail or self.detail)

    def for_api(self):
        return {"detail": self.detail}


class NotFound(Error):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Not found"


class NoContent(Error):
    status_code = status.HTTP_204_NO_CONTENT
    detail = "No content"


class Forbidden(Error):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Forbidden"


class BadRequest(Error):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Bad Request"


class InvalidJsonPatch(Error):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Invalid json patch"


class AWSAuthError(Error):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "AWS Auth Error"
    extra = None


class UserAlreadyExists(AWSAuthError):
    detail = "User already exists"


class InvalidPassword(AWSAuthError):
    detail = "Invalid password"


class UserNotConfirmed(AWSAuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not confirmed"


class NotAuthorized(AWSAuthError):
    detail = "Not authorized"

class TokenExpired(AWSAuthError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Token expired"

class InvalidToken(AWSAuthError):
    detail = "Invalid Access Token"

class InternalServerError(Error):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal server error"

class Unauthorized(Error):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"

class ErrorResponse(TypedDict):
    __errors__: list[Error]


def build_errors_for_api(errors: list[Error]) -> ErrorResponse:
    return ErrorResponse(__errors__=[e.for_api() for e in errors])


def build_error_for_api(error: Error) -> ErrorResponse:
    return build_errors_for_api([error])
