"""Custom request headers on CRUD + the replace_collections flag.

Covers the public escape hatch for raw requests that previously required
touching ``client._adapter`` directly: ``headers=`` passthrough on
get/create/update/delete, and ``update(..., replace_collections=True)`` which
sends B1S-ReplaceCollectionsOnPatch so SAP replaces child collections (e.g.
BPAddresses) instead of merging them element-by-index.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest
from pydantic import Field as PydanticField

from b1sl.b1sl import B1Config
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, merge_update_headers
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter

REPLACE_HEADER = "B1S-ReplaceCollectionsOnPatch"


class _Partner(B1Model):
    card_name: str | None = PydanticField(None, alias="CardName")


class _Partners(GenericResource[_Partner]):
    endpoint = "BusinessPartners"
    model = _Partner


class _AsyncPartners(AsyncGenericResource[_Partner]):
    endpoint = "BusinessPartners"
    model = _Partner


@pytest.fixture
def fake():
    return FakeRestAdapter()


@pytest.fixture
def afake():
    return FakeAsyncRestAdapter()


# ── merge_update_headers ─────────────────────────────────────────────────────

def test_merge_headers_noop_without_flag():
    assert merge_update_headers(None, False) is None
    caller = {"Prefer": "return=minimal"}
    assert merge_update_headers(caller, False) is caller


def test_merge_headers_adds_replace_collections():
    assert merge_update_headers(None, True) == {REPLACE_HEADER: "true"}
    merged = merge_update_headers({"Prefer": "x"}, True)
    assert merged == {"Prefer": "x", REPLACE_HEADER: "true"}


def test_merge_headers_explicit_caller_value_wins():
    merged = merge_update_headers({REPLACE_HEADER: "false"}, True)
    assert merged == {REPLACE_HEADER: "false"}


def test_merge_headers_does_not_mutate_caller_dict():
    caller: dict = {}
    merge_update_headers(caller, True)
    assert caller == {}


# ── Sync CRUD passthrough ────────────────────────────────────────────────────

def test_update_passes_custom_headers(fake):
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    _Partners(fake).update("C001", _Partner(card_name="ACME"), headers={"Prefer": "x"})
    call = fake.calls[-1]
    assert call["method"] == "PATCH"
    assert call["headers"] == {"Prefer": "x"}


def test_update_replace_collections_sets_header(fake):
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    _Partners(fake).update("C001", _Partner(card_name="ACME"), replace_collections=True)
    assert fake.calls[-1]["headers"] == {REPLACE_HEADER: "true"}


def test_update_without_headers_sends_none(fake):
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    _Partners(fake).update("C001", _Partner(card_name="ACME"))
    assert fake.calls[-1]["headers"] is None


def test_get_create_delete_pass_headers(fake):
    fake.register("GET", "BusinessPartners('C001')", response_data={"CardName": "A"})
    fake.register("POST", "BusinessPartners", response_data={"CardName": "A"})
    fake.register("DELETE", "BusinessPartners('C001')", status=204)

    res = _Partners(fake)
    res.get("C001", headers={"H": "1"})
    res.create(_Partner(card_name="A"), headers={"H": "2"})
    res.delete("C001", headers={"H": "3"})

    assert [c["headers"] for c in fake.calls] == [{"H": "1"}, {"H": "2"}, {"H": "3"}]


# ── Verbatim dict payloads ───────────────────────────────────────────────────

def test_update_dict_is_sent_verbatim(fake):
    """A dict payload bypasses to_api_payload entirely: SAP aliases, SAP
    encodings and unknown keys travel untouched."""
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    payload = {
        "CardName": "ACME",              # SAP alias, not python name
        "Frozen": "tYES",                # already SAP-encoded — must NOT re-encode
        "CampoNoModelado": 42,           # unknown key — must survive
        "BPAddresses": [{"BPCode": "C001", "RowNum": 2, "City": "Monterrey"}],
    }
    _Partners(fake).update("C001", payload)
    assert fake.calls[-1]["data"] == payload


def test_update_dict_composes_with_replace_collections(fake):
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    _Partners(fake).update(
        "C001", {"BPAddresses": []}, replace_collections=True
    )
    call = fake.calls[-1]
    assert call["data"] == {"BPAddresses": []}
    assert call["headers"] == {REPLACE_HEADER: "true"}


def test_update_model_still_uses_surgical_delta(fake):
    """The typed path keeps exclude_unset semantics (regression guard)."""
    fake.register("PATCH", "BusinessPartners('C001')", status=204)
    _Partners(fake).update("C001", _Partner(card_name="ACME"))
    assert fake.calls[-1]["data"] == {"CardName": "ACME"}


@pytest.mark.asyncio
async def test_async_update_dict_is_sent_verbatim(afake):
    afake.register("PATCH", "BusinessPartners('C001')", status=204)
    payload = {"Frozen": "tNO", "Extra": "x"}
    await _AsyncPartners(afake).update("C001", payload)
    assert afake.calls[-1]["data"] == payload


# ── Async parity ─────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_update_replace_collections_sets_header(afake):
    afake.register("PATCH", "BusinessPartners('C001')", status=204)
    await _AsyncPartners(afake).update(
        "C001", _Partner(card_name="ACME"), replace_collections=True
    )
    assert afake.calls[-1]["headers"] == {REPLACE_HEADER: "true"}


@pytest.mark.asyncio
async def test_async_crud_pass_headers(afake):
    afake.register("GET", "BusinessPartners('C001')", response_data={"CardName": "A"})
    afake.register("POST", "BusinessPartners", response_data={"CardName": "A"})
    afake.register("PATCH", "BusinessPartners('C001')", status=204)
    afake.register("DELETE", "BusinessPartners('C001')", status=204)

    res = _AsyncPartners(afake)
    await res.get("C001", headers={"H": "1"})
    await res.create(_Partner(card_name="A"), headers={"H": "2"})
    await res.update("C001", _Partner(card_name="A"), headers={"H": "3"})
    await res.delete("C001", headers={"H": "4"})

    assert [c["headers"] for c in afake.calls] == [
        {"H": "1"}, {"H": "2"}, {"H": "3"}, {"H": "4"}
    ]


# ── Batch recording + serialization ──────────────────────────────────────────

def test_batch_records_and_serializes_replace_collections_header():
    from b1sl.b1sl.batch.serializer import BatchSerializer

    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    client = B1Client(config)
    client._adapter.is_session_active = True
    client._adapter.token_expiry = datetime.now() + timedelta(hours=1)

    with client.batch() as batch:
        batch.business_partners.update(
            "C001", _Partner(card_name="ACME"), replace_collections=True
        )
        op = batch._pending[0]
        assert op.method == "PATCH"
        assert op.headers == {REPLACE_HEADER: "true"}

        body = BatchSerializer(list(batch._pending), "batch_test").serialize()
        assert f"{REPLACE_HEADER}: true" in body
