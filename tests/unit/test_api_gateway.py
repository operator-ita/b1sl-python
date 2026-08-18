"""Unit tests for ``b1sl.api_gateway`` — the SAP B1 API Gateway client.

All HTTP is mocked with respx. Wire shapes mirror what was observed live on
SAP B1 2511 (HANA): base64 text on ``ExportPDFData``, ``(---)`` sentinel on
malformed payloads, ``{}`` on unknown ``DocCode``, stringly booleans in
``LoadCR``.
"""

from __future__ import annotations

import base64
from datetime import date, datetime, timedelta
from decimal import Decimal

import httpx
import pytest
import respx

from b1sl.api_gateway import (
    APIGatewayAuthError,
    APIGatewayConfig,
    APIGatewayConnectionError,
    APIGatewayError,
    APIGatewayLayoutNotFoundError,
    APIGatewayParameterError,
    APIGatewayPDFError,
    APIGatewayResponseError,
    AsyncAPIGatewayClient,
    ReportParameter,
    build_export_payload,
    format_value,
)
from b1sl.b1sl.base_adapter import HookContext, ObservabilityConfig
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.exceptions.exceptions import B1AuthError, B1ConnectionError

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
        ("set-cookie", "Session=abc123; Path=/; HttpOnly"),
        ("set-cookie", "Cookie=xyz789; Path=/; HttpOnly"),
    ],
)


def _param(name, type_, current, allow_null="false", ptype="ReportParameter"):
    """Build a LoadCR row with the real 20-key shape (subset that matters)."""
    return {
        "parameterType": ptype,
        "values": list(current),
        "name": name,
        "description": name,
        "type": type_,
        "allowNullValue": allow_null,
        "allowMultiValue": "false",
        "isOptionalPrompt": "false",
        "currentvalues": list(current),
        "defaultValues": [],
        "initialValues": [],
    }


QUOTATION_PARAMS = [
    _param("ObjectId@", "xsd:decimal", ["23"], "true", "StoredProcedureParameter"),
    _param("DocKey@", "xsd:decimal", ["777"], "true", "StoredProcedureParameter"),
    _param("Pm-Optional.Text", "xsd:string", [], "true"),
]

LOADCR_OK = {"result": "Success", "resultSet": QUOTATION_PARAMS}


@pytest.fixture
def cfg():
    return APIGatewayConfig(
        base_url=BASE + "/",
        username="manager",
        password="secret",
        company_db="SBO_TEST",
    )


# ── Config ─────────────────────────────────────────────────────────────────────


def test_config_strips_trailing_slash_and_hides_password(cfg):
    assert cfg.base_url == BASE
    assert "secret" not in repr(cfg)


def test_config_from_env_falls_back_to_service_layer_vars(monkeypatch):
    monkeypatch.setenv("B1SL_GATEWAY_BASE_URL", "https://gw:60000")
    monkeypatch.setenv("B1SL_USERNAME", "sl_user")
    monkeypatch.setenv("B1SL_PASSWORD", "sl_pass")
    monkeypatch.setenv("B1SL_COMPANY_DB", "SBO_TEST")
    monkeypatch.setenv("B1SL_SSL_VERIFY", "0")
    monkeypatch.delenv("B1SL_GATEWAY_USERNAME", raising=False)
    monkeypatch.setenv("B1SL_GATEWAY_SESSION_TTL", "45")
    monkeypatch.setenv("B1SL_GATEWAY_MAX_CONCURRENT_EXPORTS", "0")

    c = APIGatewayConfig.from_env()

    assert c.username == "sl_user"
    assert c.company_db == "SBO_TEST"
    assert c.ssl_verify is False
    assert c.session_ttl == timedelta(seconds=45)
    assert c.max_concurrent_exports is None  # 0 disables the bound
    assert (
        APIGatewayConfig(
            base_url=BASE, username="u", password="p", company_db="d"
        ).max_concurrent_exports
        == 3
    )


def test_config_from_env_gateway_vars_win(monkeypatch):
    monkeypatch.setenv("B1SL_GATEWAY_BASE_URL", "https://gw:60000")
    monkeypatch.setenv("B1SL_USERNAME", "sl_user")
    monkeypatch.setenv("B1SL_PASSWORD", "sl_pass")
    monkeypatch.setenv("B1SL_COMPANY_DB", "SBO_PROD")
    monkeypatch.setenv("B1SL_GATEWAY_COMPANY_DB", "SBO_TEST")
    monkeypatch.setenv("B1SL_SSL_VERIFY", "0")
    monkeypatch.setenv("B1SL_GATEWAY_SSL_VERIFY", "1")

    c = APIGatewayConfig.from_env()

    assert c.company_db == "SBO_TEST"
    assert c.ssl_verify is True


def test_config_from_env_strict_requires_gateway_url(monkeypatch):
    monkeypatch.delenv("B1SL_GATEWAY_BASE_URL", raising=False)
    monkeypatch.setenv("B1SL_USERNAME", "u")
    monkeypatch.setenv("B1SL_PASSWORD", "p")
    monkeypatch.setenv("B1SL_COMPANY_DB", "db")
    with pytest.raises(EnvironmentError, match="B1SL_GATEWAY_BASE_URL"):
        APIGatewayConfig.from_env()
    assert APIGatewayConfig.from_env(strict=False).base_url == "https://dummy:60000"


def test_config_from_b1_config():
    sl = B1Config(
        base_url="https://sap:50000/b1s/v2",
        username="manager",
        password="pw",
        company_db="SBO_TEST",
        ssl_verify=False,
    )
    c = APIGatewayConfig.from_b1_config(sl, "https://sap:60000", ssl_verify=True)
    assert (c.username, c.password, c.company_db) == ("manager", "pw", "SBO_TEST")
    assert c.base_url == "https://sap:60000"
    assert c.ssl_verify is True
    assert c.read_timeout >= 120


@pytest.mark.parametrize("field", ["base_url", "username", "password", "company_db"])
def test_config_rejects_empty_required(field):
    kwargs: dict[str, str] = dict(
        base_url=BASE, username="u", password="p", company_db="db"
    )
    kwargs[field] = ""
    with pytest.raises(ValueError):
        APIGatewayConfig(**kwargs)  # type: ignore[arg-type]


# ── Payload builder ────────────────────────────────────────────────────────────


def test_report_parameter_parses_stringly_booleans():
    p = ReportParameter.from_wire(QUOTATION_PARAMS[2])
    assert p.allow_null is True
    assert p.is_optional_empty is True
    assert p.parameter_type == "ReportParameter"
    assert p.raw["isOptionalPrompt"] == "false"


def test_build_payload_omits_empty_optional_and_overrides_dockey():
    params = [ReportParameter.from_wire(r) for r in QUOTATION_PARAMS]
    payload = build_export_payload(params, {"DocKey@": 12345})
    assert payload == [
        {"name": "ObjectId@", "type": "xsd:decimal", "value": [["23"]]},
        {"name": "DocKey@", "type": "xsd:decimal", "value": [["12345"]]},
    ]


def test_build_payload_rejects_unknown_name_in_strict_mode():
    params = [ReportParameter.from_wire(r) for r in QUOTATION_PARAMS]
    with pytest.raises(APIGatewayParameterError, match="Unknown parameter"):
        build_export_payload(params, {"DocKey": 1})
    # non-strict silently ignores it
    assert len(build_export_payload(params, {"DocKey": 1}, strict=False)) == 2


def test_build_payload_requires_value_for_empty_non_nullable():
    params = [ReportParameter.from_wire(_param("Flag", "xsd:string", [], "false"))]
    with pytest.raises(APIGatewayParameterError, match="required"):
        build_export_payload(params)
    assert build_export_payload(params, {"Flag": "N"}) == [
        {"name": "Flag", "type": "xsd:string", "value": [["N"]]}
    ]


def test_build_payload_date_needs_explicit_value_and_formats_iso():
    row = _param("RangeDate@", "xsd:date", ["Date(2026, 6, 7) to Date(2026, 6, 13)"])
    params = [ReportParameter.from_wire(row)]
    with pytest.raises(APIGatewayParameterError, match="Date parameter"):
        build_export_payload(params)
    payload = build_export_payload(
        params, {"RangeDate@": (date(2026, 6, 7), datetime(2026, 6, 13, 10, 0))}
    )
    assert payload == [
        {
            "name": "RangeDate@",
            "type": "xsd:date",
            "value": [["2026-06-07", "2026-06-13"]],
        }
    ]


def test_format_value_shapes():
    assert format_value("12345") == [["12345"]]
    assert format_value(Decimal("1.50")) == [["1.50"]]
    assert format_value(["a", "b"]) == [["a", "b"]]
    assert format_value([["a"], ["b", "c"]]) == [["a"], ["b", "c"]]
    with pytest.raises(APIGatewayParameterError, match="bool"):
        format_value(True)
    with pytest.raises(APIGatewayParameterError, match="Unsupported"):
        format_value(object())


# ── Session lifecycle ──────────────────────────────────────────────────────────


@pytest.mark.asyncio
@respx.mock
async def test_login_sends_company_db_and_stores_cookies(cfg):
    login = respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))

    async with AsyncAPIGatewayClient(cfg) as gw:
        assert gw.is_session_active
        assert gw.server_session_timeout == 30
        # Reactive by default: the reported SessionTimeout is not trusted
        # (its unit is unknown), so no proactive expiry is scheduled.
        assert gw.token_expiry is None
        sent = login.calls.last.request
        body = sent.read()
        assert b'"CompanyDB": "SBO_TEST"' in body or b'"CompanyDB":"SBO_TEST"' in body
        assert gw._client is not None
        assert gw._client.cookies.get("Session") == "abc123"
        assert gw._client.cookies.get("Cookie") == "xyz789"

    assert gw.is_session_active is False
    assert gw._client is None


@pytest.mark.asyncio
@respx.mock
async def test_login_failure_raises_auth_error(cfg):
    respx.post(LOGIN).mock(return_value=httpx.Response(401, json={"error": "bad"}))
    gw = AsyncAPIGatewayClient(cfg)
    with pytest.raises(APIGatewayAuthError) as exc:
        await gw.connect()
    assert isinstance(exc.value, B1AuthError)
    assert isinstance(exc.value, APIGatewayError)
    assert gw.is_session_active is False
    await gw.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_unreachable_host_maps_to_connection_error(cfg):
    respx.post(LOGIN).mock(side_effect=httpx.ConnectError("refused"))
    gw = AsyncAPIGatewayClient(cfg)
    with pytest.raises(APIGatewayConnectionError) as exc:
        await gw.connect()
    assert isinstance(exc.value, B1ConnectionError)
    assert "API Gateway" in str(exc.value)
    await gw.aclose()


@pytest.mark.asyncio
@respx.mock
async def test_session_lost_status_triggers_single_relogin(cfg):
    login = respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.get(LIST)
    route.side_effect = [
        httpx.Response(401),
        httpx.Response(200, json={"result": "Success", "resultSet": []}),
    ]
    async with AsyncAPIGatewayClient(cfg) as gw:
        assert await gw.list_reports() == []
    assert login.call_count == 2
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_session_lost_twice_raises_auth_error(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LIST).mock(return_value=httpx.Response(403, text="forbidden"))
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayAuthError, match="Report Layout API"):
            await gw.list_reports()


@pytest.mark.asyncio
@respx.mock
async def test_expired_session_relogs_in_proactively(cfg):
    login = respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LIST).mock(
        return_value=httpx.Response(200, json={"result": "Success", "resultSet": []})
    )
    async with AsyncAPIGatewayClient(cfg) as gw:
        gw.token_expiry = datetime.now() - timedelta(seconds=1)
        await gw.list_reports()
    assert login.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_session_ttl_enables_proactive_expiry():
    cfg = APIGatewayConfig(
        base_url=BASE,
        username="u",
        password="p",
        company_db="db",
        session_ttl=timedelta(seconds=30),
    )
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    async with AsyncAPIGatewayClient(cfg) as gw:
        assert gw.token_expiry is not None
        remaining = gw.token_expiry - datetime.now()
        # 30s minus min(60s, 30s/4=7.5s) margin
        assert timedelta(seconds=20) < remaining <= timedelta(seconds=23)


@pytest.mark.asyncio
async def test_request_before_connect_raises(cfg):
    gw = AsyncAPIGatewayClient(cfg)
    with pytest.raises(APIGatewayError, match="not connected"):
        await gw.list_reports()


# ── Endpoints ──────────────────────────────────────────────────────────────────


@pytest.mark.asyncio
@respx.mock
async def test_list_reports(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LIST).mock(
        return_value=httpx.Response(
            200,
            json={
                "result": "Success",
                "resultSet": [
                    {
                        "code": "RCRI0009",
                        "root_name": "#1000004#8",
                        "name": "articulos",
                        "root_guid": "63",
                    }
                ],
            },
        )
    )
    async with AsyncAPIGatewayClient(cfg) as gw:
        reports = await gw.list_reports()
    assert len(reports) == 1
    assert reports[0].code == "RCRI0009"
    assert reports[0].name == "articulos"
    assert reports[0].raw["root_guid"] == "63"


@pytest.mark.asyncio
@respx.mock
async def test_get_report_parameters(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.get(LOADCR).mock(return_value=httpx.Response(200, json=LOADCR_OK))
    async with AsyncAPIGatewayClient(cfg) as gw:
        params = await gw.get_report_parameters("QUT20020")
    assert route.calls.last.request.url.params["DocCode"] == "QUT20020"
    assert [p.name for p in params] == ["ObjectId@", "DocKey@", "Pm-Optional.Text"]
    assert params[1].current_values == ["777"]
    assert params[2].is_optional_empty


@pytest.mark.asyncio
@respx.mock
async def test_unknown_doc_code_empty_body_raises_layout_not_found(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LOADCR).mock(return_value=httpx.Response(200, json={}))
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayLayoutNotFoundError) as exc:
            await gw.get_report_parameters("QUT99999")
    assert exc.value.doc_code == "QUT99999"


@pytest.mark.asyncio
@respx.mock
async def test_result_not_success_raises_response_error(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LIST).mock(
        return_value=httpx.Response(
            200, json={"result": "Failure", "message": "internal"}
        )
    )
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayResponseError, match="internal"):
            await gw.list_reports()


@pytest.mark.asyncio
@respx.mock
async def test_export_document_pdf_end_to_end(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LOADCR).mock(return_value=httpx.Response(200, json=LOADCR_OK))
    export = respx.post(EXPORT).mock(return_value=httpx.Response(201, text=PDF_B64))

    async with AsyncAPIGatewayClient(cfg) as gw:
        pdf = await gw.export_document_pdf("QUT20020", doc_entry=12345)

    assert pdf == PDF_BYTES
    req = export.calls.last.request
    assert req.url.params["DocCode"] == "QUT20020"
    import json

    body = json.loads(req.read())
    assert body == [
        {"name": "ObjectId@", "type": "xsd:decimal", "value": [["23"]]},
        {"name": "DocKey@", "type": "xsd:decimal", "value": [["12345"]]},
    ]


@pytest.mark.asyncio
@respx.mock
async def test_export_document_pdf_object_id_override_and_cached_params(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    loadcr = respx.get(LOADCR).mock(return_value=httpx.Response(200, json=LOADCR_OK))
    export = respx.post(EXPORT).mock(return_value=httpx.Response(201, text=PDF_B64))

    async with AsyncAPIGatewayClient(cfg) as gw:
        params = await gw.get_report_parameters("QUT20020")
        await gw.export_document_pdf(
            "QUT20020", doc_entry="1", object_id=17, parameters=params
        )
        await gw.export_document_pdf("QUT20020", doc_entry="2", parameters=params)

    assert loadcr.call_count == 1
    import json

    first = json.loads(export.calls[0].request.read())
    assert first[0] == {"name": "ObjectId@", "type": "xsd:decimal", "value": [["17"]]}


@pytest.mark.asyncio
@respx.mock
async def test_export_document_pdf_rejects_non_document_layout(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LOADCR).mock(
        return_value=httpx.Response(
            200,
            json={
                "result": "Success",
                "resultSet": [_param("showInactiveEmployee", "xsd:string", ["N"])],
            },
        )
    )
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayParameterError, match="not a document-bound"):
            await gw.export_document_pdf("RCRI0018", doc_entry=1)


@pytest.mark.asyncio
@respx.mock
async def test_export_malformed_payload_sentinel_raises_parameter_error(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.post(EXPORT).mock(return_value=httpx.Response(200, text="(---)"))
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayParameterError, match=r"\(---\)"):
            await gw.export_pdf_raw(
                "QUT20020", [{"name": "x", "type": "t", "value": ""}]
            )


@pytest.mark.asyncio
@respx.mock
async def test_export_non_pdf_body_raises_pdf_error(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    not_pdf = base64.b64encode(b"<html>error</html>").decode()
    respx.post(EXPORT).mock(return_value=httpx.Response(201, text=not_pdf))
    async with AsyncAPIGatewayClient(cfg) as gw:
        with pytest.raises(APIGatewayPDFError, match="not a PDF"):
            await gw.export_pdf_raw("QUT20020", [])


@pytest.mark.asyncio
@respx.mock
async def test_export_accepts_raw_pdf_or_quoted_base64(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.post(EXPORT)
    route.side_effect = [
        httpx.Response(201, content=PDF_BYTES),
        httpx.Response(201, text=f'"{PDF_B64}"'),
    ]
    async with AsyncAPIGatewayClient(cfg) as gw:
        assert await gw.export_pdf_raw("X", []) == PDF_BYTES
        assert await gw.export_pdf_raw("X", []) == PDF_BYTES


@pytest.mark.asyncio
@respx.mock
async def test_export_pdf_with_catalog_report_dates(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LOADCR).mock(
        return_value=httpx.Response(
            200,
            json={
                "result": "Success",
                "resultSet": [
                    _param(
                        "RangeDate@",
                        "xsd:date",
                        ["Date(2026, 6, 7) to Date(2026, 6, 13)"],
                    ),
                    _param("showInactiveEmployee", "xsd:string", ["N"]),
                ],
            },
        )
    )
    export = respx.post(EXPORT).mock(return_value=httpx.Response(201, text=PDF_B64))
    async with AsyncAPIGatewayClient(cfg) as gw:
        await gw.export_pdf(
            "RCRI0018", {"RangeDate@": (date(2026, 6, 7), date(2026, 6, 13))}
        )
    import json

    assert json.loads(export.calls.last.request.read()) == [
        {
            "name": "RangeDate@",
            "type": "xsd:date",
            "value": [["2026-06-07", "2026-06-13"]],
        },
        {"name": "showInactiveEmployee", "type": "xsd:string", "value": [["N"]]},
    ]


# ── Observability ──────────────────────────────────────────────────────────────


@pytest.mark.asyncio
@respx.mock
async def test_hooks_receive_context_with_service_tag(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.get(LIST).mock(
        return_value=httpx.Response(200, json={"result": "Success", "resultSet": []})
    )
    seen: list[HookContext] = []
    obs = ObservabilityConfig(hooks={"on_response": [seen.append]})
    async with AsyncAPIGatewayClient(cfg, observability=obs) as gw:
        await gw.list_reports()

    endpoints = [c.endpoint for c in seen]
    assert endpoints == ["/login", "/rs/v1/LoadAuthorizedCRList"]
    assert all(c.extra["service"] == "api_gateway" for c in seen)
    assert seen[0].payload is not None
    assert seen[0].payload["Password"] == "***"
    assert seen[0].db == "SBO_TEST"


@pytest.mark.asyncio
@respx.mock
async def test_export_accepts_200_with_pdf_body_under_concurrency(cfg):
    """Observed live: isolated exports answer 201, concurrent ones on the same
    session answer 200. Success is decided by the body, never by 200 vs 201."""
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    respx.post(EXPORT).mock(
        return_value=httpx.Response(
            200,
            content=PDF_B64.encode(),
            headers={"Content-Type": "application/octet-stream"},
        )
    )
    import asyncio

    async with AsyncAPIGatewayClient(cfg) as gw:
        results = await asyncio.gather(
            *(gw.export_pdf_raw("QUT20020", []) for _ in range(3))
        )
    assert all(r == PDF_BYTES for r in results)


@pytest.mark.asyncio
@respx.mock
async def test_unauthenticated_401_empty_body_triggers_relogin(cfg):
    """Observed live: without a session cookie the gateway answers a bare
    ``401`` with ``Content-Length: 0`` — no body, no WWW-Authenticate."""
    login = respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.get(LOADCR)
    route.side_effect = [
        httpx.Response(401, headers={"content-length": "0"}),
        httpx.Response(200, json=LOADCR_OK),
    ]
    async with AsyncAPIGatewayClient(cfg) as gw:
        params = await gw.get_report_parameters("QUT20020")
    assert len(params) == 3
    assert login.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_export_retries_once_on_sentinel_then_raises(cfg):
    """Observed live: under concurrent exports the gateway answers '(---)' for
    some calls (1/5, 3/5). The client retries once, then surfaces the error."""
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.post(EXPORT)
    route.side_effect = [
        httpx.Response(200, text="(---)"),
        httpx.Response(201, text=PDF_B64),
        httpx.Response(200, text="(---)"),
        httpx.Response(200, text="(---)"),
    ]
    async with AsyncAPIGatewayClient(cfg) as gw:
        assert await gw.export_pdf_raw("QUT20020", []) == PDF_BYTES
        assert route.call_count == 2
        with pytest.raises(APIGatewayParameterError, match="retried once"):
            await gw.export_pdf_raw("QUT20020", [])
    assert route.call_count == 4


@pytest.mark.asyncio
@respx.mock
async def test_export_concurrency_is_bounded_by_config():
    """max_concurrent_exports=2: five parallel exports never overlap more than 2."""
    import asyncio

    cfg = APIGatewayConfig(
        base_url=BASE,
        username="u",
        password="p",
        company_db="db",
        max_concurrent_exports=2,
    )
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    in_flight = {"now": 0, "max": 0}

    async def slow_export(request):
        in_flight["now"] += 1
        in_flight["max"] = max(in_flight["max"], in_flight["now"])
        await asyncio.sleep(0.02)
        in_flight["now"] -= 1
        return httpx.Response(201, text=PDF_B64)

    respx.post(EXPORT).mock(side_effect=slow_export)
    async with AsyncAPIGatewayClient(cfg) as gw:
        results = await asyncio.gather(*(gw.export_pdf_raw("X", []) for _ in range(5)))
    assert all(r == PDF_BYTES for r in results)
    assert in_flight["max"] == 2


@pytest.mark.asyncio
@respx.mock
async def test_login_error_envelope_with_200_is_auth_error(cfg):
    """Observed live: bad password / unknown CompanyDB answer HTTP 200 with
    {"code":-1,"message":{"value":"Failed to login…"}} and no cookie."""
    respx.post(LOGIN).mock(
        return_value=httpx.Response(
            200,
            json={
                "code": -1,
                "message": {
                    "lang": "en-us",
                    "value": "Failed to login for current user, please double check and retry",
                },
            },
        )
    )
    gw = AsyncAPIGatewayClient(cfg)
    with pytest.raises(APIGatewayAuthError, match=r"\[-1\] Failed to login"):
        await gw.connect()
    assert gw.is_session_active is False
    await gw.aclose()


def test_error_envelope_helper():
    from b1sl.api_gateway._base import error_envelope

    assert error_envelope({"Version": "0.0.1", "SessionTimeout": 30}) is None
    assert error_envelope({"code": 0, "message": "ok"}) is None
    assert (
        error_envelope({"code": 400, "message": "400 BAD_REQUEST"})
        == "[400] 400 BAD_REQUEST"
    )
    assert error_envelope({"code": -1, "message": {"value": "nope"}}) == "[-1] nope"
    assert error_envelope("(---)") is None


@pytest.mark.asyncio
@respx.mock
async def test_logout_sends_json_body_and_clears_state(cfg):
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    logout = respx.post(LOGOUT).mock(return_value=httpx.Response(415))
    async with AsyncAPIGatewayClient(cfg) as gw:
        pass
    assert logout.call_count == 1
    req = logout.calls.last.request
    assert req.headers["content-type"].startswith("application/json")
    assert req.read() == b"{}"
    assert gw.is_session_active is False


def test_config_from_django_settings(monkeypatch):
    pytest.importorskip("django")
    from django.conf import settings

    if not settings.configured:
        settings.configure()
    for k, v in {
        "B1SL_GATEWAY_BASE_URL": "https://gw:60000/",
        "B1SL_USERNAME": "dj_user",
        "B1SL_PASSWORD": "dj_pass",
        "B1SL_COMPANY_DB": "SBO_TEST",
        "B1SL_SSL_VERIFY": False,
        "B1SL_GATEWAY_SESSION_TTL": 90,
    }.items():
        monkeypatch.setattr(settings, k, v, raising=False)

    c = APIGatewayConfig.from_django_settings()

    assert c.base_url == "https://gw:60000"
    assert (c.username, c.password, c.company_db) == ("dj_user", "dj_pass", "SBO_TEST")
    assert c.ssl_verify is False
    assert c.session_ttl == timedelta(seconds=90)
    assert c.max_concurrent_exports == 3


def test_import_b1sl_does_not_load_api_gateway():
    """The gateway is opt-in: ``import b1sl`` / the SL surface must never pull it."""
    import subprocess
    import sys

    code = (
        "import sys, b1sl; from b1sl import AsyncB1Client; "
        "print('b1sl.api_gateway' in sys.modules)"
    )
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert out.stdout.strip() == "False"


@pytest.mark.asyncio
@respx.mock
async def test_loadcr_error_flag_and_error_false_shape(cfg):
    """Live: LoadCR answers {"error": false, "resultSet": [...]} (no "result").
    error=true is treated as a gateway-reported failure."""
    respx.post(LOGIN).mock(return_value=LOGIN_OK)
    respx.post(LOGOUT).mock(return_value=httpx.Response(200))
    route = respx.get(LOADCR)
    route.side_effect = [
        httpx.Response(200, json={"error": False, "resultSet": QUOTATION_PARAMS}),
        httpx.Response(200, json={"error": True, "resultSet": [], "message": "boom"}),
    ]
    async with AsyncAPIGatewayClient(cfg) as gw:
        assert len(await gw.get_report_parameters("QUT20020")) == 3
        with pytest.raises(APIGatewayResponseError, match="boom"):
            await gw.get_report_parameters("QUT20020")
