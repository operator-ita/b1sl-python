# Configuration

## Overview
The SDK uses a **hierarchical and environment-agnostic** configuration system. This allows you to switch between a local dev environment (`B1SL_ENV=dev`), a QA environment (`B1SL_ENV=test`), or a production environment (`B1SL_ENV=prod`) without changing a single line of business logic.

## Configuration Strategy

### 1. Hierarchical Loading
The `B1Environment.load(env_name)` method prioritizing sources as follows:
1.  **System Environment Variables**: The preferred source of truth (highest priority).
2.  **Env File (`.env`)**: Standard local secrets management (strictly ignored by git).
3.  **JSON Data Profiles (`configs/{env}.json`)**: Shared, non-sensitive IDs and test data profiles. (Note: These files no longer support server credentials for security reasons).

### 2. Runtime Environment Control
The SDK behavior and log formatting are controlled by a single variable:
- `B1SL_ENV`: Set to `prod` for structured JSON logs, or `dev` (default) for human-readable console output.

The SDK uses a typed `B1Env` enum to represent these states:
- `B1Env.DEV`: Human-readable logs, standard environment.
- `B1Env.TEST`: Identical to DEV, signals test isolation.
- `B1Env.PROD`: **Structured JSON logs** enabled automatically for observability pipelines.

### 3. Dry Run Mode
To prevent accidental data modification during development or debugging, the SDK includes a global **Dry Run** flag.

- `B1SL_DRY_RUN`: Set to `1` to enable.

When enabled, all writing requests (`POST`, `PATCH`, `DELETE`) are intercepted by the adapter. The SDK will log the intended action and return a dummy success result (`204 No Content`) without actually hitting the SAP Service Layer. `GET` and `Login` requests continue to work normally.

```python
# Enable via code (Global)
config = B1Config.from_env()
config.dry_run = True

# Temporary Dry Run (Pythonic Context Manager)
# This is Task-Safe via ContextVar: it only affects the current task/thread.
async with AsyncB1Client(config) as b1:
    with b1.dry_run():
        await b1.items.update("A0001", item) # Intercepted

    # Or force execution if global dry_run is True
    with b1.dry_run(enabled=False):
        await b1.items.update("A0001", item) # Sent to SAP

# IMPORTANT: Always use 'with' (sync), NOT 'async with', 
# even in async code blocks.
```

## Test Data Profiles
One of the most powerful features is the **Test Data Profile**. Instead of hardcoding item codes or customer IDs in your tests or examples, use the `test_data` object in your JSON config:

```json
/* configs/dev.json */
{
    "test_data": {
        "items": { "simple": "ITEM-A01" },
        "customers": { "retail": "C20000" }
    }
}
```

> [!CAUTION]
> **Never store `B1SL_PASSWORD` or other credentials in JSON files.** 
> All server connection parameters must be provided via environment variables or `.env` files. `configs/*.json` are intended for safe, shared test IDs used by the team.

In your code:
```python
# The idiomatic way: Automatically detects profile from B1SL_ENV (defaults to 'dev')
env = B1Environment.load()

# Access test data from the loaded JSON profile
helper = B1TestHelper(env.test_data)
item_code = helper.get_test_item("simple")  # Returns "ITEM-A01" if in 'dev'
```

By swapping `dev` for `prod` (via `B1SL_ENV`), the same script will dynamically use the production item ID (`75004730...`) and enable JSON logging without any code changes.

## Best Practice: `.real` Files
To protect production metadata, the repository is configured to ignore files with the `.real.xml` or `.real.json` extension. You can place your production metadata in `metadata/<version>/metadata_document.real.xml`, and the generator will automatically prioritize it over the generic files for that version.

## Django Integration

For projects using Django, the SDK provides first-class support for loading configuration directly from your `settings.py`.

### 1. Requirements
Add the following variables to your Django `settings.py`:
- `B1SL_BASE_URL`
- `B1SL_USERNAME`
- `B1SL_PASSWORD`
- `B1SL_COMPANY_DB`
- `B1SL_ENV` (optional, defaults to 'dev')

### 2. Loading Config
```python
from b1sl.b1sl import B1Config, B1Client

# Automatically maps B1SL_* settings to a config object
config = B1Config.from_django_settings()
client = B1Client(config)
```

### 3. Legacy Shared Adapter
If you are migrating legacy code that expects a global singleton adapter, you can use:
```python
from b1sl.b1sl.adapter import get_rest_adapter

adapter = get_rest_adapter() # Thread-safe singleton for Django
```

