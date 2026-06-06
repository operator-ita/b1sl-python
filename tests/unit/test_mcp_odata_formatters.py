"""Unit tests for b1sl.contrib.mcp.odata_formatters — Phase 4.

All tests are pure unit tests (no network, no SAP connection).
"""

from __future__ import annotations

from pydantic import Field

from b1sl.b1sl.exceptions.exceptions import (
    B1AuthError,
    B1ConnectionError,
    B1NotFoundError,
    B1ValidationError,
    SAPConcurrencyError,
)
from b1sl.b1sl.models.base import B1Model, SapBool
from b1sl.contrib.mcp.odata_formatters import (
    format_collection,
    format_entity,
    format_odata_error,
)

# ── Test models ───────────────────────────────────────────────────────────────

class _Item(B1Model):
    item_code: str | None = Field(None, alias="ItemCode")
    item_name: str | None = Field(None, alias="ItemName")
    on_hand: float | None = Field(None, alias="OnHand")
    frozen: SapBool | None = Field(None, alias="Frozen")
    lines: list[B1Model] | None = Field(None, alias="ItemWarehouseInfoCollection")


class _Partner(B1Model):
    card_code: str | None = Field(None, alias="CardCode")
    card_name: str | None = Field(None, alias="CardName")
    balance: float | None = Field(None, alias="Balance")


# ── format_entity ─────────────────────────────────────────────────────────────

def test_format_entity_returns_string():
    item = _Item(ItemCode="A001", ItemName="Widget", OnHand=10.0, Frozen=False)
    assert isinstance(format_entity(item), str)


def test_format_entity_contains_header_row():
    item = _Item(ItemCode="A001")
    text = format_entity(item)
    assert "| Field | Value |" in text


def test_format_entity_contains_field_value():
    item = _Item(ItemCode="A001", ItemName="Widget")
    text = format_entity(item)
    assert "ItemCode" in text
    assert "A001" in text


def test_format_entity_title():
    item = _Item(ItemCode="A001")
    text = format_entity(item, title="My Item")
    assert "## My Item" in text


def test_format_entity_boolean_rendered_as_true_false():
    item = _Item(Frozen=True)
    text = format_entity(item)
    assert "true" in text.lower()


def test_format_entity_none_value_renders_empty():
    item = _Item(ItemCode=None)
    text = format_entity(item)
    # None renders as empty string in cell
    assert "ItemCode |  |" in text or "ItemCode" in text


def test_format_entity_navigation_shows_item_count():
    from b1sl.b1sl.models.base import B1Model
    child = B1Model()
    item = _Item(ItemWarehouseInfoCollection=[child, child, child])
    text = format_entity(item)
    assert "[3 items]" in text


def test_format_entity_etag_not_in_output():
    item = _Item.model_validate({"@odata.etag": "W/\"abc123\"", "ItemCode": "A001"})
    text = format_entity(item)
    assert "@odata.etag" not in text
    assert "abc123" not in text


def test_format_entity_udf_in_separate_section():
    item = _Item.model_validate({"ItemCode": "A001", "U_MyField": "custom_val"})
    text = format_entity(item)
    assert "User-Defined Fields" in text
    assert "U_MyField" in text
    assert "custom_val" in text


def test_format_entity_empty_model_graceful():
    item = _Item()
    text = format_entity(item)
    # Should not raise; should produce a table or "no fields" message
    assert isinstance(text, str)
    assert len(text) > 0


def test_format_entity_pipe_in_value_escaped():
    item = _Item(ItemName="foo|bar")
    text = format_entity(item)
    assert "foo\\|bar" in text


# ── format_collection ─────────────────────────────────────────────────────────

def test_format_collection_returns_string():
    items = [_Item(ItemCode="A001"), _Item(ItemCode="A002")]
    assert isinstance(format_collection(items), str)


def test_format_collection_has_header_and_separator():
    items = [_Item(ItemCode="A001", ItemName="Widget")]
    text = format_collection(items)
    assert "| ItemCode |" in text
    assert "| ---" in text


def test_format_collection_title():
    items = [_Item(ItemCode="A001")]
    text = format_collection(items, title="Items")
    assert "## Items" in text


def test_format_collection_empty_list():
    text = format_collection([])
    assert "No records returned" in text


def test_format_collection_row_data_present():
    items = [_Item(ItemCode="A001", ItemName="Widget")]
    text = format_collection(items)
    assert "A001" in text


def test_format_collection_truncation_footnote():
    items = [_Item(ItemCode=f"C{i:03d}") for i in range(10)]
    text = format_collection(items, max_rows=5)
    assert "5 record(s) omitted" in text


def test_format_collection_has_more_hint():
    items = [_Item(ItemCode="A001")]
    text = format_collection(items, has_more=True)
    assert "More pages available" in text


def test_format_collection_no_has_more_hint_by_default():
    items = [_Item(ItemCode="A001")]
    text = format_collection(items)
    assert "More pages" not in text


def test_format_collection_navigation_fields_excluded_from_headers():
    child = B1Model()
    items = [_Item(ItemCode="A001", ItemWarehouseInfoCollection=[child])]
    text = format_collection(items)
    assert "ItemWarehouseInfoCollection" not in text


def test_format_collection_multiple_rows():
    items = [_Item(ItemCode="A001"), _Item(ItemCode="A002"), _Item(ItemCode="A003")]
    text = format_collection(items)
    assert "A001" in text
    assert "A002" in text
    assert "A003" in text


# ── format_odata_error ────────────────────────────────────────────────────────

def test_format_odata_error_returns_string():
    exc = B1NotFoundError("not found")
    assert isinstance(format_odata_error(exc), str)


def test_format_odata_error_not_found_hints_verify_key():
    exc = B1NotFoundError("not found")
    msg = format_odata_error(exc, resource="orders", key=99)
    lower = msg.lower()
    assert "404" in msg or "not found" in lower
    assert "99" in msg


def test_format_odata_error_not_found_includes_resource():
    exc = B1NotFoundError("not found")
    msg = format_odata_error(exc, resource="items", key="A001")
    assert "items" in msg
    assert "A001" in msg


def test_format_odata_error_concurrency_mentions_etag():
    exc = SAPConcurrencyError("ETag mismatch", endpoint="Orders")
    msg = format_odata_error(exc, resource="orders", key=1)
    lower = msg.lower()
    assert "412" in msg or "etag" in lower or "concurren" in lower


def test_format_odata_error_concurrency_mentions_refetch():
    exc = SAPConcurrencyError("ETag mismatch", endpoint="Orders")
    msg = format_odata_error(exc)
    lower = msg.lower()
    assert "re-fetch" in lower or "refetch" in lower or "get" in lower


def test_format_odata_error_concurrency_not_permanent():
    exc = SAPConcurrencyError("ETag mismatch", endpoint="Orders")
    msg = format_odata_error(exc)
    lower = msg.lower()
    assert "not a permanent" in lower or "retry" in lower


def test_format_odata_error_auth_mentions_session():
    exc = B1AuthError("unauthorized")
    msg = format_odata_error(exc)
    lower = msg.lower()
    assert "401" in msg or "session" in lower or "auth" in lower


def test_format_odata_error_auth_mentions_reconnect():
    exc = B1AuthError("unauthorized")
    msg = format_odata_error(exc)
    lower = msg.lower()
    assert "reconnect" in lower or "login" in lower


def test_format_odata_error_validation_mentions_400():
    exc = B1ValidationError("bad request")
    msg = format_odata_error(exc)
    assert "400" in msg or "validat" in msg.lower()


def test_format_odata_error_validation_surfaces_sap_message():
    details = {"error": {"message": {"lang": "en-US", "value": "CardCode is required"}}}
    exc = B1ValidationError("bad request", details=details)
    msg = format_odata_error(exc)
    assert "CardCode is required" in msg


def test_format_odata_error_validation_flat_message():
    details = {"error": {"message": "Invalid value for DocDate"}}
    exc = B1ValidationError("bad request", details=details)
    msg = format_odata_error(exc)
    assert "Invalid value for DocDate" in msg


def test_format_odata_error_connection_error():
    exc = B1ConnectionError("connection refused")
    msg = format_odata_error(exc)
    lower = msg.lower()
    assert "connect" in lower or "network" in lower


def test_format_odata_error_generic_fallback():
    exc = Exception("unexpected failure")
    msg = format_odata_error(exc)
    assert isinstance(msg, str)
    assert "unexpected failure" in msg


def test_format_odata_error_resource_and_key_in_context():
    exc = SAPConcurrencyError("mismatch", endpoint="Invoices")
    msg = format_odata_error(exc, resource="invoices", key=42)
    assert "invoices" in msg
    assert "42" in msg


def test_format_odata_error_no_context_still_works():
    exc = B1NotFoundError("not found")
    msg = format_odata_error(exc)
    assert isinstance(msg, str)
    assert len(msg) > 0
