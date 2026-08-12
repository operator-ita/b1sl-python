import httpx
import pytest
import respx

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.config import B1Config


@pytest.fixture
def b1_config():
    return B1Config(
        base_url="https://sap-server:50000/b1s/v1",
        username="manager",
        password="password",
        company_db="SBODemoES",
    )


@pytest.mark.asyncio
@respx.mock
async def test_async_rest_adapter_login(b1_config):
    # Mock Login
    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(
            200, json={"SessionId": "12345", "SessionTimeout": 30}
        )
    )

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        assert adapter.is_session_active is True
        assert adapter.token_expiry is not None


@pytest.mark.asyncio
@respx.mock
async def test_async_rest_adapter_get_item(b1_config):
    # Mock Login
    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(
            200, json={"SessionId": "12345", "SessionTimeout": 30}
        )
    )

    # Mock GET Item
    respx.get("https://sap-server:50000/b1s/v1/Items('A0001')").mock(
        return_value=httpx.Response(
            200, json={"ItemCode": "A0001", "ItemName": "Test Item"}
        )
    )

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        result = await adapter.get("Items('A0001')")
        assert result.status_code == 200
        assert result.data["ItemCode"] == "A0001"


@pytest.mark.asyncio
@respx.mock
async def test_async_rest_adapter_401_retry(b1_config):
    # Mock Login (initial)
    login_mock = respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(
            200, json={"SessionId": "first", "SessionTimeout": 30}
        )
    )

    # Mock GET (fails first time with 401, then succeeds)
    get_mock = respx.get("https://sap-server:50000/b1s/v1/Items('A0001')")
    get_mock.side_effect = [
        httpx.Response(401, json={"error": {"code": 401, "message": "Unauthorized"}}),
        httpx.Response(200, json={"ItemCode": "A0001"}),
    ]

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        result = await adapter.get("Items('A0001')")
        assert result.status_code == 200
        assert result.data["ItemCode"] == "A0001"
        assert login_mock.call_count == 2  # Initial login + retry login
        assert get_mock.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_async_rest_adapter_hydration(b1_config):
    """
    Test that providing a session_id bypasses the initial Login 
    and sets token_expiry to None.
    """
    login_mock = respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "fresh", "SessionTimeout": 30})
    )

    # Mock GET success using the provided session_id
    respx.get("https://sap-server:50000/b1s/v1/Items('A0001')").mock(
        return_value=httpx.Response(200, json={"ItemCode": "A0001"})
    )

    # Initialize with session_id
    adapter = AsyncRestAdapter(b1_config, session_id="existing-session")
    await adapter.connect()

    assert adapter.is_session_active is True
    assert adapter.token_expiry is None
    assert adapter.session_id == "existing-session"

    # Verify no Login request was made yet
    assert login_mock.call_count == 0

    # Perform a request
    result = await adapter.get("Items('A0001')")
    assert result.status_code == 200
    assert login_mock.call_count == 0  # Still no login because session worked

    await adapter.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_async_stale_keepalive_get_retries_then_succeeds(b1_config):
    """A GET hitting a stale server-closed keepalive retries once transparently."""
    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "s1", "SessionTimeout": 30})
    )
    route = respx.get("https://sap-server:50000/b1s/v1/Items('A0001')")
    route.side_effect = [
        httpx.RemoteProtocolError("Server disconnected without sending a response."),
        httpx.Response(200, json={"ItemCode": "A0001"}),
    ]

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        result = await adapter.get("Items('A0001')")
        assert result.status_code == 200
        assert route.call_count == 2  # original + one transparent retry


@pytest.mark.asyncio
@respx.mock
async def test_async_stale_keepalive_patch_not_retried(b1_config):
    """Non-idempotent writes are never auto-retried — raise B1ConnectionError."""
    from b1sl.b1sl.exceptions.exceptions import B1ConnectionError

    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "s1", "SessionTimeout": 30})
    )
    route = respx.patch("https://sap-server:50000/b1s/v1/Items('A0001')").mock(
        side_effect=httpx.RemoteProtocolError("Server disconnected without sending a response.")
    )

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        with pytest.raises(B1ConnectionError):
            await adapter.patch("Items('A0001')", data={"ItemName": "x"})
        assert route.call_count == 1  # no retry on PATCH


@pytest.mark.asyncio
@respx.mock
async def test_async_select_get_does_not_cache_body_etag(b1_config):
    """Async parity: a $select GET must not cache the bogus body @odata.etag,
    nor clobber a valid one cached by an earlier full GET (SAP quirk; see
    docs/18-sap-version-quirks.md)."""
    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "s1", "SessionTimeout": 30})
    )
    bogus = 'W/"356A192B7913B04C54574D18C28D46E6395428AB"'  # sha1("1")
    respx.get("https://sap-server:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(
            200, json={"@odata.etag": bogus, "ItemCode": "A1"}
        )
    )

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        await adapter.get("Items('A1')", ep_params={"$select": "ItemCode"})
        assert "/Items('A1')" not in adapter._etag_cache

        adapter._etag_cache["/Items('A1')"] = '"valid-etag"'
        await adapter.get("Items('A1')", ep_params={"$select": "ItemCode"})
        assert adapter._etag_cache.get("/Items('A1')") == '"valid-etag"'


@pytest.mark.asyncio
@respx.mock
async def test_async_full_get_still_uses_body_etag_fallback(b1_config):
    """Async parity: without $select the body @odata.etag fallback still works."""
    respx.post("https://sap-server:50000/b1s/v1/Login").mock(
        return_value=httpx.Response(200, json={"SessionId": "s1", "SessionTimeout": 30})
    )
    respx.get("https://sap-server:50000/b1s/v1/Items('A1')").mock(
        return_value=httpx.Response(
            200, json={"@odata.etag": '"body-etag"', "ItemCode": "A1"}
        )
    )

    async with AsyncRestAdapter.from_config(b1_config) as adapter:
        await adapter.get("Items('A1')")
        assert adapter._etag_cache.get("/Items('A1')") == '"body-etag"'
