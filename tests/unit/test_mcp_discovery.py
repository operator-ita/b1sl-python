"""Unit tests for b1sl.contrib.mcp.discovery — Phase 2.

All tests are pure unit tests (no network, no SAP connection).
"""

from __future__ import annotations

import pytest
from pydantic import Field

from b1sl.b1sl.models.base import B1Model, SapBool
from b1sl.contrib.mcp.discovery import (
    ELITE_RESOURCES,
    FieldDescriptor,
    ResourceDescriptor,
    entity_field_catalog,
    list_elite_resources,
    resource_descriptor,
)

# ── Minimal test model ────────────────────────────────────────────────────────

class _TestModel(B1Model):
    """Minimal B1Model subclass covering each type category."""
    item_code: str | None = Field(None, alias="ItemCode")
    quantity: int | None = Field(None, alias="Quantity")
    price: float | None = Field(None, alias="Price")
    active: SapBool | None = Field(None, alias="Active")
    custom_udf: str | None = Field(None, alias="U_Custom")
    lines: list[B1Model] | None = Field(None, alias="DocumentLines")
    related: B1Model | None = Field(None, alias="RelatedObject")


# ── ELITE_RESOURCES ───────────────────────────────────────────────────────────

def test_elite_resources_is_dict():
    assert isinstance(ELITE_RESOURCES, dict)


def test_elite_resources_contains_master_data():
    for alias in ("items", "business_partners", "activities"):
        assert alias in ELITE_RESOURCES, f"Elite alias {alias!r} missing"


def test_elite_resources_contains_sales_documents():
    for alias in ("quotations", "orders", "delivery_notes", "invoices",
                  "returns", "credit_notes", "down_payments"):
        assert alias in ELITE_RESOURCES, f"Sales alias {alias!r} missing"


def test_elite_resources_contains_purchasing():
    for alias in ("purchase_requests", "purchase_quotations", "purchase_orders",
                  "purchase_delivery_notes", "purchase_invoices",
                  "purchase_returns", "purchase_credit_notes",
                  "purchase_down_payments"):
        assert alias in ELITE_RESOURCES, f"Purchasing alias {alias!r} missing"


def test_elite_resources_contains_inventory_and_correction():
    for alias in ("inventory_gen_entries", "inventory_gen_exits", "drafts",
                  "additional_expenses", "correction_invoice",
                  "correction_purchase_invoice"):
        assert alias in ELITE_RESOURCES, f"Alias {alias!r} missing"


def test_elite_resources_all_etag_safe():
    for alias, desc in ELITE_RESOURCES.items():
        assert desc.etag_safe is True, f"{alias!r} must have etag_safe=True"


def test_elite_resources_all_have_non_empty_endpoint():
    for alias, desc in ELITE_RESOURCES.items():
        assert desc.endpoint, f"{alias!r} has empty endpoint"


def test_elite_resources_all_have_non_empty_key_field():
    for alias, desc in ELITE_RESOURCES.items():
        assert desc.key_field, f"{alias!r} has empty key_field"


def test_elite_resources_all_are_resource_descriptors():
    for alias, desc in ELITE_RESOURCES.items():
        assert isinstance(desc, ResourceDescriptor), f"{alias!r} is not a ResourceDescriptor"


def test_elite_resources_count():
    assert len(ELITE_RESOURCES) == 28


# ── list_elite_resources ──────────────────────────────────────────────────────

def test_list_elite_resources_returns_list():
    assert isinstance(list_elite_resources(), list)


def test_list_elite_resources_all_descriptors():
    for item in list_elite_resources():
        assert isinstance(item, ResourceDescriptor)


def test_list_elite_resources_matches_dict():
    assert len(list_elite_resources()) == len(ELITE_RESOURCES)


def test_list_elite_resources_preserves_order():
    result = list_elite_resources()
    assert result[0].alias == "items"
    assert result[1].alias == "business_partners"


# ── resource_descriptor ───────────────────────────────────────────────────────

def test_resource_descriptor_orders():
    desc = resource_descriptor("orders")
    assert desc.endpoint == "Orders"
    assert desc.key_field == "DocEntry"
    assert desc.etag_safe is True
    assert desc.category == "sales"
    assert desc.model_name == "Document"


def test_resource_descriptor_items():
    desc = resource_descriptor("items")
    assert desc.endpoint == "Items"
    assert desc.key_field == "ItemCode"
    assert desc.model_name == "Item"
    assert desc.category == "master_data"


def test_resource_descriptor_business_partners():
    desc = resource_descriptor("business_partners")
    assert desc.key_field == "CardCode"
    assert desc.category == "master_data"


def test_resource_descriptor_unknown_raises_key_error():
    with pytest.raises(KeyError, match="Unknown Elite alias"):
        resource_descriptor("not_an_alias")


def test_resource_descriptor_error_lists_known_aliases():
    with pytest.raises(KeyError, match="items"):
        resource_descriptor("nonexistent")


# ── entity_field_catalog ──────────────────────────────────────────────────────

def test_entity_field_catalog_returns_list():
    result = entity_field_catalog(_TestModel)
    assert isinstance(result, list)
    assert len(result) > 0


def test_entity_field_catalog_all_field_descriptors():
    for f in entity_field_catalog(_TestModel):
        assert isinstance(f, FieldDescriptor)


def test_entity_field_catalog_string_field():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert "ItemCode" in catalog
    assert catalog["ItemCode"].type_label == "string"
    assert catalog["ItemCode"].is_navigation is False
    assert catalog["ItemCode"].is_udf is False


def test_entity_field_catalog_integer_field():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert catalog["Quantity"].type_label == "integer"
    assert catalog["Quantity"].is_navigation is False


def test_entity_field_catalog_float_field():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert catalog["Price"].type_label == "number"
    assert catalog["Price"].is_navigation is False


def test_entity_field_catalog_boolean_field():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    label = catalog["Active"].type_label
    assert "boolean" in label.lower()
    assert "tYES" in label
    assert catalog["Active"].is_navigation is False


def test_entity_field_catalog_collection_navigation():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert catalog["DocumentLines"].is_navigation is True
    assert catalog["DocumentLines"].type_label == "collection"


def test_entity_field_catalog_object_navigation():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert catalog["RelatedObject"].is_navigation is True
    assert catalog["RelatedObject"].type_label == "object"


def test_entity_field_catalog_skips_etag():
    names = [f.name for f in entity_field_catalog(_TestModel)]
    assert "@odata.etag" not in names


def test_entity_field_catalog_udf_detected():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert "U_Custom" in catalog
    assert catalog["U_Custom"].is_udf is True


def test_entity_field_catalog_non_udf_not_flagged():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    assert catalog["ItemCode"].is_udf is False
    assert catalog["DocumentLines"].is_udf is False


def test_entity_field_catalog_python_name_preserved():
    catalog = {f.python_name: f for f in entity_field_catalog(_TestModel)}
    assert "item_code" in catalog
    assert catalog["item_code"].name == "ItemCode"
    assert "custom_udf" in catalog
    assert catalog["custom_udf"].name == "U_Custom"


def test_entity_field_catalog_required_false_for_optional_fields():
    catalog = {f.name: f for f in entity_field_catalog(_TestModel)}
    # All _TestModel fields have None default → required=False
    for field in catalog.values():
        assert field.required is False, f"{field.name} should have required=False"
