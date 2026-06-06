# Error Handling

The SAP B1 Python SDK provides a structured exception hierarchy to help you build resilient integrations. All exceptions are located in `b1sl.b1sl.exceptions`.

## Exception Hierarchy

All library-specific exceptions inherit from `B1Exception`.

```mermaid
graph TD
    B1Exception --> B1ConnectionError
    B1Exception --> B1AuthError
    B1Exception --> B1ResponseError
    B1Exception --> B1NotFoundError
    B1Exception --> B1ValidationError
    B1Exception --> SAPConcurrencyError
    B1ValidationError --> B1SqlNotAllowedError
    B1ValidationError --> B1SqlParamError
```

### 1. `B1Exception` (Base)
The catch-all exception. Use this if you want a broad safety net. It contains a `details` attribute with the raw SAP error body (if available).

### 2. `B1NotFoundError` (404)
Raised when a specific resource (e.g., an Item or Business Partner) does not exist in SAP.
- **Typical Use**: Checking existence or handling missing data gracefully.
- **Example**:
  ```python
  try:
      item = client.items.get("NONEXISTENT")
  except B1NotFoundError:
      print("Item was not found!")
  ```

### 3. `B1ValidationError` (400)
Raised when the Service Layer rejects a request due to invalid data, missing required fields, or business rule violations.
- **Typical Use**: Debugging payload issues or catching user input errors.

### 4. `SAPConcurrencyError` (412)
Raised when an optimistic concurrency conflict occurs (ETag mismatch).
- **Typical Use**: Implementing retry loops for high-concurrency environments.
- **See also**: [05-interaction-patterns.md](05-interaction-patterns.md) for details on the "Elite" concurrency strategy.

### 5. `B1AuthError` (401)
Raised when authentication fails (invalid credentials) or when a session has expired and cannot be automatically refreshed.

### 6. `B1SqlNotAllowedError` (400, codes 702/703)
Subclass of `B1ValidationError`. Raised when a `SQLQueries` execution is blocked by the server-side allowlist.
- Code `"702"`: the queried table is not in `b1s_sqltable.conf`.
- Code `"703"`: the queried column is in `ColumnExcludeList`.

The `sap_code` attribute identifies which restriction triggered the error.

### 7. `B1SqlParamError` (400, code 704)
Subclass of `B1ValidationError`. Raised when a `/List` invocation fails due to parameter problems — wrong name, wrong count, or type mismatch. Check that the kwargs passed to `run()` match the `:name` placeholders in `SqlText`.

See [15-sql-queries.md](./15-sql-queries.md) for full usage and error-handling examples.

## Automatic Mapping

The SDK's adapters (`RestAdapter` and `AsyncRestAdapter`) automatically map HTTP status codes to these specialized exceptions:

| HTTP Status | SAP Code | Exception Class |
|-------------|----------|-----------------|
| 400 | `"702"` / `"703"` | `B1SqlNotAllowedError` (→ `B1ValidationError`) |
| 400 | `"704"` | `B1SqlParamError` (→ `B1ValidationError`) |
| 400 | other | `B1ValidationError` |
| 401 | — | `B1AuthError` |
| 404 | — | `B1NotFoundError` |
| 412 | `"-2039"` | `SAPConcurrencyError` |
| others | — | `B1Exception` |

## The `exists()` Pattern

For high-level resources, you can use the built-in `.exists()` method which internally handles `B1NotFoundError`:

```python
if client.business_partners.exists("C1000"):
    print("Socio exists!")
else:
    print("Socio is missing.")
```

> [!IMPORTANT]
> The `exists()` method performs a full GET request to verify existence. It is designed to be compatible across different Service Layer versions.
