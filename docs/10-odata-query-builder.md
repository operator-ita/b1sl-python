# OData Query Builder Guide

The SAP B1 Python SDK provides a pythonic, type-safe fluent interface for building OData queries. You can choose between two primary ways to reference fields: the dynamic **`F` Proxy** or **Static Field Constants**.

---

## 1. The `F` Global Proxy (Dynamic)

The `F` variable is a virtual proxy that allows you to reference any SAP field without imports. 

- **Syntax**: `F.FieldName` (uses **SAP CamelCase** names).
- **Pros**: Zero imports, supports UDFs automatically, very fast for quick scripts.
- **Cons**: No IDE autocomplete.

```python
from b1sl.b1sl.resources.odata import F

# F requires the exact SAP name (CamelCase)
items = await b1.items.filter(F.QuantityOnStock > 10).execute()

# Excellent for UDFs
results = await b1.business_partners.filter(F.U_Category == "VIP").execute()
```

---

## 2. Static Field Constants (Type-Safe)

Each elite entity has a corresponding field class with explicit attributes.

- **Syntax**: `Entity.field_name` (uses **Pythonic snake_case**).
- **Pros**: Full IDE autocomplete, type discovery, less prone to typos.
- **Cons**: Requires importing the specific entity field class.

```python
from b1sl.b1sl.fields import Item

# Static constants map snake_case to SAP's CamelCase internally
items = await b1.items.filter(Item.quantity_on_stock > 10).execute()
```

---

## Field Referencing Comparison

| Feature | `F` Proxy | Static Constants (`Item`, `BP`, etc.) |
| :--- | :--- | :--- |
| **Naming Style** | **SAP CamelCase** (`F.ItemCode`) | **Pythonic snake_case** (`Item.item_code`) |
| **Autocomplete** | ❌ None | ✅ Full IDE Support |
| **Imports** | `from ...odata import F` | `from ...fields import Item` |
| **UDF Support** | ✅ Native (`F.U_MyField`) | ❌ Requires manual extension |
| **Deep Paths** | ✅ `F.Lines.Quantity` | ✅ `Order.document_lines / Line.quantity` |

---

## Filtering with Operators

You can use standard comparison operators on any field constant or `F` proxy.

| Operator | OData Equivalent | Example |
| :--- | :--- | :--- |
| `==` | `eq` | `Item.item_code == 'A001'` |
| `!=` | `ne` | `F.CardCode != 'C001'` |
| `>` | `gt` | `Item.quantity_on_stock > 10` |
| `>=` | `ge` | `F.Price >= 100.5` |
| `<` | `lt` | `Item.on_hand < 10` |
| `<=` | `le` | `F.OnHand <= 5` |

### String Functions
- `.contains(value)`
- `.startswith(value)`
- `.endswith(value)`

Example:
```python
results = await b1.items.filter(F.ItemName.contains("Cheese")).execute()
```

---

## Logic Composition (AND / OR)

Both patterns use bitwise operators `&` (AND), `|` (OR), and `~` (NOT).

> [!IMPORTANT]
> **Parentheses are mandatory** due to Python operator precedence.
> - **Correct**: `(Item.items_group_code == 100) & (F.QuantityOnStock > 0)`

---

## Expansions & Nested Selection

### 1. Dictionary Expand (Surgical Expansion)
Recommended when fetching **multiple fields** from a related entity. 

```python
from b1sl.b1sl.fields import ServiceCall, BusinessPartner

# GET /ServiceCalls(1)?$expand=BusinessPartner($select=CardCode,CardName)
sc = await client.service_calls.by_id(1).expand({
    ServiceCall.business_partner: [BusinessPartner.card_code, BusinessPartner.card_name]
}).execute()
```

### 2. Path-based Selection (`/`)
Recommended for flat selections or building nested filters.

```python
# GET /ServiceCalls(1)?$select=Subject,BusinessPartner/CardCode&$expand=BusinessPartner
sc = await client.service_calls.by_id(1).select(
    F.Subject,
    F.BusinessPartner / F.CardCode
).expand([F.BusinessPartner]).execute()
```

---

## Terminal Methods

| Method | Returns | Behavior |
| :--- | :--- | :--- |
| **`.execute()`** | `list[T] \| T` | Executes the query and returns a single page (list) or single object (by_id). |
| **`.stream()`** | `AsyncGenerator` | Returns a generator that automatically fetches **all pages** via `nextLink`. |
| **`.first()`** | `T \| None` | Adds `$top=1` and returns the first result or `None`. |
