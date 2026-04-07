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
        assert adapter._token_expiry is not None


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
