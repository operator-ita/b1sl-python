"""
Unit tests for the Dry Run mechanism.

Covers:
- Global dry_run (config.dry_run=True)
- Context manager (temporary, task-local via ContextVar)
- Both sync (RestAdapter) and async (AsyncRestAdapter) adapters
"""
import asyncio

import pytest
import respx
from httpx import Response

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter

# ─── Fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def base_config():
    return B1Config(
        base_url="https://sap-host:50000",
        username="manager",
        password="sap",
        company_db="SBODEMO",
        dry_run=False,
    )


@pytest.fixture
def dry_run_config(base_config):
    base_config.dry_run = True
    return base_config


def _login_mock(base="https://sap-host:50000/b1s/v2"):
    return respx.post(f"{base}/Login").mock(
        return_value=Response(200, json={"SessionId": "abc", "SessionTimeout": 30})
    )


# ─── Sync Adapter ────────────────────────────────────────────────────────────


class TestDryRunSync:
    """Tests for RestAdapter (synchronous)."""

    @respx.mock
    def test_global_dry_run_intercepts_post(self, dry_run_config):
        """POST must be intercepted when global dry_run=True."""
        _login_mock()
        post_route = respx.post("https://sap-host:50000/b1s/v2/Items")

        adapter = RestAdapter.from_config(dry_run_config)
        adapter.is_session_active = True
        adapter._dry_run_var.set(True)  # simulate global flag

        result = adapter._do("POST", "/Items", data={"ItemCode": "X"})

        assert result.status_code == 204
        assert not post_route.called, "POST should have been intercepted, not sent"

    @respx.mock
    def test_global_dry_run_does_not_intercept_get(self, dry_run_config):
        """GET must pass through even with dry_run=True."""
        _login_mock()
        respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        adapter = RestAdapter.from_config(dry_run_config)
        adapter.is_session_active = True
        adapter.token_expiry = None

        result = adapter._do("GET", "/Items")

        assert result.status_code == 200

    @respx.mock
    def test_global_dry_run_does_not_intercept_login(self, dry_run_config):
        """Login (POST /Login) must NOT be intercepted by dry_run."""
        login_mock = _login_mock()

        adapter = RestAdapter.from_config(dry_run_config)
        adapter._login()

        assert login_mock.called, "Login must always be sent even with dry_run=True"

    @respx.mock
    def test_context_manager_enables_dry_run(self, base_config):
        """CM with dry_run() must intercept writes even if global is False."""
        _login_mock()
        post_route = respx.post("https://sap-host:50000/b1s/v2/Items")

        adapter = RestAdapter.from_config(base_config)  # dry_run=False globally
        adapter.is_session_active = True

        with adapter.dry_run():
            assert adapter._dry_run_active is True
            result = adapter._do("POST", "/Items", data={})

        assert result.status_code == 204
        assert not post_route.called

    @respx.mock
    def test_context_manager_restores_state_after_exit(self, base_config):
        """After the CM exits, the dry_run state returns to its previous value."""
        adapter = RestAdapter.from_config(base_config)  # dry_run=False

        assert adapter._dry_run_active is False
        with adapter.dry_run():
            assert adapter._dry_run_active is True
        assert adapter._dry_run_active is False, "State must be restored after CM exit"

    @respx.mock
    def test_context_manager_force_off_overrides_global(self, dry_run_config):
        """dry_run(enabled=False) forces real execution even if global is True."""
        _login_mock()
        post_route = respx.post("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(201, json={"DocEntry": 1})
        )

        adapter = RestAdapter.from_config(dry_run_config)  # dry_run=True globally
        adapter.is_session_active = True

        with adapter.dry_run(enabled=False):
            assert adapter._dry_run_active is False
            result = adapter._do("POST", "/Items", data={})

        assert result.status_code == 201
        assert post_route.called, "POST must be sent when dry_run is forced off"


# ─── Async Adapter ───────────────────────────────────────────────────────────


class TestDryRunAsync:
    """Tests for AsyncRestAdapter (asynchronous)."""

    @pytest.mark.asyncio
    @respx.mock
    async def test_global_dry_run_intercepts_post(self, dry_run_config):
        """Async POST must be intercepted when global dry_run=True."""
        _login_mock()
        post_route = respx.post("https://sap-host:50000/b1s/v2/BusinessPartners")

        async with AsyncRestAdapter.from_config(dry_run_config) as adapter:
            result = await adapter.post("/BusinessPartners", data={"CardCode": "C001"})

        assert result.status_code == 204
        assert not post_route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_global_dry_run_does_not_intercept_get(self, dry_run_config):
        """Async GET must pass through even with dry_run=True."""
        _login_mock()
        respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )

        async with AsyncRestAdapter.from_config(dry_run_config) as adapter:
            result = await adapter.get("/Items")

        assert result.status_code == 200

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager_enables_dry_run(self, base_config):
        """CM with dry_run() must intercept async writes even if global is False."""
        _login_mock()
        post_route = respx.post("https://sap-host:50000/b1s/v2/Items")

        async with AsyncRestAdapter.from_config(base_config) as adapter:
            with adapter.dry_run():
                assert adapter._dry_run_active is True
                result = await adapter.post("/Items", data={})

        assert result.status_code == 204
        assert not post_route.called

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager_restores_state_after_exit(self, base_config):
        """After the CM exits, the async dry_run state returns to False."""
        _login_mock()

        async with AsyncRestAdapter.from_config(base_config) as adapter:
            assert adapter._dry_run_active is False
            with adapter.dry_run():
                assert adapter._dry_run_active is True
            assert adapter._dry_run_active is False

    @pytest.mark.asyncio
    @respx.mock
    async def test_context_manager_is_task_local(self, base_config):
        """
        Two concurrent tasks share the same adapter.
        Task A enters dry_run(); Task B must NOT see Task A's dry_run state.
        This validates the ContextVar task-isolation guarantee.
        """
        _login_mock()
        _login_mock()  # second login for the second client
        respx.get("https://sap-host:50000/b1s/v2/Items").mock(
            return_value=Response(200, json={"value": []})
        )
        post_route = respx.post("https://sap-host:50000/b1s/v2/Items")

        results = {}

        async def task_a(adapter):
            """Enters dry_run and records whether it was active."""
            with adapter.dry_run():
                results["task_a_active"] = adapter._dry_run_active
                await asyncio.sleep(0)  # yield to let task_b run
                result = await adapter.post("/Items", data={})
                results["task_a_result"] = result.status_code

        async def task_b(adapter):
            """Runs concurrently; must NOT see task_a's dry_run state."""
            await asyncio.sleep(0)  # let task_a enter dry_run first
            results["task_b_active"] = adapter._dry_run_active

        async with AsyncRestAdapter.from_config(base_config) as adapter:
            await asyncio.gather(task_a(adapter), task_b(adapter))

        assert results["task_a_active"] is True, "Task A should see dry_run=True"
        assert results["task_b_active"] is False, "Task B must NOT be affected by Task A's CM"
        assert results["task_a_result"] == 204, "Task A's POST should be intercepted"
        assert not post_route.called, "No real POST should have been sent"
