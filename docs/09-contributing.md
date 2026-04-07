# Contributing to SAP B1 Python SDK

Thank you for your interest in contributing to the SAP B1 Python SDK! This project aims to be the robust, type-safe, and developer-friendly gateway to the SAP Business One Service Layer.

We welcome contributions of all kinds: from fixing typos in documentation to implementing core architectural improvements.

## ️Areas of Contribution

You can contribute to many parts of the project, including:

1.  **Core Adapter**: Improving `RestAdapter` logic for session management, ETag caching, or performance.
2.  **Metadata Generator**: Enhancing the `generator.py` script to support more OData features or improving the code generation templates.
3.  **Middleware & Extensions**: Adding new Django/FastAPI middlewares or specialized resource wrappers.
4.  **Documentation**: Improving READMEs, adding examples, or fixing technical guides.
5.  **Testing**: Expanding unit and integration test coverage.

---

## Testing Architecture

To ensure the SDK remains stable without requiring a 24/7 active SAP server, we use a two-layer testing strategy:

### Layer 1: Unit Tests (Mocks/Fakes) — Speed and Logic
*   **Purpose:** Validate business logic, Pydantic field mapping (camelCase to snake_case), and SAP error handling.
*   **Tool:** `FakeRestAdapter`. It allows registering exact JSON responses without network overhead.
*   **Command:** `make test`
*   **Location:** `tests/unit/`

### Layer 2: Integration Tests (VCR/Real) — Reality and Security
*   **Purpose:** Validate against a live SAP B1 Service Layer API. It "freezes" real responses into cassettes for offline playback.
*   **Tool:** `pytest-recording` (VCR). It captures real traffic and **automatically sanitizes** it.
*   **Command:** `SAP_B1_INTEGRATION=1 make test-integration`
*   **Location:** `tests/integration/`

---

## How to Add a New Endpoint (Example: BusinessPartners)

### A. Verify the Resource
The SDK automatically generates resource classes. Ensure `BusinessPartnersResource` exists in:
`src/b1sl/b1sl/resources/_generated/businesspartners_resources.py`
*(If missing, run `./scripts/generate_models.sh`)*.

### B. Define Test Data
Add valid codes from your test database in:
`tests/fixtures/test_data.py`
```python
# Example
customers: Dict[str, str] = field(default_factory=lambda: {
    "retail": "C20000", # A real code from your SAP test DB
})
```

### C. Create the Unit Test
Create `tests/unit/test_business_partners_mock.py`:
```python
from tests.fakes.fake_rest_adapter import FakeRestAdapter
from b1sl.b1sl import B1Client

def test_get_bp_logic():
    adapter = FakeRestAdapter()
    adapter.register("GET", "/BusinessPartners('C20000')", {"CardCode": "C20000"})
    # ... your validation logic here
```

### D. Record the Cassette
Create `tests/integration/test_business_partners_real.py` decorated with `@pytest.mark.vcr`. Run:
```bash
SAP_B1_INTEGRATION=1 make test-integration
```
**Privacy Ensured**: The global `vcr_config` (in `tests/conftest.py`) will automatically redact:
1.  Your real hostname (replaced by `sap-server.example.com`).
2.  The `B1SESSION` token and `Set-Cookie` headers.
3.  `Authorization` headers.

---

## 🔄 Working with the Metadata Generator

This SDK is **metadata-driven**. Most of the code in `src/b1sl/b1sl/models/_generated/` and `src/b1sl/b1sl/resources/_generated/` is produced automatically.

### How to Update for a New SAP Version
If you need to add support for a new SAP B1 version (e.g., `1.30`):

1.  **Prepare Metadata**: Collect the `metadata_document.xml`, `service_document.json`, and `service_layer_api_reference.html` from the target Service Layer instance.
2.  **Place Files**: Create a directory `metadata/<version>/` and place the files there.
3.  **Run Pipeline**:
    ```bash
    ./scripts/generate_models.sh <version>
    ```
4.  **Verify**: The script performs a **Clean Build**, removing any orphan files from previous versions and ensuring a 1:1 match with the documentation.

### Why use the Generator?
- **Consistency**: Ensures all resources follow the same Pythonic patterns.
- **Enrichment**: Injects official SAP descriptions and JSON examples into the docstrings.
- **Safety**: Protects against Python reserved keywords and naming collisions.

---

## 📏 Standards & Rules

1.  **Pure Generation**: **NEVER** manually edit files inside `_generated/` folders. Any structural changes or bug fixes in generated code must be implemented in the generator engine at `scripts/sap_metadata_generator/generator.py`.
2.  **Naming Convention**: We use `snake_case` for Python properties (mapped from SAP's `PascalCase`).
3.  **Docstrings**: All new functions and classes must have **Google-style docstrings**.
4.  **No Secrets in Cassettes**: Before pushing, ensure your cassettes in `tests/integration/cassettes/` are clean by running:
    ```bash
    grep -r "B1SESSION" tests/integration/cassettes/ # Should return 0 results
    ```
5.  **Language**: All comments, documentation, and commit messages must be in **English**.

---

Thank you for helping us build the best SAP B1 SDK for the Python community! 🚀
