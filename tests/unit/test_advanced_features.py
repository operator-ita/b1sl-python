import httpx
import pytest
import respx

from b1sl.b1sl.async_client import AsyncB1Client
from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.exceptions.exceptions import SAPConcurrencyError


@pytest.fixture
def b1_config():
    return B1Config(
        base_url="https://sap:50000/b1s/v1",
        username="manager",
        password="password",
        company_db="SBODemoES",
    )

# ------------------------------------------------------------------------------
# ETAG & CONCURRENCY TESTS
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
@respx.mock
async def test_etag_workflow(b1_config):
    """Verify that ETag is captured from GET and sent in PATCH."""
    # 1. Mock Login
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    
    # 2. Mock GET with ETag
    respx.get("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(200, json={"ItemCode": "A1"}, headers={"ETag": '"v1"'})
    )
    
    # 3. Mock PATCH (blind, we want to check headers)
    patch_route = respx.patch("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(204)
    )
    
    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        # Initial GET
        await adapter.get("Items('A1')")
        # INTERNAL LOGIC: leading slash is added for cache keys
        assert adapter._etag_cache.get("/Items('A1')") == '"v1"'
        
        # PATCH trigger
        await adapter.patch("Items('A1')", data={"ItemName": "Updated"})
        
        # Verify If-Match header was sent
        assert patch_route.calls.last.request.headers.get("If-Match") == '"v1"'

        # Proactive invalidation: SAP answered 204 without a fresh ETag, so
        # the stale cache entry must be gone immediately after the PATCH.
        assert "/Items('A1')" not in adapter._etag_cache

@pytest.mark.asyncio
@respx.mock
async def test_concurrency_error_handling(b1_config):
    """Verify that 412 with code -2039 raises SAPConcurrencyError and clears cache."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    
    # Pre-populate cache (with leading slash)
    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Items('A1')"] = '"v-old"'
    
    # Mock 412 Failure
    conflict_json = {
        "error": {
            "code": "-2039",
            "message": {"value": "Another user has modified the record"}
        }
    }
    respx.patch("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(412, json=conflict_json)
    )
    
    async with adapter:
        with pytest.raises(SAPConcurrencyError) as excinfo:
            await adapter.patch("Items('A1')", data={"ItemName": "Conflict"})
        
        assert "Another user has modified" in str(excinfo.value)
        # Verify cache was cleared
        assert "/Items('A1')" not in adapter._etag_cache

@pytest.mark.asyncio
@respx.mock
async def test_etag_cleared_after_successful_patch(b1_config):
    """Contract step 3: a successful PATCH (204, no ETag) must clear the cache."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    respx.patch("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(204)
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Items('A1')"] = '"v1"'

    async with adapter:
        await adapter.patch("Items('A1')", data={"ItemName": "Updated"})
        assert "/Items('A1')" not in adapter._etag_cache, (
            "Stale ETag survived a successful PATCH — next DELETE would 412"
        )

@pytest.mark.asyncio
@respx.mock
async def test_etag_cleared_after_successful_delete(b1_config):
    """A successful DELETE must also clear the cached ETag (recreate-then-PATCH flow)."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    respx.delete("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(204)
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Items('A1')"] = '"v1"'

    async with adapter:
        await adapter.delete("Items('A1')")
        assert "/Items('A1')" not in adapter._etag_cache

@pytest.mark.asyncio
@respx.mock
async def test_etag_parent_cleared_after_bound_action(b1_config):
    """A bound Action POST ('/Entity(key)/Cancel') must clear the parent's ETag."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    respx.post("https://sap:50000/b1s/v1/Orders(1)/Cancel").mock(
        return_value=httpx.Response(204)
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Orders(1)"] = '"v1"'

    async with adapter:
        await adapter.post("Orders(1)/Cancel")
        assert "/Orders(1)" not in adapter._etag_cache

@pytest.mark.asyncio
@respx.mock
async def test_etag_kept_when_response_carries_fresh_etag(b1_config):
    """If SAP DOES return a fresh ETag on a write, it must be cached, not dropped."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    respx.patch("https://sap:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(204, headers={"ETag": '"v2"'})
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Items('A1')"] = '"v1"'

    async with adapter:
        await adapter.patch("Items('A1')", data={"ItemName": "Updated"})
        assert adapter._etag_cache.get("/Items('A1')") == '"v2"'

@pytest.mark.asyncio
@respx.mock
async def test_etag_not_cleared_by_dry_run(b1_config):
    """Dry Run simulates writes — it must not mutate the real ETag cache."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    adapter._etag_cache["/Items('A1')"] = '"v1"'

    async with adapter:
        with adapter.dry_run():
            await adapter.patch("Items('A1')", data={"ItemName": "Simulated"})
        assert adapter._etag_cache.get("/Items('A1')") == '"v1"'

# ------------------------------------------------------------------------------
# BATCH CLIENT TESTS
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
@respx.mock
async def test_batch_client_recording(b1_config):
    """Verify that BatchClient records and serializes requests properly."""
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "123", "SessionTimeout": 30})
    )
    
    # Mock Batch Response
    batch_response = (
        "--batch_resp\r\n"
        "Content-Type: application/http\r\n\r\n"
        "HTTP/1.1 200 OK\r\n"
        "Content-Type: application/json\r\n\r\n"
        '{"ItemCode": "B1"}\r\n'
        "--batch_resp--"
    )
    
    respx.post("https://sap:50000/b1s/v1/$batch").mock(
        return_value=httpx.Response(
            200, 
            content=batch_response, 
            headers={"Content-Type": "multipart/mixed; boundary=batch_resp"}
        )
    )
    
    async with AsyncB1Client(b1_config) as b1:
        async with b1.batch() as batch:
            # Reuses same SDK API!
            await batch.items.get("B1")
            
            assert len(batch._pending) == 1
            assert batch._pending[0].method == "GET"
            assert "Items('B1')" in batch._pending[0].endpoint
            
            results = await batch.execute()
            
            assert results.all_ok
            assert results[0].data["ItemCode"] == "B1"

@pytest.mark.asyncio
async def test_batch_changeset_grouping(b1_config):
    """Verify that changeset() assigns the same changeset ID to grouped requests."""
    from b1sl.b1sl.models.base import B1Model
    class SimpleItem(B1Model):
        item_code: str = "A1"
        item_name: str | None = None
    
    # We override the model in the resource for this test
    b1 = AsyncB1Client(b1_config)
    
    # Mocking the items resource to use our SimpleItem
    b1.items.model = SimpleItem
    
    batch = b1.batch()
    
    async with batch.changeset() as cs:
        # Now create() and update() should work as they both find expected methods
        await cs.items.create(SimpleItem(item_code="NEW"))
        await cs.items.update("A1", SimpleItem(item_name="Updated"))
        
    assert len(batch._pending) == 2
    # Both should have the same changeset ID
    cs_id = batch._pending[0].changeset_id
    assert cs_id is not None
    assert batch._pending[1].changeset_id == cs_id
    assert batch.active_changeset_id is None # Reset after exit

# ------------------------------------------------------------------------------
# 401-RETRY SEMANTIC EXCEPTION (async)
# ------------------------------------------------------------------------------

@pytest.mark.asyncio
@respx.mock
async def test_async_relogin_retry_preserves_semantic_exception(b1_config):
    """After 401 → re-login, a failing retry must raise the mapped semantic
    exception (404 → B1NotFoundError), not a re-wrapped generic B1Exception."""
    from b1sl.b1sl.exceptions.exceptions import B1NotFoundError

    respx.get("https://sap:50000/b1s/v1/Items('GONE')").mock(
        side_effect=[
            httpx.Response(401, json={"error": {"code": 301, "message": {"value": "Invalid session"}}}),
            httpx.Response(404, json={"error": {"code": -2028, "message": {"value": "No matching records found"}}}),
        ]
    )
    respx.post("https://sap:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "new", "SessionTimeout": 30})
    )

    adapter = AsyncRestAdapter(b1_config, session_id="123")
    async with adapter:
        with pytest.raises(B1NotFoundError):
            await adapter.get("Items('GONE')")
