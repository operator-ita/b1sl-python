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
| **`.list()`** | Resource | `list[T]` | **Single Page**. Returns only what SAP sends first. |
| **`.execute()`** | Builder | `list[T]` | **Single Page**. Triggers the fluent query. |
| **`.stream()`** | Either | `Generator` | **Transparent**. Fetches every page until exhaustion. |

---

## Configuration & Safety Limits

You can control the HTTP request behavior and add safety bounds to prevent runaway streams.

### `page_size`
Controls the `B1-PageSize` header. 
- **Smaller**: Less memory per request, more HTTP calls.
- **Larger**: More memory per request, fewer HTTP calls (more efficient).

```python
# Fetch 100 items at a time per HTTP request
async for item in client.items.stream(page_size=100):
    pass
```

### `max_pages`
Safety ceiling to limit the number of HTTP requests made by the stream.

```python
# Stop after fetching at most 3 pages
async for item in client.items.stream(max_pages=3):
    pass
```

### Global `.top(N)`
The `.top(N)` builder method acts as a **hard global limit** for the entire stream, regardless of page sizes.

```python
# Will fetch exactly 25 items total, even if it requires multiple pages
async for item in client.items.top(25).stream(page_size=10):
    pass
```

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
