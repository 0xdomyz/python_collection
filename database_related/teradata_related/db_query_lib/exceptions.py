"""Custom exceptions for database query library."""


class DatabaseConnectionError(Exception):
    """Raised when database connection fails."""

    pass


class QueryExecutionError(Exception):
    """Raised when query execution fails."""

    pass


class ConfigurationError(Exception):
    """Raised when configuration is invalid."""

    pass


class ThreadPoolExecutionError(Exception):
    """Raised when threadpool execution fails."""

    pass
