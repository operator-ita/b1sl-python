"""
b1sl.contrib.mcp.discovery
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Resource and entity catalog for SAP B1 OData MCP tools.

Provides a static inventory of the SDK's Elite resources (ETag-safe aliases)
and runtime field introspection for any B1Model, without hitting the network.

Typical usage::

    from b1sl.contrib.mcp.discovery import (
        ELITE_RESOURCES,
        list_elite_resources,
        entity_field_catalog,
        resource_descriptor,
    )

    resources = list_elite_resources()
    desc = resource_descriptor("orders")
    # → ResourceDescriptor(alias='orders', endpoint='Orders', key_field='DocEntry', ...)

    from b1sl.b1sl.models._generated.entities import Item
    fields = entity_field_catalog(Item)
    scalar_fields = [f for f in fields if not f.is_navigation]
"""

from __future__ import annotations

import enum as _enum_module
import types as _types_module
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Union, get_args, get_origin

if TYPE_CHECKING:
    from b1sl.b1sl.models.base import B1Model

# ── Data classes ──────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class ResourceDescriptor:
    """Static metadata for one Elite resource alias.

    All Elite resources have verified ETag concurrency support in the SAP
    Service Layer.  Non-Elite endpoints require explicit ``get_resource()``
    binding and carry no ETag guarantee.
    """

    alias: str
    """Python client property name, e.g. ``"items"``."""

    endpoint: str
    """SAP OData endpoint path segment, e.g. ``"Items"``."""

    model_name: str
    """Pydantic model class name, e.g. ``"Item"`` or ``"Document"``."""

    key_field: str
    """Primary key SAP alias used in URL paths, e.g. ``"ItemCode"``."""

    etag_safe: bool
    """Always ``True`` for Elite resources — ETag concurrency guaranteed."""

    category: str
    """Grouping: ``"master_data"``, ``"sales"``, ``"purchasing"``,
    ``"inventory"``, or ``"correction"``."""

    description: str
    """One-line human description suitable for MCP resource listings."""


@dataclass(frozen=True)
class FieldDescriptor:
    """Metadata for one declared field on a B1Model subclass.

    Derived entirely from Pydantic ``model_fields`` — no network call required.
    """

    name: str
    """SAP alias (OData field name), e.g. ``"ItemCode"``."""

    python_name: str
    """Python attribute name on the model, e.g. ``"item_code"``."""

    type_label: str
    """Human-readable type string: ``"string"``, ``"integer"``, ``"number"``,
    ``"boolean (tYES/tNO in $filter)"``, ``"collection"``, ``"object"``,
    or ``"string (enum)"``."""

    required: bool
    """``True`` if the Pydantic field declares no default value."""

    is_udf: bool
    """``True`` if ``name`` starts with ``"U_"`` (User-Defined Field)."""

    is_navigation: bool
    """``True`` for ``list[...]`` (collection) or nested model fields.
    These are accessed via ``$expand``, not ``$filter``/``$select``."""


# ── Internal type resolver ────────────────────────────────────────────────────

def _resolve_type(annotation: Any) -> tuple[str, bool]:
    """Return ``(type_label, is_navigation)`` for a raw Pydantic annotation.

    Handles:
    - ``Optional[X]`` / ``X | None``
    - ``Annotated[X, ...]`` (e.g. SapBool = Annotated[bool, BeforeValidator])
    - ``list[X]`` → collection navigation
    - Primitive scalars: str, int, float, bool
    - B1Model subclasses → object navigation
    - Enum subclasses → string (enum)
    """
    from b1sl.b1sl.models.base import B1Model

    # Step 1: Unwrap Optional / Union[X, None]
    # Handle both typing.Union (Union[X, None]) and PEP-604 types.UnionType (X | None).
    origin = get_origin(annotation)
    _is_union = (
        origin is Union
        or (
            hasattr(_types_module, "UnionType")
            and isinstance(annotation, _types_module.UnionType)
        )
    )
    if _is_union:
        non_none = [a for a in get_args(annotation) if a is not type(None)]
        if len(non_none) == 1:
            annotation = non_none[0]
            origin = get_origin(annotation)

    # Step 2: Unwrap Annotated[X, ...] — handles SapBool and similar wrappers
    if hasattr(annotation, "__metadata__"):
        annotation = get_args(annotation)[0]
        origin = get_origin(annotation)

    # Step 3: list → collection navigation property
    if origin is list:
        return "collection", True

    # Step 4: Scalar primitives
    if annotation is str:
        return "string", False
    if annotation is int:
        return "integer", False
    if annotation is float:
        return "number", False
    if annotation is bool:
        return "boolean (tYES/tNO in $filter)", False

    # Step 5: Nested B1Model subclass → single-object navigation property
    try:
        if isinstance(annotation, type) and issubclass(annotation, B1Model):
            return "object", True
    except TypeError:
        pass

    # Step 6: Enum subclass
    try:
        if isinstance(annotation, type) and issubclass(annotation, _enum_module.Enum):
            return "string (enum)", False
    except TypeError:
        pass

    return "string", False  # safe fallback (Union enums, Literals, etc.)


# ── Public introspection API ──────────────────────────────────────────────────

def entity_field_catalog(model: type[B1Model]) -> list[FieldDescriptor]:
    """Introspect a B1Model subclass and return a descriptor for each field.

    Derives field names, types, UDF status, and navigation status from Pydantic
    ``model_fields`` — no network call required.  Navigation fields (``list[...]``
    or nested model objects) are flagged with ``is_navigation=True``; they are
    accessed via ``$expand`` rather than ``$filter`` or ``$select``.

    Args:
        model: A B1Model subclass (or B1Model itself).

    Returns:
        List of :class:`FieldDescriptor`, one per declared model field, excluding
        the internal ``@odata.etag`` ETag header field.

    Example::

        from b1sl.b1sl.models._generated.entities import Item
        from b1sl.contrib.mcp.discovery import entity_field_catalog

        fields = entity_field_catalog(Item)
        scalar = [f for f in fields if not f.is_navigation]
        booleans = [f for f in fields if "tYES" in f.type_label]
    """
    result: list[FieldDescriptor] = []
    for python_name, field_info in model.model_fields.items():
        alias: str = field_info.alias or python_name
        # Skip the internal ETag header — not a queryable OData field
        if alias == "@odata.etag":
            continue
        type_label, is_navigation = _resolve_type(field_info.annotation)
        result.append(FieldDescriptor(
            name=alias,
            python_name=python_name,
            type_label=type_label,
            required=field_info.is_required(),
            is_udf=alias.startswith("U_"),
            is_navigation=is_navigation,
        ))
    return result


# ── Elite resource registry ───────────────────────────────────────────────────

def _r(
    alias: str,
    endpoint: str,
    model_name: str,
    key_field: str,
    category: str,
    description: str,
) -> ResourceDescriptor:
    return ResourceDescriptor(
        alias=alias,
        endpoint=endpoint,
        model_name=model_name,
        key_field=key_field,
        etag_safe=True,
        category=category,
        description=description,
    )


ELITE_RESOURCES: dict[str, ResourceDescriptor] = {
    # ── Master Data ──────────────────────────────────────────────────────────
    "items": _r(
        "items", "Items", "Item", "ItemCode",
        "master_data", "Item master: products, services, and resources",
    ),
    "business_partners": _r(
        "business_partners", "BusinessPartners", "BusinessPartner", "CardCode",
        "master_data", "Business partners: customers, vendors, and leads",
    ),
    "activities": _r(
        "activities", "Activities", "Activity", "ActivityCode",
        "master_data", "CRM activities: calls, meetings, and tasks",
    ),
    # ── Sales Documents ──────────────────────────────────────────────────────
    "quotations": _r(
        "quotations", "Quotations", "Document", "DocEntry",
        "sales", "Sales quotations",
    ),
    "orders": _r(
        "orders", "Orders", "Document", "DocEntry",
        "sales", "Sales orders",
    ),
    "delivery_notes": _r(
        "delivery_notes", "DeliveryNotes", "Document", "DocEntry",
        "sales", "Sales delivery notes (goods issue)",
    ),
    "invoices": _r(
        "invoices", "Invoices", "Document", "DocEntry",
        "sales", "Accounts-receivable invoices",
    ),
    "returns": _r(
        "returns", "Returns", "Document", "DocEntry",
        "sales", "Sales returns (goods return)",
    ),
    "return_request": _r(
        "return_request", "ReturnRequest", "Document", "DocEntry",
        "sales", "Sales return requests",
    ),
    "credit_notes": _r(
        "credit_notes", "CreditNotes", "Document", "DocEntry",
        "sales", "Sales credit memos",
    ),
    "down_payments": _r(
        "down_payments", "DownPayments", "Document", "DocEntry",
        "sales", "Sales down payment invoices",
    ),
    "goods_return_request": _r(
        "goods_return_request", "GoodsReturnRequest", "Document", "DocEntry",
        "sales", "Goods return requests",
    ),
    # ── Purchasing Documents ─────────────────────────────────────────────────
    "purchase_requests": _r(
        "purchase_requests", "PurchaseRequests", "Document", "DocEntry",
        "purchasing", "Purchase requests",
    ),
    "purchase_quotations": _r(
        "purchase_quotations", "PurchaseQuotations", "Document", "DocEntry",
        "purchasing", "Purchase quotations",
    ),
    "purchase_orders": _r(
        "purchase_orders", "PurchaseOrders", "Document", "DocEntry",
        "purchasing", "Purchase orders",
    ),
    "purchase_delivery_notes": _r(
        "purchase_delivery_notes", "PurchaseDeliveryNotes", "Document", "DocEntry",
        "purchasing", "Purchase delivery notes (goods receipt)",
    ),
    "purchase_invoices": _r(
        "purchase_invoices", "PurchaseInvoices", "Document", "DocEntry",
        "purchasing", "Accounts-payable invoices",
    ),
    "purchase_returns": _r(
        "purchase_returns", "PurchaseReturns", "Document", "DocEntry",
        "purchasing", "Purchase returns",
    ),
    "purchase_credit_notes": _r(
        "purchase_credit_notes", "PurchaseCreditNotes", "Document", "DocEntry",
        "purchasing", "Purchase credit memos",
    ),
    "purchase_down_payments": _r(
        "purchase_down_payments", "PurchaseDownPayments", "Document", "DocEntry",
        "purchasing", "Purchase down payment invoices",
    ),
    # ── Inventory & Specialized ──────────────────────────────────────────────
    "inventory_gen_entries": _r(
        "inventory_gen_entries", "InventoryGenEntries", "Document", "DocEntry",
        "inventory", "Inventory general entry documents",
    ),
    "inventory_gen_exits": _r(
        "inventory_gen_exits", "InventoryGenExits", "Document", "DocEntry",
        "inventory", "Inventory general exit documents",
    ),
    "drafts": _r(
        "drafts", "Drafts", "Document", "DocEntry",
        "inventory", "Draft marketing documents",
    ),
    "additional_expenses": _r(
        "additional_expenses", "AdditionalExpenses", "B1Model", "ExpnsCode",
        "inventory", "Additional expense types (freight, tax, etc.)",
    ),
    # ── Correction Marketing Documents ──────────────────────────────────────
    "correction_invoice": _r(
        "correction_invoice", "CorrectionInvoice", "Document", "DocEntry",
        "correction", "Correction invoices",
    ),
    "correction_invoice_reversal": _r(
        "correction_invoice_reversal", "CorrectionInvoiceReversal", "Document",
        "DocEntry", "correction", "Correction invoice reversals",
    ),
    "correction_purchase_invoice": _r(
        "correction_purchase_invoice", "CorrectionPurchaseInvoice", "Document",
        "DocEntry", "correction", "Correction purchase invoices",
    ),
    "correction_purchase_invoice_reversal": _r(
        "correction_purchase_invoice_reversal",
        "CorrectionPurchaseInvoiceReversal", "Document", "DocEntry",
        "correction", "Correction purchase invoice reversals",
    ),
}
"""Ordered mapping of Elite alias → :class:`ResourceDescriptor`.

Elite resources are the ~28 client aliases (``client.items``,
``client.orders``, etc.) that have verified ETag concurrency support in the
SAP Service Layer.

Non-Elite endpoints (~1 000 more) require explicit ``get_resource()`` binding
and provide **no ETag guarantee**.  Do not add entries here without verifying
ETag support against a live SAP instance.
"""


# ── Convenience functions ─────────────────────────────────────────────────────

def list_elite_resources() -> list[ResourceDescriptor]:
    """Return all Elite resource descriptors in registration order.

    Elite resources are the client aliases with verified ETag concurrency
    support.  Non-Elite endpoints are accessed via ``client.get_resource()``
    and have no ETag guarantee.

    Returns:
        Ordered list of :class:`ResourceDescriptor`.

    Example::

        for desc in list_elite_resources():
            print(f"{desc.alias:30s}  {desc.endpoint:35s}  ETag={desc.etag_safe}")
    """
    return list(ELITE_RESOURCES.values())


def resource_descriptor(alias: str) -> ResourceDescriptor:
    """Return the :class:`ResourceDescriptor` for a named Elite alias.

    Args:
        alias: Python client property name, e.g. ``"orders"``.

    Returns:
        :class:`ResourceDescriptor` with endpoint, model name, key field,
        ETag safety flag, and category.

    Raises:
        KeyError: If ``alias`` is not a known Elite resource, with a message
            listing all valid aliases.

    Example::

        desc = resource_descriptor("orders")
        print(desc.endpoint)   # "Orders"
        print(desc.key_field)  # "DocEntry"
        print(desc.etag_safe)  # True
    """
    try:
        return ELITE_RESOURCES[alias]
    except KeyError:
        known = ", ".join(sorted(ELITE_RESOURCES))
        raise KeyError(
            f"Unknown Elite alias {alias!r}. "
            f"Known aliases: {known}. "
            "For non-Elite endpoints use client.get_resource() directly."
        ) from None
