"""P3 audit-fix coverage: token_timeout fallback wiring and hydrated-cookie
host scoping."""
from __future__ import annotations

import datetime

import pytest
import respx
from httpx import Response

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter

BASE = "https://sap-host:50000"


# ── token_timeout: fallback when Login omits SessionTimeout ─────────────────

@respx.mock
def test_login_uses_token_timeout_when_session_timeout_missing():
    config = B1Config(
        base_url=BASE,
        username="manager",
        password="sap",
        company_db="SBODEMO",
        token_timeout=datetime.timedelta(seconds=600),  # 10 min
    )
    respx.post(f"{BASE}/b1s/v2/Login").mock(
        return_value=Response(200, json={"SessionId": "abc"})  # no SessionTimeout
    )

    adapter = RestAdapter.from_config(config)
    adapter._login()

    # expiry = now + (10 - 2) min; assert it landed inside that window
    remaining = adapter.token_expiry - datetime.datetime.now()
    assert datetime.timedelta(minutes=7) < remaining <= datetime.timedelta(minutes=8)


@respx.mock
def test_login_prefers_sap_session_timeout_over_config():
    config = B1Config(
        base_url=BASE,
        username="manager",
        password="sap",
        company_db="SBODEMO",
        token_timeout=datetime.timedelta(seconds=600),
    )
    respx.post(f"{BASE}/b1s/v2/Login").mock(
        return_value=Response(200, json={"SessionId": "abc", "SessionTimeout": 30})
    )

    adapter = RestAdapter.from_config(config)
    adapter._login()

    remaining = adapter.token_expiry - datetime.datetime.now()
    assert datetime.timedelta(minutes=27) < remaining <= datetime.timedelta(minutes=28)


# ── Hydrated B1SESSION cookie is scoped to the SAP host ─────────────────────

def _hydrated_cookie(adapter):
    jar = adapter.session.cookies.jar
    return next(c for c in jar if c.name == "B1SESSION")


def test_sync_hydrated_cookie_is_host_scoped():
    config = B1Config(
        base_url=BASE, username="manager", password="sap", company_db="SBODEMO"
    )
    adapter = RestAdapter(config=config, session_id="sess-123")

    cookie = _hydrated_cookie(adapter)
    assert cookie.domain == "sap-host"
    assert adapter.session_id == "sess-123"
    assert adapter.is_session_active is True


@pytest.mark.asyncio
async def test_async_hydrated_cookie_is_host_scoped(monkeypatch):
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter

    config = B1Config(
        base_url=BASE, username="manager", password="sap", company_db="SBODEMO"
    )
    adapter = AsyncRestAdapter(config=config, session_id="sess-456")

    async def no_op(*args, **kwargs):
        return None

    # connect() hydrates the cookie, then would hit the network via
    # ensure_session — stub that out.
    monkeypatch.setattr(adapter, "ensure_session", no_op)
    await adapter.connect()

    assert adapter._client is not None
    jar = adapter._client.cookies.jar
    cookie = next(c for c in jar if c.name == "B1SESSION")
    assert cookie.domain == "sap-host"
    assert adapter.is_session_active is True
    await adapter._client.aclose()
