# SAP B1 Service Layer — `SQLQueries` Entity

> Source: SAP Help Portal, Service Layer API Reference.
> This is verbatim SL behavior, not SDK documentation. For SDK-level usage notes see the "Notes for b1sl" section at the bottom.

`SQLQueries` is the OData entity that lets you persist a named SQL statement on the Service Layer and execute it later via the bounded function `/List`. It is the **SL-native way to run SQL** — works over HTTP/OData, no direct DB driver required, and is gated by a server-side table/column allowlist.

Works on both SAP HANA and Microsoft SQL Server; the SL normalizes the SQL internally so the same statement runs on both backends.

---

## CRUD on the Query Definition

### Create

```
POST https://server:50000/b1s/v1/SQLQueries HTTP/1.1
{
    "SqlCode": "sql04",
    "SqlName": "queryOnItem",
    "SqlText": "select ItemCode, ItemName, ItmsGrpCod from oitm"
}
```

Response:

```
HTTP/1.1 201 Created
{
    "odata.metadata" : "https://server:50000/b1s/v1/$metadata#SQLQueries/@Element",
    "odata.etag"     : "W/\"44486B13CDA82E54A31194A3588857803F9D1E57\"",
    "SqlCode"        : "sql04",
    "SqlName"        : "queryOnItem",
    "SqlText"        : "select [ItemCode], [ItemName], [ItmsGrpCod] from [OITM]",
    "ParamList"      : null,
    "CreateDate"     : "2020-10-08",
    "UpdateDate"     : "2020-10-08"
}
```

Note that SL **normalized** the `SqlText` on store (added brackets/quotes per backend).

### Retrieve by Key

```
GET https://server:50000/b1s/v1/SQLQueries('sql04') HTTP/1.1
```

Returns the stored definition with its current ETag.

### Patch

```
PATCH https://server:50000/b1s/v1/SQLQueries('sql04') HTTP/1.1
{
    "SqlName": "queryOnItem",
    "SqlText": "select ItemCode, ItemName from oitm"
}
```

Returns `204 No Content`.

### Delete

```
DELETE https://server:50000/b1s/v1/SQLQueries('sql04') HTTP/1.1
```

Returns `204 No Content`.

### Retrieve All (with paging)

```
GET https://server:50000/b1s/v1/SQLQueries HTTP/1.1
Prefer: odata.maxpagesize=5
```

Response includes `value: [...]` and `odata.nextLink` like any paginated SL collection.

---

## Execute: the `/List` Bounded Function

Once a `SQLQuery` exists, run it with the **bounded function `/List`**. Accepts either `GET` or `POST`.

The response is a custom shape: `value` contains rows with the **exact columns of the SELECT clause** — column aliases become JSON keys.

```
GET https://server:50000/b1s/v1/SQLQueries('sql04')/List HTTP/1.1
```

```
HTTP/1.1 200 OK
{
    "odata.metadata" : "https://server:50000/b1s/v1/$metadata#SAPB1.SQLQueryResult",
    "SqlText"        : "select [ItemCode], [ItemName], [ItmsGrpCod] from [OITM]",
    "value" : [
        { "ItemCode": "i001", "ItemName": "i001", "ItmsGrpCod": 100 },
        { "ItemCode": "i002", "ItemName": "i002", "ItmsGrpCod": 100 },
        ...
    ]
}
```

### Paging

**Mandatory** server-side paging — protects against runaway joins. Override the default page size with `Prefer: odata.maxpagesize=<N>`:

```
GET https://server:50000/b1s/v1/SQLQueries('sql0001')/List HTTP/1.1
Prefer: odata.maxpagesize=5
```

Response carries `odata.nextLink` like any other paged SL collection:

```json
"odata.nextLink": "SQLQueries('sql0001')/List?&$skip=5"
```

Under the hood SL rewrites the query with `OFFSET/FETCH` (MSSQL) or `LIMIT/OFFSET` (HANA).

### Parameterized Queries

Define named parameters in `SqlText` with a colon prefix (`:paramName`). On create, SL extracts them into `ParamList`:

```
POST .../SQLQueries
{
    "SqlCode": "sql01",
    "SqlName": "queryOnOrder",
    "SqlText": "select DocEntry, DocTotal, DocDate, comments from ordr where DocTotal > :docTotal"
}
```

Response includes `"ParamList": "docTotal"`.

To execute with values:

**POST (body)**

```
POST https://server:50000/b1s/v1/SQLQueries('sql01')/List HTTP/1.1
{
    "ParamList": "docTotal=10.1"
}
```

**GET (query string)**

```
GET https://server:50000/b1s/v1/SQLQueries('sql01')/List?docTotal=10.1 HTTP/1.1
```

Multiple parameters use `&` separation:

```
stringParam1='val1'&integerParam2=val2
```

Note that string values are quoted inside the parameter expression itself.

---

## Allowlist (Security)

Not every table or column can be queried. SL enforces a server-side allowlist.

### Table Allowlist

Configured in `<service layer installation folder>/conf/b1s_sqltable.conf` (JSON). The packaged list includes:

- **Company / Admin**: `CINF`, `OADM`, `ADM1`, `OADP`, `OCRN`, `OFPR`, `OACP`, `OBPL`, `OHLD`+`HLD1`, `OHFC`
- **Business Partners**: `OCRD`, `OCRP`, `CRD1`, `OCPR`
- **Sales Docs**: `OQUT`+`QUT1-14`, `ORDR`+`RDR1-14`, `ODLN`+`DLN1-14`, `ORRR`+`RRR1-14`, `ORDN`+`RDN1-14`, `ODPI`+`DPI1-14`, `OINV`+`INV1-14`, `ORIN`+`RIN1-14`
- **Purchase Docs**: `OPRQ`+`PRQ1-14`, `OPQT`+`PQT1-14`, `OPOR`+`POR1-14`, `OPDN`+`PDN1-14`, `OPRR`+`PRR1-14`, `ORPD`+`RPD1-14`, `ODPO`+`DPO1-14`, `OPCH`+`PCH1-14`, `ORPC`+`RPC1-14`
- **Drafts**: `ODRF`+`DRF1-14`
- **Payments**: `ORCT`, `RCT1-4`, `OVPM`, `VPM1-4`
- **Banks**: `ODSC`, `DSC1`
- **Items / Inventory**: `OITM`, `OITW`, `OIBQ`, `OBIN`, `OBTQ`, `OBBQ`, `OBTN`, `OSRQ`, `OSBQ`, `OSRN`
- **Activities**: `OCLG`, `OCLT`, `OCLS`, `ATC1`
- **Exchange Rates**: `ORTT`
- **Resources**: `ORSC`, `RSC1-6`, `ORST`
- **BOM / Production**: `OITT`, `ITT1-2`, `OWOR`, `WOR1`, `WOR4`, `ORCJ`, `ORCM`
- **Pricing**: `OPLN`, `ITM1`
- **GL**: `OJDT`, `JDT1`
- **Credit Cards / Deposits**: `OCRC`, `OCRH`, `ODPS`
- **Electronic Tx**: `ECM2`

Adding tables outside the allowlist is **outside SAP support scope** and may break security.

### Column Allowlist

Optional per-table column filtering via `ColumnIncludeList` / `ColumnExcludeList`. Example:

```json
{
    "TableList": ["ADM1", "ORDR", "CINF"],
    "ColumnExcludeList": {
        "ORDR": ["CreateDate", "UpdateDate"],
        "CINF": ["Algo", "AliasUpd", "TrailDays"]
    },
    "ColumnIncludeList": {
        "ADM1": ["CurrPeriod", "Street"]
    }
}
```

Disallowed column access → `400 Bad Request` with code `703`:

```json
{
    "error": {
        "code": 703,
        "message": { "lang": "en-us", "value": "Column 'Algo' from table 'CINF' not accessible" }
    }
}
```

Important: **case must match** the DB definition.

---

## Supported SQL Grammar

| Keyword | Example |
|---|---|
| `SELECT … FROM … WHERE` | `select ItemCode, ItemName from oitm where ItemCode > 'i01'` |
| Alias | `select t1.DocEntry as Col1 from ORDR t1` |
| `AND` / `OR` / `NOT` | `where not DocEntry = 1 and DocNum = 1` |
| Parenthesis | `where not (DocEntry = 1 or Comments <> '1234') and DocNum = 1` |
| `BETWEEN … AND …` | `where "DocEntry" BETWEEN 1 AND 10` |
| `ORDER BY` | `order by t1.DocEntry` |
| `GROUP BY … HAVING` | `group by DocStatus, DocType having count(*) > 0` |
| `IS [NOT] NULL` | `where DocEntry is not null and Comments is null` |
| Constants | `SELECT 1 as c1, 'string' as c2 FROM OITM` |
| `LIKE` | `where CardCode like 'c%'` |
| `TOP` | `select top 2 DocStatus from ordr` |
| `UNION [ALL]` | `select LineNum from rdr1 union all select LineNum from inv1` |
| `IN` / `NOT IN` | `where DocEntry in (select DocEntry from rdr1)` |
| `EXISTS` | `where exists(select 1 from rdr1 t2 where t1.DocEntry = t2.DocEntry)` |
| `INNER JOIN` | `from ordr t1 inner join rdr1 t2 on t1.DocEntry = t2.DocEntry` |
| `LEFT/RIGHT/FULL OUTER JOIN` | as above |
| Mixed joins | `inner join … left join …` |

### Supported Functions

| Function | Example |
|---|---|
| `SUM`, `AVG` | `select sum("DocTotal") as sumDocTotal from ordr` |
| `MAX`, `MIN` | `select min("DocTotal") as minDocTotal from ordr` |
| `DISTINCT`, `COUNT` | `count(distinct docEntry)` |
| `IFNULL` / `ISNULL` | `isnull(comments, 'null')` — **normalized cross-backend** |
| `LOWER`, `UPPER` | `lower(ItemCode) as lowerItemCode` |
| `LEFT`, `RIGHT` | `right(ItemCode, 1)` |

Anything not on these lists is **rejected**. More functions may be added in future SL versions.

---

## SQL Normalization (HANA ↔ MSSQL)

SL parses and rewrites identifiers so the **same raw SQL works on both backends**.

### Identifier Quoting

Raw:

```sql
select itemcode, itemName, itmsGrpCod from oitm where ItemCode > 'i01'
```

Becomes:

```sql
-- MSSQL
select [ItemCode], [ItemName], [ItmsGrpCod] from [OITM] where [ItemCode] > 'i01'

-- HANA
select "ItemCode", "ItemName", "ItmsGrpCod" from "OITM" where "ItemCode" > 'i01'
```

This works even if the raw already uses `[]` or `""` — SL still re-normalizes.

### Alias Normalization (MUST)

Without alias normalization, HANA would uppercase column aliases by default, producing different JSON keys per backend. SL normalizes aliases to preserve the user-provided case on both backends. This is **critical** because the alias becomes the JSON key in the response.

### Function Normalization

`IsNull` (MSSQL) and `IfNull` (HANA) are functionally equivalent. SL accepts both and translates to the backend-native form.

```sql
-- raw
select DocEntry, ISNULL(comments, 'null') as mssqlComments,
                 IFNULL(Comments, 'null') as hanaComments from ordr

-- MSSQL: both become ISNULL
-- HANA:  both become IFNULL
```

---

## Notes for b1sl (as of 2026-06-03)

### SDK status: fully implemented

`client.sql_queries` and `b1.sql_queries` are Elite aliases backed by
`SQLQueriesResource` / `AsyncSQLQueriesResource` in
`src/b1sl/b1sl/resources/sql_queries.py`.

### CRUD on definitions

```python
# Sync
with B1Client(config) as b1:
    b1.sql_queries.create(en.SQLQuery(sql_code="sql04", sql_name="q",
                                      sql_text="select ItemCode from oitm"))
    defn = b1.sql_queries.get("sql04")
    b1.sql_queries.update("sql04", en.SQLQuery(sql_text="select ItemCode, ItemName from oitm"))
    b1.sql_queries.delete("sql04")

# Async
async with AsyncB1Client(config) as b1:
    defn = await b1.sql_queries.get("sql04")
```

### Execute — single page

```python
# No params
result = b1.sql_queries.run("sql002")
for row in result:
    print(row["ItemCode"])

# With named params (case-sensitive, must match :name in SqlText)
result = b1.sql_queries.run("sql01", docTotal=100.0, docPartner="C001")

# SQLRunResult helpers
print(result.sql_text)      # normalized SQL SAP executed
print(result.has_more)      # True if @odata.nextLink present
print(len(result))          # row count on this page

# With page size
result = b1.sql_queries.run("sql002", page_size=50)
```

### Execute — full stream (all pages)

```python
# Sync
for row in b1.sql_queries.run_stream("sql002", page_size=100):
    process(row)

# Async
async for row in b1.sql_queries.run_stream("sql002", page_size=100):
    await process(row)

# Safety ceiling
for row in b1.sql_queries.run_stream("sql002", page_size=50, max_pages=10):
    ...
```

### Typed rows with Pydantic (optional)

```python
from pydantic import BaseModel

class ItemRow(BaseModel):
    ItemCode: str

result = b1.sql_queries.run("sql002")
rows = result.to_pydantic(ItemRow)
print(rows[0].ItemCode)
```

### Error handling

```python
from b1sl.b1sl.exceptions import B1SqlNotAllowedError, B1SqlParamError

try:
    result = b1.sql_queries.run("sql04")
except B1SqlNotAllowedError as e:
    # SAP code 702 (table) or 703 (column) in allowlist
    print(f"Blocked [{e.sap_code}]: {e}")
except B1SqlParamError as e:
    # SAP code 704 — wrong param names/count/types
    print(f"Param error: {e}")
```

Both are subclasses of `B1ValidationError` so broad `except B1ValidationError`
catches all 400s.

### Real API observations (production tenant, SL v2)

- `@odata.nextLink` uses v4 format (with `@` prefix), not v3 `odata.nextLink`.
- `$maxpagesize` as query param is **ignored** — only `Prefer: odata.maxpagesize=N` header works.
- Server default page size: **20 rows**.
- Error `code` is a **string** (`"702"`, not `702`).
- Error `message` is a **plain string**, not the `{lang, value}` object in the official docs.
- `ParamList` storage uses `,` as separator (`"a,b"`); invocation uses `&` (`"a=1&b='x'"`).

### Parameter encoding rules (`_format_sql_params`)

| Python type | Serialized form |
|---|---|
| `str` | `name='value'` (internal `'` → `''`) |
| `int` / `float` | `name=123` (bare) |
| `bool` | `name=1` or `name=0` |
| other | `str()` then quoted |

### Why this vs. direct HANA (`hdbcli`)

| | `SQLQueries` (SL endpoint) | Direct HANA (`hdbcli`) |
|---|---|---|
| Transport | HTTP (same session as rest of SDK) | TCP direct to HANA port |
| Driver | none | `hdbcli` (extra, proprietary) |
| Dry-run | ✅ inherited | ❌ |
| ETag | ✅ on definitions | ❌ |
| SQL flexibility | restricted (allowlist + keyword subset) | full HANA SQL |
| Async | ✅ | ❌ (blocking driver) |
| MSSQL compat | ✅ (SL normalizes) | ❌ (HANA only) |
