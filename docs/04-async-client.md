# Asynchronous Client (AsyncB1Client)

The `AsyncB1Client` is the recommended way to interact with SAP Business One in modern, high-concurrency Python applications like **FastAPI**, **Temporal**, or **Sanic**.

---

## 1. Why Async?

- **Concurrency**: Process multiple SAP entities (items, orders, BP) simultaneously without blocking the main event loop.
- **Resilience**: The async adapter includes sophisticated retry logic and session safety.
- **Faster Batching**: While SAP does not support true HTTP pipelining, async allows you to manage many in-flight requests concurrently, drastically reducing overall wait times for bulk tasks.

---

## 2. Basic Usage

Use the `async with` context manager to automate the lifecycle of the SAP session (Login and Logout).

```python
import asyncio
from b1sl.b1sl import AsyncB1Client, B1Environment

async def main():
    # 1. Load config
    env = B1Environment.load()
    
    # 2. Start an async session
    async with AsyncB1Client(env.config) as b1:
        # 3. Typed call
        item = await b1.items.get("A0001")
        print(f"Item: {item.item_name}")

asyncio.run(main())
```

> [!IMPORTANT]
> The `async with` block automatically handles the `POST /Logout` call for you, releasing the SAP license even if an exception occurs during the process.

---

## 3. Entity Access & Typing (First-Class Citizens)

To give you a seamless Developer Experience (DX) with full IDE auto-completion, the `AsyncB1Client` exposes **16 Canonical Convenience Aliases** mapping directly to standard Pydantic models.

### The Top 16 Aliases
- **Master Data**: `items`, `business_partners`, `users`
- **Sales Flow**: `quotations`, `orders`, `delivery_notes`, `invoices`, `incoming_payments`
- **Purchasing Flow**: `purchase_orders`, `purchase_delivery_notes`, `purchase_invoices`, `vendor_payments`
- **Operations & Support**: `production_orders`, `journal_entries`, `service_calls`, `activities`

Example:
```python
# Fully typed as AsyncGenericResource[Document]
invoice = await b1.invoices.get(100) 
```

### Dynamic Entities: The `get_resource` Contract

For any SAP entity not explicitly aliased in the top 16, the SDK uses the `get_resource()` mechanism. This provides dynamic access without sacrificing type safety. 

```python
from b1sl.b1sl.models._generated.entities.inventory import ItemWarehouseInfo

# Type-safe access to ANY endpoint dynamically
whse_resource = b1.get_resource(ItemWarehouseInfo, "ItemWarehouseInfo")
whse_data = await whse_resource.get("A0001")
```

All thin aliases (like `b1.items`) are literally just syntactic sugar delegating to `get_resource()`.

### Extending the Client (Custom Aliases)

**Is subclassing a good idea?** Yes, absolutely! For enterprise repositories where specific SAP modules are heavily used (e.g., HR modules, specific UDOs, or lesser-known endpoints), creating a domain-specific client subclass is the recommended best practice. It maintains full type safety without needing to modify the core SDK.

```python
from b1sl.b1sl import AsyncB1Client
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.models._generated.entities.inventory import ItemWarehouseInfo

class MyCompanyB1Client(AsyncB1Client):
    @property
    def warehouses(self) -> AsyncGenericResource[ItemWarehouseInfo]:
        """Custom fully-typed alias for ItemWarehouseInfo."""
        return self.get_resource(ItemWarehouseInfo, "ItemWarehouseInfo")

async def main():
    async with MyCompanyB1Client(config) as b1:
        whse = await b1.warehouses.get("A0001")
        print(whse)
```

---

## 4. High Concurrency with `asyncio.gather`

You can send many requests at once. The `AsyncRestAdapter` uses a single shared `httpx.AsyncClient` and a thread-safe `asyncio.Lock` to manage the session token across multiple concurrent tasks.

```python
async with AsyncB1Client(config) as b1:
    codes = ["A0001", "A0002", "A0003"]
    
    # Launch tasks concurrently
    tasks = [b1.items.get(code) for code in codes]
    
    # Wait for all to finish
    items = await asyncio.gather(*tasks)
```

---

## 5. Key Async Features

### Session Resilience (401 Auto-Retry)
If the SAP session expires (e.g., after 30 minutes of inactivity), the `AsyncRestAdapter` will catch the `401 Unauthorized` error, automatically perform a re-login, and retry your original request once.

### Session Locking
In high-concurrency environments like **FastAPI**, multiple requests might hit the SDK at the exact same moment. The SDK uses an internal `asyncio.Lock` to ensure that only one "Login" operation happens at a time, preventing session ID floods and license wastage.

### Manual Cleanup
If you cannot use a context manager (e.g., in a long-running background service), you can manage the adapter manually:

```python
client = AsyncB1Client(config)
await client.connect() # Manual Login
# ... use client ...
await client.aclose() # Manual Logout
```

### 5.4 Safety: Dry Run Mode (Task-Safe)
For safe debugging in shared async environments, use the `with b1.dry_run()` context manager. It uses `ContextVar` to ensure that enabling dry run in one task does NOT affect others.

```python
async with AsyncB1Client(config) as b1:
    # This block is safe; no real PATCH sent to SAP
    with b1.dry_run():
        await b1.items.update(item_code, item_data)
```

---

## 6. Performance Tips

- **Shared Client**: Always reuse the same `AsyncB1Client` instance for multiple operations within the same logical unit of work.
- **Timeout Management**: Use the `connect_timeout` and `read_timeout` in `B1Config` to tune performance based on your Service Layer's speed.
