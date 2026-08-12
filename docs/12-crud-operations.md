# CRUD Operations (Create, Read, Update, Delete)

The SAP B1 Python SDK provides a consistent, type-safe interface for performing standard CRUD operations on all supported entities.

## Resource Access

All entities are accessible through the `B1Client` (Synchronous) or `AsyncB1Client` (Asynchronous) via their corresponding aliases:

```python
# Synchronous
bp = b1.business_partners.get("C0001")

# Asynchronous
bp = await b1.business_partners.get("C0001")
```

---

## 1. Create (POST)

To create a new record, instantiate the model from `b1sl.b1sl.entities` and pass it to the `.create()` method.

```python
from b1sl.b1sl import entities as en

new_bp = en.BusinessPartner(
    card_code="NEW_BP",
    card_name="New Business Partner",
    card_type=en.BoCardTypes.cCustomer
)

# Async
created_bp = await b1.business_partners.create(new_bp)

# Sync
created_bp = b1.business_partners.create(new_bp)
```

---

## 2. Read (GET)

There are two main ways to read data: by unique identifier (Primary Key) or via the Query Builder.

### By ID
```python
# Async
bp = await b1.business_partners.get("C0001")

# Sync
bp = b1.business_partners.get("C0001")
```

### Checking Existence & Counting
```python
# Exist check (fast GET)
if await b1.business_partners.exists("C0001"):
    print("Found!")

# Count records
total_customers = await b1.business_partners.count()
print(f"Total: {total_customers}")
```

---

## 3. Update (PATCH)

SAP Business One uses the `PATCH` method for updates. The SDK strongly recommends using **"Surgical Deltas"** to avoid data loss and ETag conflicts.

### Surgical Delta Pattern (Recommended)
Instead of modifying and re-sending a complete object, create a new, minimal object containing only the fields you wish to change.

```python
# 1. Prepare only the fields to change
delta = en.BusinessPartner(
    card_name="Updated Name",
    email_address="new@example.com"
)

# 2. Apply the update
await b1.business_partners.update("C0001", delta)
```

> [!TIP]
> This pattern is more efficient and significantly reduces the chance of `SAPConcurrencyError` (412) because you are only sending what needs to be changed.

### Replacing child collections (`replace_collections=True`)

By default, SAP **merges** child collections on PATCH — existing members
always survive. A member is treated as an **in-place update** only when it
carries the collection's full identifier set; otherwise it is an **insert**.
For `DocumentLines` the identifier is `LineNum`; for **`BPAddresses`**
(verified live on SAP B1 2511, HANA, MX) it is the full quartet
**`BPCode` + `AddressName` + `AddressType` + `RowNum`** — with any of them
missing, the member is inserted: a new `AddressName` is appended (3 addresses
+ 2 sent = **5**) and an existing one fails with `-2035 This entry already
exists`. Full evidence: [docs/18-sap-version-quirks.md, Q2](18-sap-version-quirks.md).

**To edit one address**, send the 4 identifiers plus the fields to change —
no header needed:

```python
await b1.business_partners.update("C0001", {
    "BPAddresses": [{
        "BPCode": "C0001", "AddressName": "MEXICOAAA",
        "AddressType": "bo_BillTo", "RowNum": 2,
        "City": "Monterrey",                      # the actual change
    }],
})
```

To replace the collection wholesale — reshape it or **remove** members — SAP
requires the `B1S-ReplaceCollectionsOnPatch: true` header, exposed as a flag:

```python
bp = en.BusinessPartner(
    bp_addresses=[
        en.BPAddress(address_name="Warehouse", city="CDMX"),
        en.BPAddress(address_name="Office", city="Toluca"),
    ]
)
# The partner ends up with exactly these 2 addresses — no index merging.
await b1.business_partners.update("C0001", bp, replace_collections=True)
```

> [!WARNING]
> Under replace, members **absent from the payload are deleted**, and members
> sent without their `RowNum` are re-inserted with renumbered `RowNum` values.
> Never persist `RowNum` as a stable address identifier — documents reference
> addresses by `AddressName` (`PayToCode`/`ShipToCode`), which is stable as
> long as the name is kept.

### Verbatim dict payloads (`update(key, dict)`)

`update()` accepts either a typed model or a plain `dict`, and the type you
pass selects the serialization policy:

| You pass | Policy |
|---|---|
| a model (`en.Item(...)`) | **Surgical delta** — `to_api_payload()` sends only the fields you explicitly set; Python values are SAP-encoded (`True` → `"tYES"`, `date` → ISO). |
| a `dict` | **Verbatim passthrough** — sent to the wire exactly as given. No `exclude_unset`, no re-encoding. |

With a dict, the payload is entirely your responsibility: keys must be SAP
aliases (`"CardName"`, not `card_name`) and values SAP-encoded (`"tYES"`, not
`True`). This is the tool for byte-exact round-trips of data fetched from
SAP — e.g. re-sending child-collection rows without any model transformation:

```python
raw = (await b1.business_partners.get("C0001")).model_dump(by_alias=True)
rows = raw["BPAddresses"]
for r in rows:
    if r["AddressName"] == "MEXICOAAA":
        r["City"] = "Monterrey"
await b1.business_partners.update(
    "C0001", {"BPAddresses": rows}, replace_collections=True
)
```

### Custom request headers

`get()`, `create()`, `update()` and `delete()` accept a `headers=` dict that
is passed through to the Service Layer — the escape hatch for any special
header without touching private adapter internals. An explicit
`B1S-ReplaceCollectionsOnPatch` in `headers` wins over `replace_collections`.

```python
await b1.business_partners.update(
    "C0001", bp, headers={"B1S-ReplaceCollectionsOnPatch": "true"}
)
```

Caller headers are merged on top of the SDK's own (e.g. `If-Match`), so ETag
concurrency still applies. Inside `$batch`, headers are serialized into the
corresponding part.

---

## 5. ETag & Concurrency

The SDK automatically manages ETags during the request lifecycle. Every entity model has a built-in `.etag` property.

### Accessing ETag
```python
item = b1.items.get("A0001")
print(f"Current version (ETag): {item.etag}")
```

### Conflict Handling
If a conflict occurs (i.e., someone else modified the record between your GET and PATCH), the SDK raises a `SAPConcurrencyError`.

```python
from b1sl.b1sl.exceptions import SAPConcurrencyError

try:
    await b1.items.update("A0001", delta)
except SAPConcurrencyError as e:
    print("Version mismatch! Refreshing data and retrying...")
```

---

## 4. Delete (DELETE)

To remove a record, use the `.delete()` method with the resource ID.

```python
# Async
await b1.business_partners.delete("C0001")

# Sync
b1.business_partners.delete("C0001")
```

---

## Full Examples

Check the `examples/` directory for complete, runnable scripts:
- [Sync CRUD](../examples/15_sync_crud.py)
- [Async CRUD](../examples/16_async_crud.py)
- [Robust Error Handling](../examples/14_robust_error_handling.py)
