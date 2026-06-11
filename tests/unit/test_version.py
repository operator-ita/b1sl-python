"""Version is single-sourced from the installed distribution metadata."""
from importlib.metadata import version

import b1sl


def test_version_matches_distribution_metadata():
    assert b1sl.__version__ == version("b1sl-python")
    # Guard against the historical hardcoded-and-stale literal.
    assert b1sl.__version__ != "0.4.1"
