# Overrides & UDF Extensions

## Overview
While the core SDK is fully automated, the most common developer tasks involve **extending** the generated models. The SDK provides two elegant ways to handle this.

## 1. The Override System (Permanent)
The `models/_overrides/` directory allows you to permanently extend any generated entity without touching the `_generated/` core.

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

The generator will automatically detect your `Item` class and promote it to the public `entities` facade, replacing the vanilla generated version.

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
