# src\app\middleware\exceptions.py
class BaseError(Exception):
    status_code: int = 500

    def __init__(self, message: str = "Application error"):
        super().__init__(message)
        self.message = message


class ValidationError(BaseError):
    status_code = 400


class AuthError(BaseError):
    status_code = 401


class NotFoundError(BaseError):
    status_code = 404


class ServiceError(BaseError):
    status_code = 502


# src/app/exceptions.py
class ConfigError(BaseError):
    status_code = 500
