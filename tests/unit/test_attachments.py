"""Unit tests for Attachments2 support: multipart upload + binary download."""

from pathlib import Path

import httpx
import pytest

from b1sl.b1sl.exceptions.exceptions import B1NotFoundError, B1ValidationError
from b1sl.b1sl.models.multipart import SAP_FILES_FIELD, MultipartFile
from b1sl.b1sl.resources.attachments import (
    AsyncAttachmentsResource,
    AttachmentsResource,
)
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter

PDF_BYTES = b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\nbinary\x00\xff payload"

SAP_UPLOAD_RESPONSE = {
    "AbsoluteEntry": 12,
    "Attachments2_Lines": [
        {"FileName": "invoice", "FileExtension": "pdf", "LineNum": 0},
    ],
}


# ── MultipartFile ──────────────────────────────────────────────────────────────

def test_multipart_file_defaults_to_sap_files_field():
    """SAP requires every Attachments2 part to be named 'files'."""
    part = MultipartFile("invoice.pdf", PDF_BYTES)

    assert part.field_name == SAP_FILES_FIELD == "files"
    assert part.as_httpx_tuple() == (
        "files",
        ("invoice.pdf", PDF_BYTES, "application/octet-stream"),
    )


def test_multipart_file_from_path(tmp_path: Path):
    src = tmp_path / "report.pdf"
    src.write_bytes(PDF_BYTES)

    part = MultipartFile.from_path(src)

    assert part.filename == "report.pdf"
    assert part.content == PDF_BYTES
    assert part.field_name == "files"


# ── Resource: upload ───────────────────────────────────────────────────────────

def test_upload_single_file_returns_typed_entry():
    adapter = FakeRestAdapter()
    adapter.register("POST", "Attachments2", response_data=SAP_UPLOAD_RESPONSE)
    res = AttachmentsResource(adapter)

    entry = res.upload(MultipartFile("invoice.pdf", PDF_BYTES))

    assert entry.absolute_entry == 12
    call = adapter.calls[-1]
    assert call["endpoint"] == "Attachments2"
    assert [f.filename for f in call["files"]] == ["invoice.pdf"]


def test_upload_accepts_multiple_files_in_one_request():
    """SAP creates one entry with several Attachments2_Lines from one POST."""
    adapter = FakeRestAdapter()
    adapter.register("POST", "Attachments2", response_data=SAP_UPLOAD_RESPONSE)
    res = AttachmentsResource(adapter)

    res.upload([MultipartFile("a.pdf", b"a"), MultipartFile("b.png", b"b")])

    files = adapter.calls[-1]["files"]
    assert [f.filename for f in files] == ["a.pdf", "b.png"]
    # Every part uses the fixed SAP field name, not the file name.
    assert {f.field_name for f in files} == {"files"}


@pytest.mark.asyncio
async def test_async_upload_parity():
    adapter = FakeAsyncRestAdapter()
    adapter.register("POST", "Attachments2", response_data=SAP_UPLOAD_RESPONSE)
    res = AsyncAttachmentsResource(adapter)

    entry = await res.upload(MultipartFile("invoice.pdf", PDF_BYTES))

    assert entry.absolute_entry == 12
    assert [f.filename for f in adapter.calls[-1]["files"]] == ["invoice.pdf"]


# ── Resource: download ─────────────────────────────────────────────────────────

def test_download_builds_value_path_and_quoted_filename():
    adapter = FakeRestAdapter()
    adapter.register_binary("Attachments2(12)/$value", PDF_BYTES)
    res = AttachmentsResource(adapter)

    blob = res.download(12, "invoice.pdf")

    assert blob == PDF_BYTES
    call = adapter.calls[-1]
    assert call["endpoint"] == "Attachments2(12)/$value"
    # SAP expects the filename as an OData string literal (single-quoted).
    assert call["params"] == {"filename": "'invoice.pdf'"}


def test_download_joins_split_name_and_extension():
    """SAP stores FileName/FileExtension apart; callers may pass them that way."""
    adapter = FakeRestAdapter()
    adapter.register_binary("Attachments2(12)/$value", PDF_BYTES)
    res = AttachmentsResource(adapter)

    res.download(12, "invoice", "pdf")

    assert adapter.calls[-1]["params"] == {"filename": "'invoice.pdf'"}


@pytest.mark.asyncio
async def test_async_download_parity():
    adapter = FakeAsyncRestAdapter()
    adapter.register_binary("Attachments2(12)/$value", PDF_BYTES)
    res = AsyncAttachmentsResource(adapter)

    blob = await res.download(12, "invoice.pdf")

    assert blob == PDF_BYTES
    assert adapter.calls[-1]["params"] == {"filename": "'invoice.pdf'"}


# ── Adapter primitives (real adapter, mocked transport) ────────────────────────

def _adapter(monkeypatch, handler):
    """Build a real RestAdapter whose transport is a MockTransport."""
    from b1sl.b1sl.config import B1Config
    from b1sl.b1sl.rest_adapter import RestAdapter

    adapter = RestAdapter(
        B1Config(
            base_url="https://sap-server:50000/b1s/v2",
            username="manager",
            password="password",
            company_db="SBODemoES",
        )
    )
    adapter.session = httpx.Client(transport=httpx.MockTransport(handler))
    # Skip login entirely: the session is treated as already valid.
    monkeypatch.setattr(adapter, "_handle_token_login", lambda: None)
    monkeypatch.setattr(adapter, "_handle_token_logout", lambda: None)
    return adapter


def test_post_multipart_sends_form_data_not_json(monkeypatch):
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["content_type"] = request.headers["content-type"]
        seen["body"] = request.content
        return httpx.Response(201, json=SAP_UPLOAD_RESPONSE)

    adapter = _adapter(monkeypatch, handler)

    result = adapter.post_multipart(
        "Attachments2", [MultipartFile("invoice.pdf", PDF_BYTES)]
    )

    assert result.status_code == 201
    assert result.data["AbsoluteEntry"] == 12
    # httpx owns Content-Type so the boundary matches the body.
    assert seen["content_type"].startswith("multipart/form-data; boundary=")
    assert b'name="files"' in seen["body"]
    assert b'filename="invoice.pdf"' in seen["body"]
    assert PDF_BYTES in seen["body"]


def test_post_multipart_maps_sap_errors(monkeypatch):
    """The two-part JSON+binary shape from SAP's manual is rejected — 400 must map."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            json={"error": {"code": "-1000", "message": {"value": "invalid"}}},
        )

    adapter = _adapter(monkeypatch, handler)

    with pytest.raises(B1ValidationError):
        adapter.post_multipart("Attachments2", [MultipartFile("a.pdf", b"a")])


def test_post_multipart_rejects_empty_file_list(monkeypatch):
    adapter = _adapter(monkeypatch, lambda r: httpx.Response(201, json={}))

    with pytest.raises(ValueError, match="at least one file"):
        adapter.post_multipart("Attachments2", [])


def test_post_multipart_honours_dry_run(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("dry-run must not send a request")

    adapter = _adapter(monkeypatch, handler)

    with adapter.dry_run():
        result = adapter.post_multipart(
            "Attachments2", [MultipartFile("a.pdf", b"a")]
        )

    assert result.status_code == 204
    assert result.data is None


def test_get_binary_returns_raw_bytes_undecoded(monkeypatch):
    """_do() would run .json()/.text over this and corrupt it."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200, content=PDF_BYTES, headers={"Content-Type": "application/pdf"}
        )

    adapter = _adapter(monkeypatch, handler)

    blob = adapter.get_binary("Attachments2(12)/$value")

    assert blob == PDF_BYTES
    assert isinstance(blob, bytes)


def test_get_binary_maps_missing_file_to_not_found(monkeypatch):
    """SAP answers 404 -2028 when the file is gone from the attachments share."""

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"error": {"code": "-2028", "message": {"value": "a.pdf not found"}}},
        )

    adapter = _adapter(monkeypatch, handler)

    with pytest.raises(B1NotFoundError):
        adapter.get_binary("Attachments2(12)/$value")


def test_get_binary_does_not_send_if_none_match(monkeypatch):
    """A cached ETag would make SAP reply 304 with an empty body."""
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["headers"] = request.headers
        return httpx.Response(200, content=PDF_BYTES)

    adapter = _adapter(monkeypatch, handler)
    adapter._etag_cache["/Attachments2(12)/$value"] = 'W/"abc"'

    adapter.get_binary("Attachments2(12)/$value")

    assert "if-none-match" not in seen["headers"]


# ── Async adapter primitives (parity with the sync transport tests) ────────────

def _async_adapter(monkeypatch, handler):
    """Build a real AsyncRestAdapter whose transport is a MockTransport."""
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
    from b1sl.b1sl.config import B1Config

    adapter = AsyncRestAdapter(
        B1Config(
            base_url="https://sap-server:50000/b1s/v2",
            username="manager",
            password="password",
            company_db="SBODemoES",
        )
    )
    adapter._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))

    async def _noop(*args, **kwargs):
        return None

    monkeypatch.setattr(adapter, "ensure_session", _noop)
    return adapter


@pytest.mark.asyncio
async def test_async_post_multipart_sends_form_data(monkeypatch):
    seen: dict = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["content_type"] = request.headers["content-type"]
        seen["body"] = request.content
        return httpx.Response(201, json=SAP_UPLOAD_RESPONSE)

    adapter = _async_adapter(monkeypatch, handler)

    result = await adapter.post_multipart(
        "Attachments2", [MultipartFile("invoice.pdf", PDF_BYTES)]
    )

    assert result.data["AbsoluteEntry"] == 12
    assert seen["content_type"].startswith("multipart/form-data; boundary=")
    assert b'name="files"' in seen["body"]
    assert PDF_BYTES in seen["body"]


@pytest.mark.asyncio
async def test_async_post_multipart_honours_dry_run(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("dry-run must not send a request")

    adapter = _async_adapter(monkeypatch, handler)

    with adapter.dry_run():
        result = await adapter.post_multipart(
            "Attachments2", [MultipartFile("a.pdf", b"a")]
        )

    assert result.status_code == 204


@pytest.mark.asyncio
async def test_async_get_binary_returns_raw_bytes(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, content=PDF_BYTES)

    adapter = _async_adapter(monkeypatch, handler)

    blob = await adapter.get_binary("Attachments2(12)/$value")

    assert blob == PDF_BYTES


@pytest.mark.asyncio
async def test_async_get_binary_maps_missing_file_to_not_found(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            404,
            json={"error": {"code": "-2028", "message": {"value": "a.pdf not found"}}},
        )

    adapter = _async_adapter(monkeypatch, handler)

    with pytest.raises(B1NotFoundError):
        await adapter.get_binary("Attachments2(12)/$value")


# ── Public client surface (no _adapter access needed) ─────────────────────────

def _client_with(adapter):
    """Build a B1Client bound to a pre-made adapter, skipping connect()."""
    from b1sl.b1sl.client import B1Client
    from b1sl.b1sl.config import B1Config

    client = B1Client(
        B1Config(
            base_url="https://sap-server:50000/b1s/v2",
            username="manager",
            password="password",
            company_db="SBODemoES",
        )
    )
    client._adapter = adapter
    return client


def test_client_exposes_multipart_and_binary_publicly():
    """The gateway use case: uploads/downloads without touching private attrs."""
    adapter = FakeRestAdapter()
    adapter.register("POST", "Attachments2", response_data=SAP_UPLOAD_RESPONSE)
    adapter.register_binary("Attachments2(12)/$value", PDF_BYTES)
    client = _client_with(adapter)

    data = client.post_multipart("Attachments2", MultipartFile("a.pdf", b"a"))
    assert data["AbsoluteEntry"] == 12

    blob = client.get_binary("Attachments2(12)/$value", {"filename": "'a.pdf'"})
    assert blob == PDF_BYTES
    assert adapter.calls[-1]["params"] == {"filename": "'a.pdf'"}


def test_client_attachments_property_returns_typed_resource():
    adapter = FakeRestAdapter()
    adapter.register("POST", "Attachments2", response_data=SAP_UPLOAD_RESPONSE)
    client = _client_with(adapter)

    entry = client.attachments.upload(MultipartFile("invoice.pdf", PDF_BYTES))

    assert entry.absolute_entry == 12


# ── $batch interaction ─────────────────────────────────────────────────────────

def test_batch_rejects_file_upload_with_a_clear_error():
    """A $batch body is already multipart — uploads cannot nest inside it."""
    from b1sl.b1sl.batch._recording_adapter import _SyncRecordingAdapter

    adapter = _SyncRecordingAdapter.__new__(_SyncRecordingAdapter)

    with pytest.raises(NotImplementedError, match="cannot be recorded inside a .batch"):
        adapter.post_multipart("Attachments2", [MultipartFile("a.pdf", b"a")])

    with pytest.raises(NotImplementedError, match="cannot be recorded inside a .batch"):
        adapter.get_binary("Attachments2(12)/$value")
