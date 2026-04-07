"""
test_b1sl_adapter.py — Pure pytest tests for B1Config and RestAdapter.
No Django dependency.
"""

from datetime import timedelta

import pytest

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter

# ── B1Config ────────────────────────────────────────────────────────────── #


def test_b1config_from_env_missing_vars():
    """from_env() must raise EnvironmentError listing missing variables."""
    with pytest.MonkeyPatch.context() as mp:
        mp.delenv("SAPB1CLIENT_BASE_URL", raising=False)
        mp.delenv("SAPB1CLIENT_USERNAME", raising=False)
        mp.delenv("SAPB1CLIENT_PASSWORD", raising=False)
        mp.delenv("SAPB1CLIENT_COMPANY_DB", raising=False)
        with pytest.raises(EnvironmentError) as exc:
            B1Config.from_env()
        assert "SAPB1CLIENT_BASE_URL" in str(exc.value)


def test_b1config_from_env_success():
    """from_env() must parse all required and optional env vars."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("SAPB1CLIENT_BASE_URL", "https://sap:50000/b1s/v1")
        mp.setenv("SAPB1CLIENT_USERNAME", "manager")
        mp.setenv("SAPB1CLIENT_PASSWORD", "secret")
        mp.setenv("SAPB1CLIENT_COMPANY_DB", "SBODEMOUS")
        mp.setenv("SAPB1CLIENT_TOKEN_TIMEOUT", "1800")
        mp.setenv("SAPB1CLIENT_CONNECT_TIMEOUT", "15")
        mp.setenv("SAPB1CLIENT_READ_TIMEOUT", "90")

        config = B1Config.from_env()

        assert config.base_url == "https://sap:50000/b1s/v1"
        assert config.username == "manager"
        assert config.company_db == "SBODEMOUS"
        assert config.token_timeout == timedelta(seconds=1800)
        assert config.connect_timeout == 15.0
        assert config.read_timeout == 90.0


def test_b1config_validation_empty_base_url():
    with pytest.raises(ValueError, match="base_url"):
        B1Config(base_url="", username="u", password="p", company_db="db")


def test_b1config_validation_empty_credentials():
    with pytest.raises(ValueError, match="credentials"):
        B1Config(base_url="https://x", username="", password="", company_db="db")


# ── RestAdapter ──────────────────────────────────────────────────────────── #


@pytest.fixture
def minimal_config():
    return B1Config(
        base_url="https://sap:50000/b1s/v1",
        username="manager",
        password="secret",
        company_db="SBODEMOUS",
    )


def test_rest_adapter_is_not_singleton(minimal_config):
    """
    After the audit patch, RestAdapter must NOT be a Singleton.
    Two calls to from_config() must return two distinct instances.
    """
    a = RestAdapter.from_config(minimal_config)
    b = RestAdapter.from_config(minimal_config)
    assert a is not b, "RestAdapter still behaves as a Singleton — patch not applied"


def test_rest_adapter_from_config_sets_fields(minimal_config):
    adapter = RestAdapter.from_config(minimal_config)
    assert adapter.url == "https://sap:50000/b1s/v1"
    assert adapter._username == "manager"
    assert adapter._connect_timeout == minimal_config.connect_timeout
    assert adapter._read_timeout == minimal_config.read_timeout


def test_rest_adapter_timeout_defaults(minimal_config):
    adapter = RestAdapter.from_config(minimal_config)
    assert adapter._connect_timeout == 10.0
    assert adapter._read_timeout == 60.0


# ── _parse_sap_error ─────────────────────────────────────────────────────── #

from json import JSONDecodeError
from unittest.mock import MagicMock


def _mock_response(status: int, body=None, json_error=False):
    r = MagicMock()
    r.status_code = status
    r.reason = "Bad Request"
    if json_error:
        r.json.side_effect = JSONDecodeError("no JSON", "", 0)
    else:
        r.json.return_value = body
    return r


@pytest.mark.parametrize(
    "body,expected_code,expected_msg_fragment",
    [
        # Shape A — standard OData
        (
            {"error": {"code": -2028, "message": {"value": "Item does not exist"}}},
            "-2028",
            "Item does not exist",
        ),
        # Shape B — bare string message
        (
            {"error": {"code": "-5002", "message": "No matching records found"}},
            "-5002",
            "No matching records found",
        ),
        # Shape C — lang-keyed dict
        (
            {
                "error": {
                    "code": 131,
                    "message": {"lang": "en-US", "value": "Auth failed"},
                }
            },
            "131",
            "Auth failed",
        ),
        # Shape D — JSON but not OData format → fallback
        (
            {"detail": "Something went wrong"},
            "unknown",
            "HTTP 400",
        ),
    ],
)
def test_parse_sap_error_shapes(body, expected_code, expected_msg_fragment):
    r = _mock_response(400, body)
    code, msg = RestAdapter._parse_sap_error(r)
    assert code == expected_code
    assert expected_msg_fragment in msg


def test_parse_sap_error_non_json():
    r = _mock_response(503, json_error=True)
    r.reason = "Service Unavailable"
    code, msg = RestAdapter._parse_sap_error(r)
    assert code == "unknown"
    assert "503" in msg
