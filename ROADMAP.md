# Roadmap / TODOs (Target: v0.1.x+)

*(All v0.1.x roadmap items have been completed!)*

---

## ✅ Recently Completed

- **Transparent Pagination Generators**: Implemented `.stream()` for resources to automatically handle fetching next pages using `odata.nextLink`.
- **$batch Request Support**: Implemented a recording-adapter based `BatchClient` that supports multi-resource transactions and complex result parsing.
- **Dynamic UDF Handling**: Implemented a unified `.udfs` proxy on the `B1Model` base class for type-safe, ergonomic User-Defined Field access.
- **OData Query Builder (Fluent API)**: Implemented Pythonic operator overloading on `F` schema constants.
- **Example Usage:** `client.items.filter((F.Item.on_hand > 5) & (F.Item.item_name.contains("QUESO")))`

