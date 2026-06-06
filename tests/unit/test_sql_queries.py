"""Unit tests for SQLQueriesResource and AsyncSQLQueriesResource.

Covers:
1. run() — single page, no params
2. run() — with named parameters (encoding check)
3. run_stream() — follows @odata.nextLink across two pages
4. Error mapping — B1SqlNotAllowedError (702) and B1SqlParamError (704)
5. SQLRunResult helpers — __iter__, __len__, has_more, to_pydantic
6. _format_sql_params — encoding correctness
7. run(method="GET") opt-in
8. AsyncSQLQueriesResource — mirrors all sync scenarios
"""

import pytest
from pydantic import BaseModel

from b1sl.b1sl.exceptions.exceptions import B1SqlNotAllowedError, B1SqlParamError
from b1sl.b1sl.models.result import Result
from b1sl.b1sl.resources.sql_queries import (
    AsyncSQLQueriesResource,
    SQLQueriesResource,
    SQLQueryInfo,
    SQLRunResult,
    _format_sql_params,
)
from tests.fakes.fake_rest_adapter import FakeAsyncRestAdapter, FakeRestAdapter

# ── Helpers ────────────────────────────────────────────────────────────────────

def _fake_list_response(rows: list[dict], next_link: str | None = None) -> Result:
    """Build a Result that mimics a real /List response (v4 @odata.nextLink)."""
    data: dict = {
        "@odata.context": "https://sap-server.example.com/b1s/v2/$metadata#SAPB1.SQLQueryResult",
        "SqlText": "select T0.\"ItemCode\" from \"OITM\" T0",
        "value": rows,
    }
    if next_link:
        data["@odata.nextLink"] = next_link
    return Result(
        status_code=200,
        message="OK",
        data=data,
        next_link=next_link,
    )


def _fake_error_result(code: str, message: str) -> Result:
    """Build a Result that mimics a SAP 400 error."""
    return Result(
        status_code=400,
        message="Bad Request",
        data={"error": {"code": code, "details": [{"code": "", "message": ""}], "message": message}},
    )


# ── _format_sql_params ─────────────────────────────────────────────────────────

class TestFormatSqlParams:
    def test_empty(self):
        assert _format_sql_params({}) == ""

    def test_integer(self):
        assert _format_sql_params({"docEntry": 5}) == "docEntry=5"

    def test_float(self):
        assert _format_sql_params({"total": 100.5}) == "total=100.5"

    def test_string_quoted(self):
        assert _format_sql_params({"cardCode": "C001"}) == "cardCode='C001'"

    def test_string_with_single_quote_escaped(self):
        # Internal ' must be doubled: O'Brien → 'O''Brien'
        assert _format_sql_params({"name": "O'Brien"}) == "name='O''Brien'"

    def test_bool_true(self):
        assert _format_sql_params({"active": True}) == "active=1"

    def test_bool_false(self):
        assert _format_sql_params({"active": False}) == "active=0"

    def test_multiple_params(self):
        result = _format_sql_params({"docTotal": 10.1, "docPartner": "C001"})
        assert result == "docTotal=10.1&docPartner='C001'"


# ── SQLRunResult ───────────────────────────────────────────────────────────────

class TestSQLRunResult:
    def _make_result(self, rows=None, next_link=None):
        return SQLRunResult(
            rows=rows or [{"ItemCode": "A"}, {"ItemCode": "B"}],
            sql_text="select ...",
            next_link=next_link,
        )

    def test_len(self):
        r = self._make_result()
        assert len(r) == 2

    def test_iter(self):
        r = self._make_result()
        codes = [row["ItemCode"] for row in r]
        assert codes == ["A", "B"]

    def test_getitem(self):
        r = self._make_result()
        assert r[0]["ItemCode"] == "A"

    def test_has_more_false(self):
        r = self._make_result()
        assert r.has_more is False

    def test_has_more_true(self):
        r = self._make_result(next_link="SQLQueries('sql002')/List?&$skip=20")
        assert r.has_more is True

    def test_to_pydantic(self):
        class ItemRow(BaseModel):
            ItemCode: str

        r = self._make_result(rows=[{"ItemCode": "A001"}, {"ItemCode": "A002"}])
        typed = r.to_pydantic(ItemRow)
        assert len(typed) == 2
        assert typed[0].ItemCode == "A001"

    def test_from_raw_v4_next_link(self):
        data = {
            "@odata.context": "...",
            "SqlText": "select ...",
            "value": [{"X": 1}],
            "@odata.nextLink": "SQLQueries('q')/List?&$skip=20",
        }
        r = SQLRunResult._from_raw(data)
        assert r.next_link == "SQLQueries('q')/List?&$skip=20"
        assert r.rows == [{"X": 1}]
        assert r.sql_text == "select ..."

    def test_from_raw_v3_next_link(self):
        data = {"value": [{"X": 1}], "odata.nextLink": "SQLQueries('q')/List?$skip=5"}
        r = SQLRunResult._from_raw(data)
        assert r.next_link == "SQLQueries('q')/List?$skip=5"


# ── SQLQueriesResource (sync) ──────────────────────────────────────────────────

class TestSQLQueriesResourceRun:
    def _make_resource(self):
        adapter = FakeRestAdapter()
        resource = SQLQueriesResource(adapter)
        return resource, adapter

    def test_run_no_params_uses_post(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": "ITEM-001"}, {"ItemCode": "ITEM-002"}]
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(rows).data)

        result = resource.run("sql002")

        assert len(result) == 2
        assert result[0]["ItemCode"] == "ITEM-001"
        assert result.sql_text == "select T0.\"ItemCode\" from \"OITM\" T0"
        assert result.has_more is False
        # Verify POST was used
        assert adapter.calls[0]["method"] == "POST"

    def test_run_with_params_encodes_body(self):
        resource, adapter = self._make_resource()
        rows = [{"DocEntry": 1, "DocTotal": 2000.0}]
        adapter.register("POST", "SQLQueries('sql01')/List", _fake_list_response(rows).data)

        result = resource.run("sql01", docTotal=10.1, docPartner="C001")

        assert len(result) == 1
        posted_body = adapter.calls[0]["data"]
        assert posted_body == {"ParamList": "docTotal=10.1&docPartner='C001'"}

    def test_run_page_size_sets_prefer_header(self):
        resource, adapter = self._make_resource()
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response([]).data)

        resource.run("sql002", page_size=5)

        headers = adapter.calls[0]["headers"]
        assert headers == {"Prefer": "odata.maxpagesize=5"}

    def test_run_returns_next_link_when_present(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": f"I{i:03d}"} for i in range(20)]
        next_link = "SQLQueries('sql002')/List?&$skip=20"
        adapter.register(
            "POST",
            "SQLQueries('sql002')/List",
            _fake_list_response(rows, next_link=next_link).data,
        )

        result = resource.run("sql002")

        assert result.has_more is True
        assert result.next_link == next_link


class TestSQLQueriesResourceRunStream:
    def _make_resource(self):
        adapter = FakeRestAdapter()
        resource = SQLQueriesResource(adapter)
        return resource, adapter

    def test_run_stream_single_page(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": "A001"}, {"ItemCode": "A002"}]
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(rows).data)

        results = list(resource.run_stream("sql002"))

        assert results == rows
        assert len(adapter.calls) == 1

    def test_run_stream_follows_next_link(self):
        resource, adapter = self._make_resource()
        page1_rows = [{"ItemCode": f"P1_{i}"} for i in range(3)]
        page2_rows = [{"ItemCode": f"P2_{i}"} for i in range(2)]

        next_link = "SQLQueries('sql002')/List?&$skip=3"
        # First page: POST
        adapter.register(
            "POST",
            "SQLQueries('sql002')/List",
            _fake_list_response(page1_rows, next_link=next_link).data,
        )
        # Second page: GET (nextLink is always GET)
        adapter.register(
            "GET",
            "SQLQueries('sql002')/List",
            _fake_list_response(page2_rows).data,
        )

        results = list(resource.run_stream("sql002"))

        assert len(results) == 5
        assert results[0]["ItemCode"] == "P1_0"
        assert results[3]["ItemCode"] == "P2_0"
        assert len(adapter.calls) == 2

    def test_run_stream_respects_max_pages(self):
        resource, adapter = self._make_resource()
        page_rows = [{"ItemCode": "X"}]
        next_link = "SQLQueries('sql002')/List?&$skip=1"

        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(page_rows, next_link).data)
        # Register a second page that should NOT be fetched
        adapter.register("GET", "SQLQueries('sql002')/List", _fake_list_response(page_rows, next_link).data)

        results = list(resource.run_stream("sql002", max_pages=1))

        assert len(results) == 1
        assert len(adapter.calls) == 1


# ── Error mapping ──────────────────────────────────────────────────────────────

class TestSQLErrorMapping:
    """Verify that B1SqlNotAllowedError and B1SqlParamError are raised correctly.

    These tests use the real exception classes directly (no adapter needed)
    since the mapping logic is tested in isolation.
    """

    def test_b1_sql_not_allowed_702(self):
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            raise B1SqlNotAllowedError(
                "SAP SQL allowlist violation [702]: Table 'OSRI' not accessible",
                sap_code="702",
                details={"error": {"code": "702", "message": "Table 'OSRI' not accessible"}},
            )
        err = exc_info.value
        assert err.sap_code == "702"
        assert "OSRI" in str(err)
        assert err.details is not None

    def test_b1_sql_not_allowed_703(self):
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            raise B1SqlNotAllowedError(
                "SAP SQL allowlist violation [703]: Column 'Password' not accessible",
                sap_code="703",
            )
        assert exc_info.value.sap_code == "703"

    def test_b1_sql_param_error_704(self):
        with pytest.raises(B1SqlParamError) as exc_info:
            raise B1SqlParamError("SAP SQL parameter error: Parameter error.")
        err = exc_info.value
        assert err.sap_code == "704"

    def test_not_allowed_is_subclass_of_validation_error(self):
        from b1sl.b1sl.exceptions.exceptions import B1ValidationError
        err = B1SqlNotAllowedError("test", sap_code="702")
        assert isinstance(err, B1ValidationError)

    def test_param_error_is_subclass_of_validation_error(self):
        from b1sl.b1sl.exceptions.exceptions import B1ValidationError
        err = B1SqlParamError("test")
        assert isinstance(err, B1ValidationError)

    def test_raise_if_sql_error_702(self):
        from b1sl.b1sl.base_adapter import BaseRestAdapter
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            BaseRestAdapter._raise_if_sql_error(
                400,
                "702",
                "Table 'OSRI' not accessible",
                {"error": {"code": "702", "message": "Table 'OSRI' not accessible"}},
            )
        assert exc_info.value.sap_code == "702"

    def test_raise_if_sql_error_704(self):
        from b1sl.b1sl.base_adapter import BaseRestAdapter
        with pytest.raises(B1SqlParamError):
            BaseRestAdapter._raise_if_sql_error(400, "704", "Parameter error.", None)

    def test_raise_if_sql_error_ignores_non_400(self):
        from b1sl.b1sl.base_adapter import BaseRestAdapter
        # Should not raise for non-400 status even with SQL code
        BaseRestAdapter._raise_if_sql_error(404, "702", "not found", None)

    def test_raise_if_sql_error_ignores_unknown_code(self):
        from b1sl.b1sl.base_adapter import BaseRestAdapter
        # Code 400 but unknown SAP code → let B1ValidationError fallback handle it
        BaseRestAdapter._raise_if_sql_error(400, "999", "some other error", None)


# ── run(method="GET") opt-in (P6) ─────────────────────────────────────────────

class TestSQLQueriesResourceRunGet:
    def _make_resource(self):
        adapter = FakeRestAdapter()
        resource = SQLQueriesResource(adapter)
        return resource, adapter

    def test_run_get_uses_get_method(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": "A001"}]
        adapter.register("GET", "SQLQueries('sql002')/List", _fake_list_response(rows).data)

        result = resource.run("sql002", method="GET")

        assert len(result) == 1
        assert adapter.calls[0]["method"] == "GET"

    def test_run_get_with_params_passes_as_query_params(self):
        resource, adapter = self._make_resource()
        rows = [{"DocEntry": 1}]
        adapter.register("GET", "SQLQueries('sql01')/List", _fake_list_response(rows).data)

        result = resource.run("sql01", method="GET", docEntry=5)

        assert len(result) == 1
        assert adapter.calls[0]["method"] == "GET"
        # params are forwarded as query params, not body
        assert adapter.calls[0]["data"] is None


# ── AsyncSQLQueriesResource (P1) ───────────────────────────────────────────────

class TestAsyncSQLQueriesResourceRun:
    def _make_resource(self):
        adapter = FakeAsyncRestAdapter()
        resource = AsyncSQLQueriesResource(adapter)
        return resource, adapter

    @pytest.mark.asyncio
    async def test_run_no_params_uses_post(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": "ITEM-001"}, {"ItemCode": "ITEM-002"}]
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(rows).data)

        result = await resource.run("sql002")

        assert len(result) == 2
        assert result[0]["ItemCode"] == "ITEM-001"
        assert result.sql_text == "select T0.\"ItemCode\" from \"OITM\" T0"
        assert result.has_more is False
        assert adapter.calls[0]["method"] == "POST"

    @pytest.mark.asyncio
    async def test_run_with_params_encodes_body(self):
        resource, adapter = self._make_resource()
        rows = [{"DocEntry": 1}]
        adapter.register("POST", "SQLQueries('sql01')/List", _fake_list_response(rows).data)

        result = await resource.run("sql01", docTotal=10.1, docPartner="C001")

        assert len(result) == 1
        posted_body = adapter.calls[0]["data"]
        assert posted_body == {"ParamList": "docTotal=10.1&docPartner='C001'"}

    @pytest.mark.asyncio
    async def test_run_page_size_sets_prefer_header(self):
        resource, adapter = self._make_resource()
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response([]).data)

        await resource.run("sql002", page_size=5)

        headers = adapter.calls[0]["headers"]
        assert headers == {"Prefer": "odata.maxpagesize=5"}

    @pytest.mark.asyncio
    async def test_run_returns_next_link_when_present(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": f"I{i:03d}"} for i in range(20)]
        next_link = "SQLQueries('sql002')/List?&$skip=20"
        adapter.register(
            "POST",
            "SQLQueries('sql002')/List",
            _fake_list_response(rows, next_link=next_link).data,
        )

        result = await resource.run("sql002")

        assert result.has_more is True
        assert result.next_link == next_link


class TestAsyncSQLQueriesResourceRunStream:
    def _make_resource(self):
        adapter = FakeAsyncRestAdapter()
        resource = AsyncSQLQueriesResource(adapter)
        return resource, adapter

    @pytest.mark.asyncio
    async def test_run_stream_single_page(self):
        resource, adapter = self._make_resource()
        rows = [{"ItemCode": "A001"}, {"ItemCode": "A002"}]
        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(rows).data)

        results = [row async for row in resource.run_stream("sql002")]

        assert results == rows
        assert len(adapter.calls) == 1

    @pytest.mark.asyncio
    async def test_run_stream_follows_next_link(self):
        resource, adapter = self._make_resource()
        page1_rows = [{"ItemCode": f"P1_{i}"} for i in range(3)]
        page2_rows = [{"ItemCode": f"P2_{i}"} for i in range(2)]
        next_link = "SQLQueries('sql002')/List?&$skip=3"

        adapter.register(
            "POST",
            "SQLQueries('sql002')/List",
            _fake_list_response(page1_rows, next_link=next_link).data,
        )
        adapter.register(
            "GET",
            "SQLQueries('sql002')/List",
            _fake_list_response(page2_rows).data,
        )

        results = [row async for row in resource.run_stream("sql002")]

        assert len(results) == 5
        assert results[0]["ItemCode"] == "P1_0"
        assert results[3]["ItemCode"] == "P2_0"
        assert len(adapter.calls) == 2

    @pytest.mark.asyncio
    async def test_run_stream_respects_max_pages(self):
        resource, adapter = self._make_resource()
        page_rows = [{"ItemCode": "X"}]
        next_link = "SQLQueries('sql002')/List?&$skip=1"

        adapter.register("POST", "SQLQueries('sql002')/List", _fake_list_response(page_rows, next_link).data)
        adapter.register("GET", "SQLQueries('sql002')/List", _fake_list_response(page_rows, next_link).data)

        results = [row async for row in resource.run_stream("sql002", max_pages=1)]

        assert len(results) == 1
        assert len(adapter.calls) == 1


# ── P2 — Adapter↔exception integration tests ──────────────────────────────────

class TestSQLQueriesResourceErrorPropagation:
    """Verify SQL exceptions raised by the adapter propagate out of run() / run_stream().

    The FakeRestAdapter raises pre-constructed exceptions via the ``raises=``
    argument to ``register()``.  This covers the propagation path that the real
    adapter follows: adapter raises → _action doesn't catch → run() re-raises.
    """

    def _make_sync(self):
        adapter = FakeRestAdapter()
        return SQLQueriesResource(adapter), adapter

    def _make_async(self):
        adapter = FakeAsyncRestAdapter()
        return AsyncSQLQueriesResource(adapter), adapter

    # ── sync ──────────────────────────────────────────────────────────────────

    def test_sync_run_propagates_702(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "POST", "SQLQueries('sql002')/List",
            raises=B1SqlNotAllowedError("Table blocked", sap_code="702"),
        )
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            resource.run("sql002")
        assert exc_info.value.sap_code == "702"

    def test_sync_run_propagates_703(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "POST", "SQLQueries('sql002')/List",
            raises=B1SqlNotAllowedError("Column blocked", sap_code="703"),
        )
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            resource.run("sql002")
        assert exc_info.value.sap_code == "703"

    def test_sync_run_propagates_704(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "POST", "SQLQueries('sql01')/List",
            raises=B1SqlParamError("Parameter error."),
        )
        with pytest.raises(B1SqlParamError) as exc_info:
            resource.run("sql01", docTotal=100.0)
        assert exc_info.value.sap_code == "704"

    def test_sync_run_stream_propagates_702(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "POST", "SQLQueries('sql002')/List",
            raises=B1SqlNotAllowedError("Table blocked", sap_code="702"),
        )
        with pytest.raises(B1SqlNotAllowedError):
            list(resource.run_stream("sql002"))

    # ── async ─────────────────────────────────────────────────────────────────

    @pytest.mark.asyncio
    async def test_async_run_propagates_702(self):
        resource, adapter = self._make_async()
        adapter.register(
            "POST", "SQLQueries('sql002')/List",
            raises=B1SqlNotAllowedError("Table blocked", sap_code="702"),
        )
        with pytest.raises(B1SqlNotAllowedError) as exc_info:
            await resource.run("sql002")
        assert exc_info.value.sap_code == "702"

    @pytest.mark.asyncio
    async def test_async_run_propagates_704(self):
        resource, adapter = self._make_async()
        adapter.register(
            "POST", "SQLQueries('sql01')/List",
            raises=B1SqlParamError("Parameter error."),
        )
        with pytest.raises(B1SqlParamError) as exc_info:
            await resource.run("sql01", docTotal=100.0)
        assert exc_info.value.sap_code == "704"

    @pytest.mark.asyncio
    async def test_async_run_stream_propagates_702(self):
        resource, adapter = self._make_async()
        adapter.register(
            "POST", "SQLQueries('sql002')/List",
            raises=B1SqlNotAllowedError("Table blocked", sap_code="702"),
        )
        with pytest.raises(B1SqlNotAllowedError):
            async for _ in resource.run_stream("sql002"):
                pass


# ── describe() ────────────────────────────────────────────────────────────────

def _fake_sql_query_entity(
    sql_code: str = "sql04",
    sql_name: str = "queryOnItem",
    sql_text: str = 'SELECT "ItemCode" FROM "OITM"',
    param_list: str | None = None,
) -> dict:
    return {
        "SqlCode": sql_code,
        "SqlName": sql_name,
        "SqlText": sql_text,
        "ParamList": param_list,
        "CreateDate": "2026-06-01",
        "UpdateDate": "2026-06-01",
    }


class TestSQLQueriesResourceDescribe:
    def _make_sync(self):
        adapter = FakeRestAdapter()
        return SQLQueriesResource(adapter), adapter

    def _make_async(self):
        adapter = FakeAsyncRestAdapter()
        return AsyncSQLQueriesResource(adapter), adapter

    def test_describe_no_params(self):
        resource, adapter = self._make_sync()
        adapter.register("GET", "SQLQueries('sql04')", _fake_sql_query_entity())

        info = resource.describe("sql04")

        assert isinstance(info, SQLQueryInfo)
        assert info.sql_code == "sql04"
        assert info.sql_name == "queryOnItem"
        assert info.params == []

    def test_describe_single_param(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list="docTotal"),
        )

        info = resource.describe("sql01")

        assert info.params == ["docTotal"]

    def test_describe_multiple_params(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list="docTotal,cardCode,docDate"),
        )

        info = resource.describe("sql01")

        assert info.params == ["docTotal", "cardCode", "docDate"]

    def test_describe_strips_whitespace_in_param_list(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list=" docTotal , cardCode "),
        )

        info = resource.describe("sql01")

        assert info.params == ["docTotal", "cardCode"]

    def test_describe_null_param_list_returns_empty(self):
        resource, adapter = self._make_sync()
        adapter.register(
            "GET", "SQLQueries('sql04')",
            _fake_sql_query_entity(param_list=None),
        )

        info = resource.describe("sql04")

        assert info.params == []

    def test_run_704_enriches_expected_params(self):
        resource, adapter = self._make_sync()
        # run() raises 704
        adapter.register(
            "POST", "SQLQueries('sql01')/List",
            raises=B1SqlParamError("Parameter error."),
        )
        # describe() GET called automatically on 704
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list="docTotal,cardCode"),
        )

        with pytest.raises(B1SqlParamError) as exc_info:
            resource.run("sql01", wrong_param=1)

        assert exc_info.value.expected_params == ["docTotal", "cardCode"]

    @pytest.mark.asyncio
    async def test_async_describe_single_param(self):
        resource, adapter = self._make_async()
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list="docTotal"),
        )

        info = await resource.describe("sql01")

        assert info.params == ["docTotal"]

    @pytest.mark.asyncio
    async def test_async_run_704_enriches_expected_params(self):
        resource, adapter = self._make_async()
        adapter.register(
            "POST", "SQLQueries('sql01')/List",
            raises=B1SqlParamError("Parameter error."),
        )
        adapter.register(
            "GET", "SQLQueries('sql01')",
            _fake_sql_query_entity(param_list="docTotal"),
        )

        with pytest.raises(B1SqlParamError) as exc_info:
            await resource.run("sql01", wrong_param=1)

        assert exc_info.value.expected_params == ["docTotal"]
