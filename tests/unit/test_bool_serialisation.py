"""
tests/unit/test_bool_serialisation.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Verify that Python booleans are correctly encoded to SAP tYES / tNO sentinels
in both the synchronous and asynchronous resource paths.

Two scenarios are tested for each client type:
  - update (PATCH):  uses to_api_payload() / exclude_unset  → delta only
  - create (POST):   uses model_dump(exclude_none) + re-encode → full payload

The FakeRestAdapter and FakeAsyncRestAdapter capture the payload that would be
sent over the wire so we can assert on the serialised form without an actual SAP
server.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from b1sl.b1sl import B1Client, B1Config
from b1sl.b1sl.models._generated.entities import (
    Item,  # uses __init__ so forward refs resolve
)
from b1sl.b1sl.models._generated.entities.businesspartners import BusinessPartner as BP
from tests.fakes.fake_rest_adapter import FakeRestAdapter

# ─────────────────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def fake_adapter() -> FakeRestAdapter:
    return FakeRestAdapter()


@pytest.fixture
def sync_client(fake_adapter: FakeRestAdapter) -> B1Client:
    config = B1Config(
        base_url="https://sap.example.com/b1s/v2",
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )
    return B1Client(config=config, adapter=fake_adapter)


# ─────────────────────────────────────────────────────────────────────────────
# Sync: update (PATCH) — to_api_payload(), exclude_unset
# ─────────────────────────────────────────────────────────────────────────────


def test_sync_update_encodes_bool_true_as_tYES(
    sync_client: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """PATCH with frozen=True must send 'Frozen': 'tYES' (not Python bool)."""
    fake_adapter.register("PATCH", "BusinessPartners('C0001')", response_data=None, status=204)

    sync_client.business_partners.update("C0001", BP(frozen=True))

    sent_data = fake_adapter.calls[0]["data"]
    assert sent_data == {"Frozen": "tYES"}, (
        f"Expected {{'Frozen': 'tYES'}}, got {sent_data}"
    )


def test_sync_update_encodes_bool_false_as_tNO(
    sync_client: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """PATCH with frozen=False must send 'Frozen': 'tNO'."""
    fake_adapter.register("PATCH", "BusinessPartners('C0001')", response_data=None, status=204)

    sync_client.business_partners.update("C0001", BP(frozen=False))

    sent_data = fake_adapter.calls[0]["data"]
    assert sent_data == {"Frozen": "tNO"}


def test_sync_update_sends_only_set_fields(
    sync_client: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """PATCH must send only explicitly set fields (exclude_unset semantics)."""
    fake_adapter.register("PATCH", "BusinessPartners('C0001')", response_data=None, status=204)

    sync_client.business_partners.update("C0001", BP(frozen=True))

    sent_data = fake_adapter.calls[0]["data"]
    # Only 'Frozen' was set; CardCode, CardName, etc. must NOT appear
    assert list(sent_data.keys()) == ["Frozen"]


# ─────────────────────────────────────────────────────────────────────────────
# Sync: create (POST) — model_dump(exclude_none) + re-encode
# ─────────────────────────────────────────────────────────────────────────────


def test_sync_create_encodes_bool_true_as_tYES(
    sync_client: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """POST must encode Python True as 'tYES' in the SAP payload."""
    returned_item = {"ItemCode": "NEW-001", "ItemName": "Widget", "Frozen": "tYES"}
    fake_adapter.register("POST", "Items", response_data=returned_item)

    created = sync_client.items.create(Item(item_code="NEW-001", item_name="Widget", frozen=True))

    sent_data = fake_adapter.calls[0]["data"]
    assert sent_data.get("Frozen") == "tYES"
    # Also verify the returned model is correctly parsed (tYES → True)
    assert created.frozen is True


def test_sync_create_does_not_send_none_fields(
    sync_client: B1Client, fake_adapter: FakeRestAdapter
) -> None:
    """POST must not include fields whose value is None (exclude_none semantics)."""
    returned_item = {"ItemCode": "NEW-001", "ItemName": "Widget"}
    fake_adapter.register("POST", "Items", response_data=returned_item)

    sync_client.items.create(Item(item_code="NEW-001", item_name="Widget"))

    sent_data = fake_adapter.calls[0]["data"]
    # Fields like Frozen, QuantityOnStock, etc. should not appear
    none_keys = [k for k, v in sent_data.items() if v is None]
    assert none_keys == [], f"None-valued keys must not be sent: {none_keys}"


# ─────────────────────────────────────────────────────────────────────────────
# Async: update (PATCH) — to_api_payload(), exclude_unset
# ─────────────────────────────────────────────────────────────────────────────


class FakeAsyncRestAdapter:
    """Minimal async adapter that captures calls without network I/O."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def _record(self, method: str, endpoint: str, data: Any = None) -> MagicMock:
        self.calls.append({"method": method, "endpoint": endpoint, "data": data})
        mock = MagicMock()
        mock.data = {}
        mock.status_code = 204
        return mock

    async def get(self, endpoint: str, ep_params: dict | None = None, data: dict | None = None):
        return self._record("GET", endpoint, data)

    async def post(self, endpoint: str, ep_params: dict | None = None, data: dict | None = None):
        return self._record("POST", endpoint, data)

    async def patch(self, endpoint: str, ep_params: dict | None = None, data: dict | None = None):
        return self._record("PATCH", endpoint, data)

    async def delete(self, endpoint: str, ep_params: dict | None = None, data: dict | None = None):
        return self._record("DELETE", endpoint, data)

    def _clear_etag(self, *args, **kwargs):
        """Mock ETag invalidation."""
        pass



def _make_async_resource(fake_async_adapter: FakeAsyncRestAdapter):
    """Build an AsyncGenericResource[BusinessPartner] backed by the fake adapter."""
    from b1sl.b1sl.resources.async_base import AsyncGenericResource

    class BPResource(AsyncGenericResource):
        endpoint = "BusinessPartners"
        model = BP

    return BPResource(fake_async_adapter)  # type: ignore[arg-type]


def _make_async_item_resource(fake_async_adapter: FakeAsyncRestAdapter):
    """Build an AsyncGenericResource[Item] backed by the fake adapter."""
    from b1sl.b1sl.resources.async_base import AsyncGenericResource

    class ItemResource(AsyncGenericResource):
        endpoint = "Items"
        model = Item

    return ItemResource(fake_async_adapter)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_async_update_encodes_bool_true_as_tYES() -> None:
    """Async PATCH with frozen=True must send 'Frozen': 'tYES'."""
    adapter = FakeAsyncRestAdapter()
    resource = _make_async_resource(adapter)

    await resource.update("C0001", BP(frozen=True))

    sent_data = adapter.calls[0]["data"]
    assert sent_data == {"Frozen": "tYES"}


@pytest.mark.asyncio
async def test_async_update_encodes_bool_false_as_tNO() -> None:
    """Async PATCH with frozen=False must send 'Frozen': 'tNO'."""
    adapter = FakeAsyncRestAdapter()
    resource = _make_async_resource(adapter)

    await resource.update("C0001", BP(frozen=False))

    sent_data = adapter.calls[0]["data"]
    assert sent_data == {"Frozen": "tNO"}


@pytest.mark.asyncio
async def test_async_update_sends_only_set_fields() -> None:
    """Async PATCH must be a delta: only fields explicitly set are sent."""
    adapter = FakeAsyncRestAdapter()
    resource = _make_async_resource(adapter)

    await resource.update("C0001", BP(frozen=True))

    sent_data = adapter.calls[0]["data"]
    assert list(sent_data.keys()) == ["Frozen"]


# ─────────────────────────────────────────────────────────────────────────────
# Async: create (POST) — model_dump(exclude_none) + re-encode
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_async_create_encodes_bool_true_as_tYES() -> None:
    """Async POST must encode Python True as 'tYES'."""
    adapter = FakeAsyncRestAdapter()
    # Override post to return a parseable response
    async def fake_post(endpoint, ep_params=None, data=None):
        adapter.calls.append({"method": "POST", "endpoint": endpoint, "data": data})
        mock = MagicMock()
        mock.data = {"ItemCode": "NEW-001", "Frozen": "tYES"}
        return mock
    adapter.post = fake_post  # type: ignore[method-assign]

    resource = _make_async_item_resource(adapter)
    await resource.create(Item(item_code="NEW-001", frozen=True))

    sent_data = adapter.calls[0]["data"]
    assert sent_data.get("Frozen") == "tYES"


@pytest.mark.asyncio
async def test_async_create_does_not_send_none_fields() -> None:
    """Async POST must not include None-valued fields."""
    adapter = FakeAsyncRestAdapter()
    async def fake_post(endpoint, ep_params=None, data=None):
        adapter.calls.append({"method": "POST", "endpoint": endpoint, "data": data})
        mock = MagicMock()
        mock.data = {"ItemCode": "NEW-001", "ItemName": "Widget"}
        return mock
    adapter.post = fake_post  # type: ignore[method-assign]

    resource = _make_async_item_resource(adapter)
    await resource.create(Item(item_code="NEW-001", item_name="Widget"))

    sent_data = adapter.calls[0]["data"]
    none_keys = [k for k, v in sent_data.items() if v is None]
    assert none_keys == [], f"None-valued keys must not be sent: {none_keys}"


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────


def _build_result(data: dict, method: str, endpoint: str, body: Any = None) -> MagicMock:
    """Build a MagicMock result, recording the call on the adapter's call list."""
    mock = MagicMock()
    mock.data = data
    mock.status_code = 201
    return mock
