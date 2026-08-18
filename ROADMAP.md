# Roadmap / TODOs (Target: v0.1.x+)

*(All v0.1.x roadmap items have been completed!)*

---

## 🔎 Open verification items — `b1sl.api_gateway` (shipped in 0.13.0)

Neither blocks current consumers (document layouts use no multi-value
parameters, and the clients re-login reactively on `401` regardless of the
session lifetime). Tracked here so they never read as closed:

- [ ] **Real API Gateway session lifetime / unit of `SessionTimeout: 30`.**
  Measured so far (test tenant, 2026-08-17): a session with zero traffic was
  still valid at **+32 min** after login and one last used at +29 min was
  still valid at **+40 min** — so `30` is neither seconds nor minutes. The
  exact lifetime (and whether it is sliding or absolute) is unknown beyond
  those lower bounds; the +62 min probe was lost. To close: chain probes in
  processes shorter than 60 min (persist the cookie jar between runs) until a
  session actually answers `401`, then decide whether `session_ttl` deserves
  a non-`None` default. Until then the clients stay reactive-only.
- [ ] **`allowMultiValue` / multi-range parameter shapes.** `format_value`
  emits `[["v1", "v2"]]` for a flat sequence and passes `[[...], [...]]`
  through, but no layout on the verified system declared a multi-value
  parameter — acceptance is inferred from the verified `xsd:date` range form.
  A survey of 49 real document layouts (QUT/RDR/DLN/INV families, 2026-08-17)
  found **none** with `allowMultiValue: "true"`, so the sales-document flow is
  unaffected; the gap only matters for catalog reports.
  To close: run `export_pdf()` against a catalog layout with
  `allowMultiValue: "true"` (and one with several ranges), then remove the
  `TODO(unverified)` in `src/b1sl/api_gateway/payload.py` and the warnings in
  the docstrings / `docs/20-api-gateway.md`.

---

## ✅ Recently Completed

- **Transparent Pagination Generators**: Implemented `.stream()` for resources to automatically handle fetching next pages using `odata.nextLink`.
- **$batch Request Support**: Implemented a recording-adapter based `BatchClient` that supports multi-resource transactions and complex result parsing.
- **Dynamic UDF Handling**: Implemented a unified `.udfs` proxy on the `B1Model` base class for type-safe, ergonomic User-Defined Field access.
- **OData Query Builder (Fluent API)**: Implemented Pythonic operator overloading on `F` schema constants.
- **Example Usage:** `client.items.filter((F.Item.on_hand > 5) & (F.Item.item_name.contains("Widget")))`

