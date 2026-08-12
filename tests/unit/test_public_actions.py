"""Public action/function/service-method escape hatches.

Covers the promotion of `_action`/`_function` to public API (`action()`,
`function()`), the new `B1Client.call_service_method()` /
`AsyncB1Client.call_service_method()` root-level entry point, and the public
`base_url` property — so external callers never need to touch `_adapter` or
underscore methods.
"""
from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from b1sl.b1sl import B1Config
from b1sl.b1sl.async_client import AsyncB1Client
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter


class _Invoices(GenericResource[B1Model]):
    endpoint = "Invoices"
    model = B1Model


class _AsyncInvoices(AsyncGenericResource[B1Model]):
    endpoint = "Invoices"
    model = B1Model


@pytest.fixture
def fake():
    return FakeRestAdapter()


@pytest.fixture
def afake():
    return FakeAsyncRestAdapter()


# ── Bound action() / function() — sync ───────────────────────────────────────

def test_action_posts_to_keyed_endpoint(fake):
    fake.register("POST", "Invoices(123)/Cancel", response_data={"DocEntry": 456})
    data = _Invoices(fake).action(123, "Cancel")
    assert data == {"DocEntry": 456}
    call = fake.calls[-1]
    assert call["method"] == "POST"
    assert call["endpoint"] == "Invoices(123)/Cancel"
    assert call["data"] == {}


def test_action_with_payload_and_string_key(fake):
    fake.register("POST", "Invoices('A-1')/Close", response_data=None, status=204)
    _Invoices(fake).action("A-1", "Close", {"Remarks": "done"})
    assert fake.calls[-1]["data"] == {"Remarks": "done"}


def test_action_get_method_for_bounded_function(fake):
    fake.register("GET", "Invoices(1)/List", response_data={"value": []})
    data = _Invoices(fake).action(1, "List", method="GET", params={"$top": "1"})
    assert data == {"value": []}
    call = fake.calls[-1]
    assert call["method"] == "GET"
    assert call["params"] == {"$top": "1"}


def test_function_gets_unkeyed_endpoint(fake):
    fake.register("GET", "Invoices/GetTotals", response_data={"Total": 10})
    data = _Invoices(fake).function("GetTotals", {"Year": 2026})
    assert data == {"Total": 10}
    call = fake.calls[-1]
    assert call["method"] == "GET"
    assert call["endpoint"] == "Invoices/GetTotals"
    assert call["params"] == {"Year": 2026}


def test_underscore_aliases_are_backwards_compatible():
    assert GenericResource._action is GenericResource.action
    assert GenericResource._function is GenericResource.function
    assert AsyncGenericResource._action is AsyncGenericResource.action
    assert AsyncGenericResource._function is AsyncGenericResource.function


# ── Bound action() / function() — async parity ───────────────────────────────

@pytest.mark.asyncio
async def test_async_action_posts_to_keyed_endpoint(afake):
    afake.register("POST", "Invoices(123)/Cancel", response_data={"DocEntry": 456})
    data = await _AsyncInvoices(afake).action(123, "Cancel")
    assert data == {"DocEntry": 456}
    assert afake.calls[-1]["endpoint"] == "Invoices(123)/Cancel"


@pytest.mark.asyncio
async def test_async_function_gets_unkeyed_endpoint(afake):
    afake.register("GET", "Invoices/GetTotals", response_data={"Total": 10})
    data = await _AsyncInvoices(afake).function("GetTotals")
    assert data == {"Total": 10}


# ── call_service_method() — unbound root operations ──────────────────────────

def test_call_service_method_posts_to_root(fake):
    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    client = B1Client(config, adapter=fake)
    fake.register(
        "POST", "SBOBobService_GetCurrencyRate", response_data={"Rate": 17.05}
    )
    data = client.call_service_method(
        "SBOBobService_GetCurrencyRate", {"Currency": "USD", "Date": "20260811"}
    )
    assert data == {"Rate": 17.05}
    call = fake.calls[-1]
    assert call["method"] == "POST"
    assert call["endpoint"] == "SBOBobService_GetCurrencyRate"
    assert call["data"] == {"Currency": "USD", "Date": "20260811"}


def test_call_service_method_defaults_to_empty_payload(fake):
    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    client = B1Client(config, adapter=fake)
    fake.register("POST", "SBOBobService_GetLocalCurrency", response_data="MXN")
    assert client.call_service_method("SBOBobService_GetLocalCurrency") == "MXN"
    assert fake.calls[-1]["data"] == {}


@pytest.mark.asyncio
async def test_async_call_service_method_posts_to_root():
    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    afake = FakeAsyncRestAdapter()
    client = AsyncB1Client(config, adapter=afake)  # type: ignore[arg-type]
    afake.register(
        "POST", "SBOBobService_SetCurrencyRate", response_data=None, status=204
    )
    payload = {"Currency": "EUR", "Rate": "4.8", "RateDate": "20260811"}
    await client.call_service_method("SBOBobService_SetCurrencyRate", payload)
    assert afake.calls[-1]["endpoint"] == "SBOBobService_SetCurrencyRate"
    assert afake.calls[-1]["data"] == payload


# ── base_url property ────────────────────────────────────────────────────────

def test_client_base_url_exposes_adapter_url(fake):
    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    client = B1Client(config, adapter=fake)
    assert client.base_url == "https://fake-sap:50000/b1s/v2"


def test_real_adapter_base_url_is_normalized():
    config = B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    client = B1Client(config)
    assert client.base_url == "https://sap-host:50000/b1s/v2"


# ── Batch recording of public action() ───────────────────────────────────────

def test_batch_records_bound_action():
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
        batch.orders.action(123, "Cancel")
        assert len(batch._pending) == 1
        op = batch._pending[0]
        assert op.method == "POST"
        assert op.endpoint == "Orders(123)/Cancel"
