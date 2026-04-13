# OData Query Builder Guide

The SAP B1 Python SDK provides a pythonic, type-safe fluent interface for building OData queries. This guide explains how to use the `QueryBuilder` and field constants to create precise and maintainable requests.

## Key Features
- **Operator Overloading**: Use standard Python operators (`==`, `!=`, `>`, etc.) for filtering.
- **Fluent Interface**: Chain methods like `.filter()`, `.select()`, `.top()`, and `.execute()`.
- **Type Safety**: Use descriptive entity constants instead of strings to avoid typos.
- **Path-based Navigation**: Use the `/` operator to access nested properties in filters and selections.

---

## Basic Usage

Import the field constants for the entity you are working with.

```python
from b1sl.b1sl.fields import Item

# Fetch the top 5 items
items = client.items.select(Item.item_code, Item.item_name).top(5).execute()
```

---

## Filtering with Operators

You can use standard comparison operators on any field constant.

| Operator | OData Equivalent | Example |
| :--- | :--- | :--- |
| `==` | `eq` | `Item.item_code == 'A001'` |
| `!=` | `ne` | `Item.item_code != 'A001'` |
| `>` | `gt` | `Item.quantity_on_stock > 10` |
| `>=` | `ge` | `Item.price >= 100.5` |
| `<` | `lt` | `Item.on_hand < 10` |
| `<=` | `le` | `Item.on_hand <= 5` |

### String Functions
- `.contains(value)`
- `.startswith(value)`
- `.endswith(value)`

Example:
```python
results = client.items.filter(Item.item_name.contains("Cheese")).execute()
```

---

## Expansions & Nested Selection

### 1. Dictionary Expand (Surgical Expansion)
Recommended when fetching **multiple fields** from a related entity. 

```python
from b1sl.b1sl.fields import ServiceCall, BusinessPartner

# GET /ServiceCalls(1)?$expand=BusinessPartner($select=CardCode,CardName)
sc = client.service_calls.by_id(1).expand({
    ServiceCall.business_partner: [BusinessPartner.card_code, BusinessPartner.card_name]
}).execute()
```

### 2. Path-based Selection (`/`)
Recommended for flat selections or building nested filters.

```python
# GET /ServiceCalls(1)?$select=Subject,BusinessPartner/CardCode&$expand=BusinessPartner
sc = client.service_calls.by_id(1).select(
    ServiceCall.subject,
    ServiceCall.business_partner / BusinessPartner.card_code
).expand([ServiceCall.business_partner]).execute()
```

---

## Logic Composition (AND / OR)

Use bitwise operators `&` (AND), `|` (OR), and `~` (NOT).

> [!IMPORTANT]
> **Parentheses are mandatory.** 
> - **Correct**: `(Item.active == 'tYES') & (Item.on_hand > 0)`

---

## Date and Time Handling

The SDK automatically formats Python `datetime` types.

```python
from datetime import date

orders = client.orders.filter(Item.doc_date >= date(2024, 1, 1)).execute()
```

---

## Terminal Methods

- **`.execute()`**: Triggers the request. Returns a `list` or a single object.
- **`.first()`**: Adds `$top=1` and returns the first result or `None`.
