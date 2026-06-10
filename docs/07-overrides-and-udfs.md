# Overrides & UDF Extensions

## Overview
While the core SDK is fully automated, the most common developer tasks involve **extending** the generated models. The SDK provides two elegant ways to handle this.

## 1. The Override System (Permanent)
The `models/_overrides/` directory allows you to permanently extend any generated entity without touching the `_generated/` core. `_generated/` is wiped on every metadata regeneration (new Service Layer versions); `_overrides/` survives — that is the whole point of the split.

### How to use it:
1.  **Inherit**: Create a new file (e.g., `inventory.py`) in `_overrides/`.
2.  **Import & Extend**: Inherit from the generated base class (with a prefix like `_Item`).
3.  **Implement**: Add calculated properties, custom methods, or extra Pydantic fields.

```python
# models/_overrides/inventory.py
from .._generated.entities.inventory import Item as _Item

class Item(_Item):
    @property
    def available_stock(self) -> float:
        """OnHand - Committed + Ordered"""
        return (self.quantity_on_stock or 0.0) - ...
```

That's it — **no registration step**. Discovery is dynamic at runtime: on the first entity access, the SDK scans `_overrides/`, and any class that

- is defined in a module directly under `_overrides/`,
- has the **same name** as a generated entity, and
- **subclasses** that generated entity

replaces the generated class everywhere: `en.Item`, nested validation inside other models, and resource deserialization (`client.items.get(...)` returns *your* `Item`). A class that shadows an entity name **without** subclassing it is ignored, and a warning is emitted on the `b1sl` logger.

You do **not** need to re-run the generator for an override to take effect. Re-running `./scripts/generate_models.sh` additionally refreshes the facade's `TYPE_CHECKING` imports so IDEs and type checkers resolve `en.Item` to your subclass (runtime behavior is identical either way).

Two rules keep the layering clean:
- Overrides import from `_generated/` (inheritance) — never the other way around. The generated code only discovers overrides lazily, after imports settle, so importing your override module directly (`from b1sl.b1sl.models._overrides.inventory import Item`) is safe in any import order.
- By convention, one module per domain mirrors `_generated/entities/` (`inventory.py`, `sales.py`, …), but any module name under `_overrides/` is scanned.

### Worked example: a brand-new override from scratch

Suppose you want every sales document to expose its freight total (SAP
splits freight into `DocumentAdditionalExpenses` lines instead of a single
field). Creating this one file **is the whole task** — no registration, no
map, no generator run:

```python
# models/_overrides/sales.py  ← just create this file. That's the whole task.
from .._generated.entities.general import Document as _Document


class Document(_Document):
    @property
    def freight_total(self) -> float:
        """Sum of all additional-expense lines (freight, insurance, ...)."""
        expenses = self.document_additional_expenses or []
        return sum(expense.line_total or 0.0 for expense in expenses)
```

It takes effect immediately, everywhere the entity is served:

```python
from b1sl.b1sl import entities as en

order = client.orders.get(123)            # Elite resource → returns YOUR Document
print(order.freight_total)

quote = en.Quotation(card_code="C001")    # aliases too: Quotation IS Document,
print(quote.freight_total)                # so Order, Invoice, DeliveryNote, …
                                          # all gain the property
```

Note the reach of this particular example: `Order`, `Invoice`, `Quotation`,
`DeliveryNote`, etc. are all entity-set aliases of the single `Document`
model, so overriding `Document` extends every marketing document at once.
If you want behavior for only one document type, put the logic behind a
check on `doc_object_code` instead of relying on the class name.

## 2. Managing UDFs (Dynamic)
The SDK's "Vanilla" policy excludes `U_` fields from the core to maintain stability. However, you can still interact with them effortlessly:

### Pattern A: Spontaneous Access (No Setup)
`B1Model` is configured with `extra="allow"`. Any UDFs returned by SAP are preserved in `model.__pydantic_extra__`.

```python
item = client.items.get("C100")
# Use the .get() helper in B1Model for safe UDF access
color = item.get("U_Color", "Not Found")
```

Now `item.my_color` is a first-class citizen with full IDE autocompletion and type checking.

### Pattern C: Dynamic `.udfs` Mapping (Recommended for one-offs)
The most elegant way to handle UDFs without modifying any code is using the `.udfs` property. It provides a protected dictionary-like interface that ensures you only touch `U_` fields.

```python
item = client.items.get("C100")

# 1. Access UDFs (Strictly requires 'U_' prefix)
color = item.udfs["U_Color"]

# 2. Update UDFs
item.udfs["U_Priority"] = "High"

# 3. Use in constructor
new_item = en.Item(
    item_code="NEW",
    udfs={"U_Custom": "Value"}
)
```

**Why use `.udfs`?**
- **Safety**: It raises a `KeyError` if you try to access a non-`U_` field, preventing accidental overwrites of standard SAP fields.
- **Explicitness**: It clearly separates SAP core fields from your implementation's custom fields.
- **Native Serialization**: Values in `.udfs` are automatically included in the root of the JSON payload when calling `.to_api_payload()`.

### Pattern D: Schema Discovery & Validation (Advanced)
If you need to programmatically discover what UDFs are available in the current environment or validate data against SAP's metadata before sending it, use the `get_udf_schema()` method.

```python
# 1. Discover
schema = await b1.items.get_udf_schema()

# 2. Inspect
if "U_Size" in schema:
    field = schema["U_Size"]
    print(f"SAP Type: {field.type}, Size: {field.size}")

# 3. Validate and Build Payload
# This catch types errors (e.g. string into numeric) before hitting SAP
try:
    payload = schema.validate_and_dump({"U_Size": 10, "U_Color": "Blue"})
    await b1.items.update("A001", {"udfs": payload})
except Exception as e:
    print(f"Validation Error: {e}")
```

The returned `UDFSchema` object is a powerful meta-container that can also generate dedicated Pydantic models on-the-fly (`to_pydantic_model()`).


## Architecture Policy
- **Prefer Overrides for Calculations**: Keep business logic in `_overrides/`.
- **Prefer `.udfs` for Dynamic Data**: Use the mapping for fields that don't need dedicated typing.
- **Prefer Typed UDFs for Stability**: If a UDF is critical to your app logic, declare it in an override.
- **NEVER EDIT `_generated/`**: This is the only strict rule.
