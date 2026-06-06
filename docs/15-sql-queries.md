# SQL Queries

The `SQLQueries` endpoint lets you persist a named SQL statement on the SAP Service Layer and execute it later via the bounded function `/List`. It is the **SL-native way to run SQL over HTTP** — no direct database driver needed, and it works on both SAP HANA and Microsoft SQL Server backends.

The SDK exposes this endpoint through the `client.sql_queries` Elite alias, backed by `SQLQueriesResource` (sync) and `AsyncSQLQueriesResource` (async).

> For the raw SAP HTTP-level semantics see `docs/reference/sl/sql-queries.md`.

---

## Storing a Query Definition (CRUD)

A `SQLQuery` entity stores the code, name, and SQL text. CRUD works identically to any other resource.

```python
from b1sl.b1sl import B1Client, B1Config, entities as en

with B1Client(B1Config.from_env()) as client:
    # Create
    client.sql_queries.create(en.SQLQuery(
        sql_code="q_items",
        sql_name="All Items",
        sql_text='SELECT T0."ItemCode", T0."ItemName", T0."OnHand" FROM "OITM" T0',
    ))

    # Read
    defn = client.sql_queries.get("q_items")
    print(defn.sql_text)

    # Update (surgical delta — send only what changes)
    client.sql_queries.update("q_items", en.SQLQuery(sql_name="All Items v2"))

    # Delete
    client.sql_queries.delete("q_items")
```

---

## Executing a Query — `run()`

`run()` invokes the `/List` bounded function and returns a `SQLRunResult` containing the first page of rows.

```python
result = client.sql_queries.run("q_items")

# Row access
for row in result:
    print(row["ItemCode"], row["OnHand"])

# Metadata
print(result.sql_text)   # normalized SQL that SAP actually ran
print(len(result))       # rows on this page
print(result.has_more)   # True if more pages exist
```

### Named Parameters

Parameters in `SqlText` are declared with a colon prefix (`:paramName`). Pass them as keyword arguments to `run()` — names are **case-sensitive** and must match the declaration exactly.

```python
# SqlText: "SELECT ... FROM ORDR WHERE DocTotal > :docTotal AND CardCode = :cardCode"
result = client.sql_queries.run("q_orders", docTotal=1000.0, cardCode="C001")
```

Parameter encoding is handled automatically:

| Python type | Encoded form |
| :--- | :--- |
| `str` | `name='value'` (internal `'` escaped as `''`) |
| `int` / `float` | `name=123` (bare number) |
| `bool` | `name=1` or `name=0` |
| other | `str()` conversion, then quoted |

### Page Size

SAP's default page size is 20 rows. Override it with `page_size`:

```python
result = client.sql_queries.run("q_items", page_size=100)
```

> `$maxpagesize` as a query parameter is **ignored** by Service Layer v2. The SDK correctly sends `Prefer: odata.maxpagesize=N` as a header.

### GET vs POST

By default `run()` uses `POST` (parameters in the request body). This avoids URL length limits and keeps parameter values out of server logs. Use `method="GET"` only if the stored query is read via a tool that doesn't support POST.

```python
result = client.sql_queries.run("q_items", method="GET")
```

---

## Streaming All Pages — `run_stream()`

When the result set spans multiple pages, `run_stream()` follows `@odata.nextLink` automatically and yields one row at a time — memory-efficient and safe for large datasets.

```python
# Sync
for row in client.sql_queries.run_stream("q_items", page_size=50):
    process(row)

# Async
async for row in b1.sql_queries.run_stream("q_items", page_size=50):
    await process(row)
```

### Safety Ceiling

Use `max_pages` to cap the number of HTTP requests:

```python
for row in client.sql_queries.run_stream("q_items", page_size=50, max_pages=10):
    ...
```

### How Pagination Works Internally

`run_stream()` uses a two-phase approach:

1. **First page** — `POST SQLQueries('code')/List` with body `{"ParamList": "..."}`.
2. **Subsequent pages** — `GET SQLQueries('code')/List` following the relative `@odata.nextLink`.

This asymmetry matches SAP's own behavior: `nextLink` URLs are always GET-based regardless of how the first page was requested.

---

## Typed Rows with Pydantic

When the SELECT shape is known at development time, convert raw `dict` rows to typed Pydantic instances using `result.to_pydantic()`:

```python
from pydantic import BaseModel

class ItemRow(BaseModel):
    ItemCode: str
    ItemName: str | None = None
    OnHand: float | None = None

result = client.sql_queries.run("q_items")
rows: list[ItemRow] = result.to_pydantic(ItemRow)

print(rows[0].ItemCode)   # full IDE autocomplete
```

Column aliases in the `SELECT` clause become the field names — they are **case-sensitive** and must match exactly.

---

## Error Handling

The SDK maps SAP SQL-specific error codes to typed exceptions before falling back to the generic `B1ValidationError`:

| SAP code | Exception | Cause |
| :--- | :--- | :--- |
| `"702"` | `B1SqlNotAllowedError` | Table not in `b1s_sqltable.conf` allowlist |
| `"703"` | `B1SqlNotAllowedError` | Column in `ColumnExcludeList` |
| `"704"` | `B1SqlParamError` | Wrong param name, count, or type |

Both exceptions are subclasses of `B1ValidationError`, so a broad `except B1ValidationError` catches all 400-level errors.

```python
from b1sl.b1sl.exceptions.exceptions import B1SqlNotAllowedError, B1SqlParamError

try:
    result = client.sql_queries.run("q_items", wrongParam=1)
except B1SqlNotAllowedError as e:
    if e.sap_code == "702":
        print(f"Table blocked — update b1s_sqltable.conf: {e}")
    else:
        print(f"Column blocked — update ColumnExcludeList: {e}")
except B1SqlParamError as e:
    # Check that kwarg names match the :name placeholders in SqlText
    print(f"Parameter mismatch: {e}")
```

> **Note on code `"702"` vs `"703"`**: both are raised as `B1SqlNotAllowedError`. Use `e.sap_code` to distinguish table-level from column-level blocks.

---

## Async Client

The async API mirrors the sync surface exactly:

```python
import asyncio
from b1sl.b1sl import AsyncB1Client, B1Config

async def main():
    async with AsyncB1Client(B1Config.from_env()) as b1:
        # Single page
        result = await b1.sql_queries.run("q_items")

        # Full stream
        async for row in b1.sql_queries.run_stream("q_items", page_size=100):
            print(row["ItemCode"])

asyncio.run(main())
```

---

## SQLQueries vs. `saphdb`

The SDK also ships an optional `saphdb` subpackage for direct HANA connectivity. Here's when to choose each:

| | `SQLQueries` (this feature) | `saphdb` (direct HANA) |
| :--- | :--- | :--- |
| Transport | HTTP (same session as the rest of the SDK) | TCP direct to HANA port |
| Driver | None | `hdbcli` (proprietary, extra required) |
| MSSQL support | ✅ (SL normalizes SQL) | ❌ (HANA only) |
| SQL flexibility | Restricted (allowlist + keyword subset) | Full HANA SQL |
| Dry-run | ✅ inherited | ❌ |
| Async | ✅ | ❌ (blocking driver) |
| ETag on definitions | ✅ | ❌ |

Use `SQLQueries` when you need portability, HTTP transport, and SDK integration. Use `saphdb` when you need unrestricted SQL on HANA and are willing to take on the extra driver dependency.

---

## Security Notes

SAP enforces a server-side allowlist on both tables and columns:

- **Table allowlist**: `<SL install>/conf/b1s_sqltable.conf` — queries against unlisted tables return error `702`.
- **Column exclude list**: Per-table column filtering in the same config file — queries against excluded columns return error `703`.

Neither condition can be fixed at runtime. Coordinate with the SAP basis team if you need to add tables or adjust column visibility.

---

## See Also

- `docs/reference/sl/sql-queries.md` — raw SAP HTTP semantics and SQL grammar reference.
- `examples/22_sql_queries.py` — runnable demo covering all scenarios.
- `src/b1sl/b1sl/resources/sql_queries.py` — implementation source.
