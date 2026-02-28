"""Configuration management from environment variables."""

import os
from dataclasses import dataclass
from typing import Optional

from .exceptions import ConfigurationError


@dataclass
class DatabaseConfig:
    """Database configuration loaded from environment variables."""

    host: str
    user: str
    password: str
    database: str = "DBC"
    logmech: str = "TD2"
    charset: str = "UTF8"

    @classmethod
    def from_env(cls, required: bool = True) -> "DatabaseConfig":
        """
        Load configuration from environment variables.

        Environment variables:
            - TERADATA_HOST (required)
            - TERADATA_USER (required)
            - TERADATA_PASSWORD (required)
            - TERADATA_DATABASE (optional, default: DBC)
            - TERADATA_LOGMECH (optional, default: TD2)
            - TERADATA_CHARSET (optional, default: UTF8)

        Args:
            required: If True, raise error if required vars missing. If False, allow None values.

        Returns:
            DatabaseConfig instance

        Raises:
            ConfigurationError: If required environment variables are missing.
        """
        host = os.getenv("TERADATA_HOST")
        user = os.getenv("TERADATA_USER")
        password = os.getenv("TERADATA_PASSWORD")

        if required and not all([host, user, password]):
            missing = [
                name
                for name, value in [
                    ("TERADATA_HOST", host),
                    ("TERADATA_USER", user),
                    ("TERADATA_PASSWORD", password),
                ]
                if not value
            ]
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        if not required and not any([host, user, password]):
            # Return test config if none are set
            return cls(
                host=host or "localhost",
                user=user or "test_user",
                password=password or "test_pass",
                database=os.getenv("TERADATA_DATABASE", "DBC"),
                logmech=os.getenv("TERADATA_LOGMECH", "TD2"),
                charset=os.getenv("TERADATA_CHARSET", "UTF8"),
            )

        return cls(
            host=host or "localhost",
            user=user or "test_user",
            password=password or "test_pass",
            database=os.getenv("TERADATA_DATABASE", "DBC"),
            logmech=os.getenv("TERADATA_LOGMECH", "TD2"),
            charset=os.getenv("TERADATA_CHARSET", "UTF8"),
        )

    def get_sqlalchemy_connection_string(self) -> str:
        """Get SQLAlchemy connection string."""
        return f"teradatasql://{self.user}:{self.password}@{self.host}/{self.database}"

    def get_teradataml_params(self) -> dict:
        """Get Teradataml connection parameters."""
        return {
            "host": self.host,
            "username": self.user,
            "password": self.password,
            "database": self.database,
            "logmech": self.logmech,
            "charset": self.charset,
        }
