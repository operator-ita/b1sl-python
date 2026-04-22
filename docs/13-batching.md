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

## Result Inspection

Results are returned as a `BatchResults` container, which flattens all responses (including those from changesets) into a single ordered list.

```python
if results.all_ok:
    print(f"Entities created: {results[2].entity.item_code}")
else:
    for r in results.failed:
        print(f"Error in op {r.index}: {r.error}")
```

## Important Constraints

-   **GET in ChangeSets**: OData V4 prohibits `GET` operations within a ChangeSet. The SDK enforces this at runtime.
-   **Explicit Execution**: You must call `await batch.execute()` within the context block to trigger the actual network request.

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
