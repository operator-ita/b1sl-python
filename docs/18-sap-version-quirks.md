# SAP Version Quirks

A living registry of version-specific SAP Business One Service Layer behaviors
that the SDK works around. Each entry records the evidence so future
maintainers (and SAP support tickets) don't have to re-derive it.

**When to add an entry**: any time the SDK gains a workaround whose reason
lives on SAP's side — a wire-level behavior that contradicts the OData spec,
SAP's own documentation, or common sense. Record the SAP version and platform
where it was observed, the raw evidence, and the SDK mitigation. Re-verify
entries when upgrading SAP versions; if SAP fixes one, note the fixed version
here rather than deleting the entry.

This document is excluded from the wheel (like all of `docs/`) but versioned
in git.

---

## Q1 — `$select` reads return a frozen, unusable `@odata.etag` in the body

| | |
|---|---|
| **Observed on** | SAP Business One **2511**, HANA, Service Layer OData v4 (`/b1s/v2`) |
| **Date verified** | 2026-08-12 |
| **SDK mitigation** | `trust_body=False` in `_extract_etag()` (`base_adapter.py`) — `$select` responses never touch the ETag cache |
| **Regression tests** | `tests/unit/test_rest_adapter.py` (`$select` block), `tests/unit/test_async_adapter.py` |
| **SAP acknowledgment** | None found as of 2026-08 (see Research below). Candidate for a new SAP support incident. |

### Symptom

After a `GET` with `$select` on an ETag-enabled ("Elite") entity, the next
`PATCH`/`DELETE` on that entity fails with:

```json
HTTP 412
{"error": {"code": "-2039", "message": "Another user or another operation
modified data; to continue, open the window again (ODBC -2039)"}}
```

…even though nobody touched the record. The SDK surfaced it as a
false-positive `SAPConcurrencyError`.

### Wire evidence (captured with raw httpx, no SDK involved)

Full entity read — header and body ETags present and consistent:

```http
GET /b1s/v2/Items('9990130012001')
HTTP/1.1 200 OK
ETag: W/"1B6453892473A467D07372D45EB05ABC2031647A"

{"@odata.etag": "W/\"1B6453892473A467D07372D45EB05ABC2031647A\"", ...}
```

Projected read — header **absent**, body annotation present but **wrong**:

```http
GET /b1s/v2/Items('9990130012001')?$select=ItemCode,ItemName
HTTP/1.1 200 OK
(no ETag header)

{"@odata.context": "...",
 "@odata.etag": "W/\"356A192B7913B04C54574D18C28D46E6395428AB\"",
 "ItemCode": "9990130012001", "ItemName": "..."}
```

Three facts make the body value provably unusable:

1. **SAP rejects its own ETag**: sending that body `@odata.etag` verbatim as
   `If-Match` in a PATCH → `412 -2039`.
2. **It never changes**: across 5 writes to the same record, the full-GET ETag
   advanced (`sha1("2")` → `sha1("4")` → `sha1("6")`) while the `$select` body
   ETag stayed at `sha1("1")` forever.
3. **A PATCH with no `If-Match` after a `$select` read succeeds** (204) — the
   failure was purely the poisoned ETag, not a server-side lock.

### Root cause

SAP's weak ETags are `W/"sha1(<version counter as decimal string>)"` — the
hashes observed match `sha1("1")`, `sha1("2")`, `sha1("4")`, `sha1("6")`
exactly, incrementing once per write. The official Service Layer manual
(§5.4 "ETag Metadata") confirms the ETag derives from a per-entity concurrency
property declared in the OData metadata:

```xml
<Annotation Term="Org.OData.Core.V1.OptimisticConcurrency">
  <Collection><PropertyPath>DataVersion</PropertyPath></Collection>
</Annotation>
```

Inference (mechanism, unconfirmed by SAP): with `$select`, the SQL projection
never loads that version column, so the serializer stamps
`@odata.etag = sha1(default value 1)`. SAP omitting the ETag *header* on
projected reads suggests intent — a projected read is not a valid basis for
optimistic concurrency — but the OData serializer stamps the body annotation
unconditionally, producing the inconsistent value.

### SDK behavior after the fix

- `$select` responses never write to the ETag cache (bogus body value ignored,
  and a valid ETag cached by an earlier full GET is not clobbered).
- A header `ETag` is always authoritative, including on `$select` responses —
  if SAP ever fixes this, the SDK picks it up automatically with no change.
- Consequence for callers: an update after a `$select`-only read is a **blind
  write** (no optimistic concurrency). If concurrency protection matters for a
  flow, do a full `GET` before writing.

### Research (2026-08)

- **Official manual**: [Working with SAP Business One Service Layer
  (v10.0)](https://help.sap.com/doc/fc2f5477516c404c8bf9ad1315a17238/10.0/en-US/Working_with_SAP_Business_One_Service_Layer.pdf),
  ch. 5. Documents ETag support (FP 2102+), weak validation, the exact `-2039`
  412 body, and §5.4's `OptimisticConcurrency` annotation. **Never mentions
  `$select` + ETag**; every example uses full GETs. (Its examples even use
  `W/"356A192B..."` = `sha1("1")`.)
- **No public report of this exact defect** was found: no SAP Note/KBA, no SAP
  Community thread, no issue in other SL SDKs (checked B1SLayer's tracker —
  only an unrelated `$batch` ETag question,
  [#54](https://github.com/bgmulinari/B1SLayer/issues/54)).
- **Precedent for `$select` projection bugs**: [SAP Note 2722485 —
  `$select` returns `null` for some UDT-derived
  fields](https://community.sap.com/t5/enterprise-resource-planning-q-a/sap-b1-service-layer-select-option-doesn-t-work-for-some-user-defined/qaq-p/814529)
  (different symptom, same subsystem) — officially acknowledged and patched,
  showing SL's `$select` column resolution has a history of correctness bugs.
- Nearest `-2039` KBA
  ([3195415](https://userapps.support.sap.com/sap/support/knowledge/en/3195415))
  is a DI-API/UI scenario, unrelated to Service Layer projections.
