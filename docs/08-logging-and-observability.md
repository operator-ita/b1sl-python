# Logging & Observability

The SAP B1 Python SDK is built for high-concurrency environments (like FastAPI and Temporal) where traceability and structured data are essential.

## Core Principles

- **Request IDs (`req_id`)**: Every operation (login, request, retry, logout) is traced with a unique 8-character ID.
- **Contextual Context**: Logs automatically include the SAP `User`, the Target `DB`, and the current `SessionID`.
- **Environment Aware**: Automatic switching between human-friendly console logs and machine-friendly JSON.
- **Redaction by Default**: Passwords and sensitive credentials are automatically masked in all log outputs.
- **High-Performance Infrastructure**: Observability primitives (hooks & timing) are handled via non-blocking, defensive dispatchers.
- **Safety Mode (Dry Run)**: Logs automatically prefix intercepted write operations with `[DRY RUN]` for clear auditability.

---

## 1. Quick Setup

The easiest way to initialize logs is using the built-in `setup_logging()` helper.

```python
from b1sl.b1sl.logging_utils import setup_logging
from b1sl.b1sl import B1Env

# Call this at the entry point of your application
# 1. Automatic loading from B1SL_ENV
setup_logging() 

# 2. OR Explicit loading (Preferred for testability)
env = B1Environment.load()
setup_logging(env=env.config.environment)
```

### Environment Variables
The SDK behavior is controlled by the `B1SL_ENV` variable:

| Variable | Value | Mode | Output Format |
| :--- | :--- | :--- | :--- |
| `B1SL_ENV` | `dev` (default) | Development | Human-readable text with `[ReqID]` prefix |
| `B1SL_ENV` | `test` | Testing | Same as dev, specifically for test isolation |
| `B1SL_ENV` | `prod` | Production | Structured JSON (ELK, Datadog ready) |

---

## 2. Using the Global Logger

The SDK exposes a root logger called `sdk_logger` that you can configure to fit your application's needs.

```python
from b1sl.b1sl import sdk_logger
import logging

# Example: Add a custom FileHandler to the entire SDK
fh = logging.FileHandler('sap_audit.log')
sdk_logger.addHandler(fh)

# Example: Set level globally
sdk_logger.setLevel(logging.DEBUG)
```

---

## 3. Injecting Custom Loggers

You can pass your own `logging.Logger` instance directly to any client. The SDK will use your logger and inject the OData context via the `extra` parameter.

```python
import logging
from b1sl.b1sl import AsyncB1Client

my_app_logger = logging.getLogger("my_app.integrations")

async with AsyncB1Client(config, logger=my_app_logger) as b1:
    # All internal SDK logs will now use 'my_app_logger'
    pass
```

---

## 4. Advanced Observability (Hooks & Metrics)

For enterprise monitoring (Datadog, Prometheus, Elastic), the SDK provides a **Hook Pattern** that allows you to intercept every response or error without logic coupling.

### ObservabilityConfig

The `ObservabilityConfig` object is the central point for configuring SDK telemetry.

```python
from b1sl.b1sl import ObservabilityConfig, HookContext

# 1. Define your hooks (Sync or Async)
def my_metrics_hook(ctx):
    # ctx is a frozen (immutable) HookContext
    send_to_datadog(
        metric="sap.request.duration",
        value=ctx.duration_ms,
        tags=[f"method:{ctx.http_method}", f"db:{ctx.db}"]
    )

# 2. Configure the object
obs = ObservabilityConfig(
    hooks={"on_response": [my_metrics_hook]},
    context_extras={"service_name": "inventory-api"},
    slow_request_threshold_ms=2000.0  # Alert if > 2s
)

# 3. Inject into the Client (Thread-safe)
client = B1Client(config, observability=obs)

# Standalone Execution (from project root)
# python examples/observability.py
```

### HookContext Contract

The `HookContext` is an **immutable** (frozen) dataclass passed to all hooks. It ensures that a bug in a hook cannot corrupt the SDK's execution.

| Field | Description |
| :--- | :--- |
| `req_id` | Trace ID for log correlation. |
| `http_method` | GET, POST, etc. |
| `base_url` | The SL base URL (e.g., https://sap:50000/b1s/v1). |
| `endpoint` | The specific resource path (e.g., /Items). |
| `query_params` | Raw query string ($filter=...) for selective logging. |
| `status_code` | HTTP Status (None on network failure). |
| `duration_ms` | Precise execution time in milliseconds. |
| `exc` | Captured Exception (if `on_error` event). |
| `extra` | Custom metadata from `context_extras`. |

---

## 5. Structured JSON Schema (Production)

When `B1SL_ENV=prod` is set, or `setup_logging(env=B1Env.PROD)` is called, logs are emitted as JSON.

> [!NOTE]
> **Privacy by Design:** For security reasons, the full URL is not logged in production by default to prevent leaking sensitive tokens in `query_params`. Users can explicitly log `ctx.query_params` in their custom hooks if required.

**Example JSON Log:**
```json
{
  "timestamp": "2026-04-06T05:30:00.123Z",
  "level": "WARNING",
  "logger": "b1sl.RestAdapter",
  "message": "[a1b2c3d4][manager] [GET /Items] -> 200 (2150.5ms) ⚠ SLOW",
  "req_id": "a1b2c3d4",
  "db": "SBO_DEMO",
  "user": "manager",
  "status_code": 200,
  "http_method": "GET",
  "endpoint": "/Items",
  "duration_ms": 2150.5
}
```

> [!TIP]
> This format allows tools like **Datadog** or **Grafana Loki** to index fields like `req_id` or `duration_ms` automatically, enabling powerful dashboarding and alerting.

---

## 6. Practical Example
For a complete, interactive demonstration of custom hooks and context extras, see:
👉 **[examples/observability.py](../examples/observability.py)**
