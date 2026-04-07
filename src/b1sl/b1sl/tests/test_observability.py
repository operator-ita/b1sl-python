import logging
from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.base_adapter import HookContext, HookDispatcher, ObservabilityConfig
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter


def test_hook_context_immutability():
    ctx = HookContext(
        req_id="123",
        http_method="GET",
        base_url="http://test",
        endpoint="/Items",
        query_params="",
        db="db",
        user="user",
        status_code=200,
        duration_ms=10.0,
    )
    with pytest.raises(AttributeError):  # frozen=True
        ctx.status_code = 500


def test_to_log_extra_contract():
    extra_data = {"test_key": "test_val"}
    ctx = HookContext(
        req_id="123",
        http_method="GET",
        base_url="http://test",
        endpoint="/Items",
        query_params="",
        db="db",
        user="user",
        status_code=200,
        duration_ms=10.5,
        extra=extra_data,
    )
    log_extra = ctx.to_log_extra()

    assert log_extra["req_id"] == "123"
    assert log_extra["duration_ms"] == 10.5
    assert log_extra["test_key"] == "test_val"
    assert (
        "query_params" not in log_extra
    )  # Should not be in log_extra by default for privacy


def test_hook_dispatcher_isolation():
    """Verify that a failing hook does not stop other hooks or the dispatcher."""
    logger = MagicMock(spec=logging.Logger)

    def failing_hook(ctx):
        raise ValueError("Boom!")

    success_mock = MagicMock()

    dispatcher = HookDispatcher(hooks={"on_response": [failing_hook, success_mock]})
    ctx = MagicMock(spec=HookContext)

    # Should not raise exception
    dispatcher.dispatch("on_response", ctx, logger)

    # Second hook should have been called
    success_mock.assert_called_once_with(ctx)
    # Logger should have warned about the failure
    assert logger.warning.called


@pytest.mark.asyncio
async def test_async_hook_dispatcher_isolation():
    logger = MagicMock(spec=logging.Logger)

    async def failing_async_hook(ctx):
        raise ValueError("Async Boom!")

    success_async_mock = AsyncMock()

    dispatcher = HookDispatcher(
        hooks={"on_response": [failing_async_hook, success_async_mock]}
    )
    ctx = MagicMock(spec=HookContext)

    await dispatcher.adispatch("on_response", ctx, logger)

    success_async_mock.assert_called_once_with(ctx)
    assert logger.warning.called


def test_rest_adapter_observability_integration():
    """Integration test for RestAdapter with ObservabilityConfig."""
    hook_mock = MagicMock()
    obs = ObservabilityConfig(
        hooks={"on_response": [hook_mock]}, context_extras={"tenant": "admin"}
    )

    config = B1Config("http://sap", "user", "pass", "db")
    adapter = RestAdapter(config, observability=obs)

    # Mock transport
    adapter._execute_request = MagicMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.reason = "OK"
    mock_resp.content = b"{}"
    mock_resp.json.return_value = {}
    mock_resp.headers = {}
    adapter._execute_request.return_value = mock_resp

    adapter._do("GET", "Items", ep_params={"$top": 1})

    # Verify hook was called
    assert hook_mock.called
    ctx = hook_mock.call_args[0][0]
    assert isinstance(ctx, HookContext)
    assert ctx.endpoint == "/Items"
    assert ctx.query_params == "%24top=1"
    assert ctx.extra["tenant"] == "admin"
    assert ctx.duration_ms > 0


@pytest.mark.asyncio
async def test_async_rest_adapter_observability_integration():
    hook_mock = MagicMock()
    obs = ObservabilityConfig(hooks={"on_response": [hook_mock]})

    config = B1Config("http://sap", "user", "pass", "db")
    adapter = AsyncRestAdapter(config, observability=obs)

    # Mock httpx client
    adapter._client = AsyncMock()
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.reason_phrase = "OK"
    mock_resp.content = b"{}"
    mock_resp.json.return_value = {}
    mock_resp.headers = {}
    adapter._client.request.return_value = mock_resp

    from datetime import datetime, timedelta

    adapter.is_session_active = True
    adapter.token_expiry = datetime.now() + timedelta(hours=1)

    await adapter._do("GET", "Items")

    assert hook_mock.called
    ctx = hook_mock.call_args[0][0]
    assert ctx.endpoint == "/Items"
    assert ctx.duration_ms > 0
