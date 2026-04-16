# SAP B1 Python SDK - AI Agent Context

## Project Mission
Provide a high-performance, async-first, and metadata-driven Python SDK for SAP Business One Service Layer.

## Development Environment
- **Package Manager**: Use `uv` exclusively.
- **Virtual Env**: Located at `.venv/` in the repository root.
- **Python Version**: 3.11+.
- **Main Commands**:
  - `uv sync`: Install dependencies.
  - `make test`: Run unit tests.
  - `make test-vcr`: Run integration tests with recorded cassettes.
  - `make lint`: Run Ruff and Mypy.

## Repository Architecture
- `src/b1sl/`: The core package. This is what gets published to PyPI.
- `scripts/sap_metadata_generator/`: The engine that generates models and resources from OData XML/JSON metadata.
- `metadata/`: Versioned SAP metadata files (XML, JSON, HTML).
- `_generated/` folders: **NEVER** edit files inside these. Any change must be done in the generator script or as an override in `_overrides/`.

## Distribution & Releases
- **GitHub vs PyPI**: Documentation, examples, scripts, agents context, and skills are excluded from the PyPI wheel.
- **Versioning**: Uses Semantic Versioning (SemVer) `vMAJOR.MINOR.PATCH`.
- **Release Flow**:
  1. `make release v=X.Y.Z` (Commits, tags, and pushes).
  2. GitHub Actions (`publish.yml`) triggers on tag to publish to PyPI.

## AI Agent Rules
1. **English Only**: All comments, documentation, and commits must be in English.
2. **Metadata Priority**: If the user asks for a new field or entity, check if it's in the metadata first. If missing, update metadata and regenerate.
3. **Pydantic v2**: Everything is built on Pydantic v2.
4. **Testing**: Always run `make test` before proposing a change. Integration tests (`make test-vcr`) should be verified if network logic changes.
5. **Linting & Typing**: 
   - Use `make lint` to validate the **entire** repository (parity with CI).
   - `_generated` folders are excluded from strict checking; any errors should be fixed in the generator or via overrides.
6. **Resource Access (Elite vs Generic)**:
   - **Tier 1 (Elite Aliases)**: Only a core subset of entities with direct SAP ETag support (e.g., `client.items`, `client.business_partners`) have direct properties on the client.
   - **Standard (Generic Access)**: All other entities MUST use the `get_resource(Model, "Path")` pattern. This signals that ETag concurrency protection is NOT guaranteed.

7. **Architectural Principles**:
   - **Vanilla Policy**: Models must be version-agnostic (Vanilla) and compatible with Generic Resource Access.
   - **Async/Sync Symmetry**: Every `GenericResource` must have an `AsyncGenericResource` counterpart. Fluent `QueryBuilder` and `AsyncQueryBuilder` must support the same parameters.
   - **Reliable Mutation (ETag Invalidation)**: SAP SL returns `204 No Content` on PATCH/DELETE without a new ETag header. Every `update()` must proactively invalidate (clear) the cached ETag in the adapter.
   - **Status-Code Mapping**: Adapters must map HTTP status codes to semantic exceptions (e.g., 404 -> `B1NotFoundError`) using a standardized mapping dictionary.
   - **Surgical Deltas**: Encourage users (and agents) to create fresh, minimal model instances for updates to ensure clean PATCH payloads.

8. **Generated Code Policy**:
   - NEVER edit files in `_generated/` folders.
   - Use overrides in `_overrides/` to inject custom logic or fix model resolution issues (e.g., using `model_rebuild()`).
