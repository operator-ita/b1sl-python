# Transparent Pagination Streams

When dealing with large datasets in SAP Business One, the Service Layer automatically paginates results. By default, a simple request might only return the first 20 or 50 records, along with an `odata.nextLink`.

The SDK provides a **Transparent Pagination Stream** API that automatically handles subsequent page fetches, allowing you to iterate over thousands of records using a single, memory-efficient Python generator.

---

## Basic Usage

The `.stream()` method is available on all resources and builders.

### Async Example
```python
# Automatically fetches next pages as you iterate
async for item in client.items.stream():
    print(f"Processing {item.item_code}...")
```

### Sync Example
```python
# Memory efficient iteration
for item in client.items.stream():
    print(f"Processing {item.item_code}...")
```

---

## Comparison: `.list()` vs `.execute()` vs `.stream()`

Understanding the semantics of each terminal method is critical for performance and correctness.

| Method | Source | Returns | Pagination Behavior |
| :--- | :--- | :--- | :--- |
| **`.list()`** | Resource | `PaginatedResult[T]` | **Single Page** with metadata (`next_params`, `has_more`). |
| **`.execute()`** | Builder | `PaginatedResult[T]` | **Single Page** with metadata. Triggers the fluent query. |
| **`.stream()`** | Either | `Generator` | **Transparent**. Fetches every page until exhaustion. |

---

## What `.top(N)` means

`.top(N)` is a **total cap** — "at most N rows" — everywhere it appears, matching
the OData `$top` spec and the convention of boto3 (`MaxItems`), google-cloud
(`max_results`), etc. It is **not** a page size; use `.page_size()` (below) for
the per-request batch.

| Method | `.top(N)` behaviour | HTTP requests |
| :--- | :--- | :--- |
| **`.execute()`** | Eagerly collects up to **N** rows, following `nextLink` across server pages. | `ceil((N+1) / page)` |
| **`.stream()`** | Global cap on total rows yielded (lazy generator). | as needed |
| **`.list()`** | Low-level: returns **one server page** (≤ N rows) plus a cursor. | exactly 1 |

So `client.items.top(100).execute()` returns up to 100 rows even though SAP's
server page is 20 — the SDK pages internally. `.top()` is enforced client-side
and never sent to SAP as `$top` (which SAP would re-apply per `$skip`).

## Manual Pagination with `PaginatedResult`

`.list()` and `.execute()` return a `PaginatedResult[T]` — it behaves like a
list (iteration, `len()`, indexing, slicing) and additionally carries the
OData pagination metadata:

```python
page = client.items.list(query)        # ONE raw server page
print(len(page), page[0].item_code)    # list-like access

while page.has_more:
    page = client.items.list(params=page.next_params)  # fetch next page
```

- `page.next_params` is the ready-to-use query-param dict for the next page
  (derived from `odata.nextLink`, with your original `$filter`/`$select`
  re-injected — see the Filter Persistence Guarantee below). It is `None` on
  the last page.
- `page.next_skip` is the **absolute `$skip`** for the next call (gap-free),
  or `None` on the last page. Prefer it over computing `skip + top` yourself:
  when a server page is smaller than the requested `$top`, those two diverge and
  the manual form silently skips records.
- `page.has_more` is sugar for `page.next_params is not None`.
- `page.total_count` is the server-side total (`@odata.count`) — the full
  result-set size, not the page size. It is `None` unless you asked for it with
  `$count=true` (`ODataQuery(count=True)`), so you get the total without a
  separate `$count` round-trip.
- `page.to_list()` returns the records as a plain `list[T]`.

The async client is symmetric: `page = await client.items.list(...)`.

### `$top` and `has_more` (fence-post, low-level `.list()`)

SAP B1 omits `@odata.nextLink` when the requested `$top` fits within a single
server page (`top ≤ page size`) — from its perspective the request is "satisfied"
once `$top` rows are returned. A naive `has_more` would therefore read `False`
under a small `.top(N)` even when more matching rows exist, silently hiding them.
(Verified against a live 10.0 HANA server: `top=5` on a 10k-row collection
returns 5 rows and **no** nextLink.) To avoid that, `.list()` transparently
requests one extra row (`$top + 1`), truncates the page back to `N`, and sets
`has_more=True` when the extra row materialises — synthesising the next `$skip`
cursor so manual paging keeps working:

```python
page = client.items.list(ODataQuery(filter="Properties64 eq 'tYES'", top=20))
len(page)        # 20 (the probe's 21st row is truncated away)
page.has_more    # True when a 21st matching row exists — no false positives
page.next_skip   # 20

while page.has_more:                                   # paginate in 20-row pages
    page = client.items.list(params=page.next_params)
```

This costs at most one extra row over the wire per page and never affects
requests without `$top`. (`.execute()` builds on this for its first page, then
keeps paging until it has collected the full `.top(N)`.)

---

## Configuration & Safety Limits

You can control the HTTP request behavior and add safety bounds to prevent runaway streams.

### `page_size`
Controls the `B1S-PageSize` header — how many rows SAP returns per HTTP request.
- **Smaller**: Less memory per request, more HTTP calls.
- **Larger**: More memory per request, fewer HTTP calls (more efficient).

It is available three ways, all equivalent:

```python
# As a stream() argument
async for item in client.items.stream(page_size=100):
    pass

# As a builder method (composable; also works with .list()/.execute())
page = client.items.filter("ItemType eq 'itItems'").page_size(100).execute()
async for item in client.items.page_size(100).stream():
    pass

# As a list() keyword
page = client.items.list(page_size=100)
```

An explicit `stream(page_size=...)` argument overrides any `.page_size()` set on
the builder. Unlike `.top()`, `page_size` sets SAP's *page boundary* (so it
emits an `@odata.nextLink`); it does not cap the total rows.

### `max_pages`
Safety ceiling to limit the number of HTTP requests made by the stream.

```python
# Stop after fetching at most 3 pages
async for item in client.items.stream(max_pages=3):
    pass
```

### Global `.top(N)`
In stream mode, `.top(N)` acts as a **hard global cap on total rows yielded** —
not a page size. It is enforced client-side and the stream stops once `N` rows
have been produced, possibly mid-page.

```python
# Fetches exactly 25 items total across multiple pages (3 × page_size 10, then stops)
async for item in client.items.top(25).stream(page_size=10):
    pass
```

> **Why `$top` is not sent to SAP in stream mode.** `stream()` strips `$top`
> from the server request and enforces the cap purely client-side. This keeps
> `.top(N)` unambiguous as a *global total* and avoids forwarding a `$top` that
> would otherwise be re-applied relative to each page's `$skip` cursor (muddled
> semantics). In practice SAP still pages correctly either way — when
> `top > page_size` it returns a nextLink, and when `top ≤ page_size` a single
> page already holds all `N` rows — so this is a clarity/robustness measure, not
> a fix for observed data loss. (`.list()`/`.execute()` *do* send `$top` and use
> the fence-post probe above to keep `has_more` correct.)

---

## Filter Persistence Guarantee

A common bug in manual pagination is forgetting to re-apply filters to `nextLink` requests (which SAP sometimes omits in the URL). 

The SDK's `build_next_params` logic **guarantees** that your original `$filter`, `$select`, and `$orderby` parameters are re-injected into every subsequent page request. Your stream will never "leak" outside its initial scope.

---

## Advanced Patterns

### Collection: Gathering into a single list
If you really need all items in memory at once, use a list comprehension. The SDK will handle all HTTP requests required to fill the list.
```python
# Async — using static constants (recommended for clarity)
from b1sl.b1sl.fields import Item
items = [item async for item in client.items.filter(Item.frozen == 'tNO').stream()]

# Sync
items = list(client.items.filter(Item.frozen == 'tNO').stream())
```

### Progress Tracking (Count + Stream)
Since generators don't know the total size in advance, call `.count()` first if you need to calculate progress.
```python
# 1. Very fast header-only request
total = await client.items.filter(query).count()

# 2. Iterate with progress
count = 0
async for item in client.items.filter(query).stream():
    count += 1
    print(f"Processing {count}/{total} ({(count/total)*100:.1f}%)")
```

### Aggregation
Streaming is ideal for counting or collecting data without loading everything into memory at once.

```python
total_value = 0
async for item in client.items.stream():
    total_value += (item.price or 0)
```

### Safety Bounds with `islice` (Sync)
For sync clients, you can use `itertools.islice` to consume only a part of the stream.

```python
from itertools import islice

# Consume exactly 50 items from a larger collection
for item in islice(client.items.stream(), 50):
    process(item)
```
