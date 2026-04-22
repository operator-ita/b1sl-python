"""
Unit tests for the B1S-Schema Header support.

Covers:
- Global schema (config.b1s_schema)
- Context manager (temporary, task-local via ContextVar)
- Query builder integration (.with_schema())
- Both sync (RestAdapter) and async (AsyncRestAdapter) adapters
"""
import asyncio
from unittest.mock import MagicMock

import pytest
import respx
from httpx import Response
from pydantic import Field

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.base import GenericResource
from b1sl.b1sl.rest_adapter import RestAdapter

# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def base_config():
    return B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
        b1s_schema=None,
    )


@pytest.fixture
def schema_config(base_config):
    base_config.b1s_schema = "demo.schema"
    return base_config


def _login_mock(base="https://sap-host:50000/b1s/v2"):
    return respx.post(f"{base}/Login").mock(
        return_value=Response(200, json={"SessionId": "abc", "SessionTimeout": 30})
    )


class MockModel(B1Model):
    item_code: str | None = Field(None, alias="ItemCode")


# ─── Sync Adapter ────────────────────────────────────────────────────────────


class TestSchemaHeaderSync:
    """Tests for RestAdapter (synchronous)."""

    @respx.mock
    def test_global_schema_header_injected(self, schema_config):
        """B1S-Schema header must be injected when set globally."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        adapter = RestAdapter.from_config(schema_config)
        adapter.is_session_active = True

        result = adapter._do("GET", "/Items")

        assert result.status_code == 200
        assert get_route.called
        assert get_route.calls.last.request.headers.get("B1S-Schema") == "demo.schema"

    @respx.mock
    def test_no_schema_header_by_default(self, base_config):
        """B1S-Schema header must NOT be present if not configured."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        adapter = RestAdapter.from_config(base_config)
        adapter.is_session_active = True

        result = adapter._do("GET", "/Items")

        assert result.status_code == 200
        assert get_route.called
        assert "B1S-Schema" not in get_route.calls.last.request.headers

    @respx.mock
    def test_context_manager_overrides_schema(self, base_config):
        """CM with with_schema() must inject the header temporarily."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        adapter = RestAdapter.from_config(base_config)  # No global schema
        adapter.is_session_active = True

        with adapter.with_schema("temp.schema"):
            assert adapter._schema_active == "temp.schema"
            result = adapter._do("GET", "/Items")

        assert result.status_code == 200
        assert get_route.called
        assert get_route.calls.last.request.headers.get("B1S-Schema") == "temp.schema"
        assert adapter._schema_active is None

    @respx.mock
    def test_context_manager_can_disable_schema(self, schema_config):
        """CM with None must remove the header temporarily even if globally set."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        adapter = RestAdapter.from_config(schema_config)  # demo.schema globally
        adapter.is_session_active = True

        with adapter.with_schema(None):
            assert adapter._schema_active is None
            result = adapter._do("GET", "/Items")

        assert result.status_code == 200
        assert get_route.called
        assert "B1S-Schema" not in get_route.calls.last.request.headers
        assert adapter._schema_active == "demo.schema"


# ─── Async Adapter ───────────────────────────────────────────────────────────


class TestSchemaHeaderAsync:
    """Tests for AsyncRestAdapter (asynchronous)."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_global_schema_header_injected(self, schema_config):
        """Async GET must have the B1S-Schema header when set globally."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        async with AsyncRestAdapter.from_config(schema_config) as adapter:
            result = await adapter.get("/Items")

        assert result.status_code == 200
        assert get_route.called
        assert get_route.calls.last.request.headers.get("B1S-Schema") == "demo.schema"

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager_overrides_schema(self, base_config):
        """CM with with_schema() must inject the header temporarily for async."""
        _login_mock()
        get_route = respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        async with AsyncRestAdapter.from_config(base_config) as adapter:
            with adapter.with_schema("async.schema"):
                assert adapter._schema_active == "async.schema"
                result = await adapter.get("/Items")

        assert result.status_code == 200
        assert get_route.called
        assert get_route.calls.last.request.headers.get("B1S-Schema") == "async.schema"
        assert adapter._schema_active is None

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager_is_task_local(self, base_config):
        """
        Two concurrent tasks share the same adapter.
        Task A uses a schema; Task B must NOT see Task A's schema.
        This validates the ContextVar task-isolation guarantee.
        """
        _login_mock()
        _login_mock()
        respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        results = {}

        async def task_a(adapter):
            with adapter.with_schema("task_a.schema"):
                results["task_a_active"] = adapter._schema_active
                await asyncio.sleep(0)  # yield
                await adapter.get("/Items")
                # We can't easily assert headers per-call in this setup due to race conditions
                # in reading `get_route.calls.last`, but checking the ContextVar is sufficient.

        async def task_b(adapter):
            await asyncio.sleep(0)  # let task_a set its schema
            results["task_b_active"] = adapter._schema_active

        async with AsyncRestAdapter.from_config(base_config) as adapter:
            await asyncio.gather(task_a(adapter), task_b(adapter))

        assert results["task_a_active"] == "task_a.schema"
        assert results["task_b_active"] is None


# ─── Query Builder ───────────────────────────────────────────────────────────


class TestQueryBuilderSchema:
    def test_query_builder_with_schema(self):
        """QueryBuilder fluent API must correctly trigger the adapter context manager."""
        adapter = MagicMock()
        
        # We need a context manager mock for `with_schema`
        cm_mock = MagicMock()
        adapter.with_schema.return_value = cm_mock
        cm_mock.__enter__.return_value = cm_mock
        
        resource: GenericResource[MockModel] = GenericResource(adapter)
        resource.endpoint = "Items"
        resource.model = MockModel

        # Setup mock return value
        adapter.get.return_value = MagicMock(data={"value": [{"ItemCode": "A001"}]})

        # Execute query with schema
        results = resource.with_schema("fluent.schema").top(5).execute()

        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0].item_code == "A001"
        
        # Verify adapter's with_schema was called
        adapter.with_schema.assert_called_once_with("fluent.schema")
        
        # Verify CM was entered and exited
        assert cm_mock.__enter__.called
        assert cm_mock.__exit__.called

    def test_query_builder_stream_with_schema(self):
        """QueryBuilder stream must correctly trigger the adapter context manager."""
        adapter = MagicMock()
        cm_mock = MagicMock()
        adapter.with_schema.return_value = cm_mock
        cm_mock.__enter__.return_value = cm_mock
        
        resource: GenericResource[MockModel] = GenericResource(adapter)
        resource.endpoint = "Items"
        resource.model = MockModel

        # Setup mock stream data
        mock_result = MagicMock(data={"value": [{"ItemCode": "A001"}]})
        mock_result.next_link = None
        adapter.get.return_value = mock_result

        # Execute stream with schema
        generator = resource.with_schema("stream.schema").stream()
        results = list(generator)

        assert len(results) == 1
        assert results[0].item_code == "A001"
        
        # Verify adapter's with_schema was called
        adapter.with_schema.assert_called_once_with("stream.schema")
        assert cm_mock.__enter__.called
        assert cm_mock.__exit__.called
