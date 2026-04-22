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
