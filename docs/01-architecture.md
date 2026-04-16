# SDK Architecture & Principles

## Core Vision
This SDK is designed as a **metadata-first**, type-safe bridge between Python and SAP Business One. Unlike traditional "wrapper" libraries that require manual maintenance for every new SAP field or entity, this project automates the entire model and resource layer by parsing OData metadata.

---

## Architectural Pillars

The following pillars describe **how the SDK is built internally**. Understanding them will help you navigate the codebase and extend it correctly.

### 1. Separation of Concerns (Generated vs. Handcrafted)
The codebase is strictly divided into three layers:
- **`models/_generated/`**: Fully automated Pydantic v2 models. **Never edit these files.** They are overwritten on every schema refresh.
- **`models/_overrides/`**: Manual extensions. This is the place to add calculated properties, custom methods, or fix metadata quirks.
- **`entities/` (Public Facade)**: A unified namespace that blends generated models with your manual overrides. Developers should only import from here:
  ```python
  from b1sl.b1sl import entities as en
  item = en.Item(item_code="A001")
  ```

### 2. The `B1Model` Base Class
Every entity inherits from `B1Model`, which provides global data normalization transparently:
- **Boolean Coercion**: Automatically maps SAP's `"tYES"`/`"tNO"` to Python `bool`.
- **Date Handling**: Converts SAP's `/Date(ms)/` strings into Python `date` objects.
- **Null Filtering**: The `.to_api_payload()` method uses `exclude_unset=True` (Pydantic), so only fields you explicitly set are sent to SAP. This is the foundation of the **Surgical Delta** pattern.

### 3. Service-Resource Pattern (Elite vs Generic)
The SDK embraces a "Concurrency-Elite" architecture to reduce memory bloat and signal safe usage:
- **Elite Properties**: Only a small subset of highly-used SAP entities that guarantee OData ETag concurrency locking (e.g., `items`, `business_partners`, `orders`) are exposed as direct native properties on the `B1Client` (e.g., `client.items`).
- **Generic Access**: For the other ~1000+ endpoints that lack ETag safety or are less commonly used, developers must explicitly bind the resource dynamically using `client.get_resource(Model, "EndpointName")`. This conscious step acts as a safety signal.

Each resource, whether Elite or Generic, provides:
- **Standard CRUD**: `get()`, `list()`, `create()`, `update()`, `delete()`.
- **Typed OData**: A fluent, Pythonic `QueryBuilder` with operator overloading on `fields` constants for type-safe filtering and expansions.
- **Unbound Actions**: SAP business logic methods (like `Cancel`, `Close`, `Reopen`) extracted from the OData metadata.

### 4. Metadata Integrity (The "Vanilla" Policy)
By default, the generator filters out all User-Defined Fields (`U_*`) and User-Defined Tables (`@*`). This ensures the core SDK remains version-agnostic and clean. Customizations are handled locally via the Override system or the Hybrid interaction pattern described in [05-interaction-patterns.md](./05-interaction-patterns.md).

---

## Design Patterns & Technical Rationale

The following patterns describe **how you should use the SDK** as a developer. They are deliberate design decisions aligned with modern software engineering and the specific constraints of SAP Service Layer.

### 1. Data Mapper over Active Record
This SDK follows the **Data Mapper** pattern, not **Active Record** (as found in Django ORM or Rails).

| | Active Record | Data Mapper (this SDK) |
|:--|:--|:--|
| **Model** | Knows how to save itself | Pure data container (DTO) |
| **Persistence** | `bp.save()` | `client.business_partners.update(id, bp)` |
| **Testing** | Requires DB/network | Models are testable in isolation |

```python
# ✅ Good (Data Mapper)
client.business_partners.update("C001", en.BusinessPartner(card_name="New Name"))

# ❌ Avoid (Active Record style — not supported and unsafe in SAP)
bp.card_name = "New Name"
bp.save()
```

### 2. Surgical (Delta) Mutations
Only send the fields you intend to change. The SDK enforces this by using `exclude_unset=True` when serializing payloads for `PATCH` requests.

```python
# ✅ Good — sends only {"CardName": "New Name"} to SAP
client.items.update("A001", en.Item(item_name="New Name"))

# ❌ Avoid — fetching all 500 fields and sending them back risks
# overwriting unrelated data and triggering read-only field validation errors.
item = client.items.get("A001")
item.item_name = "New Name"
client.items.update("A001", item)
```

### 3. Optimistic Concurrency & ETag Strategy
SAP Service Layer uses **Optimistic Locking** via HTTP ETags to prevent "Lost Updates" in concurrent environments. The SDK handles this automatically with a "Proactive Invalidation" policy:

1. **Capture**: Every successful `GET` caches the `ETag` header.
2. **Injection**: Every `PATCH` / `DELETE` attaches it as `If-Match: <cached-etag>`.
3. **Proactive Invalidation**: After a successful `PATCH`, the SDK **immediately clears** the cached ETag. Since SAP often returns `204 No Content` without a new ETag header, clearing the cache prevents using a stale version in subsequent calls (like a DELETE immediately after an UPDATE).
4. **Collision Handling**: If a real conflict occurs (status `412`), the SDK raises `SAPConcurrencyError`.

> [!TIP]
> **The Robust Retry Pattern**.
> When performing sequential mutations on the same object, always use a retry loop that performs a fresh `GET` on conflict. This handles both external modifications and SAP's ETag-reporting gaps.
