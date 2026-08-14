# Attachments (`Attachments2`)

`Attachments2` is the one core SAP entity whose payload is **not** JSON: files
are uploaded as `multipart/form-data` and downloaded as a raw binary `$value`
stream. The typed query builder and `adapter.post()` only speak JSON, so the
SDK exposes a dedicated resource plus two low-level primitives.

## Quick start

```python
from b1sl import MultipartFile

# Upload — one request, one new Attachments2 entry
entry = client.attachments.upload(MultipartFile("invoice.pdf", pdf_bytes))
print(entry.absolute_entry)          # -> 12

# Download — raw bytes back
blob = client.attachments.download(12, "invoice.pdf")
```

Async is symmetric:

```python
async with AsyncB1Client(config) as b1:
    entry = await b1.attachments.upload(MultipartFile("invoice.pdf", pdf_bytes))
    blob = await b1.attachments.download(entry.absolute_entry, "invoice.pdf")
```

Reading files from disk:

```python
client.attachments.upload(MultipartFile.from_path("/tmp/invoice.pdf"))
```

## Several files in one entry

A single POST may carry several files. SAP creates **one** `Attachments2` entry
holding one `Attachments2_Line` per file (`LineNum` 0, 1, …):

```python
entry = client.attachments.upload([
    MultipartFile("contract.pdf", contract_bytes),
    MultipartFile("annex.png", annex_bytes),
])
for line in entry.attachments2_lines or []:
    print(line.line_num, line.file_name, line.file_extension)
```

`MultipartFile.field_name` defaults to `"files"` because SAP requires that
exact field name on every part — the real file name travels in `filename`.
Don't override it for `Attachments2`.

## Linking an attachment to a document

`AbsoluteEntry` is what documents reference through their
`AttachmentEntry` field:

```python
entry = client.attachments.upload(MultipartFile("po.pdf", pdf_bytes))
client.orders.update(123, en.Document(attachment_entry=entry.absolute_entry))
```

## Metadata reads

Metadata is ordinary JSON and goes through the inherited `GenericResource`
methods:

```python
meta = client.attachments.get(12)
print(meta.attachments2_lines[0].file_name)
```

## Generic primitives

`upload()`/`download()` are thin wrappers over two adapter primitives, usable
against any Service Layer endpoint that needs a non-JSON body:

```python
# POST multipart/form-data anywhere — returns the parsed JSON response
data = client.post_multipart("Attachments2", MultipartFile("a.pdf", raw_bytes))

# GET a raw binary body anywhere
blob = client.get_binary("Attachments2(12)/$value",
                         {"filename": "'invoice.pdf'"})
```

Both run through the adapters' full request pipeline — the same one every JSON
call uses — so all of the SDK's guarantees hold:

- **Session lifecycle**: automatic login, and with `reuse_token=False` the
  session license is released after every transfer (no leaked sessions).
- **Resilience**: the 401 re-login retry, the one-shot retry of idempotent
  GETs on stale server-closed keepalives, and network errors mapped to
  `B1ConnectionError` (never raw httpx exceptions).
- **Semantic errors**: 404 → `B1NotFoundError`, 400 → `B1ValidationError`, etc.
- **Observability**: `req_id`, duration timing, structured logs, and
  `ObservabilityConfig` `on_response`/`on_error` hooks fire for file transfers
  exactly like for JSON writes.
- **Dry-run**: `post_multipart()` returns a synthetic 204 without sending
  anything. (`get_binary()` is a read; dry-run does not apply.)
- **Headers**: every public method (client and resource, sync and async)
  accepts `headers=` for per-request headers, forwarded to the wire.

ETag handling is deliberately special-cased:

- `post_multipart()` **never sends `If-Match`** — multipart has no concurrency
  semantics (same rule as `$batch`) — and a successful upload proactively
  invalidates any cached ETag for the path.
- `get_binary()` exists because `get()` funnels every body through
  `response.json()` with a `response.text` fallback, which corrupts binary
  payloads. It never sends `If-None-Match` (a cached ETag would make SAP
  answer `304` with an empty body) and never touches the ETag cache — a
  `$value` read is a file fetch, not a basis for optimistic concurrency.

File names are escaped as proper OData string literals: an apostrophe in the
name (`o'brien contract.pdf`) is doubled on the wire, same as entity keys.

## Limitations

**No `DELETE`.** SAP never implemented removal for `Attachments2`, in any
version or configuration — `client.attachments.delete(12)` reaches the server
and comes back as `400` code `220` ("Attachments2 is not allowed to remove").
Remove the line from the entry with `update()` instead. Full evidence in
[`18-sap-version-quirks.md`](18-sap-version-quirks.md) Q4b.

**No ETag concurrency.** `client.attachments` is a specialized resource, not an
Elite alias — SAP offers no optimistic concurrency here, so writes are blind.

**Not batchable.** A `$batch` body is itself multipart and cannot nest a file
upload, nor carry a binary response. Recording either inside `client.batch()`
raises `NotImplementedError` immediately rather than failing at execute time.

**The official manual is wrong about the upload body.** §3.17.3 documents a
two-part JSON+binary shape that SAP rejects with `400 -1000`. See
[`18-sap-version-quirks.md`](18-sap-version-quirks.md) Q4a.
