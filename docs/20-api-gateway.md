# API Gateway (Crystal Reports → PDF)

`b1sl.api_gateway` is an **async client for the SAP Business One API Gateway**
— the native SAP service (`sbo-api-gateway-service.jar`) that exposes Crystal
Reports layouts over REST and renders them to PDF. It produces the *official*
document: the same PDF the SAP B1 client emits when you click **Print**.

It is a sibling of the Service Layer SDK, not part of it. The two are separate
SAP services:

| | Service Layer (`b1sl.b1sl`) | API Gateway (`b1sl.api_gateway`) |
|---|---|---|
| Default port | `50000` | **`60000`** |
| Base path | `/b1s/v2/` | **`/rs/v1/`** |
| Session | `B1SESSION` cookie | its own cookies (`Session`, `Cookie`), `SessionTimeout` from `/login` |
| SAP authorization | object permissions | **General Authorizations → Report Layout API** (per user) |
| Error signalling | HTTP status + OData `error` body | mostly **`200 OK` + sentinel bodies** (see below) |

Because the response semantics are incompatible, the gateway client shares
`b1sl`'s building blocks (config, `ObservabilityConfig` hooks, the `B1Exception`
hierarchy) but does **not** inherit from the Service Layer adapter/client, and
gateway responses never flow through the OData `Result` path.

## Quick start

```python
from b1sl.api_gateway import APIGatewayConfig, AsyncAPIGatewayClient

cfg = APIGatewayConfig(
    base_url="https://sap-host:60000",   # scheme + host + port only
    username="manager",
    password="…",
    company_db="SBODemoMX",              # selects the tenant — set deliberately
)

async with AsyncAPIGatewayClient(cfg) as gw:
    # Print quotation DocEntry 12345 with the QUT20020 layout
    pdf = await gw.export_document_pdf("QUT20020", doc_entry=12345)
    assert pdf.startswith(b"%PDF-")
```

Configuration from the environment reuses the Service Layer credentials — a
deployment that already sets `B1SL_USERNAME` / `B1SL_PASSWORD` /
`B1SL_COMPANY_DB` only needs the gateway URL:

```python
cfg = APIGatewayConfig.from_env()   # B1SL_GATEWAY_BASE_URL + B1SL_* fallbacks
```

| Variable | Fallback | Meaning |
|---|---|---|
| `B1SL_GATEWAY_BASE_URL` | — (required) | `https://host:60000` |
| `B1SL_GATEWAY_USERNAME` | `B1SL_USERNAME` | SAP user |
| `B1SL_GATEWAY_PASSWORD` | `B1SL_PASSWORD` | |
| `B1SL_GATEWAY_COMPANY_DB` | `B1SL_COMPANY_DB` | tenant |
| `B1SL_GATEWAY_SSL_VERIFY` | `B1SL_SSL_VERIFY` | `0`/`1` |
| `B1SL_GATEWAY_CONNECT_TIMEOUT` / `_READ_TIMEOUT` | `10` / `120` | seconds |
| `B1SL_GATEWAY_SESSION_TTL` | — | seconds; overrides the server's `SessionTimeout` |

Or derive from an existing `B1Config`:

```python
cfg = APIGatewayConfig.from_b1_config(b1_config, base_url="https://sap-host:60000")
```

> **Same user, two tenants.** The SAP user is usually shared between the
> production and test company databases; the **only** thing that decides
> which one you print from is `company_db`. Never take it from a caller-supplied
> parameter.

## The four endpoints

| Method | Path | Client method |
|---|---|---|
| `POST` | `/login` | `login()` (automatic) |
| `GET` | `/rs/v1/LoadAuthorizedCRList` | `list_reports() -> list[ReportInfo]` |
| `GET` | `/rs/v1/LoadCR?DocCode=<code>` | `get_report_parameters(code) -> list[ReportParameter]` |
| `POST` | `/rs/v1/ExportPDFData?DocCode=<code>` | `export_pdf()`, `export_document_pdf()`, `export_pdf_raw()` |

### `list_reports()` — general catalog only

`LoadAuthorizedCRList` returns the **general-catalog** reports (`RCRI00xx`).
Document-bound print layouts (`QUT200xx` quotations, `INV200xx` invoices…) are
**not** listed by any endpoint: their code is read by hand in the SAP B1
client, *Print Layout Designer* → column "Layout ID". Keep that mapping
versioned in your application.

### `get_report_parameters(doc_code)`

Returns the layout's parameter definitions. Each `ReportParameter` exposes
`name`, `type` (`xsd:decimal` / `xsd:string` / `xsd:date`), `current_values`
(flat list of strings), `allow_null`, `allow_multi_value`, `parameter_type`
(`ReportParameter` / `StoredProcedureParameter`) and the full wire dict in
`raw`. Booleans arrive as `"true"`/`"false"` strings on the wire and are
coerced.

Document-bound layouts always carry `ObjectId@` (SAP object type — `23` =
quotations) and `DocKey@` (`DocEntry`).

The success body is `{"error": false, "resultSet": [...]}` (`LoadCR` uses an
`error` flag where `LoadAuthorizedCRList` uses `"result": "Success"`; the
client treats `error: true` or a non-`Success` result as
`APIGatewayResponseError`).

Unknown `DocCode` → the gateway answers `200 {}` (no 404). The client raises
`APIGatewayLayoutNotFoundError` — usually a sign that a hard-coded layout
mapping drifted from what exists in SAP.

### `export_document_pdf(doc_code, doc_entry, *, object_id=None, values=None, parameters=None)`

Prints one SAP document. It **always sets `DocKey@` explicitly**:

> ⚠️ `LoadCR` preloads a `DocKey@` value, but it is stored in the layout
> definition, not resolved against the database. It may point at an arbitrary
> (or nonexistent) document. Relying on it means silently printing the wrong
> document with a `200 OK`.

**Pass `object_id`** (SAP object type: 23 quotations, 17 orders, 15
deliveries, 13 invoices …) unless you know the layout preloads it: in a survey
of 49 real document layouts on one system only 7 preloaded `ObjectId@`. Real
layouts spell the parameter both `ObjectId@` and `ObjectID@` — names are
resolved case-insensitively, so callers never need to know which — and some
declare no object-type parameter at all (`DocKey@` only), in which case
`object_id` is ignored. Layouts with further **required** parameters (some
invoice layouts want `ExtParam@`, `FolioPref@`, `FolioNum@`) need them in
`values=`; otherwise `APIGatewayParameterError` names the missing parameter
locally, before any call. Pass `parameters=` (a cached
`get_report_parameters()` result) to skip the `LoadCR` round-trip when
printing many documents with the same layout.

### `export_pdf(doc_code, values=None, *, parameters=None, strict=True)`

General form for catalog reports with arbitrary Crystal parameters:

```python
from datetime import date

pdf = await gw.export_pdf(
    "RCRI0018",
    {"RangeDate@": (date(2026, 6, 7), date(2026, 6, 13)), "showInactiveEmployee": "N"},
)
```

`values` accepts scalars (`str`, `int`, `Decimal`, `date`, `datetime`), a flat
sequence (date range, multi-value) or an already-shaped `[[…]]` list. `bool`
is rejected on purpose — Crystal layouts expect a literal (`"Y"`/`"N"`,
`"true"`/`"false"`) that only the layout author knows.

### `export_pdf_raw(doc_code, payload)`

The verbatim escape hatch: `payload` is the `[{"name","type","value":[[…]]}]`
array, sent untouched. Response validation (sentinel, base64, magic bytes)
still applies.

## Payload rules (`build_export_payload`)

The `ExportPDFData` body is a JSON **array**, one entry per parameter:

```json
[
  {"name": "DocKey@",   "type": "xsd:decimal", "value": [["12345"]]},
  {"name": "ObjectId@", "type": "xsd:decimal", "value": [["23"]]}
]
```

`build_export_payload(parameters, values)` merges `LoadCR` definitions with
your values under these rules — every one learned by breaking the call, none in
SAP's manual:

1. **Empty + nullable parameters are omitted entirely.** Including one — even
   as `""` — makes the export fail. (Optional `Pm-<Table>.<Field>` formula
   parameters on document layouts are the canonical case.)
2. **Empty + not nullable** without a supplied value → `APIGatewayParameterError`
   locally (`strict=True`), before hitting the wire.
3. **`xsd:date` needs an explicit value** (from `values` or a `resolver`). `LoadCR` echoes dates as
   `"Date(2026, 6, 7) to Date(2026, 6, 13)"`; sending that back (or Crystal
   formula syntax) fails with `Unparseable date`. What works: ISO strings, a
   range as two ISO strings **in the same inner array** —
   `[["2026-06-07", "2026-06-13"]]`. Pass `date` objects and the builder
   formats them.
4. **Unknown names** in `values` are rejected (`strict=True`) — a typo would
   otherwise be dropped silently. Case differences are not typos: keys are
   resolved case-insensitively against the layout's names first
   (`ObjectId@` → `ObjectID@`).
5. Everything else resends `current_values` as-is. `xsd:decimal` accepts
   strings or JSON numbers; strings are sent.

> ⚠️ **Unverified: multi-value parameters** (`allowMultiValue: "true"`) and
> non-date ranges. The builder emits `[["v1", "v2"]]` for a flat sequence and
> passes `[["a", "b"], ["c"]]` through, but no layout on the verified system
> declared a multi-value parameter, so those shapes are inferred from the
> verified date-range form, not measured. There is a `TODO(unverified)` in
> `payload.py`; verify against a real multi-value layout before relying on it.

## Resolving layout-specific parameters (the extension point)

Layouts differ per installation: one company's invoice layout takes only
`DocKey@`, another's requires a fiscal folio (`FolioPref@`, `FolioNum@`) or an
`ExtParam@`. The library deliberately **never guesses** those values — what a
parameter means is knowledge of your SAP installation and your layout, and a
wrong guess prints a wrong document with `201 OK`. Instead it gives you two
tools so *your* application can supply them cleanly:

1. **Ask before printing** — `missing_required_parameters(parameters, values)`
   returns the `ReportParameter`s that `build_export_payload` would still
   reject (empty and not nullable, or a date without an explicit value),
   without raising. `ReportParameter.is_required` is the per-parameter flag.
   Use it to decide up front: refuse, look the values up, or ask a person.
2. **Plug in a resolver** — `export_pdf(..., resolver=fn)` /
   `export_document_pdf(..., resolver=fn)` /
   `build_export_payload(..., resolver=fn)` accept a
   `ParameterResolver`: `fn(param: ReportParameter) -> value | None`. It is
   consulted for every parameter `values` does not cover; `None` means "no
   opinion" and the default rules apply (preloaded value → omitted if
   nullable → error naming the parameter). Precedence: `values` → `resolver`
   → preloaded `current_values`.

```python
from b1sl.api_gateway import missing_required_parameters

# Application-owned knowledge, per installation — not the library's.
doc = await b1.invoices.get(doc_entry)          # Service Layer, fetched up front
MY_RESOLVERS = {
    "FolioPref@": lambda: doc.series_string,
    "FolioNum@": lambda: doc.doc_num,
}

params = await gw.get_report_parameters(layout)
needed = missing_required_parameters(params, {"DocKey@": doc_entry})
if any(p.name not in MY_RESOLVERS for p in needed):
    raise ValueError(f"layout {layout} needs {[p.name for p in needed]}")

pdf = await gw.export_document_pdf(
    layout, doc_entry=doc_entry, object_id=13, parameters=params,
    resolver=lambda p: MY_RESOLVERS[p.name]() if p.name in MY_RESOLVERS else None,
)
```

The resolver is synchronous on purpose: values usually derive from data the
caller already holds; fetch anything I/O-bound before the call (the
`missing_required_parameters` step tells you what to fetch). Resolver keys
match layout names case-insensitively like `values` do.

## Failure detection — the gateway does not use HTTP status codes

| Signal | What it means | Exception |
|---|---|---|
| `ExportPDFData` → `200 OK`, body is the 5 bytes `(---)` (`application/json`) | the gateway's generic "could not render": malformed payload (wrong shape, empty optional included, unparseable value), unknown `DocCode`, **or a transient collision between concurrent exports** | retried once, then `APIGatewayParameterError` |
| `/login` → `200 OK` with `{"code":-1,"message":{"value":"Failed to login…"}}`, no cookie | bad password / unknown `CompanyDB` (verified; also no user lock-out after single failures) | `APIGatewayAuthError` |
| `LoadCR` → `200 OK`, body `{}` | `DocCode` does not exist | `APIGatewayLayoutNotFoundError` |
| decoded body does not start with `%PDF-` | not a document (HTML error page, garbage) | `APIGatewayPDFError` |
| `LoadCR` without `DocCode` → `400 {"code":400,"message":"400 BAD_REQUEST"}` | the only real HTTP error seen; `DocCode=` (empty) answers `{}` instead | `APIGatewayResponseError` |
| `result` ≠ `"Success"` in a JSON body | gateway-reported failure | `APIGatewayResponseError` |
| `/login` non-2xx, or `401`/`403` after one re-login | transport-level login failure / dead session even after re-login | `APIGatewayAuthError` |
| DNS / refused / timeout | gateway down (independent of Service Layer!) | `APIGatewayConnectionError` |

All of them derive from `APIGatewayError` (itself a `B1Exception`), so the
gateway boundary can be isolated with one `except`. `APIGatewayConnectionError`
and `APIGatewayAuthError` also inherit from `B1ConnectionError` /
`B1AuthError` for callers that already catch those broadly — but the message
always names the API Gateway so a gateway outage is never misread as a Service
Layer failure.

The `ExportPDFData` success body is **raw base64 text**, served as
`Content-Type: application/octet-stream` with a
`Content-Disposition: form-data; name="attachment"; filename="<DocCode>.pdf"`
header and `201 Created`. Under concurrent exports on one session some calls
come back **`200 OK` with the `(---)` sentinel** instead (1 of 5 and 3 of 5 in
two measured rounds of five; rounds of three and two came back clean). The
client therefore never keys success on `200` vs `201` — it decodes any 2xx
body, retries a `(---)` exactly once (the export is idempotent) and verifies
the magic bytes before returning `bytes`. A raw binary PDF or a JSON-quoted
base64 string are tolerated too.

## Session handling

* `connect()` / `async with` (or `with` on the sync client) logs in;
  `aclose()` / `close()` logs out and closes the pool. Logout is `POST /logout`
  with an empty JSON body — verified to invalidate the server session
  (subsequent requests get `401`). The gateway routes it through a Spring OIDC
  handler (`/auth/oidc.logout`) that never answers 2xx — `400` with a JSON
  body, `415` without one, `405` to GET — yet invalidates the session in every
  variant; `/Logout`, `/rs/v1/Logout` and `/rs/v1/logout` are plain `404`s and
  do nothing. The client treats any answer as success and clears its cookies.
* Bad credentials do **not** come back as `401`: `/login` answers `200` with
  `{"code":-1,"message":{"lang":"en-us","value":"Failed to login for current
  user, please double check and retry"}}` and sets no cookie (same body for an
  unknown `CompanyDB`). The client checks that envelope (and the presence of
  `SessionTimeout`) and raises `APIGatewayAuthError`. Two single failed
  attempts did not lock the SAP user.
* Every call goes through `ensure_session()`, guarded by an `asyncio.Lock` so
  concurrent tasks never race into parallel logins.
* **Expiry is handled reactively by default.** `/login` reports
  `SessionTimeout: 30`, but that is *not* 30 minutes: measured live, a
  session with zero traffic was still valid **32 min after login**, and one
  last used at +29 min was still valid at **+40 min**; the real lifetime (and
  the field's unit) is unknown beyond "longer than that". Guessing a TTL
  would only produce needless logins and orphaned server sessions, so the
  client schedules no proactive refresh (`token_expiry` stays `None`) and
  instead re-logs in when the gateway says so: a `401`/`403` or a redirect
  (`3xx`, `follow_redirects` is off so a login-page redirect can't swallow
  the cookies) triggers **one** re-login and retry. All gateway endpoints are
  reads, so the retry is safe. Verified: a request without (or with an
  invalid) session cookie gets a bare `401` with `Content-Length: 0` (no
  body, no `WWW-Authenticate`, no redirect).
* Opt-in proactive refresh: set `APIGatewayConfig.session_ttl` (or
  `B1SL_GATEWAY_SESSION_TTL` seconds) and the client re-logs in that long
  after each login, minus `session_refresh_margin` (capped at ¼ of the TTL).
  Useful if you measure a real limit on your gateway.
* Cookies: `/login` sets two `Set-Cookie` headers — `Session` and `Cookie`,
  same value, both `Secure; HTTPOnly`, no `Path`/`Domain`/`Max-Age` — so the
  gateway must be reached over HTTPS. httpx's jar handles them; the client
  never reads or forwards them itself.

## Concurrency

Calls on one client share one session and run in parallel (asyncio tasks on
the async client, threads on the sync one — both serialise only the login).
Measured on the verified system:

* `LoadCR`: 10 concurrent on one session all `200`, 0.22–0.71 s each vs
  0.21 s sequential — parallel, mild contention, no failures.
* `ExportPDFData`: parallel rendering is real (five in ~2.1–3.3 s each vs
  2.4 s isolated, all successful bodies byte-identical to the sequential
  export), but the gateway **drops some renders under load** — answering
  `(---)` for 1 of 5 and 3 of 5 in two rounds of five, while rounds of three
  and two were clean.

The client therefore applies two guards, both configurable:

* `APIGatewayConfig.max_concurrent_exports` (default **3**, env
  `B1SL_GATEWAY_MAX_CONCURRENT_EXPORTS`, `0` disables) — a per-client
  semaphore around `ExportPDFData` only; `LoadCR`/list calls are unbounded.
* One automatic retry when an export answers `(---)`.

If you still see `APIGatewayParameterError` under load, lower the bound.

## Observability

`AsyncAPIGatewayClient(cfg, observability=ObservabilityConfig(...))` accepts
the same hooks contract as the Service Layer adapters
(`docs/08-logging-and-observability.md`): `on_response` / `on_error` receive a
`HookContext` whose `extra["service"] == "api_gateway"`. Login payloads are
logged with the password redacted. Logger: `b1sl.api_gateway`.

## Sync client

`APIGatewayClient` is the synchronous twin — same members and signatures
(enforced by `tests/unit/test_sync_async_parity.py`), `httpx.Client` under
the hood, `threading.Lock` around login, safe to share across threads:

```python
from b1sl.api_gateway import APIGatewayClient, APIGatewayConfig

with APIGatewayClient(APIGatewayConfig.from_env()) as gw:
    pdf = gw.export_document_pdf("QUT20020", doc_entry=12345)
```

## Scope and non-goals

* **PDF only** — the verified flow is `ExportPDFData`.
* **No layout discovery for document-bound layouts** — SAP offers none.
* **Crystal Reports only** — PLD layouts are not served by the gateway.
* **Read-only against SAP** — rendering a layout writes nothing.
* No dry-run mode: nothing to intercept.

## Tests and cassettes

Unit tests (`tests/unit/test_api_gateway.py`, `test_api_gateway_sync.py`)
mock the wire with respx and cover both twins, the payload builder and the
config. `tests/integration/test_api_gateway_real.py` holds VCR cassettes
recorded once against a real gateway (test tenant) and replayed offline by
`make test-vcr`; they pin the real wire shape (login body, `resultSet`
layouts, base64 export body, `201`, the `400` logout) with everything
identifying scrubbed at record time — host, tenant, credentials, cookies,
`CompanyID`, layout codes (`LAY00001`/`RPT0000x`), catalog names, `DocKey`
(`1001`), parameter names, and the PDF (replaced by a synthetic one). Both
clients are enrolled in `tests/unit/test_sync_async_parity.py`.

## Verified against

SAP B1 2511 (HANA), API Gateway `Version: "0.0.1"`, 2026-08-17: `/login`,
`LoadAuthorizedCRList`, `LoadCR`, `ExportPDFData` with catalog (`RCRI0018`,
date range) and quotation layouts (`QUT20008/20020/20021`, `ObjectId@ = 23`,
`DocKey@` overridden). The `(---)` sentinel, the empty-optional rule, the date
format and the unreliable preloaded `DocKey@` were all observed there, and
re-checked against a second (test) tenant of the same system: raw base64 body,
`Set-Cookie` shape, bare `401` when unauthenticated, and the concurrency
figures above. Also verified on the test tenant: `/logout` behaviour, the `200`+error
envelope on bad credentials, `LoadCR` `400` without `DocCode`, the
concurrency figures above, and the session-lifetime lower bounds (idle
session alive at +32 min, keepalive session alive at +40 min). The exact
lifetime beyond that was **not** measured — which is why expiry is reactive.
