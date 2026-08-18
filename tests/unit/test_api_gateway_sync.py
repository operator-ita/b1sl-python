"""Unit tests for ``APIGatewayClient`` — the sync twin of the API Gateway client.

Mirrors the key scenarios of ``test_api_gateway.py``; the shared decoding /
payload logic is covered there and not repeated.
"""

from __future__ import annotations

import base64
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

import httpx
import pytest
import respx

from b1sl.api_gateway import (
    APIGatewayAuthError,
    APIGatewayClient,
    APIGatewayConfig,
    APIGatewayConnectionError,
    APIGatewayError,
    APIGatewayLayoutNotFoundError,
    APIGatewayParameterError,
)
from b1sl.b1sl.base_adapter import HookContext, ObservabilityConfig

BASE = "https://gw-host:60000"
LOGIN = f"{BASE}/login"
LOGOUT = f"{BASE}/logout"
LIST = f"{BASE}/rs/v1/LoadAuthorizedCRList"
LOADCR = f"{BASE}/rs/v1/LoadCR"
EXPORT = f"{BASE}/rs/v1/ExportPDFData"

PDF_BYTES = b"%PDF-1.7\n%\xe2\xe3\xcf\xd3\n1 0 obj\n<<>>\nendobj\n%%EOF\n"
PDF_B64 = base64.b64encode(PDF_BYTES).decode()

LOGIN_OK = httpx.Response(
    200,
    json={"Version": "0.0.1", "SessionTimeout": 30},
    headers=[
        ("set-cookie", "Session=abc123; Secure; HTTPOnly"),
        ("set-cookie", "Cookie=abc123; Secure; HTTPOnly"),
    ],
)
LOADCR_OK = {
    "result": "Success",
    "resultSet": [
        {
            "name": "ObjectId@",
            "type": "xsd:decimal",
            "currentvalues": ["23"],
            "allowNullValue": "true",
        },
        {
            "name": "DocKey@",
            "type": "xsd:decimal",
            "currentvalues": ["777"],
            "allowNullValue": "true",
        },
        {
            "name": "Pm-Optional.Text",
            "type": "xsd:string",
            "currentvalues": [],
            "allowNullValue": "true",
        },
    ],
}


@pytest.fixture
def cfg():
    return APIGatewayConfig(
        base_url=BASE, username="manager", password="secret", company_db="SBO_TEST"
    )


def _mock_session():
    login = respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    return login


@respx.mock
def test_context_manager_logs_in_and_out(cfg):
    login = _mock_session()
    logout = respx.post(LOGOUT)
    with APIGatewayClient(cfg) as gw:
        assert gw.is_session_active
        assert gw.server_session_timeout == 30
        assert gw.token_expiry is None  # reactive by default (no session_ttl)
        assert gw._client is not None
        assert gw._client.cookies.get("Session") == "abc123"
        body = login.calls.last.request.read()
        assert b"SBO_TEST" in body and b"secret" in body  # sent to SAP, never logged
    assert logout.call_count == 1
    assert gw.is_session_active is False
    assert gw._client is None


@respx.mock
def test_login_failure_and_connection_error(cfg):
    respx.post(LOGIN).mock(return_value=httpx.Response(401))
    with pytest.raises(APIGatewayAuthError):
        APIGatewayClient(cfg).connect()
    respx.post(LOGIN).mock(side_effect=httpx.ConnectError("refused"))
    with pytest.raises(APIGatewayConnectionError, match="API Gateway"):
        APIGatewayClient(cfg).connect()


def test_request_before_connect_raises(cfg):
    with pytest.raises(APIGatewayError, match="not connected"):
        APIGatewayClient(cfg).list_reports()


@respx.mock
def test_401_relogin_once_then_auth_error(cfg):
    login = _mock_session()
    route = respx.get(LIST)
    route.side_effect = [
        httpx.Response(401),
        httpx.Response(200, json={"result": "Success", "resultSet": []}),
        httpx.Response(401),
        httpx.Response(401),
    ]
    with APIGatewayClient(cfg) as gw:
        assert gw.list_reports() == []
        assert login.call_count == 2
        with pytest.raises(APIGatewayAuthError):
            gw.list_reports()
    assert login.call_count == 3


@respx.mock
def test_expired_session_relogs_in(cfg):
    login = _mock_session()
    respx.get(LIST).mock(
        return_value=httpx.Response(200, json={"result": "Success", "resultSet": []})
    )
    with APIGatewayClient(cfg) as gw:
        gw.token_expiry = datetime.now() - timedelta(seconds=1)
        gw.list_reports()
    assert login.call_count == 2


@respx.mock
def test_export_document_pdf_end_to_end(cfg):
    _mock_session()
    respx.get(LOADCR).mock(return_value=httpx.Response(200, json=LOADCR_OK))
    export = respx.post(EXPORT).mock(return_value=httpx.Response(201, text=PDF_B64))
    with APIGatewayClient(cfg) as gw:
        pdf = gw.export_document_pdf("QUT20020", doc_entry=12345)
    assert pdf == PDF_BYTES
    assert json.loads(export.calls.last.request.read()) == [
        {"name": "ObjectId@", "type": "xsd:decimal", "value": [["23"]]},
        {"name": "DocKey@", "type": "xsd:decimal", "value": [["12345"]]},
    ]


@respx.mock
def test_body_level_errors(cfg):
    _mock_session()
    respx.get(LOADCR).mock(return_value=httpx.Response(200, json={}))
    respx.post(EXPORT).mock(return_value=httpx.Response(200, text="(---)"))
    with APIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayLayoutNotFoundError):
            gw.get_report_parameters("NOPE")
        with pytest.raises(APIGatewayParameterError):
            gw.export_pdf_raw("QUT20020", [])


@respx.mock
def test_thread_safe_concurrent_exports_single_login(cfg):
    login = _mock_session()
    respx.post(EXPORT).mock(return_value=httpx.Response(200, text=PDF_B64))
    with APIGatewayClient(cfg) as gw:
        with ThreadPoolExecutor(max_workers=5) as pool:
            results = list(
                pool.map(lambda _: gw.export_pdf_raw("QUT20020", []), range(5))
            )
    assert all(r == PDF_BYTES for r in results)
    assert login.call_count == 1


@respx.mock
def test_hooks_dispatch_sync(cfg):
    _mock_session()
    respx.get(LIST).mock(
        return_value=httpx.Response(200, json={"result": "Success", "resultSet": []})
    )
    seen: list[HookContext] = []
    obs = ObservabilityConfig(hooks={"on_response": [seen.append]})
    with APIGatewayClient(cfg, observability=obs) as gw:
        gw.list_reports()
    assert [c.endpoint for c in seen] == ["/login", "/rs/v1/LoadAuthorizedCRList"]
    assert seen[0].payload is not None and seen[0].payload["Password"] == "***"
    assert seen[0].extra["service"] == "api_gateway"


@respx.mock
def test_sync_login_error_envelope_and_sentinel_retry(cfg):
    respx.post(LOGIN).mock(
        return_value=httpx.Response(
            200, json={"code": -1, "message": {"value": "Failed to login"}}
        )
    )
    with pytest.raises(APIGatewayAuthError, match="Failed to login"):
        APIGatewayClient(cfg).connect()

    _mock_session()
    route = respx.post(EXPORT)
    route.side_effect = [
        httpx.Response(200, text="(---)"),
        httpx.Response(201, text=PDF_B64),
    ]
    with APIGatewayClient(cfg) as gw:
        assert gw.export_pdf_raw("QUT20020", []) == PDF_BYTES
    assert route.call_count == 2  # sentinel once, then the PDF


@respx.mock
def test_sync_export_pdf_with_resolver(cfg):
    _mock_session()
    respx.get(LOADCR).mock(
        return_value=httpx.Response(
            200,
            json={
                "error": False,
                "resultSet": [
                    {
                        "name": "showInactive",
                        "type": "xsd:string",
                        "currentvalues": [],
                        "allowNullValue": "false",
                    },
                ],
            },
        )
    )
    export = respx.post(EXPORT).mock(return_value=httpx.Response(201, text=PDF_B64))
    with APIGatewayClient(cfg) as gw:
        gw.export_pdf(
            "RPT00001", resolver=lambda p: "N" if p.name == "showInactive" else None
        )
    assert json.loads(export.calls.last.request.read()) == [
        {"name": "showInactive", "type": "xsd:string", "value": [["N"]]}
    ]
