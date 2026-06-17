"""P2 audit-fix coverage: filtered count(), $skiptoken, key escaping,
nested payload encoding, semantic network/412 errors, env precedence,
MCP read-only toolset, and the lazy top-level package."""
from __future__ import annotations

import datetime

import httpx
import pytest
import respx
from httpx import Response

from b1sl.b1sl import entities as en
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.exceptions.exceptions import (
    B1ConnectionError,
    B1PaginationError,
    SAPConcurrencyError,
)
from b1sl.b1sl.pagination import build_next_params
from b1sl.b1sl.resources.base import format_entity_key
from b1sl.b1sl.rest_adapter import RestAdapter

BASE = "https://sap-host:50000"


@pytest.fixture
def config():
    return B1Config(
        base_url=BASE, username="manager", password="sap", company_db="SBODEMO"
    )


@pytest.fixture
def adapter(config):
    a = RestAdapter.from_config(config)
    a.is_session_active = True
    a.token_expiry = datetime.datetime.now() + datetime.timedelta(hours=1)
    return a


# ── QueryBuilder.count() honours $filter ─────────────────────────────────────

def test_query_builder_count_sends_filter():
    from b1sl.b1sl.resources.base import GenericResource
    from tests.fakes.fake_rest_adapter import FakeRestAdapter

    fake = FakeRestAdapter()
    fake.register("GET", "Items/$count", response_data="42")

    class ItemsResource(GenericResource):
        endpoint = "Items"
        model = en.Item

    count = ItemsResource(fake).filter("Frozen eq 'tNO'").count()

    assert count == 42
    assert fake.calls[-1]["params"] == {"$filter": "Frozen eq 'tNO'"}


@pytest.mark.asyncio
async def test_async_query_builder_count_sends_filter():
    from typing import Any, cast

    from b1sl.b1sl.resources.async_base import AsyncGenericResource
    from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter

    fake = FakeAsyncRestAdapter()
    fake.register("GET", "Items/$count", response_data="7")

    class ItemsResource(AsyncGenericResource):
        endpoint = "Items"
        model = en.Item

    count = await ItemsResource(cast(Any, fake)).filter("Frozen eq 'tNO'").count()

    assert count == 7
    assert fake.calls[-1]["params"] == {"$filter": "Frozen eq 'tNO'"}


# ── Pagination: $skiptoken support + no-cursor loop guard ────────────────────

def test_build_next_params_carries_skiptoken():
    params = build_next_params(
        {"$filter": "Frozen eq 'tNO'"},
        "https://sap:50000/b1s/v2/Items?$skiptoken=abc123",
    )
    assert params["$skiptoken"] == "abc123"
    assert params["$filter"] == "Frozen eq 'tNO'"  # filters survive


def test_build_next_params_without_cursor_raises():
    """A nextLink with no $skip/$skiptoken would loop on the same page forever."""
    with pytest.raises(B1PaginationError, match="no recognised cursor"):
        build_next_params({}, "https://sap:50000/b1s/v2/Items?$top=20")


# ── Entity-key escaping ──────────────────────────────────────────────────────

def test_format_entity_key_escapes_quotes():
    assert format_entity_key("A001") == "'A001'"
    assert format_entity_key("O'Brien") == "'O''Brien'"
    assert format_entity_key("x') or true or ('") == "'x'') or true or ('''"
    assert format_entity_key(42) == "42"


def test_resource_get_uses_escaped_key():
    from b1sl.b1sl.resources.base import GenericResource
    from tests.fakes.fake_rest_adapter import FakeRestAdapter

    fake = FakeRestAdapter()
    fake.register("GET", "Items('O''Brien')", response_data={"ItemCode": "O'Brien"})

    class ItemsResource(GenericResource):
        endpoint = "Items"
        model = en.Item

    item = ItemsResource(fake).get("O'Brien")
    assert item.item_code == "O'Brien"


# ── Nested payload encoding (bools/dates inside DocumentLines) ───────────────

def test_to_api_payload_encodes_nested_collections():
    doc = en.Document(
        card_code="C001",
        document_lines=[
            en.DocumentLine(
                item_code="A001",
                quantity=1.0,
                tax_liable=en.BoYesNoEnum.tYES,
            )
        ],
    )
    payload = doc.to_api_payload()
    line = payload["DocumentLines"][0]
    assert line["TaxLiable"] == "tYES"


def test_encode_sap_value_recurses_all_shapes():
    from b1sl.b1sl.models.base import encode_sap_value

    nested = {
        "Lines": [
            {"Frozen": True, "Date": datetime.date(2026, 6, 15)},
            {"Frozen": False, "Tag": ("x", True)},
        ]
    }
    out = encode_sap_value(nested)
    assert out["Lines"][0] == {"Frozen": "tYES", "Date": "2026-06-15"}
    assert out["Lines"][1]["Frozen"] == "tNO"
    assert out["Lines"][1]["Tag"] == ["x", "tYES"]


def test_create_encodes_nested_bools(config):
    from b1sl.b1sl.resources.base import GenericResource
    from tests.fakes.fake_rest_adapter import FakeRestAdapter

    fake = FakeRestAdapter()
    fake.register("POST", "Orders", response_data={"CardCode": "C001"})

    class OrdersResource(GenericResource):
        endpoint = "Orders"
        model = en.Document

    doc = en.Document(
        card_code="C001",
        document_lines=[
            en.DocumentLine(item_code="A001", tax_liable=en.BoYesNoEnum.tNO)
        ],
    )
    OrdersResource(fake).create(doc)

    sent = fake.calls[-1]["data"]
    assert sent["DocumentLines"][0]["TaxLiable"] == "tNO"


# ── Semantic exceptions: network failure and bare 412 ────────────────────────

@respx.mock
def test_network_failure_raises_connection_error(adapter):
    respx.get(f"{BASE}/b1s/v2/Items").mock(side_effect=httpx.ConnectError("refused"))
    with pytest.raises(B1ConnectionError):
        adapter.get("/Items")


@respx.mock
def test_stale_keepalive_get_retries_then_succeeds(adapter):
    """A GET hitting a stale server-closed keepalive retries once transparently."""
    route = respx.get(f"{BASE}/b1s/v2/Items").mock(
        side_effect=[
            httpx.RemoteProtocolError("Server disconnected without sending a response."),
            Response(200, json={"value": []}),
        ]
    )
    result = adapter.get("/Items")
    assert result.status_code == 200
    assert route.call_count == 2  # original + one transparent retry


@respx.mock
def test_stale_keepalive_get_retry_exhausted_raises_connection_error(adapter):
    """If the retry also hits RemoteProtocolError, raise B1ConnectionError."""
    route = respx.get(f"{BASE}/b1s/v2/Items").mock(
        side_effect=httpx.RemoteProtocolError("Server disconnected without sending a response.")
    )
    with pytest.raises(B1ConnectionError):
        adapter.get("/Items")
    assert route.call_count == 2  # original + one retry, no more


@respx.mock
def test_stale_keepalive_patch_not_retried_raises_connection_error(adapter):
    """Non-idempotent writes are never auto-retried — caller decides."""
    route = respx.patch(f"{BASE}/b1s/v2/Items('A1')").mock(
        side_effect=httpx.RemoteProtocolError("Server disconnected without sending a response.")
    )
    with pytest.raises(B1ConnectionError):
        adapter.patch("Items('A1')", data={"ItemName": "x"})
    assert route.call_count == 1  # no retry on PATCH


@respx.mock
def test_412_without_sap_code_maps_to_concurrency_error(adapter):
    """412 must raise SAPConcurrencyError even when SAP omits code -2039."""
    respx.patch(f"{BASE}/b1s/v2/Items('A1')").mock(
        return_value=Response(412, json={"error": {"code": "999", "message": {"value": "Precondition failed"}}})
    )
    with pytest.raises(SAPConcurrencyError):
        adapter.patch("Items('A1')", data={"ItemName": "x"})


# ── B1Environment.load precedence: env vars > json defaults ─────────────────

def test_environment_load_reads_env_vars(monkeypatch, tmp_path):
    monkeypatch.setenv("B1SL_BASE_URL", "https://from-env:50000/b1s/v2")
    monkeypatch.setenv("B1SL_USERNAME", "env-user")
    monkeypatch.setenv("B1SL_PASSWORD", "env-pass")
    monkeypatch.setenv("B1SL_COMPANY_DB", "ENVDB")
    monkeypatch.setenv("B1SL_ENV", "dev")

    from b1sl.b1sl.config_manager import B1Environment

    env = B1Environment.load(configs_dir=str(tmp_path))
    assert env.config.base_url == "https://from-env:50000/b1s/v2"
    assert env.config.username == "env-user"
    assert env.test_data == {}  # no json profile in tmp dir


def test_environment_load_merges_json_test_data(monkeypatch, tmp_path):
    monkeypatch.setenv("B1SL_BASE_URL", "https://from-env:50000/b1s/v2")
    monkeypatch.setenv("B1SL_USERNAME", "env-user")
    monkeypatch.setenv("B1SL_PASSWORD", "env-pass")
    monkeypatch.setenv("B1SL_COMPANY_DB", "ENVDB")

    (tmp_path / "dev.json").write_text(
        '{"test_data": {"items": {"simple": "X-1"}}, '
        '"base_url": "https://json-should-NOT-win:50000"}'
    )

    from b1sl.b1sl.config_manager import B1Environment

    env = B1Environment.load(env_name="dev", configs_dir=str(tmp_path))
    # JSON provides test_data only; credentials/URL always come from env.
    assert env.test_data["items"]["simple"] == "X-1"
    assert env.config.base_url == "https://from-env:50000/b1s/v2"


def test_environment_load_strict_requires_credentials(monkeypatch, tmp_path):
    for var in ("B1SL_BASE_URL", "B1SL_USERNAME", "B1SL_PASSWORD", "B1SL_COMPANY_DB"):
        monkeypatch.delenv(var, raising=False)

    from b1sl.b1sl.config_manager import B1Environment

    with pytest.raises(EnvironmentError):
        B1Environment.load(configs_dir=str(tmp_path), strict=True)


# ── MCP: read-only toolset ───────────────────────────────────────────────────

def test_build_resource_toolset_read_only_omits_writes():
    from b1sl.contrib.mcp.odata_schemas import build_resource_toolset

    full = build_resource_toolset("orders", en.Document)
    ro = build_resource_toolset("orders", en.Document, read_only=True)

    assert len(full) == 5
    assert len(ro) == 2
    ro_names = {t["name"] for t in ro}
    assert not any(("create" in n or "patch" in n or "delete" in n) for n in ro_names)


# ── Top-level package: lazy re-exports ───────────────────────────────────────

def test_top_level_package_forwards_public_surface():
    import b1sl

    assert b1sl.B1Client.__name__ == "B1Client"
    assert b1sl.AsyncB1Client.__name__ == "AsyncB1Client"
    assert b1sl.entities.Item is en.Item

    with pytest.raises(AttributeError):
        b1sl.does_not_exist
