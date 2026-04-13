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
