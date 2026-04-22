from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import timedelta

from b1sl.b1sl.environment import B1Env


@dataclass
class B1Config:
    """
    Configuration object for SAP B1 Service Layer connections.

    This dataclass holds the necessary parameters to authenticate and
    communicate with the SAP SL API. It includes support for session
    management and timeout settings.

    AI Role: Core configuration schema. Use 'from_env' or
    'from_django_settings' for automatic mapping from the environment.

    Attributes:
        base_url (str): Target SL URL (e.g., https://host:50000/b1s/v2).
        username (str): B1 user name.
        password (str): B1 user password.
        company_db (str): Target Company Database.
        environment (B1Env): Deployment stage. Defaults to B1Env.DEV.
            Controls log format (JSON in PROD, human-readable otherwise).
            Set via the ``B1SL_ENV`` environment variable.
        ssl_verify (bool, optional): Default True.
        reuse_token (bool, optional): Default True.
        token_timeout (timedelta, optional): Default 900s.
        max_page_size (int, optional): Default 20.
        connect_timeout (float, optional): TCP timeout (seconds).
        read_timeout (float, optional): Read timeout (seconds).
        dry_run (bool, optional): If True, POST/PATCH/DELETE requests are intercepted and logged without being sent to SAP. Defaults to False.
    """

    base_url: str
    username: str
    password: str
    company_db: str
    environment: B1Env = B1Env.DEV
    ssl_verify: bool = True
    reuse_token: bool = True
    token_timeout: timedelta = field(default_factory=lambda: timedelta(seconds=900))
    max_page_size: int = 20
    connect_timeout: float = 10.0  # seconds to establish TCP connection
    read_timeout: float = 60.0  # seconds to wait for SAP to respond
    etag_cache_size: int = 256
    dry_run: bool = False
    b1s_schema: str | None = None

    def __post_init__(self) -> None:
        """Validates all required parameters are present after initialisation."""
        if not self.base_url:
            raise ValueError("B1Config.base_url cannot be empty")
        if not self.username or not self.password:
            raise ValueError("B1Config credentials (username/password) cannot be empty")
        if not self.company_db:
            raise ValueError("B1Config.company_db cannot be empty")

    @classmethod
    def from_env(cls, strict: bool = True) -> "B1Config":
        """
        Factory method that loads configuration from OS environment variables.

        AI Role: Standard way to load config. Expects variables prefixed
        with B1SL_ (e.g., B1SL_BASE_URL).

        Args:
            strict (bool): If True (default), raises EnvironmentError if
                required variables are missing. If False, returns a dummy
                config for testing/VCR playback.

        Returns:
            B1Config: Loaded instance.

        Raises:
            EnvironmentError: If strict is True and any required variable is missing.
        """
        required = {
            "base_url": "B1SL_BASE_URL",
            "username": "B1SL_USERNAME",
            "password": "B1SL_PASSWORD",
            "company_db": "B1SL_COMPANY_DB",
        }
        missing = [key for attr, key in required.items() if not os.environ.get(key)]

        if missing and strict:
            raise EnvironmentError(
                f"Missing required SAP B1 config env vars: {missing}"
            )

        kwargs = {
            "base_url": os.environ.get("B1SL_BASE_URL", "https://dummy:50000/b1s/v2"),
            "username": os.environ.get("B1SL_USERNAME", "dummy"),
            "password": os.environ.get("B1SL_PASSWORD", "dummy"),
            "company_db": os.environ.get("B1SL_COMPANY_DB", "SBODemoMX"),
            "ssl_verify": os.environ.get("B1SL_SSL_VERIFY", "1") == "1",
            "reuse_token": os.environ.get("B1SL_REUSE_TOKEN", "1") == "1",
            "token_timeout": timedelta(
                seconds=int(os.environ.get("B1SL_TOKEN_TIMEOUT", 900))
            ),
            "max_page_size": int(os.environ.get("B1SL_MAX_PAGE_SIZE", 20)),
            "etag_cache_size": int(os.environ.get("B1SL_ETAG_CACHE_SIZE", 256)),
            "connect_timeout": float(os.environ.get("B1SL_CONNECT_TIMEOUT", 10)),
            "read_timeout": float(os.environ.get("B1SL_READ_TIMEOUT", 60)),
            "environment": B1Env(os.environ.get("B1SL_ENV", "dev").lower()),
            "dry_run": os.environ.get("B1SL_DRY_RUN", "0") == "1",
            "b1s_schema": os.environ.get("B1SL_SCHEMA"),
        }

        return cls(**kwargs)

    @classmethod
    def from_django_settings(cls) -> "B1Config":
        """
        Factory method that loads configuration from django.conf.settings.

        AI Role: Use this only when running within a Django application.

        Returns:
            B1Config: Instance populated from settings.py variables.
        """
        from django.conf import settings

        return cls(
            base_url=getattr(settings, "B1SL_BASE_URL", ""),
            username=getattr(settings, "B1SL_USERNAME", ""),
            password=getattr(settings, "B1SL_PASSWORD", ""),
            company_db=getattr(settings, "B1SL_COMPANY_DB", ""),
            environment=B1Env(getattr(settings, "B1SL_ENV", "dev").lower()),
            ssl_verify=getattr(settings, "B1SL_SSL_VERIFY", True),
            reuse_token=getattr(settings, "B1SL_REUSE_TOKEN", True),
            token_timeout=timedelta(
                seconds=int(getattr(settings, "B1SL_TOKEN_TIMEOUT", 900))
            ),
            max_page_size=int(getattr(settings, "B1SL_MAX_PAGE_SIZE", 20)),
            etag_cache_size=int(getattr(settings, "B1SL_ETAG_CACHE_SIZE", 256)),
            connect_timeout=float(getattr(settings, "B1SL_CONNECT_TIMEOUT", 10)),
            read_timeout=float(getattr(settings, "B1SL_READ_TIMEOUT", 60)),
            dry_run=getattr(settings, "B1SL_DRY_RUN", False),
            b1s_schema=getattr(settings, "B1SL_SCHEMA", None),
        )
