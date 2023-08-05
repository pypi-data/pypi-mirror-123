"""True Checker API exceptions."""


class TrueCheckerException(Exception):
    """Base (root) True Checker exception."""


class BadRequest(TrueCheckerException):
    """
    Base Bad Request exception.

    Status: 400
    """


class Unauthorized(BadRequest):
    """
    Unauthorized exception.

    Occurs on troubles with Telegram token.
    Status: 401
    """


class BadState(BadRequest):
    """
    State conflict exception.

    Occurs if current state is not fits for request.
    Status: 409
    """


class ValidationError(BadRequest):
    """
    Wrong params are passed to API method.

    Status: 422
    """


class NotFound(BadRequest):
    """
    Requested object is not found.

    Status: 404
    """
