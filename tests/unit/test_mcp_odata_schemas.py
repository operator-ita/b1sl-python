"""Unit tests for b1sl.contrib.mcp.odata_schemas — Phase 3.

All tests are pure unit tests (no network, no SAP connection).
"""

from __future__ import annotations

import pytest
from pydantic import Field

from b1sl.b1sl.models.base import B1Model, SapBool
from b1sl.contrib.mcp.odata_schemas import (
    build_resource_toolset,
    odata_create_tool_definition,
    odata_delete_tool_definition,
    odata_get_tool_definition,
    odata_list_tool_definition,
    odata_patch_tool_definition,
)

# ── Test models ───────────────────────────────────────────────────────────────

class _OrderModel(B1Model):
    """Minimal model mirroring a Document-style resource (alias='orders')."""

    doc_entry: int | None = Field(None, alias="DocEntry")
    card_code: str | None = Field(None, alias="CardCode")
    doc_total: float | None = Field(None, alias="DocTotal")
    active: SapBool | None = Field(None, alias="Active")
    lines: list[B1Model] | None = Field(None, alias="DocumentLines")


class _ItemModel(B1Model):
    """Minimal model mirroring items (alias='items', key=ItemCode/string)."""

    item_code: str | None = Field(None, alias="ItemCode")
    item_name: str | None = Field(None, alias="ItemName")
    frozen: SapBool | None = Field(None, alias="Frozen")


class _RequiredFieldModel(B1Model):
    """Model with one required field to verify CREATE required list."""

    doc_entry: int | None = Field(None, alias="DocEntry")
    card_code: str = Field(..., alias="CardCode")  # required — no default


# ── Shared assertion helpers ───────────────────────────────────────────────────

def _assert_tool_shape(tool: dict) -> None:
    assert "name" in tool
    assert "description" in tool
    assert "inputSchema" in tool
    schema = tool["inputSchema"]
    assert schema["type"] == "object"
    assert "properties" in schema


# ── odata_list_tool_definition ────────────────────────────────────────────────

def test_list_tool_name():
    tool = odata_list_tool_definition("orders", _OrderModel)
    assert tool["name"] == "orders_list"


def test_list_tool_shape():
    _assert_tool_shape(odata_list_tool_definition("orders", _OrderModel))


def test_list_tool_has_all_query_params():
    props = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    for param in ("filter", "select", "orderby", "top", "skip", "expand",
                  "page_size", "max_pages"):
        assert param in props, f"Missing query param: {param!r}"


def test_list_tool_no_required_fields():
    schema = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]
    assert "required" not in schema


def test_list_tool_filter_mentions_tyesno():
    desc = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]["filter"]["description"]
    assert "tYES" in desc
    assert "tNO" in desc


def test_list_tool_filter_mentions_case_sensitive():
    desc = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]["filter"]["description"]
    assert "case-sensitive" in desc.lower()


def test_list_tool_select_warns_100plus_fields():
    desc = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]["select"]["description"]
    assert "100+" in desc or "100" in desc


def test_list_tool_select_includes_example_fields():
    desc = odata_list_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]["select"]["description"]
    # Should contain at least one known scalar field name from _OrderModel
    assert "DocEntry" in desc or "CardCode" in desc or "DocTotal" in desc


def test_list_tool_items_alias():
    tool = odata_list_tool_definition("items", _ItemModel)
    assert tool["name"] == "items_list"


# ── odata_get_tool_definition ─────────────────────────────────────────────────

def test_get_tool_name():
    tool = odata_get_tool_definition("orders", _OrderModel)
    assert tool["name"] == "orders_get"


def test_get_tool_shape():
    _assert_tool_shape(odata_get_tool_definition("orders", _OrderModel))


def test_get_tool_key_in_required():
    schema = odata_get_tool_definition("orders", _OrderModel)["inputSchema"]
    assert "DocEntry" in schema["required"]


def test_get_tool_key_type_integer():
    props = odata_get_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert props["DocEntry"]["type"] == "integer"


def test_get_tool_key_type_string_for_items():
    props = odata_get_tool_definition("items", _ItemModel)["inputSchema"]["properties"]
    assert props["ItemCode"]["type"] == "string"


def test_get_tool_has_select_and_expand():
    props = odata_get_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert "select" in props
    assert "expand" in props


def test_get_tool_select_warns_100plus_fields():
    desc = odata_get_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]["select"]["description"]
    assert "100+" in desc or "100" in desc


# ── odata_patch_tool_definition ───────────────────────────────────────────────

def test_patch_tool_name():
    tool = odata_patch_tool_definition("orders", _OrderModel)
    assert tool["name"] == "orders_patch"


def test_patch_tool_shape():
    _assert_tool_shape(odata_patch_tool_definition("orders", _OrderModel))


def test_patch_tool_description_surgical_delta():
    desc = odata_patch_tool_definition("orders", _OrderModel)["description"]
    lower = desc.lower()
    assert "only" in lower or "surgical" in lower


def test_patch_tool_description_never_include_unmodified():
    desc = odata_patch_tool_definition("orders", _OrderModel)["description"]
    # Must warn against sending unmodified fields
    assert "never" in desc.lower() or "only" in desc.lower()


def test_patch_tool_key_only_in_required():
    schema = odata_patch_tool_definition("orders", _OrderModel)["inputSchema"]
    assert schema["required"] == ["DocEntry"]


def test_patch_tool_other_fields_optional():
    schema = odata_patch_tool_definition("orders", _OrderModel)["inputSchema"]
    required = schema.get("required", [])
    for field_name in ("CardCode", "DocTotal", "Active", "DocumentLines"):
        assert field_name not in required, f"{field_name} should be optional in PATCH"


def test_patch_tool_boolean_field_type():
    props = odata_patch_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert props["Active"]["type"] == "boolean"


def test_patch_tool_navigation_field_included():
    props = odata_patch_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert "DocumentLines" in props
    assert props["DocumentLines"]["type"] == "array"


def test_patch_tool_etag_not_in_properties():
    props = odata_patch_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert "@odata.etag" not in props


# ── odata_create_tool_definition ──────────────────────────────────────────────

def test_create_tool_name():
    tool = odata_create_tool_definition("orders", _OrderModel)
    assert tool["name"] == "orders_create"


def test_create_tool_shape():
    _assert_tool_shape(odata_create_tool_definition("orders", _OrderModel))


def test_create_tool_no_required_when_all_optional():
    schema = odata_create_tool_definition("orders", _OrderModel)["inputSchema"]
    assert "required" not in schema


def test_create_tool_required_fields_from_catalog():
    schema = odata_create_tool_definition("orders", _RequiredFieldModel)["inputSchema"]
    assert "required" in schema
    assert "CardCode" in schema["required"]
    assert "DocEntry" not in schema["required"]


def test_create_tool_navigation_field_is_array():
    props = odata_create_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert props["DocumentLines"]["type"] == "array"


# ── odata_delete_tool_definition ──────────────────────────────────────────────

def test_delete_tool_name():
    tool = odata_delete_tool_definition("orders", _OrderModel)
    assert tool["name"] == "orders_delete"


def test_delete_tool_shape():
    _assert_tool_shape(odata_delete_tool_definition("orders", _OrderModel))


def test_delete_tool_key_required():
    schema = odata_delete_tool_definition("orders", _OrderModel)["inputSchema"]
    assert schema["required"] == ["DocEntry"]


def test_delete_tool_only_key_in_properties():
    props = odata_delete_tool_definition("orders", _OrderModel)["inputSchema"]["properties"]
    assert list(props.keys()) == ["DocEntry"]


def test_delete_tool_description_irreversible():
    desc = odata_delete_tool_definition("orders", _OrderModel)["description"]
    assert "irreversible" in desc.lower()


# ── build_resource_toolset ────────────────────────────────────────────────────

def test_build_resource_toolset_returns_five_tools():
    tools = build_resource_toolset("orders", _OrderModel)
    assert len(tools) == 5


def test_build_resource_toolset_all_dicts():
    for tool in build_resource_toolset("orders", _OrderModel):
        assert isinstance(tool, dict)


def test_build_resource_toolset_name_convention():
    tools = build_resource_toolset("orders", _OrderModel)
    names = [t["name"] for t in tools]
    assert names == [
        "orders_list",
        "orders_get",
        "orders_patch",
        "orders_create",
        "orders_delete",
    ]


def test_build_resource_toolset_all_have_required_keys():
    for tool in build_resource_toolset("items", _ItemModel):
        _assert_tool_shape(tool)


def test_build_resource_toolset_unknown_alias_raises():
    with pytest.raises(KeyError, match="Unknown Elite alias"):
        build_resource_toolset("not_an_alias", _OrderModel)
