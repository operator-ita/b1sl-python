"""VCR integration tests for ``b1sl.api_gateway`` (SAP B1 API Gateway).

Recorded once against a real gateway (test tenant), replayed offline in CI
(``make test-vcr``). The cassettes prove the *wire shape* the clients rely on
— login body, ``resultSet`` layouts, base64 export body, status codes and
headers — not the business content: everything identifying is scrubbed at
record time by the module-level ``vcr_config`` below (host, tenant,
credentials, cookies, ``CompanyID``, layout codes and names, ``DocKey``, and
the PDF itself, which is replaced by a tiny synthetic PDF).

Re-record (real gateway, test tenant only)::

    B1SL_GATEWAY_BASE_URL=https://host:60000 B1SL_GATEWAY_USERNAME=… \\
    B1SL_GATEWAY_PASSWORD=… B1SL_GATEWAY_COMPANY_DB=<test tenant> \\
    B1SL_GATEWAY_TEST_DOC_CODE=<a document-bound layout code> \\
    PYTHONPATH=src:. .venv/bin/pytest tests/integration/test_api_gateway_real.py \\
        --record-mode=once
"""

from __future__ import annotations

import base64
import json
import os
import re
from typing import Any
from urllib.parse import urlsplit

import pytest

from b1sl.api_gateway import (
    DOC_KEY_PARAM,
    OBJECT_ID_PARAM,
    APIGatewayClient,
    APIGatewayConfig,
    AsyncAPIGatewayClient,
)

PLACEHOLDER_HOST = "sap-server.example.com"
PLACEHOLDER_DOC_CODE = "LAY00001"
PLACEHOLDER_DOC_KEY = "1001"
REDACTED = "[REDACTED]"

# A minimal but valid PDF; replaces the real rendered document in cassettes.
SYNTHETIC_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)
SYNTHETIC_PDF_B64 = base64.b64encode(SYNTHETIC_PDF).decode()


def _recording(request: Any) -> bool:
    return (request.config.getoption("--record-mode") or "none") != "none"


def _real_doc_code() -> str:
    return os.environ.get("B1SL_GATEWAY_TEST_DOC_CODE", "")


def _gw_hosts() -> list[str]:
    hosts: list[str] = []
    base = os.environ.get("B1SL_GATEWAY_BASE_URL", "")
    if base:
        parts = urlsplit(base)
        if parts.netloc:
            hosts.append(parts.netloc)
        if parts.hostname and parts.hostname != parts.netloc:
            hosts.append(parts.hostname)
    return hosts


# ── Scrubbing ─────────────────────────────────────────────────────────────────


def _scrub_text(value: str) -> str:
    for host in _gw_hosts():
        value = value.replace(host, PLACEHOLDER_HOST)
    real = _real_doc_code()
    if real:
        value = value.replace(real, PLACEHOLDER_DOC_CODE)
    return value


def _scrub_request(request: Any) -> Any:
    request.uri = re.sub(r"https?://[^/]+", f"https://{PLACEHOLDER_HOST}", request.uri)
    request.uri = _scrub_text(request.uri)
    for hname in list(request.headers.keys()):
        hval = request.headers[hname]
        if isinstance(hval, str):
            request.headers[hname] = _scrub_text(hval)
    if request.body:
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return request
        if isinstance(data, dict):  # /login
            for key in list(data):
                if key.lower() in {"password", "companydb", "username"}:
                    data[key] = REDACTED
        elif isinstance(data, list):  # ExportPDFData payload
            for item in data:
                if isinstance(item, dict) and item.get("name") == DOC_KEY_PARAM:
                    item["value"] = [[PLACEHOLDER_DOC_KEY]]
        request.body = json.dumps(data).encode("utf-8")
    return request


def _scrub_parameters(rows: list[Any]) -> list[Any]:
    """Keep the shape of a ``LoadCR`` resultSet, drop anything layout-specific."""
    out = []
    n = 0
    for row in rows:
        if not isinstance(row, dict):
            continue
        row = dict(row)
        name = row.get("name")
        if name == DOC_KEY_PARAM:
            for key in ("values", "currentvalues", "defaultValues", "initialValues"):
                if row.get(key):
                    row[key] = [PLACEHOLDER_DOC_KEY]
        elif name != OBJECT_ID_PARAM:
            n += 1
            row["name"] = f"Param{n}"
            row["description"] = f"Param{n}"
        row["defaultValuesDescription"] = {}
        out.append(row)
    return out


def _scrub_response(response: Any) -> Any:
    headers = response.get("headers", {})
    for hname in list(headers.keys()):
        hl = hname.lower()
        if hl in {"set-cookie", "cookie", "authorization", "companyid"}:
            headers[hname] = [REDACTED]
        else:
            headers[hname] = [
                _scrub_text(v) if isinstance(v, str) else v for v in headers[hname]
            ]

    try:
        raw = response["body"]["string"]
        body_str = raw.decode("utf-8")
    except Exception:
        return response

    new_body: str | None = None
    try:
        data = json.loads(body_str)
    except json.JSONDecodeError:
        data = None

    if isinstance(data, dict) and isinstance(data.get("resultSet"), list):
        rows = data["resultSet"]
        if rows and isinstance(rows[0], dict) and "parameterType" in rows[0]:
            data["resultSet"] = _scrub_parameters(rows)
        else:  # LoadAuthorizedCRList — catalog names are company data
            data["resultSet"] = [
                {
                    "code": f"RPT{i:05d}",
                    "name": REDACTED,
                    "root_name": REDACTED,
                    "root_guid": str(i),
                }
                for i in range(1, min(len(rows), 3) + 1)
            ]
        new_body = json.dumps(data)
    elif data is None:
        stripped = body_str.strip()
        try:
            decoded = base64.b64decode(stripped, validate=False)
        except Exception:
            decoded = b""
        if decoded.startswith(b"%PDF-"):
            new_body = SYNTHETIC_PDF_B64
    if new_body is None:
        new_body = body_str

    new_body = _scrub_text(new_body)
    encoded = new_body.encode("utf-8")
    response["body"]["string"] = encoded
    for hname in list(headers.keys()):
        if hname.lower() == "content-length":
            headers[hname] = [str(len(encoded))]
    return response


@pytest.fixture
def vcr_config() -> dict[str, Any]:
    """Gateway-specific scrubbing (overrides the Service Layer one for this module)."""
    return {
        "filter_headers": ["Authorization", "Cookie", "Set-Cookie", "CompanyID"],
        "before_record_request": _scrub_request,
        "before_record_response": _scrub_response,
        "decode_compressed_response": True,
        "record_mode": "once",
    }


# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture
def gw_config(request) -> APIGatewayConfig:
    if _recording(request):
        cfg = APIGatewayConfig.from_env(strict=True)
        if not _real_doc_code():
            pytest.skip("B1SL_GATEWAY_TEST_DOC_CODE is required to record.")
        return cfg
    return APIGatewayConfig(
        base_url=f"https://{PLACEHOLDER_HOST}",
        username="manager",
        password=REDACTED,
        company_db=REDACTED,
        ssl_verify=False,
    )


@pytest.fixture
def doc_code(request) -> str:
    return _real_doc_code() if _recording(request) else PLACEHOLDER_DOC_CODE


# ── Tests ─────────────────────────────────────────────────────────────────────


@pytest.mark.vcr
def test_gateway_sync_flow(gw_config, doc_code):
    """login → LoadAuthorizedCRList → LoadCR → ExportPDFData, sync client."""
    with APIGatewayClient(gw_config) as gw:
        assert gw.is_session_active
        assert gw.server_session_timeout == 30

        reports = gw.list_reports()
        assert reports and all(r.code for r in reports)

        params = gw.get_report_parameters(doc_code)
        names = {p.name for p in params}
        assert DOC_KEY_PARAM in names and OBJECT_ID_PARAM in names
        doc_key = next(p for p in params if p.name == DOC_KEY_PARAM)
        assert doc_key.current_values, "layout must preload a DocKey@ to print"

        # Print the document the layout preloads (test tenant); real callers
        # always pass their own doc_entry.
        pdf = gw.export_document_pdf(
            doc_code, doc_entry=doc_key.current_values[0], parameters=params
        )
        assert pdf.startswith(b"%PDF-")
        assert len(pdf) > 100
    assert gw.is_session_active is False


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_gateway_async_flow(gw_config, doc_code):
    """Same flow through the async twin (separate cassette)."""
    async with AsyncAPIGatewayClient(gw_config) as gw:
        params = await gw.get_report_parameters(doc_code)
        doc_key = next(p for p in params if p.name == DOC_KEY_PARAM)
        pdf = await gw.export_document_pdf(
            doc_code, doc_entry=doc_key.current_values[0], parameters=params
        )
    assert pdf.startswith(b"%PDF-")
