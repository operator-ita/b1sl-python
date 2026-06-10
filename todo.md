# TODO

## P1 — `entities` import compiles all SAP entity schemas eagerly (~2.4 GiB RSS, ~14.5 s)

**Status: DONE** — import now 0.93s / 81 MiB (was 14.5s / 2.44 GiB); a typical
app touching a few entities stays under ~200 MiB. `entities.preload()` restores
eager warm-up for deployments that want it.

### Problem

Importing `b1sl.b1sl.entities` takes **14.5 s and 2.44 GiB RSS** (measured locally,
Python 3.12, Pydantic v2). Under a throttled CPU (e.g. a 500m-limit k8s pod) this
becomes ~140 s of startup and makes the SDK unusable in pods with < 3 GiB memory.
Reported by a user running Django + gunicorn in Kubernetes.

The PEP 562 lazy load in `src/b1sl/b1sl/__init__.py` only defers the *module*
import. The moment `entities` is touched, two generated files force a full build
of every Pydantic core schema:

1. `src/b1sl/b1sl/models/_generated/entities/__init__.py` — runs
   `model_rebuild(_types_namespace=_NAMESPACE)` over **all ~280 entity models**.
   This loop is 100% of the cost (13 s / 2.4 GiB).
2. `src/b1sl/b1sl/entities/__init__.py` (facade) — runs a *duplicate* rebuild
   loop (a no-op by then, but dead weight).

Measured breakdown:

| Stage | Time | RSS |
|---|---|---|
| Define all ~1000 classes (no rebuild) | 1.1 s | 96 MiB |
| Eager `model_rebuild()` loop | 13 s | 2.4 GiB |
| Rebuild only `Item` | 0.33 s | +31 MiB |
| Rebuild only `Document` (= Order/Invoice/…) | 0.11 s | +24 MiB |
| Rebuild only `BusinessPartner` | 0.08 s | +21 MiB |

Per-model lazy rebuild is therefore viable: a typical app touching 5–10 entities
should land around 150–250 MiB / ~2 s instead of 2.4 GiB / 14.5 s.

### Plan

Both offending files are auto-generated, so the fix goes in the generator
(`scripts/b1sl_metadata_generator/generator.py`) followed by a regeneration
(`./scripts/generate_models.sh 1.27` — `.real` metadata is present locally).

- [x] `generate_entities_init()`: drop the eager rebuild loop; keep
      `_ALL_MODELS` / `_NAMESPACE`; add thread-safe `ensure_built(model)`
      (lock + `__pydantic_complete__` check + `model_rebuild`) and `preload()`.
- [x] `generate_entities_facade()`: stop importing entity classes at runtime.
      Emit instead:
      - eager star-imports for enums + complex types only (cheap, already built),
      - `_ENTITY_NAMES` frozenset + `_ALIASES` dict (alias → entity name),
      - PEP 562 `__getattr__` that resolves the name, calls `ensure_built`,
        and caches the class in module globals,
      - `__dir__`, `preload()`, unchanged `__all__`,
      - the full entity import block + alias assignments under
        `if TYPE_CHECKING:` so mypy/IDEs still resolve `en.Item`.
- [x] Regenerate models (`./scripts/generate_models.sh 1.27`). The pre-existing
      `fields/` formatting drift was fixed afterwards: the script now ends with
      `ruff check --fix` + `ruff format` on generated output, and `fields/` was
      recommitted once in canonical style (regen is now byte-idempotent).
- [x] `B1Model.model_rebuild()` override injecting the master `_NAMESPACE`:
      internal call sites (`client.py` Elite properties) and user code that
      imports models from `_generated/` directly rely on pydantic's automatic
      rebuild-on-first-use, which otherwise can't resolve cross-domain
      forward references. Without this, 21 unit tests fail.
- [x] Update the stale "~14s" comment in `src/b1sl/b1sl/__init__.py`.
- [x] Add `tests/unit/test_entities_lazy.py` (subprocess-isolated, 9 tests):
      lazy access builds only the closure, aliases, override-first import
      order, thread-safe first access, `preload()`, AttributeError/`__dir__`,
      dynamic override discovery without regen, non-subclass shadow warning.
- [x] Benchmark after: import 0.93s / 81 MiB; Item+Order+BusinessPartner in
      use: 172 MiB total. `preload()`: 9.9s / 2.4 GiB (the old eager cost).
- [x] `make test` (472 passed), `make test-vcr` (2 passed), ruff clean.
      mypy: only the 2 pre-existing `SQLQuery` errors in `sql_queries.py`
      (verified present on main before this change).
- [x] Docs: lazy-build + `preload()` documented in `docs/01-architecture.md`
      and CLAUDE.md.

### Known pre-existing issues surfaced while testing

- [x] Circular import: importing `b1sl.b1sl.models._overrides.inventory`
      *before* anything else triggered `_generated/entities/__init__` →
      `_overrides.inventory` (partially initialized) → ImportError.
      **Fixed**: the generated package no longer imports `_overrides` at
      init time. Overrides are discovered dynamically by
      `_apply_overrides()` on first entity access (same-name subclass in
      any `_overrides/` module — no registration, no regen needed; a
      non-subclass shadow is ignored with a `b1sl` logger warning).
      Bonus: new overrides now take effect at runtime without re-running
      the generator (previously they were silently dead until regen).
- [x] mypy: `Name "SQLQuery" is not defined` ×2 in
      `src/b1sl/b1sl/resources/sql_queries.py`. **Fixed**: `SQLQuery` imported
      under `TYPE_CHECKING` (`# noqa: F401` — ruff can't see the string-form
      generic usage); classes keep `GenericResource["SQLQuery"]` since base
      class specs are evaluated at runtime.
- [x] `b1sl/__init__.py` over-broad warnings suppression. **Fixed**: the whole
      `ArbitraryTypeWarning` try/except was dead pydantic-v1 compat code —
      in pydantic 2.x it always fell to the `except` branch silencing ALL
      b1sl/pydantic warnings. Removed entirely.

### Follow-up (separate task, not in this fix)

- [x] Generator emits `Enum | Literal[...]` unions where the Literal duplicates
      the str-enum's values. **Fixed**: the Literal arm now lives in a
      per-enum `<Enum>Field` alias that is `Enum | Literal[...]` only under
      `TYPE_CHECKING` and the bare enum at runtime — mypy still accepts plain
      DI API strings (and rejects invalid ones), pydantic builds half the
      union arms. Measured: the gain is real per enum field (~1.4x build,
      ~1.7x mem in isolation) but enum fields are a small share of the full
      graph, so `preload()` only improved 12.6s/2444 MiB → 11.9s/2316 MiB.
      Behavior note: plain-string inputs now coerce to the StrEnum member
      (previously stayed `str` because the Literal won the smart union);
      equality, JSON and `to_api_payload()` output are identical.
