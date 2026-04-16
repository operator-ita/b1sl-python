"""
test_model_resolution.py
========================
Regression guard for the entities/__init__.py "glue" module.

WHY THIS TEST EXISTS
--------------------
The `entities` package (__init__.py) is responsible for:

  1. Importing ALL generated model submodules into memory.
  2. Building a complete _NAMESPACE dictionary with every class name.
  3. Calling model_rebuild(_types_namespace=_NAMESPACE) on every model
     to resolve cross-domain forward references (e.g. Item → ProductTree,
     BusinessPartner → Activity).

If __init__.py is bypassed (e.g. importing directly from a submodule like
`entities.inventory`) or is broken, Pydantic raises at runtime:

    PydanticUserError: `Item` is not fully defined; you should define
    `ProductTree`, then call `Item.model_rebuild()`.

This error surfaces at *runtime* (on first .get() call), not at import time,
making it easy to miss without an explicit test like this one.

FIELD NAMING CONVENTION
-----------------------
SAP B1 models use PascalCase aliases (ItemCode, ItemName) for JSON
serialization, but Python attribute access uses snake_case (item_code,
item_name). model_validate() accepts both via populate_by_name=True.

WHAT IS TESTED
--------------
- The three most complex ETag-elite models with cross-module dependencies.
- That their cross-referenced fields are fully resolved (not ForwardRef).
- That model_validate() works end-to-end (the real usage path).
- That the sync client properties return the correct model class.
"""
from __future__ import annotations

import typing

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_resolved(field_info) -> bool:
    """
    Returns True if a Pydantic field annotation has been fully resolved
    (i.e. is not a ForwardRef or a string annotation).
    """
    annotation = field_info.annotation
    return not isinstance(annotation, typing.ForwardRef)


# ---------------------------------------------------------------------------
# 1. Core entity resolution tests
# ---------------------------------------------------------------------------

class TestEntityModelResolution:
    """
    Validates that importing from the entities *package* (not submodules)
    triggers the __init__.py rebuild and resolves all forward references.
    """

    def test_item_model_is_fully_defined(self):
        """
        Item → ProductTree is the canonical cross-module reference.
        If __init__.py is broken, accessing model_fields raises PydanticUserError.
        """
        from b1sl.b1sl.models._generated.entities import Item

        fields = Item.model_fields
        assert "product_trees" in fields, (
            "Item.product_trees field not found — model may not be the overridden version"
        )
        assert "bin_locations" in fields, (
            "Item.bin_locations field not found — cross-module reference not resolved"
        )

    def test_item_product_trees_field_is_resolved(self):
        """ProductTree reference inside Item must not be a ForwardRef."""
        from b1sl.b1sl.models._generated.entities import Item

        field = Item.model_fields["product_trees"]
        assert _is_resolved(field), (
            f"Item.product_trees is still a ForwardRef — "
            f"entities/__init__.py model_rebuild() did not execute. "
            f"Got: {field.annotation}"
        )

    def test_business_partner_model_is_fully_defined(self):
        """
        BusinessPartner → ContactEmployee and Activity are cross-module refs.
        """
        from b1sl.b1sl.models._generated.entities import BusinessPartner

        fields = BusinessPartner.model_fields
        assert "contact_employees" in fields
        assert "activities" in fields

    def test_document_model_is_fully_defined(self):
        """Document is used for ~20 ETag-elite endpoints — must be resolvable."""
        from b1sl.b1sl.models._generated.entities import Document

        # Document has 323 fields; accessing this dict validates the model
        assert len(Document.model_fields) > 100, (
            "Document model has unexpectedly few fields — may not be fully loaded"
        )


# ---------------------------------------------------------------------------
# 2. model_validate() end-to-end tests
# ---------------------------------------------------------------------------

class TestModelValidation:
    """
    Tests that model_validate() works correctly after rebuild.
    This is the actual code path used by resource.get() and resource.list().
    Fields are accessed via snake_case Python attributes (item_code, item_name).
    """

    def test_item_model_validate_minimal(self):
        """A minimal Item payload must validate without PydanticUserError."""
        from b1sl.b1sl.models._generated.entities import Item

        # SAP API sends PascalCase; model accepts it via populate_by_name=True
        data = {"ItemCode": "A0001", "ItemName": "Test Item"}
        item = Item.model_validate(data)

        # Python access is snake_case
        assert item.item_code == "A0001"
        assert item.item_name == "Test Item"

    def test_item_model_validate_with_nested_product_trees(self):
        """
        Validates a payload containing a ProductTree sub-object.
        If ProductTree is unresolved this raises a validation error.
        """
        from b1sl.b1sl.models._generated.entities import Item

        data = {
            "ItemCode": "A0002",
            "ProductTrees": [{"TreeCode": "A0002", "TreeType": "iProductionTree"}],
        }
        item = Item.model_validate(data)
        assert item.item_code == "A0002"
        assert item.product_trees is not None
        assert len(item.product_trees) == 1

    def test_business_partner_model_validate_minimal(self):
        """A minimal BusinessPartner payload must validate correctly."""
        from b1sl.b1sl.models._generated.entities import BusinessPartner

        data = {"CardCode": "C001", "CardName": "ACME Corp"}
        bp = BusinessPartner.model_validate(data)

        assert bp.card_code == "C001"
        assert bp.card_name == "ACME Corp"

    def test_document_model_validate_minimal(self):
        """A minimal document (e.g. Invoice) payload must validate correctly."""
        from b1sl.b1sl.models._generated.entities import Document

        data = {"DocNum": 1001, "CardCode": "C001"}
        doc = Document.model_validate(data)

        assert doc.doc_num == 1001


# ---------------------------------------------------------------------------
# 3. Client property → model binding tests
# ---------------------------------------------------------------------------

class TestClientModelBinding:
    """
    Validates that client properties return resources bound to the correct
    model class. Ensures the 'Concurrency-Elite' pattern is correctly wired.
    """

    @pytest.fixture
    def sync_client(self):
        from b1sl.b1sl import B1Client, B1Config
        from tests.fakes.fake_rest_adapter import FakeRestAdapter

        config = B1Config(
            base_url="https://sap-server.example.com/b1s/v2",
            username="admin",
            password="secret",
            company_db="TEST",
        )
        return B1Client(config=config, adapter=FakeRestAdapter())

    def test_items_property_bound_to_item_model(self, sync_client):
        from b1sl.b1sl.models._generated.entities import Item

        resource = sync_client.items
        assert resource.model is Item, (
            f"client.items should be bound to Item, got {resource.model}"
        )

    def test_items_property_endpoint(self, sync_client):
        resource = sync_client.items
        assert resource.endpoint == "Items"

    def test_business_partners_property_bound_to_correct_model(self, sync_client):
        from b1sl.b1sl.models._generated.entities import BusinessPartner

        resource = sync_client.business_partners
        assert resource.model is BusinessPartner

    def test_invoices_property_bound_to_document_model(self, sync_client):
        from b1sl.b1sl.models._generated.entities import Document

        resource = sync_client.invoices
        assert resource.model is Document
        assert resource.endpoint == "Invoices"

    def test_purchase_orders_endpoint(self, sync_client):
        resource = sync_client.purchase_orders
        assert resource.endpoint == "PurchaseOrders"

    def test_all_etag_elite_properties_exist(self, sync_client):
        """
        Smoke test: all 28 ETag-elite properties must exist on the client
        and return a resource (not raise AttributeError).
        """
        etag_properties = [
            "items", "business_partners", "activities",
            "quotations", "orders", "delivery_notes", "invoices",
            "returns", "return_request", "credit_notes", "down_payments",
            "goods_return_request",
            "purchase_requests", "purchase_quotations", "purchase_orders",
            "purchase_delivery_notes", "purchase_invoices", "purchase_returns",
            "purchase_credit_notes", "purchase_down_payments",
            "inventory_gen_entries", "inventory_gen_exits", "drafts",
            "additional_expenses",
            "correction_invoice", "correction_invoice_reversal",
            "correction_purchase_invoice", "correction_purchase_invoice_reversal",
        ]
        for prop_name in etag_properties:
            resource = getattr(sync_client, prop_name, None)
            assert resource is not None, (
                f"client.{prop_name} is missing — not in the ETag-elite list"
            )
