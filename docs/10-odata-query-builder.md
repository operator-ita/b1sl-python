# OData Query Builder Guide

The SAP B1 Python SDK provides a pythonic, type-safe fluent interface for building OData queries. The recommended way to reference fields is the **Static Field Constants** in `b1sl.b1sl.fields`; the dynamic **`F` proxy** is the escape hatch for UDFs and ad-hoc names.

---

## 1. Static Field Constants (Recommended)

Each entity has a generated field class whose snake_case attributes map to the
exact SAP property names — including the irregular ones a naive conversion
would get wrong (`service_call_id` → `ServiceCallID`, `bplid` → `BPLID`).

- **Syntax**: `Entity.field_name` (Pythonic **snake_case**, same vocabulary as the response models).
- **Pros**: Full IDE autocomplete; a typo raises `AttributeError` instantly on your machine instead of an SAP 400 at runtime; query and response read in the same casing.
- **Cons**: Requires an import; cannot reference UDFs (they are not in `$metadata`).

```python
from b1sl.b1sl.fields import Item, Order   # Order/Invoice/… alias Document

items = await b1.items.filter(Item.quantity_on_stock > 10).execute()
big_orders = await b1.orders.filter(Order.doc_total > 1000).execute()

for o in big_orders:
    print(o.doc_total)   # query and response share the same snake_case names
```

---

## 2. The `F` Global Proxy (Escape Hatch)

`F` is a raw passthrough: `F.AnyName` becomes the literal OData token `AnyName`,
with **no validation and no name translation**. Use it for the two things the
static constants cannot express:

- **UDFs** — custom `U_*` fields are not in `$metadata`, so no constant exists.
- **Dynamic / ad-hoc names** — field names only known at runtime.

```python
from b1sl.b1sl.resources.odata import F

# UDFs: the legitimate home of F
results = await b1.business_partners.filter(F.U_Category == "VIP").execute()

# Raw SAP names work too, but you give up autocomplete and typo safety:
items = await b1.items.filter(F.QuantityOnStock > 10).execute()
```

> [!WARNING]
> `F` accepts anything — `F.DocTotall` happily produces an invalid query that
> fails only when SAP rejects it at runtime (`SAP Error -1000`). Prefer the
> static constants for every field that exists in metadata.

---

## Field Referencing Comparison

| Feature | Static Constants (`Item`, `Order`, …) | `F` Proxy |
| :--- | :--- | :--- |
| **Naming Style** | **Pythonic snake_case** (`Item.item_code`) | **SAP CamelCase** (`F.ItemCode`) |
| **Autocomplete** | ✅ Full IDE Support | ❌ None |
| **Typo behavior** | ✅ Instant `AttributeError`, no network | ❌ HTTP round-trip, SAP error at runtime |
| **Irregular names** | ✅ Resolved from metadata (`ServiceCallID`, `BPLID`) | ❌ You must recall SAP's exact spelling |
| **Imports** | `from ...fields import Item` | `from ...odata import F` |
| **UDF Support** | ❌ Not in metadata (see Typed Overrides) | ✅ Native (`F.U_MyField`) |
| **Deep Paths** | ✅ `Order.document_lines / DocumentLine.quantity` | ✅ `F.DocumentLines / F.Quantity` |

---

## Filtering with Operators

You can use standard comparison operators on any field constant or `F` proxy.

| Operator | OData Equivalent | Example |
| :--- | :--- | :--- |
| `==` | `eq` | `Item.item_code == 'A001'` |
| `!=` | `ne` | `BusinessPartner.card_code != 'C001'` |
| `>` | `gt` | `Item.quantity_on_stock > 10` |
| `>=` | `ge` | `Order.doc_total >= 100.5` |
| `<` | `lt` | `Item.quantity_on_stock < 10` |
| `<=` | `le` | `F.U_Stock <= 5` (UDF — `F` territory) |

### String Functions
- `.contains(value)`
- `.startswith(value)`
- `.endswith(value)`

Example:
```python
from b1sl.b1sl.fields import Item

results = await b1.items.filter(Item.item_name.contains("Cheese")).execute()
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
Recommended for flat selections or building nested filters. The `/` operator
composes navigation paths from any mix of constants:

```python
from b1sl.b1sl.fields import BusinessPartner, ServiceCall

# GET /ServiceCalls(1)?$select=Subject,BusinessPartner/CardCode&$expand=BusinessPartner
sc = await client.service_calls.by_id(1).select(
    ServiceCall.subject,
    ServiceCall.business_partner / BusinessPartner.card_code,
).expand([ServiceCall.business_partner]).execute()
```

> [!NOTE]
> Attribute chaining (`F.BusinessPartner.card_code`) is **not** a thing — `F`
> values are plain strings. Always compose paths with `/`.

---

## Terminal Methods

| Method | Returns | Behavior |
| :--- | :--- | :--- |
| **`.execute()`** | `PaginatedResult[T] \| T` | Executes the query and returns a single page (list-like, exposing `next_params` / `has_more`) or a single object (by_id). |
| **`.stream()`** | `AsyncGenerator` | Returns a generator that automatically fetches **all pages** via `nextLink`. |
| **`.first()`** | `T \| None` | Adds `$top=1` and returns the first result or `None`. |
