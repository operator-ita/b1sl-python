# Metadata Generation Pipeline

## The Engine
The SDK is built around a powerful **automated generation engine** (`scripts/sap_metadata_generator/`). 

Its primary purpose is to transform three SAP source files into a type-safe Python SDK:
1.  **`$metadata` (XML)**: Defines the schema, entity types, and navigation properties.
2.  **Service Document (JSON)**: Lists which entities are currently exposed on the tenant.
3.  **API Reference (HTML)**: Enriches the codebase with descriptions, examples, and correct HTTP verbs from SAP's official documentation.

## Running the Pipeline

To update your SDK models and resources for a new version:

1.  **Capture sources**: Save `$metadata`, `/b1s/v2/`, and the API Reference HTML into `metadata/<version>/`.
2.  **Execute the build**:
    ```bash
    ./scripts/generate_models.sh <version>
    ```

### Generation Logic (The "Magic" Steps)
1.  **Filtering**: Any entity starting with `U_`, `@`, or custom prefixes is ignored to ensure a stable, vanilla core.
2.  **Enrichment**: Descriptions are extracted from HTML and injected as docstrings.
3.  **Dedicated Services**: Unbound actions (like `Cancel`, `Close`) are grouped into service classes.
4.  **Forward References**: A master namespace is created in `entities/__init__.py`, and `model_rebuild()` is called on all entities to resolve circular dependencies (e.g., `Item` <-> `ProductTree`).
5.  **Types Arbitrator**: A unified `_types.py` is created to ensure Service classes use overridden and rebuilt versions of models.

## Development Constraints
-   **Never edit `_generated/`**: All files in `_generated/` directories are strictly automated. Hand-crafted changes will be lost.
-   **Use `.real` files for local production**: To use production metadata safely without committing it to Git, name your files as `metadata_document.real.xml` and `service_document.real.json`. The generator will automatically prioritize these files.
