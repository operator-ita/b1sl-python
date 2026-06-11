# Changelog

All notable changes to `b1sl-python` are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/) (pre-1.0:
minor versions may include breaking changes).

## [Unreleased]

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

[Unreleased]: https://github.com/operator-ita/b1sl-python/compare/v0.6.0...HEAD
[0.6.0]: https://github.com/operator-ita/b1sl-python/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/operator-ita/b1sl-python/compare/v0.4.1...v0.5.0
[0.4.0]: https://github.com/operator-ita/b1sl-python/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/operator-ita/b1sl-python/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/operator-ita/b1sl-python/compare/v0.1.2...v0.2.0
[0.1.0]: https://github.com/operator-ita/b1sl-python/releases/tag/v0.1.0
