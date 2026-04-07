from __future__ import annotations

import os
from dataclasses import dataclass, field
from datetime import timedelta


@dataclass
class SapHDBConfig:
    address: str
    port: int
    user: str
    password: str
    schema: str
    reuse_connection: bool = False
    connection_timeout: timedelta = field(
        default_factory=lambda: timedelta(seconds=900)
    )

    @classmethod
    def from_env(cls) -> "SapHDBConfig":
        """Load config from environment variables (no Django dependency)."""
        missing = []
        required = {
            "address": "SAPODBCLIENT_ADDRESS",
            "port": "SAPODBCLIENT_PORT",
            "user": "SAPODBCLIENT_USER",
            "password": "SAPODBCLIENT_PASSWORD",
            "schema": "SAPODBCLIENT_COMPANY_DB",
        }
        kwargs = {}
        for attr, env_key in required.items():
            val = os.environ.get(env_key)
            if not val:
                missing.append(env_key)
            kwargs[attr] = val

        if missing:
            raise EnvironmentError(
                f"Missing required SAP HDB config env vars: {missing}"
            )

        kwargs["port"] = int(kwargs["port"])
        # Standard pythonic way to parse boolean environment variables
        env_reuse = os.environ.get("SAPODBCLIENT_REUSE_CONNECTION", "False").lower()
        kwargs["reuse_connection"] = env_reuse in ("true", "1", "t", "y", "yes")

        kwargs["connection_timeout"] = timedelta(
            seconds=int(os.environ.get("SAPODBCLIENT_CONNECTION_TIMEOUT", 900))
        )
        return cls(**kwargs)

    @classmethod
    def from_django_settings(cls) -> "SapHDBConfig":
        """Load from django.conf.settings — only call this inside a Django app."""
        from django.conf import settings

        return cls(
            address=settings.SAPODBCLIENT_ADDRESS,
            port=int(settings.SAPODBCLIENT_PORT),
            user=settings.SAPODBCLIENT_USER,
            password=settings.SAPODBCLIENT_PASSWORD,
            schema=settings.SAPODBCLIENT_COMPANY_DB,
            reuse_connection=getattr(settings, "SAPODBCLIENT_REUSE_CONNECTION", False),
            connection_timeout=timedelta(
                seconds=int(getattr(settings, "SAPODBCLIENT_CONNECTION_TIMEOUT", 900))
            ),
        )
