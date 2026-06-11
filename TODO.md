# TODO — Quality & Security Audit (2026-06-10, v0.6.0 working tree)

Consolidated findings from a 4-dimension audit (security, architecture/quality,
testing/CI, packaging/API). Every item was verified against the actual code
(file:line cited). Items are ordered by priority; check off as fixed.

---

## P0 — Fix before releasing 0.6.0

> All five P0 items fixed on 2026-06-10 (same audit day). 503 unit tests pass,
> `make lint` clean. New coverage: `tests/unit/test_batch_sync.py`,
> ETag-invalidation tests in `test_advanced_features.py` / `test_rest_adapter.py`,
> `tests/unit/test_version.py`.

- [x] **`$batch` bypasses dry-run — real writes execute under `with client.dry_run()`**
  `batch/client.py:103` → `async_rest_adapter.py:383` (`post_batch`) calls
  `self._client.post()` directly, never passing through the `_dry_run_active`
  gate in `_do()` (`async_rest_adapter.py:249`). The documented contract
  ("intercepts all writes") is silently violated for every batched
  create/update/delete.
  **Fix**: check `_dry_run_active` in `BatchClient.execute()` (or `post_batch`)
  and return a synthesized all-204 batch response without sending.

- [x] **Sync batch is broken end-to-end (public API that cannot work)**
  `B1Client.batch()` exists (`client.py:114`) but `BatchClient.execute()` is
  async-only and `RestAdapter` has no `post_batch`. Worse, sync resources call
  the recording adapter's `async def` methods without awaiting — reproduced:
  `batch.items.count()` → `AttributeError: 'coroutine' object has no attribute
  'data'` and `_pending` stays empty.
  **Fix**: remove `batch()` from `B1Client` and document batch as async-only
  (pre-1.0, breaking OK), or implement the full sync path (`RestAdapter.post_batch`
  + sync `execute()` + sync-aware recording adapter).

- [x] **ETag proactive invalidation is incomplete — guaranteed stale-ETag 412s**
  Only `update()` clears the cache (`resources/base.py:351`,
  `async_base.py:250`). `delete()` (`base.py:353-355`) and `_action()` POSTs
  (e.g. `/Cancel`, which DO send `If-Match` per `base_adapter.py:362-364`)
  never clear. Direct adapter usage gets no invalidation at all.
  **Fix**: move invalidation into the adapters' `_do` success path for
  PATCH/DELETE/keyed-POST so all call paths (sync, async, resource, raw)
  are covered. Add tests asserting `_etag_cache` is cleared after PATCH and
  DELETE (currently untested — see P1 testing item).

- [x] **`__version__ = "0.4.1"` vs pyproject `0.6.0`**
  `src/b1sl/__init__.py:5`. Two releases stale; ships in the wheel.
  **Fix**: single-source via `importlib.metadata.version("b1sl-python")` or
  hatch `[tool.hatch.version] path = ...`; add a tag↔version assertion to
  `make release` and `publish.yml`.

- [x] **Sync client leaks the SAP session license on close**
  `RestAdapter.close()` (`rest_adapter.py:59-62`) only closes the httpx pool;
  with `reuse_token=True` (default) logout never fires, so the session holds a
  license until SAP-side timeout. Async `aclose()` does log out
  (`async_rest_adapter.py:106-112`).
  **Fix**: attempt `_logout()` in `close()` when the session is active,
  swallowing errors like the async path does.

## P1 — High (next sprint)

> All seven P1 items fixed on 2026-06-10. mypy now runs with the pydantic
> plugin and `attr-defined`/`arg-type`/`call-arg`/`union-attr` armed (0 errors
> across src/tests/examples — re-arming caught 4 real bugs: example 08's
> nonexistent `return_requests`, example 18's broken UDFSchema iteration,
> example 10's nonexistent `adapter.url`, and generic re-wrapping of semantic
> exceptions in BOTH adapters' 401-retry). CI: lint job (ruff+mypy) + test
> matrix 3.11–3.14; the 3 root-level test files moved into tests/unit/.
> publish.yml: Trusted Publishing + tag↔version gate — NOTE: requires
> one-time setup on pypi.org (Add GitHub publisher: repo
> operator-ita/b1sl-python, workflow publish.yml, environment pypi) BEFORE
> the next tag push, and PYPI_TOKEN secret can then be deleted.

- [x] **Re-arm mypy — the current config masks real bugs**
  `pyproject.toml:101` disables 11 error codes including `attr-defined`,
  `arg-type`, `call-arg`, `union-attr`. Concrete masked bug: `base.py:351`
  calls `_clear_etag` on `RestAdapterProtocol`, which doesn't declare it
  (`adapter_protocol.py:6-28`) — this is how the sync-batch breakage slipped
  through. **Fix**: add `_clear_etag`/`with_schema` to the protocol, re-enable
  at least `attr-defined`, `arg-type`, `call-arg`, `union-attr`, fix fallout.

- [x] **CI gaps: no version matrix, 15 tests invisible, no mypy**
  `ci.yml:38` runs only `pytest tests/unit/` on Python 3.12 — the 3.13/3.14
  support advertised in v0.5.0 has never been CI-verified, and
  `tests/test_b1sl_adapter.py`, `test_async_adapter.py`, `test_middleware.py`
  (config validation, async 401-retry, Django middleware) never run in CI.
  **Fix**: matrix `["3.11", "3.12", "3.13", "3.14"]`; move the 3 root test
  files into `tests/unit/`; add `uv run mypy .` step.

- [x] **publish.yml: switch to PyPI Trusted Publishing**
  `publish.yml:46-49` uses a long-lived `PYPI_TOKEN` while `id-token: write`
  is already declared but unused. Tag push by anyone with write access =
  publish. **Fix**: Trusted Publishing (OIDC), drop the token; add
  tag↔pyproject version check before upload.

- [x] **Sync 401-retry loses semantic exceptions**
  On retry failure sync collapses to generic
  `B1Exception("Request failed after session retry")` (`rest_adapter.py:266-270`);
  async re-enters `_do` and maps 404→`B1NotFoundError` etc. correctly
  (`async_rest_adapter.py:260-267`). Also: sync 401-retry has zero test
  coverage. **Fix**: mirror the async retry structure; add the sync test.

- [x] **`B1Config` repr exposes the plaintext password**
  `config.py` dataclass has no `repr=False` — `print(config)`, tracebacks, and
  APM frame-capture all serialize the live password.
  **Fix**: `field(repr=False)` on `password` (ideally also username/company_db)
  or custom `__repr__` emitting `password='***'`.

- [x] **TLS: `.env.example` ships `B1SL_SSL_VERIFY=0` and disabling is silent**
  `.env.example:9` normalizes verify-off (MITM exposure of the Login POST and
  B1SESSION cookie); no warning is ever emitted on the disabled path.
  **Fix**: default the example to `1` with a self-signed-cert comment; emit a
  one-time `logger.warning` when `ssl_verify` is falsy; consider accepting a
  CA-bundle path instead of bool-only.

- [x] **`$batch` errors bypass the semantic exception layer**
  `async_rest_adapter.py:395` `raise_for_status()` throws raw
  `httpx.HTTPStatusError` — no 400/401/404/412 mapping, no hooks, no 401
  re-login retry for the batch request itself.
  **Fix**: route `post_batch` failures through the standard status→exception
  mapping and the re-auth lock.

## P2 — Medium

> All P2 items resolved on 2026-06-10. Namespace decision: the outer
> `b1sl/__init__.py` now lazily re-exports the public surface (PEP 562) —
> `from b1sl import B1Client, entities` works, `import b1sl` stays at ~45 ms;
> the deep `b1sl.b1sl` path remains canonical internally. Flattening was
> consciously deferred (churn > benefit while re-export covers the UX gap).
> reuse_token=False now means per-request logout on BOTH surfaces. New
> executable parity tests (`test_sync_async_parity.py`) lock the contract.

- [x] **Decide the `b1sl.b1sl` doubled namespace before more users arrive**
  Outer `src/b1sl/__init__.py` is an empty shell; PyPI users `import b1sl` and
  find nothing. The umbrella's reason to exist (`saphdb`) was removed in 0.6.0.
  **Fix (pre-1.0 window)**: re-export the SL surface in the outer `__init__`
  (cheap, ~0.2s) or flatten `src/b1sl/b1sl/` → `src/b1sl/`. Also
  `rm -rf src/b1sl/saphdb/` (only `__pycache__` leftovers remain).

- [x] **Sync/async surface drift (beyond the P0/P1 items)**
  - `GenericResource.orderby(expression)` lacks async's `desc=` and
    `ODataField` hint (`base.py:172` vs `async_base.py:88`).
  - `B1Client.__init__` accepts `adapter=` DI; `AsyncB1Client` doesn't.
    `AsyncB1Client` accepts `session_id=` hydration; sync doesn't.
  - `reuse_token=False`: sync logs out after every request; async never does.
  - `AsyncRestAdapter.login()` wraps in `B1AuthError`, sync doesn't;
    `logout()` returns `Result(500)` in async, raises in sync.
  **Fix**: align each pair; then add a parity test asserting both clients/
  resources/builders expose identical public method sets and signatures
  (none exists today).

- [x] **412 without SAP code -2039 → generic `B1Exception`**
  `base_adapter.py:400` requires `sap_code == "-2039"`; `_HTTP_STATUS_TO_EXC`
  has no 412 entry. CLAUDE.md promises "412 → SAPConcurrencyError"
  unconditionally. **Fix**: add 412 to the status map as fallback.

- [x] **Duplicate Django contrib trees, one dead**
  `src/b1sl/b1sl/contrib/django/` and `src/b1sl/contrib/django/` are
  near-identical; tests import only the latter; the former has 0% coverage
  and ships in the wheel. **Fix**: delete `src/b1sl/b1sl/contrib/django/`,
  move middleware tests into `tests/unit/`.

- [x] **Nested payload encoding gap (bools/dates inside collections)**
  `to_api_payload()` re-encodes `tYES`/dates top-level only
  (`models/base.py:317-331`) — a `bool` or `date` inside `DocumentLines[...]`
  serializes as raw JSON `true`/ISO. **Fix**: recurse into nested models/lists
  during payload encoding; add a round-trip test with document lines.

- [x] **Pagination infinite-loop hazard on `$skiptoken`**
  `build_next_params` only advances `$skip` (`pagination.py:56-66`); a
  `$skiptoken`-style nextLink would re-fetch the same page forever
  (`max_pages` is the only escape, default None).
  **Fix**: parse and carry through any `$skiptoken`; add a loop-guard that
  raises if next_params equals the previous request's params.

- [x] **Coverage gaps on core contracts**
  - `B1Environment.load()` env > `.env` > json precedence: 0 tests
    (`config_manager.py:61-75`).
  - ETag invalidation after PATCH/DELETE: not asserted anywhere
    (`test_advanced_features.py:26-53` stops at If-Match).
  - Sync adapter ETag flow and 401-retry: 0 tests.
  - `resources/udo.py` get/update/delete: untested (54%).
  - `batch/serializer.py` multipart branches: 64%.
  **Fix**: targeted unit tests for each; they cover the P0/P1 fixes above.

- [x] **Mocks without `spec=` hide signature drift**
  Zero uses of `MagicMock(spec=...)`/autospec in the suite; bare-mock adapters
  pass even when method signatures drift. `tests/fakes/fake_rest_adapter.py`
  exists and is the better pattern. **Fix**: `spec=RestAdapterProtocol` (or the
  fake) wherever an adapter is mocked.

- [x] **`docs/14-pagination-streams.md:126` documents a nonexistent API**
  `client.items.filter(query).count()` — `QueryBuilder` has no `count()`, and
  resource-level `count()` ignores filters.
  **Fix**: implement `QueryBuilder.count()` (GET `$count?$filter=...`) on both
  builders (the useful option), or rewrite the doc block.

- [x] **`B1ConnectionError`/`B1ResponseError` are never raised**
  All network failures become generic `B1Exception`
  (`rest_adapter.py:289-291`); the `isinstance(B1ConnectionError)` branch in
  `contrib/mcp/odata_formatters.py:304` is dead code, and the docstring still
  references `requests` (fossil). **Fix**: map `httpx.ConnectError`/timeout →
  `B1ConnectionError`; update docstrings.

- [x] **Entity-key interpolation does not escape quotes**
  `f"'{key}'"` in `base.py:297,307,343,354,378`, `async_base.py`,
  `crossjoin.py:150` — a key like `A')/Cancel` is interpolated raw into the
  path. Not RCE (SAP 400s it) but inconsistent with the value path and a
  defense-in-depth gap when keys flow from untrusted input (e.g. MCP tools).
  **Fix**: shared `_format_key()` with `'`→`''` doubling everywhere.

- [x] **MCP toolset has no read-only mode**
  `contrib/mcp/odata_schemas.py:614-639` always emits `*_create/patch/delete`
  tools — an MCP server grants the LLM writes on every Elite entity by
  default, and the grammar modules are prompt-side advice, not enforcement.
  **Fix**: `build_resource_toolset(..., read_only=True)` option; document that
  safety rests on SAP SL's own enforcement + recommend `dry_run()` pairing.

- [x] **sdist ships tests, cassettes, `configs/`, `.env.example`**
  `[tool.hatch.build.targets.sdist]` excludes don't cover `/tests` or
  `/configs`; redacted today, but any future cassette that slips redaction
  publishes straight to PyPI. **Fix**: extend the exclude list (or switch to
  an include allowlist). Wheel itself verified clean (581 files, no leaks).

- [x] **No CHANGELOG.md**
  Published package with breaking 0.6.0 changes (saphdb/hana removal,
  PaginatedResult) and no migration record.
  **Fix**: Keep-a-Changelog format, backfill 0.4.0–0.6.0 from git log, add
  `Changelog` to `[project.urls]`.

- [x] **`ResourceProxy._wrap_async` swallows `AttributeError`/`TypeError`**
  `batch/client.py:42-49` — this is what hid the recording adapter's missing
  `_clear_etag`. **Fix**: narrow the except or log loudly.

## P3 — Low / housekeeping

> All P3 items resolved on 2026-06-10. Decisions: `token_timeout` was WIRED
> (login fallback when SAP omits `SessionTimeout`, replacing the hardcoded
> 30 min) while `max_page_size` was REMOVED (breaking: `B1Config` kwarg and
> `B1SL_MAX_PAGE_SIZE` are gone — `page_size` per call is the real knob);
> the `hana` keyword was kept consciously (SQLQueries runs SQL over HANA).
> Batch If-Match remains a documented limitation (docs/13 + CLAUDE.md), not
> implemented. Verified: 545 unit + 2 VCR green, lint clean, PEP 639 wheel
> metadata inspected (`License-Expression: MIT`, license file shipped), live
> smoke of scoped-cookie hydration against the real server passed.

- [x] **VCR redaction gaps**: `UserName` not in the redaction set
  (`tests/conftest.py:72` — a prod re-record would leak a real username);
  `SessionId` scrub is top-level-only; host rewrite regex requires `/b1s/` in
  the URL. Harden all three before the next `make test-record`.
- [x] **Hydrated `B1SESSION` cookie is unscoped + redirects followed**
  (`async_rest_adapter.py:88-90`): scope to host/path or disable cross-host
  redirects. Document that a session ID is a bearer-credential equivalent.
- [x] **Batch parts never carry `If-Match`** (recording adapter bypasses
  `_build_headers`) — concurrency protection silently absent inside `$batch`;
  document at minimum. *(Documented in docs/13-batching.md + CLAUDE.md.)*
- [x] **Dead code**: `models/odata_query_model.py` (zero importers, references
  a nonexistent method), `_types.py` (unused `T`), legacy
  `src/b1sl/b1sl/adapter.py` (eager Django global with bare `except` at
  import, references a private app layout), fossil comments in both adapters,
  empty `src/b1sl/b1sl/tests/` dir, stale warning-filter comment in
  `_generated/entities/__init__.py:621`.
- [x] **Unused config knobs**: `token_timeout` (copied, never read),
  `max_page_size` (never read). Wire or remove. *(token_timeout wired as the
  login fallback; max_page_size removed.)*
- [x] **`logging_utils.B1JSONFormatter` is never installed** by the SDK while
  `config.py:27-29` docstring claims PROD JSON logs are automatic; also remove
  (or guard) the `session_id` field so it can never log the cookie.
  *(Docstrings now state setup_logging() is the opt-in; session_id dropped
  from the formatter's extracted fields.)*
- [x] **Test ergonomics**: drop `--cov` from `addopts` (every run pays
  instrumentation; collection alone 9.7s), keep coverage in CI/`make test-ci`;
  align `make test-ci` with what CI actually runs (currently differs in both
  directions, incl. missing `--record-mode=none`).
- [x] **`make release` uses `git add .`** — can sweep untracked junk into
  release commits. Stage explicitly. *(Now `git add -u` + a pyproject
  version↔tag gate before committing.)*
- [x] **PEP 639**: `license = "MIT"` SPDX string + `license-files`;
  add `Programming Language :: Python :: 3` and
  `Operating System :: OS Independent` classifiers; drop or keep the `hana`
  keyword consciously. *(Kept — SQLQueries runs SQL over HANA.)*
- [x] **`strict=False` config injects dummy credentials** (`config.py:95-99`)
  — document loudly as test-only.

---

## Verified clean (no action)

- OData filter **value** escaping is correct (`'`→`''`, `odata.py:14-19`);
  injection attempt confirmed neutralized. Same in SQLQueries param binding.
- Password masked in all log/hook paths (`base_adapter.py:449-451`); session
  IDs never written to logs.
- Repo secret hygiene: cassettes redacted, no real hosts/IPs/credentials, no
  `.env` ever committed, `.gitignore` covers `.real.*`.
- Lazy entity facade contract upheld: `_overrides` imported only lazily under
  RLock; no eager rebuild loops; `import b1sl.b1sl` = 0.2s, entities = 1.25s.
- `batch.execute()` never raises on individual op failures; per-part `index`
  preserved (async path).
- Re-auth locking present and correct in both adapters (`threading.Lock` /
  `asyncio.Lock` with double-checked expiry).
- `dry_run`/`with_schema` ContextVars are per-instance and task/thread-safe
  (single-op writes and bound Actions correctly gated).
- `py.typed` ships; wheel content clean; PyPI metadata/URLs/extras consistent;
  README claims verified (LICENSE exists, links resolve, remote matches).
- Dependency floors modern and upper-bounded.
- Docs spot-check: 6 of 7 sampled code blocks execute correctly against the
  current source (the seventh is the `filter().count()` item above).
