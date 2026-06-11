# 13. OData $batch Support

The SAP B1 Python SDK supports OData `$batch` requests using a **Proxy-based Recording Pattern**. This allows you to group multiple operations into a single HTTP request while maintaining high performance and atomic integrity.

## Why use Batching?

1.  **Performance (Network Efficiency)**: Grouping 50 GET requests into 1 batch reduces network latency and avoids the overhead of 50 SSL/TCP handshakes.
2.  **Atomicity (Transaction Integrity)**: Using a `changeset` ensures that either all write operations succeed, or all are rolled back. This is critical for complex operations like creating an Invoice along with its corresponding payment.
3.  **Concurrency**: Reduces the window of time where data might be outdated between multiple sequential calls.

## Using the Batch Client

The `batch()` context manager intercepts standard resource calls and enqueues them.

```python
async with b1.batch() as batch:
    # Operations are enqueued, not executed
    await batch.items.top(1).execute() 
    
    # Atomic transaction scope
    async with batch.changeset() as cs:
        await cs.items.create(en.Item(item_code="B101", item_name="New Item"))
        await cs.business_partners.update("C20000", update_data)

    # DISPATCH: One single HTTP POST $batch
    results = await batch.execute()
```

### Sync client

`B1Client.batch()` has full parity — same recording API, plain `with` blocks:

```python
with B1Client(config) as b1:
    with b1.batch() as batch:
        batch.items.top(1).execute()

        with batch.changeset() as cs:
            cs.items.create(en.Item(item_code="B101", item_name="New Item"))
            cs.business_partners.update("C20000", update_data)

        results = batch.execute()
```

### Dry Run

`$batch` honours Dry Run like every other write path: under `B1SL_DRY_RUN=1`
or inside `with b1.dry_run():`, `batch.execute()` returns a synthesized
`BatchResults` (one `204` per recorded operation, `index` preserved) without
sending anything to SAP.

## Result Inspection

Results are returned as a `BatchResults` container, which flattens all responses (including those from changesets) into a single ordered list.

```python
if results.all_ok:
    print(f"Entities created: {results[2].entity.item_code}")
else:
    for r in results.failed:
        print(f"Error in op {r.index}: {r.error}")
```

## SQL Queries (`/List`) inside a Batch

The `SQLQueries` bounded function `/List` (see [15. SQL Queries](15-sql-queries.md)) **is supported inside `$batch`** — verified against a live Service Layer: each part returns an inner `200` with its own row page. The ergonomic path works exactly like any other resource:

```python
batch = b1.batch()
await batch.sql_queries.run("EXPENSIVE_QUERY", cardCode="C20000")
await batch.sql_queries.run("EXPENSIVE_QUERY", cardCode="C30000")

results = await batch.execute()
for r in results:
    rows = r.data.get("value", [])   # raw JSON rows, see note below
```

Each call is enqueued as `POST SQLQueries('CODE')/List` with the `ParamList` body, and `page_size=N` is honored via a per-part `Prefer: odata.maxpagesize=N` header.

Two differences versus a direct `b1.sql_queries.run()`:

-   **Raw rows, not `SQLRunResult`**: batch results come back as the raw response dict — read the rows from `r.data["value"]`. Helpers like `.has_more` are not available.
-   **First page only**: `odata.nextLink` is not followed inside a batch. For full datasets use `run_stream()` outside the batch.

Since `/List` is a read, enqueue it as a **top-level** batch operation — not inside a `changeset()`.

## Important Constraints

-   **GET in ChangeSets**: OData V4 prohibits `GET` operations within a ChangeSet. The SDK enforces this at runtime.
-   **Explicit Execution**: You must call `await batch.execute()` within the context block to trigger the actual network request.
-   **No ETag concurrency inside `$batch`**: batch parts never carry an
    `If-Match` header — the recording proxy bypasses the adapter layer that
    injects cached ETags. A batched `update()`/`delete()` performs a *last
    write wins* overwrite, unlike the same call outside a batch (which raises
    `SAPConcurrencyError` on a stale ETag). If optimistic concurrency matters
    for a write, execute it as a regular single operation instead.

### The "Defensive Analysis" Pattern (Recommended)

Because `batch.execute()` supports **Partial Success**, it does not raise exceptions. Instead, you should follow this pattern:

1.  **Check Global Flag**: Use `all_ok` for a fast initial check.
2.  **Iterate Failures**: If not all okay, iterate `results.failed` to log exactly what went wrong.
3.  **Handle Atomic Sets**: Remember that a failed op inside a ChangeSet means the *entire* ChangeSet failed.

```python
results = await batch.execute()

# 1. High-level gate
if results.all_ok:
    return results[0].entity

# 2. Granular Traceability
for failure in results.failed:
    # Use failure.index to match back to your original code logic
    print(f"❌ Operation {failure.index} failed with status {failure.status}")
    print(f"   Reason: {failure.error}")
```
