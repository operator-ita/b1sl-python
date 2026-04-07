"""
test_02_rest_adapter.py — RestAdapter unit tests (pure pytest, no Django).

These are offline tests using mocks — no live SAP connection required.
Integration tests that require a live SAP instance belong in a separate
``tests/integration/`` directory that is skipped in CI.
"""

from datetime import timedelta
from json import JSONDecodeError
from unittest.mock import MagicMock, patch

import pytest

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter


@pytest.fixture
def config():
    return B1Config(
        base_url="https://sap:50000/b1s/v1",
        username="manager",
        password="s3cr3t",
        company_db="TESTDB",
        reuse_token=False,
        connect_timeout=5.0,
        read_timeout=30.0,
    )


@pytest.fixture
def adapter(config):
    return RestAdapter.from_config(config)


# ── Singleton removed ────────────────────────────────────────────────────── #


def test_no_singleton(config):
    """Two from_config() calls must return two distinct objects."""
    a = RestAdapter.from_config(config)
    b = RestAdapter.from_config(config)
    assert a is not b


# ── Constructor ──────────────────────────────────────────────────────────── #


def test_adapter_stores_config_fields(adapter, config):
    assert adapter.url == config.base_url
    assert adapter._username == config.username
    assert adapter._connect_timeout == 5.0
    assert adapter._read_timeout == 30.0


# ── Token expiry ─────────────────────────────────────────────────────────── #


def test_is_token_expire_when_no_expiry(adapter):
    adapter.token_expiry = None
    assert adapter._is_token_expire() is True


def test_is_token_expire_when_future(adapter):
    from datetime import datetime

    adapter.token_expiry = datetime.now() + timedelta(hours=1)
    assert adapter._is_token_expire() is False


def test_is_token_expire_when_past(adapter):
    from datetime import datetime

    adapter.token_expiry = datetime.now() - timedelta(seconds=1)
    assert adapter._is_token_expire() is True


# ── _parse_sap_error ─────────────────────────────────────────────────────── #


def _mock_resp(status, body=None, json_raises=False):
    r = MagicMock()
    r.status_code = status
    r.reason = "Error"
    if json_raises:
        r.json.side_effect = JSONDecodeError("", "", 0)
    else:
        r.json.return_value = body
    return r


@pytest.mark.parametrize(
    "body,exp_code,exp_fragment",
    [
        (
            {"error": {"code": -2028, "message": {"value": "Item does not exist"}}},
            "-2028",
            "Item does not exist",
        ),
        (
            {"error": {"code": "-5002", "message": "No records found"}},
            "-5002",
            "No records found",
        ),
        (
            {"error": {"code": 0, "message": {"lang": "en", "value": "Auth error"}}},
            "0",
            "Auth error",
        ),
        ({"detail": "not SAP format"}, "unknown", "HTTP 400"),
    ],
)
def test_parse_sap_error_shapes(body, exp_code, exp_fragment):
    r = _mock_resp(400, body)
    code, msg = RestAdapter._parse_sap_error(r)
    assert code == exp_code
    assert exp_fragment in msg


def test_parse_sap_error_non_json():
    r = _mock_resp(500, json_raises=True)
    r.reason = "Internal Server Error"
    code, msg = RestAdapter._parse_sap_error(r)
    assert code == "unknown"
    assert "500" in msg


# ── Password never appears in debug logs ─────────────────────────────────── #


def test_password_not_logged(adapter, caplog):
    """The Password field must be redacted before any log statement in _do."""
    import logging

    with caplog.at_level(logging.DEBUG, logger="b1sl.b1sl.rest_adapter"):
        with patch.object(adapter, "_execute_request") as mock_exec:
            mock_resp = MagicMock()
            mock_resp.status_code = 200
            mock_resp.reason = "OK"  # must be str for Result.message
            mock_resp.content = b'{"SessionId":"abc","Version":"1","SessionTimeout":30}'
            mock_resp.json.return_value = {
                "SessionId": "abc",
                "Version": "1",
                "SessionTimeout": 30,
            }
            mock_resp.headers = {}
            mock_resp.raise_for_status.return_value = None
            mock_exec.return_value = mock_resp
            adapter._do(
                http_method="POST",
                endpoint="/Login",
                data={
                    "UserName": "manager",
                    "Password": "s3cr3t",
                    "CompanyDB": "TESTDB",
                },
                _is_login=True,
            )
    full_log = " ".join(caplog.messages)
    assert "s3cr3t" not in full_log, "Raw password found in log output!"
    assert "***" in full_log, "Password redaction marker '***' missing from log"


# ── Timeout passed to session.request ────────────────────────────────────── #


def test_execute_request_passes_timeout(adapter):
    with patch.object(adapter.session, "request") as mock_req:
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {}
        mock_req.return_value = mock_resp
        adapter._execute_request("GET", "https://sap/b1s/v1/Items", {}, None, None)
    _, kwargs = mock_req.call_args
    assert "timeout" in kwargs
    assert kwargs["timeout"] == (5.0, 30.0)
