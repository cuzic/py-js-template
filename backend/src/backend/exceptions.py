"""Custom exceptions for the backend application."""


class BaseApplicationError(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, code: str | None = None):
        self.message = message
        self.code = code
        super().__init__(message)


class InvalidCredentialsError(BaseApplicationError):
    """Raised when authentication credentials are invalid."""

    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message, code="INVALID_CREDENTIALS")


class UserNotFoundError(BaseApplicationError):
    """Raised when a user is not found."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message, code="USER_NOT_FOUND")


class TokenExpiredError(BaseApplicationError):
    """Raised when an authentication token has expired."""

    def __init__(self, message: str = "Token has expired"):
        super().__init__(message, code="TOKEN_EXPIRED")


class ValidationError(BaseApplicationError):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message, code="VALIDATION_ERROR")
