# Changelog

All notable changes to `b1sl-python` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/) (pre-1.0:
minor versions may include breaking changes).

## [Unreleased]

## [0.10.0] — 2026-08-12

### Added
- **Verbatim dict payloads in `update()`** — the signature is now
  `update(key, entity: T | dict, ...)` (sync, async and UDO resources). A
  typed model keeps the Surgical Delta policy (`to_api_payload()`,
  `exclude_unset`, SAP value encoding); a `dict` is sent to the wire exactly
  as given — no serialization, no re-encoding — for byte-exact round-trips of
  raw SAP data. Documented in `docs/12-crud-operations.md`.

### Changed
- **`BPAddresses` PATCH semantics corrected** (docs Q2 + VCR test): live
  bisection on SAP B1 2511 showed the collection is *not* append-only — a
  member updates **in place** when it carries the full identifier quartet
  `BPCode` + `AddressName` + `AddressType` + `RowNum`; with any missing it is
  an INSERT (append or `-2035`). Under `replace_collections`, rows sent with
  their `RowNum` keep it; rows without are renumbered. The VCR test now pins
  the in-place path too.

## [0.9.0] — 2026-08-12

### Added
- **Custom request headers on CRUD** — `get()`, `create()`, `update()` and
  `delete()` (sync and async, including `UDOResource`) accept a keyword-only
  `headers=` dict passed through to the Service Layer. Caller headers merge on
  top of the SDK's own (`If-Match` etc.), so ETag concurrency is preserved;
  inside `$batch` they are serialized into the corresponding part. This
  removes the last known reason to call `client._adapter` directly.
- **`update(..., replace_collections=True)`** — semantic flag that sends
  `B1S-ReplaceCollectionsOnPatch: true`, making SAP replace child collections
  (e.g. `BPAddresses`) wholesale instead of merging them (default PATCH keeps
  existing members; verified live on SAP B1 MX). An explicit header in
  `headers=` wins over the flag. Documented in `docs/12-crud-operations.md`.
- **VCR integration test for BPAddresses PATCH semantics**
  (`tests/integration/test_bp_addresses_real.py`) — pins the server behavior
  behind `replace_collections` (append-only default, `-2035` on existing
  `AddressName`, wholesale replace with the header) as a replayable cassette;
  re-record after SAP upgrades to detect semantic drift. Full evidence
  registry: `docs/18-sap-version-quirks.md` Q2.

### Fixed
- **Cassette scrubbing hardened** (`tests/conftest.py`): real hosts are now
  scrubbed from request headers (`Host:`) and response headers (`Location:`),
  which the httpx-based adapter records; UDFs are dropped key-and-value (even
  `U_*` field *names* are company-internal schema metadata); SAP enum literals
  (`tYES`/`tNO`, `bo_*`) are exempt from body redaction so replayed cassettes
  still pass model validation.

## [0.8.0] — 2026-08-12

### Added
- **Public API for OData actions and functions** — consumers no longer need to
  touch `_adapter` or underscore methods:
  - `resource.action(key, name, payload=None, *, params=None, headers=None,
    method="POST")` — bound actions/functions on a keyed entity
    (e.g. `invoices.action(123, "Cancel")`). Also records inside `$batch`
    blocks (`batch.orders.action(...)`). The previous `_action` name remains
    as a backwards-compatible alias.
  - `resource.function(name, params=None)` — unkeyed, read-only
    `GET Endpoint/FunctionName` calls (`_function` kept as alias).
  - `client.call_service_method(name, payload=None)` (sync and async) — the
    low-level escape hatch for the ~1000 unbound `*Service_*` root operations
    (e.g. `SBOBobService_SetCurrencyRate`). A single entry point covers both
    SL "actions" and "functions", since the Service Layer invokes both as
    POST with a JSON body. Goes through the adapter, so dry-run interception
    and semantic exception mapping apply; no ETag concurrency (unbound).
- **`client.base_url`** (sync and async) — public read-only property exposing
  the normalized Service Layer base URL (including `/b1s/<version>`);
  previously only reachable via the private `_adapter`.

### Fixed
- **False-positive `SAPConcurrencyError` (412 / SAP -2039) on PATCH/DELETE
  after a `GET` with `$select`.** Verified on SAP B1 2511 (HANA): projected
  reads omit the `ETag` response header but still carry a body `@odata.etag`
  computed from a version field the projection never loaded — frozen at
  `sha1("1")` regardless of the record's real version. The adapter's body
  fallback cached that value and poisoned the next `If-Match`. `$select`
  responses now never touch the ETag cache (they neither cache the bogus
  value nor clobber a valid ETag from an earlier full GET); a header `ETag`
  remains authoritative if SAP ever sends one. Note: an update after a
  `$select`-only read is a blind write — do a full `GET` first when
  optimistic concurrency matters. Full wire-level evidence in
  `docs/18-sap-version-quirks.md`.

## [0.7.0] — 2026-06-17

### Changed
- **`.top(N).execute()` is now a total cap, not a single server page.**
  Following the OData `$top` spec (and the convention of boto3 `MaxItems` /
  google-cloud `max_results`), `.top(N)` means "at most N rows" everywhere.
  Previously `client.items.top(100).execute()` returned only one server page
  (~20 rows) and callers who computed the next offset as `skip + top` silently
  skipped records. Now `execute()` follows `@odata.nextLink` internally and
  returns up to N rows in one call, making `ceil((N+1) / page_size)` requests;
  `has_more` reflects rows beyond N. `$top` is enforced client-side and never
  sent to SAP. **Unchanged:** `.top(N)` with N ≤ the server page size (incl.
  `.first()`), `resource.list()` (still one raw page), `.stream()`,
  `.page_size()`, and the `PaginatedResult` surface.

  *Migration:* if you relied on `.top(N).execute()` returning a single page
  (i.e. used `.top()` as a page-size hint), switch to `.page_size(N).list()` or
  plain `.list()`. Manual paging via `while page.has_more: list(params=...)` is
  unaffected.
- **`crossjoin(...).execute()` now returns `PaginatedResult[dict]`** (was
  `list[dict]`). It is list-like — iteration, `len()`, indexing and `==` against
  a list all still work, so existing loops are unaffected — and now also exposes
  `has_more` / `next_skip` / `total_count`. `.top(N)` is a total cap (eager-fills
  across server pages; `$top` enforced client-side). The low-level
  `query_service(...).execute()` escape hatch is intentionally left as `list[dict]`
  (one server page, forwards `$top` as-is).

### Added
- **`PaginatedResult.next_skip`** — the absolute `$skip` for the next page
  (gap-free), or `None` on the last page. Prefer it over `skip + top`, which
  diverges (and skips records) when a server page is smaller than `$top`.
- **`PaginatedResult.total_count`** — the server-side total row count
  (`@odata.count`), populated only when the request asked for it (`$count=true` /
  `ODataQuery(count=True)`); `None` otherwise. Independent of paging — the full
  result-set size. Captured on `list()`, `.execute()` (incl. eager `.top()`),
  and `$crossjoin`. Also added as `Result.total_count`.

## [0.6.2] — 2026-06-17

### Fixed
- **Stale keepalive connections no longer surface as a generic `B1Exception`.**
  When SAP B1 closes an idle keepalive server-side, the next request raised
  `httpx.RemoteProtocolError` ("Server disconnected without sending a response"),
  which is a `TransportError` (not a `NetworkError`) and so fell through to the
  generic `B1Exception` wrapper. Both the sync and async adapters now handle it:
  idempotent `GET`s are transparently retried once (the dead connection is
  evicted from the pool, so the retry uses a fresh one), and non-idempotent
  writes (`PATCH`/`POST`/`DELETE`) raise `B1ConnectionError` so the caller can
  decide whether to retry. Note: httpx/httpcore's transport `retries=` does
  **not** cover this case — it only retries connection establishment.

## [0.6.1] — 2026-06-17

### Fixed
- **Boolean filters now render as `'tYES'`/`'tNO'`, not `true`/`false`.** SAP B1
  has no real `Edm.Boolean` properties — every boolean-style field is a
  `BoYesNoEnum` (`tNO`/`tYES`), and SAP rejects `$filter=Frozen eq false` with
  HTTP 400. `format_odata_value(bool)` previously emitted `true`/`false`, so any
  filter like `Item.frozen == True` silently produced an invalid request. It now
  emits the enum literal, matching what `to_api_payload()` serialises.
- **`has_more` is correct under `$top`.** SAP omits `@odata.nextLink` when the
  requested `$top` fits within a single server page (`top ≤ page size`), so
  `.top(N).execute()` / `.list()` reported `has_more=False` even when more rows
  matched — silent truncation. `list()` now issues a fence-post probe (requests
  `$top + 1`, truncates back to `N`) and synthesises the next-page cursor when
  the extra row materialises.
- **`.stream()` no longer forwards `$top` to SAP.** Forwarding it re-applied
  `$top` relative to each page's `$skip` cursor (muddled paging); `.top()` is now
  enforced purely client-side as a global cap. Applies to both the generic
  resource and `$crossjoin` streams.

### Added
- **`.page_size(N)` builder method** — sets SAP's server-side page size via the
  `B1S-PageSize` header (the per-request batch, distinct from `.top()`'s total
  cap). Available on the fluent builder (works with `.list()`/`.execute()`/
  `.stream()`), as a resource-level shortcut, and on the `$crossjoin` builders.

## [0.6.0] — 2026-06-10

### Breaking
- **Removed the `saphdb` subpackage** (direct SAP HANA / `hdbcli` access) and the
  `hana` extra. The SDK is now Service-Layer-only; for SQL over HANA use the
  `SQLQueries` resource (`client.sql_queries`) or `hdbcli` directly.
- **`list()` / `execute()` now return `PaginatedResult[T]`** instead of `list[T]`.
  `PaginatedResult` is a `Sequence` (iteration, `len()`, indexing all work), and
  adds `next_params` / `has_more` for manual paging. Only literal
  `isinstance(x, list)` checks break.
- Removed the duplicate `b1sl.b1sl.contrib.django` package (use
  `b1sl.contrib.django`), the legacy `b1sl.b1sl.adapter` module-level Django
  global, and the dead `models/odata_query_model.py` / `_types.py` modules.
- **Removed the unused `max_page_size` config knob** (`B1Config` field,
  `B1SL_MAX_PAGE_SIZE` env var, Django setting) — it was never read. Use the
  per-call `page_size` parameter instead. `token_timeout` is now actually
  wired: it is the fallback session lifetime when SAP's Login response omits
  `SessionTimeout` (previously a hardcoded 30 min).

### Added
- **Top-level package re-exports**: `from b1sl import B1Client, entities, fields`
  now works (lazy PEP 562 forwarding — `import b1sl` stays instant).
- **Sync `$batch`**: `B1Client.batch()` now returns a working `SyncBatchClient`
  (plain `with` blocks, sync `execute()`); `RestAdapter.post_batch` added.
- **Dry-run-aware `$batch`**: under `with b1.dry_run():`, `batch.execute()`
  returns synthesized per-op 204s without sending anything to SAP.
- **Filtered counts**: `QueryBuilder.count()` / `AsyncQueryBuilder.count()` —
  `client.orders.filter(...).count()` sends `GET $count?$filter=...`.
- **Session hydration on the sync side**: `B1Client(config, session_id=...)` /
  `RestAdapter(session_id=...)` (parity with the async client); `AsyncB1Client`
  gained the `adapter=` dependency-injection parameter (parity with sync).
- **`$skiptoken` pagination support** plus a loop guard: a nextLink with no
  recognised cursor now raises `B1PaginationError` instead of refetching the
  same page forever.
- **MCP read-only mode**: `build_resource_toolset(alias, model, read_only=True)`
  omits the create/patch/delete tools.
- `fields` facade now exposes entity-set aliases (`fields.Order`,
  `fields.Invoice`, … → `DocumentFields`), mirroring `entities`.

### Fixed
- **ETag proactive invalidation is now complete and adapter-level**: successful
  PATCH, DELETE and bound-Action POSTs clear the stale cached ETag (Actions also
  clear the keyed parent path). Previously only `update()` cleared, so
  DELETE-after-UPDATE flows hit guaranteed 412s.
- **Sync client released its SAP session license only on server timeout** —
  `B1Client.close()` / context-manager exit now logs out.
- **`count()` was broken**: `GET <Entity>/$count` returns bare `text/plain`;
  both adapters now fall back to the raw body instead of raising "Bad JSON".
- **`page_size` was a no-op**: the per-request page-size header is
  `B1S-PageSize` (the previously sent `B1-PageSize` is ignored by SAP).
- **401 re-login retry kept semantic exceptions**: after a re-login, a failing
  retry now raises the mapped exception (`B1NotFoundError`, …) in both adapters
  instead of a re-wrapped generic `B1Exception`.
- **`$batch` failures map to semantic exceptions** and re-login once on 401.
- Bare 412 (without SAP code -2039) now raises `SAPConcurrencyError`.
- Network-level failures now raise `B1ConnectionError` (DNS, refused, timeout).
- **Nested payload encoding**: bools/dates/enums inside collections (e.g.
  `DocumentLines`) are now encoded to SAP wire format (`tYES`/ISO dates) —
  previously only top-level fields were converted.
- Entity keys are OData-escaped (`'` → `''`) when interpolated into resource
  paths.
- `__version__` is single-sourced from package metadata (was stale at 0.4.1).
- `B1Config` no longer exposes the password in `repr()`/`str()`.
- A warning is emitted when TLS verification is disabled; `.env.example` no
  longer ships `B1SL_SSL_VERIFY=0`.
- Hydrated `B1SESSION` cookies (`session_id=...`) are now scoped to the SAP
  host so they can never be sent to another domain via a cross-host redirect.
- The JSON log formatter no longer extracts a `session_id` field — the
  session cookie is a bearer-credential equivalent and must not reach logs.

### Tooling
- mypy re-armed (`attr-defined`, `arg-type`, `call-arg`, `union-attr` active,
  pydantic plugin enabled) and now runs in CI; tests run on a 3.11–3.14 matrix.
- PyPI publishing switched to Trusted Publishing (OIDC) with a tag↔version gate.
- Executable sync/async parity tests guard the dual-surface contract.
- sdist no longer ships `tests/`, `configs/`, or `.env.example`.
- PEP 639 license metadata (`License-Expression: MIT` + bundled license file).
- VCR cassette redaction hardened: usernames, nested `SessionId`s, and the
  recording host (anywhere in bodies) are scrubbed.
- `make release` gates on pyproject↔tag version match and stages only
  tracked changes; coverage instrumentation is now opt-in
  (`make test-ci` / `coverage-html`) instead of on every pytest run.

## [0.5.0] — 2026-06-04

### Added
- Python 3.13 / 3.14 support (`requires-python >=3.11,<3.15`).
- Dynamic override discovery: `_overrides/` modules are scanned lazily on first
  entity access — adding an override no longer requires regeneration.

### Changed
- **Lazy entity schemas**: the `entities` facade resolves models via PEP 562 and
  builds each pydantic core schema on first access. Importing `entities`
  dropped from ~14.5 s / 2.4 GiB to under ~1 s / ~80 MiB. `entities.preload()`
  is the opt-in eager warm-up.

## [0.4.0] — 2026-05

### Added
- `SQLQueries` resource (`client.sql_queries`): `create/describe/run/run_stream`
  with bounded-function (`/List`) support and SQL error subclasses
  (`B1SqlSyntaxError`, `B1SqlNotAllowedError`, `B1SqlParamError`).
- MCP helper toolkit (`b1sl.contrib.mcp`): Elite resource discovery, SQL/OData
  grammar prompts, tool-definition builders, and result formatters.
- `$crossjoin` support (`client.crossjoin`) and `QueryService_PostQuery`
  row-level filters (`client.query_service`).
- Per-part headers in `$batch` requests.

## [0.3.0] — 2026-05

### Added
- Advanced `UDFSchema` introspection: discovery (`get_udf_schema()`), membership
  tests, `to_pydantic_model()`, `validate_and_dump()`.

## [0.2.0] — 2026-04

### Changed
- Removed `B1ClientMixin` in favour of direct, type-safe resource access.
- Proactive ETag invalidation and semantic status-code exception mapping
  (`B1NotFoundError`, `B1AuthError`, `SAPConcurrencyError`, …).
- Fluent OData query builder with operator overloading.

## [0.1.0] — 2026-04-07

Initial public release: sync/async clients, metadata-generated Pydantic models,
session management with re-auth locking, ETag concurrency, `$batch` with
changesets, transparent pagination, dry-run mode, VCR-backed test
infrastructure.

[Unreleased]: https://github.com/operator-ita/b1sl-python/compare/v0.10.0...HEAD
[0.10.0]: https://github.com/operator-ita/b1sl-python/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/operator-ita/b1sl-python/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/operator-ita/b1sl-python/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/operator-ita/b1sl-python/compare/v0.6.2...v0.7.0
[0.6.2]: https://github.com/operator-ita/b1sl-python/compare/v0.6.1...v0.6.2
[0.6.1]: https://github.com/operator-ita/b1sl-python/compare/v0.6.0...v0.6.1
[0.6.0]: https://github.com/operator-ita/b1sl-python/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/operator-ita/b1sl-python/compare/v0.4.1...v0.5.0
[0.4.0]: https://github.com/operator-ita/b1sl-python/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/operator-ita/b1sl-python/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/operator-ita/b1sl-python/compare/v0.1.2...v0.2.0
[0.1.0]: https://github.com/operator-ita/b1sl-python/releases/tag/v0.1.0
