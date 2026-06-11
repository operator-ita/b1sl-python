"""
Sync $batch support (SyncBatchClient) and Dry Run interception for $batch.

Covers the P0 fixes:
- B1Client.batch() returns a working SyncBatchClient (recording + execute).
- batch.execute() honours dry_run() on both sync and async clients.
"""
from datetime import datetime, timedelta

import pytest
import respx
from httpx import Response

from b1sl.b1sl import AsyncB1Client, B1Client, B1Config
from b1sl.b1sl import entities as en
from b1sl.b1sl.batch.client import BatchClient, SyncBatchClient

BASE = "https://sap-host:50000"


@pytest.fixture
def config():
    return B1Config(
        base_url=BASE,
        username="manager",
        password="sap",
        company_db="SBODEMO",
    )


@pytest.fixture
def client(config):
    c = B1Client(config)
    # Pretend we already hold a valid session so execute() skips Login.
    c._adapter.is_session_active = True
    c._adapter.token_expiry = datetime.now() + timedelta(hours=1)
    return c


# ── Recording ────────────────────────────────────────────────────────────────

def test_sync_batch_records_operations(client):
    batch = client.batch()
    assert isinstance(batch, SyncBatchClient)

    batch.items.get("A1")
    batch.items.update("A1", en.Item(item_name="Renamed"))
    batch.items.delete("A1")

    assert len(batch._pending) == 3
    assert [r.method for r in batch._pending] == ["GET", "PATCH", "DELETE"]
    assert "Items('A1')" in batch._pending[0].endpoint
    # The recorded op must remember its model for response parsing
    assert batch._pending[0].model_type is not None


def test_sync_batch_records_fluent_chain(client):
    batch = client.batch()
    batch.items.top(1).execute()

    assert len(batch._pending) == 1
    assert batch._pending[0].method == "GET"


def test_sync_batch_changeset_grouping(client):
    batch = client.batch()
    with batch.changeset() as cs:
        cs.items.create(en.Item(item_code="NEW"))
        cs.items.update("A1", en.Item(item_name="Updated"))

    assert len(batch._pending) == 2
    cs_id = batch._pending[0].changeset_id
    assert cs_id is not None
    assert batch._pending[1].changeset_id == cs_id
    assert batch.active_changeset_id is None  # reset after exit


def test_sync_get_in_changeset_raises(client):
    batch = client.batch()
    with batch.changeset():
        with pytest.raises(ValueError, match="GET operations are not allowed"):
            batch.items.get("A1")


# ── Execution ────────────────────────────────────────────────────────────────

@respx.mock
def test_sync_batch_execute_round_trip(client):
    batch_response = (
        "--batch_resp\r\n"
        "Content-Type: application/http\r\n\r\n"
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n\r\n"
        '{"ItemCode": "B1"}\r\n'
        "--batch_resp--"
    )
    route = respx.post(f"{BASE}/b1s/v2/$batch").mock(
        return_value=Response(
            200,
            content=batch_response,
            headers={"Content-Type": "multipart/mixed; boundary=batch_resp"},
        )
    )

    with client.batch() as batch:
        batch.items.get("B1")
        results = batch.execute()

    assert route.called
    assert results.all_ok
    assert results[0].data["ItemCode"] == "B1"
    # The request body must be the serialized multipart we recorded
    sent_body = route.calls.last.request.content.decode()
    assert "GET" in sent_body and "Items('B1')" in sent_body


@respx.mock
def test_sync_batch_empty_execute_sends_nothing(client):
    # No routes mocked: any HTTP call would fail loudly.
    with client.batch() as batch:
        results = batch.execute()
    assert len(results) == 0
    assert results.all_ok


# ── Dry Run interception ─────────────────────────────────────────────────────

@respx.mock
def test_sync_batch_dry_run_intercepts_writes(client):
    """Under dry_run(), execute() must synthesize 204s and never touch SAP."""
    batch = client.batch()
    batch.items.update("A1", en.Item(item_name="X"))
    batch.items.delete("A1")

    with client.dry_run():
        results = batch.execute()

    # No respx route was defined for $batch: reaching SAP would have raised.
    assert len(results) == 2
    assert results.all_ok
    assert all(r.status == 204 for r in results)
    # Index traceability is preserved even in dry run
    assert [r.index for r in results] == [0, 1]


@pytest.mark.asyncio
@respx.mock
async def test_async_batch_dry_run_intercepts_writes(config):
    b1 = AsyncB1Client(config)
    batch = b1.batch()
    assert isinstance(batch, BatchClient)

    await batch.items.update("A1", en.Item(item_name="X"))

    with b1.dry_run():
        results = await batch.execute()

    assert len(results) == 1
    assert results[0].status == 204
