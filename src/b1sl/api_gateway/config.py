from __future__ import annotations

import os
from dataclasses import dataclass, field, replace
from datetime import timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from b1sl.b1sl.config import B1Config


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class APIGatewayConfig:
    """
    Connection settings for the SAP B1 **API Gateway** (Crystal Reports over
    REST — a service distinct from the Service Layer).

    Attributes:
        base_url: Gateway root, e.g. ``https://host:60000``. Only the scheme,
            host and port — the client appends ``/login`` and ``/rs/v1/…``
            itself.
        username / password / company_db: SAP credentials. Same user as the
            Service Layer typically; the user needs the *Report Layout API*
            general authorization. ``company_db`` is what selects the tenant
            (test vs production) — set it deliberately, never from a caller
            supplied value.
        ssl_verify: TLS certificate verification. Gateways often ship with a
            self-signed certificate; prefer installing the CA over disabling.
        connect_timeout / read_timeout: seconds. PDF rendering can be slow,
            hence the generous read default.
        session_ttl: Enables *proactive* re-login this long after each login
            (minus ``session_refresh_margin``). ``None`` (default) means
            reactive only: the gateway's ``SessionTimeout: 30`` is not
            minutes (a session outlived 40 min live) and its real unit is
            unknown, so the client re-logs in when the gateway answers
            ``401`` instead of guessing.
        session_refresh_margin: How long before the ``session_ttl`` expiry
            the client proactively re-logs in (capped at a quarter of it).
        max_concurrent_exports: Upper bound on parallel ``ExportPDFData``
            calls per client. Measured live: with five parallel exports on
            one session the gateway dropped 1–3 of them (``(---)``); rounds
            of three were clean. ``None``/``0`` disables the bound.
    """

    base_url: str
    username: str
    # repr=False keeps the live password out of repr()/tracebacks/APM captures.
    password: str = field(repr=False)
    company_db: str
    ssl_verify: bool = True
    connect_timeout: float = 10.0
    read_timeout: float = 120.0
    session_ttl: timedelta | None = None
    session_refresh_margin: timedelta = field(
        default_factory=lambda: timedelta(seconds=60)
    )
    max_concurrent_exports: int | None = 3

    def __post_init__(self) -> None:
        if not self.base_url:
            raise ValueError("APIGatewayConfig.base_url cannot be empty")
        if not self.username or not self.password:
            raise ValueError(
                "APIGatewayConfig credentials (username/password) cannot be empty"
            )
        if not self.company_db:
            raise ValueError("APIGatewayConfig.company_db cannot be empty")
        self.base_url = self.base_url.rstrip("/")

    @classmethod
    def from_env(cls, strict: bool = True) -> APIGatewayConfig:
        """Load from environment variables.

        Reads ``B1SL_GATEWAY_BASE_URL`` (required — the gateway has its own
        host:port) plus ``B1SL_GATEWAY_USERNAME`` / ``B1SL_GATEWAY_PASSWORD``
        / ``B1SL_GATEWAY_COMPANY_DB`` / ``B1SL_GATEWAY_SSL_VERIFY``, each
        falling back to the Service Layer's ``B1SL_*`` counterpart so a
        deployment that already configures ``b1sl`` only needs the URL.

        Args:
            strict: When ``True`` (default) raise ``EnvironmentError`` if
                anything required is missing. ``strict=False`` fills dummy
                values — for unit tests only.
        """

        def pick(gw_key: str, sl_key: str) -> str | None:
            return os.environ.get(gw_key) or os.environ.get(sl_key)

        base_url = os.environ.get("B1SL_GATEWAY_BASE_URL")
        username = pick("B1SL_GATEWAY_USERNAME", "B1SL_USERNAME")
        password = pick("B1SL_GATEWAY_PASSWORD", "B1SL_PASSWORD")
        company_db = pick("B1SL_GATEWAY_COMPANY_DB", "B1SL_COMPANY_DB")

        missing = [
            key
            for key, val in (
                ("B1SL_GATEWAY_BASE_URL", base_url),
                ("B1SL_GATEWAY_USERNAME|B1SL_USERNAME", username),
                ("B1SL_GATEWAY_PASSWORD|B1SL_PASSWORD", password),
                ("B1SL_GATEWAY_COMPANY_DB|B1SL_COMPANY_DB", company_db),
            )
            if not val
        ]
        if missing and strict:
            raise EnvironmentError(
                f"Missing required SAP B1 API Gateway config env vars: {missing}"
            )

        ssl_default = _env_bool("B1SL_SSL_VERIFY", True)
        ttl_raw = os.environ.get("B1SL_GATEWAY_SESSION_TTL")
        return cls(
            base_url=base_url or "https://dummy:60000",
            username=username or "dummy",
            password=password or "dummy",
            company_db=company_db or "SBODemoMX",
            ssl_verify=_env_bool("B1SL_GATEWAY_SSL_VERIFY", ssl_default),
            connect_timeout=float(os.environ.get("B1SL_GATEWAY_CONNECT_TIMEOUT", "10")),
            read_timeout=float(os.environ.get("B1SL_GATEWAY_READ_TIMEOUT", "120")),
            session_ttl=timedelta(seconds=int(ttl_raw)) if ttl_raw else None,
            max_concurrent_exports=int(
                os.environ.get("B1SL_GATEWAY_MAX_CONCURRENT_EXPORTS", "3")
            )
            or None,
        )

    @classmethod
    def from_b1_config(
        cls, config: B1Config, base_url: str, **overrides: Any
    ) -> APIGatewayConfig:
        """Derive gateway settings from an existing Service Layer ``B1Config``.

        Reuses ``username`` / ``password`` / ``company_db`` / ``ssl_verify`` /
        timeouts; only the gateway ``base_url`` is new. Any keyword override
        wins (e.g. ``ssl_verify=True``).
        """
        cfg = cls(
            base_url=base_url,
            username=config.username,
            password=config.password,
            company_db=config.company_db,
            ssl_verify=config.ssl_verify,
            connect_timeout=config.connect_timeout,
            read_timeout=max(config.read_timeout, 120.0),
        )
        return replace(cfg, **overrides) if overrides else cfg

    @classmethod
    def from_django_settings(cls) -> APIGatewayConfig:
        """Load from ``django.conf.settings`` (``B1SL_GATEWAY_*`` names).

        Mirrors ``B1Config.from_django_settings``: ``B1SL_GATEWAY_BASE_URL``
        is required; credentials, ``COMPANY_DB`` and ``SSL_VERIFY`` fall back
        to the Service Layer's ``B1SL_*`` settings so a Django project that
        already configures ``b1sl`` only adds the gateway URL.
        """
        from django.conf import settings

        def pick(gw_key: str, sl_key: str, default: Any = "") -> Any:
            return getattr(settings, gw_key, None) or getattr(settings, sl_key, default)

        ttl = getattr(settings, "B1SL_GATEWAY_SESSION_TTL", None)
        return cls(
            base_url=getattr(settings, "B1SL_GATEWAY_BASE_URL", ""),
            username=pick("B1SL_GATEWAY_USERNAME", "B1SL_USERNAME"),
            password=pick("B1SL_GATEWAY_PASSWORD", "B1SL_PASSWORD"),
            company_db=pick("B1SL_GATEWAY_COMPANY_DB", "B1SL_COMPANY_DB"),
            ssl_verify=bool(pick("B1SL_GATEWAY_SSL_VERIFY", "B1SL_SSL_VERIFY", True)),
            connect_timeout=float(
                getattr(settings, "B1SL_GATEWAY_CONNECT_TIMEOUT", 10)
            ),
            read_timeout=float(getattr(settings, "B1SL_GATEWAY_READ_TIMEOUT", 120)),
            session_ttl=timedelta(seconds=int(ttl)) if ttl else None,
            max_concurrent_exports=int(
                getattr(settings, "B1SL_GATEWAY_MAX_CONCURRENT_EXPORTS", 3)
            )
            or None,
        )
