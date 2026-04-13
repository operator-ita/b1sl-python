# SDK Architecture & Principles

## Core Vision
This SDK is designed as a **metadata-first**, type-safe bridge between Python and SAP Business One. Unlike traditional "wrapper" libraries that require manual maintenance for every new SAP field or entity, this project automates the entire model and resource layer by parsing OData metadata.

## Architectural Pillars

### 1. Separation of Concerns (Generated vs. Handcrafted)
The codebase is strictly divided into three layers:
- **`models/_generated/`**: Fully automated Pydantic v2 models. **Never edit these files.** They are overwritten on every schema refresh.
- **`models/_overrides/`**: Manual extensions. This is the place to add calculated properties, custom methods, or fix metadata quirks.
- **`entities/` (Public Facade)**: A unified namespace that blends generated models with your manual overrides. Developers should only import from here.

### 2. The `B1Model` Base Class
Every entity inherits from `B1Model`, which provides global data normalization:
- **Boolean Coercion**: Automatically maps SAP's `"tYES"`/`"tNO"` to Python `bool`.
- **Date Handling**: Converts SAP's `/Date(ms)/` strings into ISO dates.
- **Null Filtering**: The `.to_api_payload()` method automatically excludes `None` values (except when explicitly requested), preventing accidental overwrites of existing SAP data.

### 3. Service-Resource Pattern
The SDK creates dedicated "Service" classes (e.g., `ItemsService`, `OrdersService`) that group:
- **Standard CRUD**: `get()`, `list()`, `update()`, `create()`, `delete()`.
- **Typed OData**: Integration with a fluent, pythonic `QueryBuilder` that supports operator overloading on field constants for type-safe filtering and expansions.
- **Unbound Actions**: Business logic methods (like `Cancel`, `Close`, `Reopen`) extracted from the SAP API Reference.

### 4. Metadata Integrity (The "Vanilla" Policy)
By default, the generator filters out all User-Defined Fields (`U_*`) and User-Defined Tables (`@*`). This ensures the core SDK remains version-agnostic and clean. Customizations are handled locally via the Override system or the Hybrid interaction pattern.
