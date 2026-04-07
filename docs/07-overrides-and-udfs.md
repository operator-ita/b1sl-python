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

### Pattern B: Typed UDFs (Scaling)
If your application relies heavily on certain UDFs, declare them in an override:

```python
# models/_overrides/inventory.py
from pydantic import Field

class Item(_Item):
    # Mapping U_RealColor to Python snake_case
    my_color: str | None = Field(None, alias="U_RealColor")
```

Now `item.my_color` is a first-class citizen with full IDE autocompletion and type checking.

## Architecture Policy
- **Prefer Overrides for Calculations**: Keep business logic in `_overrides/`.
- **Prefer Hybrid Access for One-Off UDFs**: Only declare UDFs you depend on for typing.
- **NEVER EDIT `_generated/`**: This is the only strict rule.
