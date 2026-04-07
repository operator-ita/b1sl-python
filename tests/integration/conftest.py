import os
from datetime import datetime, timedelta

import pytest

from b1sl.b1sl import B1Client, B1Environment

# Load common test fixtures (test_data)
pytest_plugins = ["tests.fixtures.test_data"]


@pytest.fixture(scope="session")
def sap_env() -> B1Environment:
    """Provides a fully loaded B1Environment for integration tests.

    Uses B1Environment.load() which pulls credentials from B1SL_* env vars.
    Skips tests with a clear message if required variables are missing.
    """
    # 1. Respect the global kill-switch
    if os.getenv("SAP_B1_INTEGRATION", "1") == "0":
        pytest.skip("SAP_B1_INTEGRATION=0. Skipping real connection tests.")

    # 2. Try to load the environment
    try:
        # Load profile from B1SL_ENV (default: dev)
        # We use strict=True here because this fixture is for REAL connection tests.
        return B1Environment.load(strict=True)
    except (EnvironmentError, OSError) as e:
        pytest.skip(
            f"Integration test configuration missing: {str(e)}. "
            "Please check your .env file or environment variables."
        )


@pytest.fixture(scope="session")
def sap_client(sap_env: B1Environment) -> B1Client:
    """Real SAP client fixture for integration testing."""
    client = B1Client(config=sap_env.config)
    return _apply_test_state(client)


@pytest.fixture(scope="session")
def sap_client_vcr() -> B1Client:
    """Fixture providing a B1Client configured for VCR playback.

    Uses standardized placeholders that match existing cassettes, allowing
    tests to run in CI or local without any real environment variables.
    """
    from b1sl.b1sl.config import B1Config
    from b1sl.b1sl.environment import B1Env

    config = B1Config(
        base_url="https://sap-server.example.com:50000/b1s/v2",
        company_db="[REDACTED]",
        username="manager",
        password="[REDACTED]",
        environment=B1Env.DEV,
        ssl_verify=False,
    )
    client = B1Client(config=config)
    return _apply_test_state(client)


def _apply_test_state(client: B1Client) -> B1Client:
    """Injects fake session state to bypass auto-login in tests."""
    client._adapter.is_session_active = True
    client._adapter.token_expiry = datetime.now() + timedelta(days=1)
    client._adapter.reuse_token = True
    return client
