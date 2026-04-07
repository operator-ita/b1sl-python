import pytest

from b1sl.b1sl import B1Environment
from b1sl.b1sl.testing import B1TestHelper


@pytest.fixture(scope="session")
def test_data() -> B1TestHelper:
    """Provides business test data loaded from the current environment profile.

    Skips the test if the environment cannot be loaded (missing credentials).
    This allows the same fixture to be used in both VCR and real integration tests.
    """
    try:
        env = B1Environment.load()
        return B1TestHelper(env.test_data)
    except (EnvironmentError, OSError) as e:
        # If we can't load the environment, we can't get the test data.
        # We skip so it doesn't crash the entire test session.
        pytest.skip(f"Test data could not be loaded: {str(e)}")
