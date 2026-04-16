# Roadmap / TODOs (Target: v0.1.x+)

## 1. Dynamic UDF (User Defined Fields) Handling
**Context:** Currently, UDFs (fields starting with `U_`) are either filtered out or treated as raw `str/Any` through Pydantic's `extra="allow"`. If a developer wants strict validation, they must create a custom subclass extending the generated entity.
**Proposal:** 
- Implement an interceptor at the Pydantic Base model level that automatically parses unknown fields starting with `U_` into a special `udfs` dictionary property.
- This avoids needing to declare a new class just to serialize/deserialize basic UDFs while keeping the core metadata clean.

## 2. Transparent Pagination Generators
**Context:** The API returns `odata.nextLink` for large recordsets. Currently, the user likely needs to manually inspect `result.next_link` and make a subsequent request.
**Proposal:** 
- Add an `async for` generator (e.g., `client.items.stream()`) that internally handles fetching the next pages automatically as the developer iterates over the results.

## 3. $batch Request Support
**Context:** SAP B1 Service Layer supports OData `$batch` requests to execute multiple creates/updates in a single HTTP transaction.
**Proposal:**
- Implement a `BatchBuilder` utility that allows queuing operations and submitting them together to drastically reduce HTTP overhead for bulk sync processes.

---

## ✅ Recently Completed

- **OData Query Builder (Fluent API)**: Implemented Pythonic operator overloading on `F` schema constants.
- **Example Usage:** `client.items.filter((F.Item.on_hand > 5) & (F.Item.item_name.contains("QUESO")))`

