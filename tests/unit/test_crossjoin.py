"""Unit tests for CrossJoinQueryBuilder and AsyncCrossJoinQueryBuilder."""
from unittest.mock import AsyncMock, MagicMock

import pytest

from b1sl.b1sl.resources.crossjoin import (
    AsyncCrossJoinQueryBuilder,
    CrossJoinQueryBuilder,
)


def _mock_adapter(pages: list[dict]) -> MagicMock:
    """Build a mock sync adapter that yields successive pages."""
    adapter = MagicMock()
    responses = []
    for i, page in enumerate(pages):
        r = MagicMock()
        r.data = page
        r.next_link = None if i == len(pages) - 1 else f"http://sap/b1s/v1/$crossjoin?$skip={i+1}"
        responses.append(r)
    adapter.get.side_effect = responses
    return adapter


def _mock_async_adapter(pages: list[dict]) -> MagicMock:
    adapter = MagicMock()
    responses = []
    for i, page in enumerate(pages):
        r = MagicMock()
        r.data = page
        r.next_link = None if i == len(pages) - 1 else f"http://sap/b1s/v1/$crossjoin?$skip={i+1}"
        responses.append(r)
    adapter.get = AsyncMock(side_effect=responses)
    return adapter


# ── Construction ──────────────────────────────────────────────────────────────

def test_requires_at_least_two_entities():
    adapter = MagicMock()
    with pytest.raises(ValueError, match="at least 2"):
        CrossJoinQueryBuilder(adapter, "Orders")


def test_async_requires_at_least_two_entities():
    adapter = MagicMock()
    with pytest.raises(ValueError, match="at least 2"):
        AsyncCrossJoinQueryBuilder(adapter, "Orders")


def test_path_two_entities():
    adapter = MagicMock()
    qb = CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
    assert qb._path == "$crossjoin(Orders,BusinessPartners)"


def test_path_three_entities():
    adapter = MagicMock()
    qb = CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners", "Activities")
    assert qb._path == "$crossjoin(Orders,BusinessPartners,Activities)"


# ── Validation ────────────────────────────────────────────────────────────────

def test_bare_crossjoin_raises_valueerror():
    adapter = MagicMock()
    qb = CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
    with pytest.raises(ValueError, match="bare crossjoin"):
        qb.execute()


def test_bare_crossjoin_async_raises_valueerror():
    adapter = MagicMock()
    qb = AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
    with pytest.raises(ValueError, match="bare crossjoin"):
        import asyncio
        asyncio.run(qb.execute())


# ── $expand param construction ────────────────────────────────────────────────

def test_expand_dict_to_param():
    adapter = _mock_adapter([{"value": []}])
    qb = CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
    qb.expand({"Orders": ["DocEntry", "DocNum"], "BusinessPartners": ["CardCode"]})
    qb.execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$expand"] == "Orders($select=DocEntry,DocNum),BusinessPartners($select=CardCode)"


def test_expand_arithmetic_passthrough():
    """Calculated columns (mul/sub/add/div) are verbatim strings in the select list."""
    adapter = _mock_adapter([{"value": []}])
    qb = CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
    qb.expand({"Orders": ["DocEntry mul (DocNum sub 1) as DocSeq"], "BusinessPartners": ["CardCode", "CardName"]})
    qb.execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert "DocEntry mul (DocNum sub 1) as DocSeq" in params["$expand"]
    assert "CardCode,CardName" in params["$expand"]


# ── $filter ───────────────────────────────────────────────────────────────────

def test_filter_navigation_path():
    adapter = _mock_adapter([{"value": []}])
    qb = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry"], "BusinessPartners": ["CardCode"]})
        .filter("Orders/CardCode eq BusinessPartners/CardCode and Orders/DocNum le 3")
    )
    qb.execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$filter"] == "Orders/CardCode eq BusinessPartners/CardCode and Orders/DocNum le 3"


def test_filter_with_string_function():
    adapter = _mock_adapter([{"value": []}])
    qb = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry"], "BusinessPartners": ["CardCode"]})
        .filter("startswith(BusinessPartners/CardCode,'c00')")
    )
    qb.execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert "$filter" in params


# ── $apply aggregation ────────────────────────────────────────────────────────

def test_apply_no_expand_is_valid():
    """$apply alone satisfies the validation rule (no $expand needed)."""
    adapter = _mock_adapter([{"value": [{"BusinessPartners": {"CardCode": "c001"}, "Orders": {"MaxDocNum": 5}}]}])
    expr = (
        "filter(Orders/CardCode eq BusinessPartners/CardCode)"
        "/groupby((BusinessPartners/CardCode),aggregate(Orders(DocNum with max as MaxDocNum)))"
    )
    rows = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .apply(expr)
        .execute()
    )
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$apply"] == expr
    assert len(rows) == 1
    assert rows[0]["BusinessPartners"]["CardCode"] == "c001"


def test_apply_count_variant():
    adapter = _mock_adapter([{"value": [{"BusinessPartners": {"CardCode": "c001"}, "Orders": {"CountDocEntry": 3}}]}])
    expr = (
        "filter(Orders/CardCode eq BusinessPartners/CardCode)"
        "/groupby((BusinessPartners/CardCode),aggregate(Orders/$count as CountDocEntry))"
    )
    CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners").apply(expr).execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$apply"] == expr


# ── ordering / top / skip ─────────────────────────────────────────────────────

def test_orderby_asc():
    adapter = _mock_adapter([{"value": []}])
    CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners").expand({"Orders": ["DocNum"]}).orderby("Orders/DocNum").execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$orderby"] == "Orders/DocNum"


def test_orderby_desc():
    adapter = _mock_adapter([{"value": []}])
    CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners").expand({"Orders": ["DocNum"]}).orderby("Orders/DocNum", desc=True).execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$orderby"] == "Orders/DocNum desc"


def test_top_and_skip():
    adapter = _mock_adapter([{"value": []}])
    (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry"]})
        .top(10)
        .skip(20)
        .execute()
    )
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$top"] == "10"
    assert params["$skip"] == "20"


# ── execute return type ───────────────────────────────────────────────────────

def test_execute_returns_list_of_dicts():
    row = {"Orders": {"DocEntry": 2, "DocNum": 1}, "BusinessPartners": {"CardCode": "c001"}}
    adapter = _mock_adapter([{"value": [row]}])
    rows = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry", "DocNum"], "BusinessPartners": ["CardCode"]})
        .filter("Orders/CardCode eq BusinessPartners/CardCode")
        .execute()
    )
    assert isinstance(rows, list)
    assert rows[0] == row
    assert isinstance(rows[0], dict)


def test_execute_empty_result():
    adapter = _mock_adapter([{"value": []}])
    rows = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry"]})
        .execute()
    )
    assert rows == []


# ── stream / pagination ───────────────────────────────────────────────────────

def test_stream_follows_next_link():
    page1 = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
    page2 = {"value": [{"Orders": {"DocNum": 3}}]}
    adapter = _mock_adapter([page1, page2])
    rows = list(
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .stream()
    )
    assert len(rows) == 3
    assert adapter.get.call_count == 2


def test_stream_max_pages():
    page1 = {"value": [{"Orders": {"DocNum": 1}}]}
    page2 = {"value": [{"Orders": {"DocNum": 2}}]}
    page3 = {"value": [{"Orders": {"DocNum": 3}}]}
    adapter = _mock_adapter([page1, page2, page3])
    rows = list(
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .stream(max_pages=2)
    )
    assert len(rows) == 2
    assert adapter.get.call_count == 2


def test_stream_top_cap():
    page1 = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}, {"Orders": {"DocNum": 3}}]}
    adapter = _mock_adapter([page1])
    rows = list(
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .top(2)
        .stream()
    )
    assert len(rows) == 2


def test_stream_does_not_forward_top_to_sap():
    """crossjoin .top(N) must be enforced client-side, not forwarded to SAP. The
    mock simulates a strict SAP that drops the nextLink under any $top — proving
    the stream still pages correctly because we strip $top from the request."""
    def fake_get(path, ep_params=None, headers=None, data=None):
        ep_params = ep_params or {}
        r = MagicMock()
        if "$top" in ep_params:
            r.data = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
            r.next_link = None
            return r
        skip = int(ep_params.get("$skip", 0))
        if skip == 0:
            r.data = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
            r.next_link = "http://sap/b1s/v1/$crossjoin?$skip=2"
        else:
            r.data = {"value": [{"Orders": {"DocNum": 3}}, {"Orders": {"DocNum": 4}}]}
            r.next_link = None
        return r

    adapter = MagicMock()
    adapter.get.side_effect = fake_get
    rows = list(
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .top(3)
        .stream(page_size=2)
    )

    assert [r["Orders"]["DocNum"] for r in rows] == [1, 2, 3]
    for call in adapter.get.call_args_list:
        assert "$top" not in (call.kwargs.get("ep_params") or {})


def test_page_size_sets_header_on_execute_and_stream():
    adapter = _mock_adapter([{"value": []}])
    qb = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .page_size(50)
    )
    qb.execute()
    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "50"}


def test_stream_page_size_arg_overrides_builder():
    adapter = _mock_adapter([{"value": [{"Orders": {"DocNum": 1}}]}])
    list(
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .page_size(50)
        .stream(page_size=99)
    )
    assert adapter.get.call_args.kwargs["headers"] == {"B1S-PageSize": "99"}


# ── first() ───────────────────────────────────────────────────────────────────

def test_first_returns_first_row():
    row = {"Orders": {"DocNum": 42}}
    adapter = _mock_adapter([{"value": [row, {"Orders": {"DocNum": 99}}]}])
    result = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result == row


def test_first_returns_none_when_empty():
    adapter = _mock_adapter([{"value": []}])
    result = (
        CrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result is None


# ── correct URL path is used ──────────────────────────────────────────────────

def test_get_called_with_correct_path():
    adapter = _mock_adapter([{"value": []}])
    CrossJoinQueryBuilder(adapter, "SalesOpportunities", "BusinessPartners").expand({"SalesOpportunities": ["CardCode"]}).execute()
    url_arg = adapter.get.call_args[0][0]
    assert url_arg == "$crossjoin(SalesOpportunities,BusinessPartners)"


# ── async builder mirrors ─────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_execute_returns_list_of_dicts():
    row = {"Orders": {"DocEntry": 2}, "BusinessPartners": {"CardCode": "c001"}}
    adapter = _mock_async_adapter([{"value": [row]}])
    rows = await (
        AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocEntry"], "BusinessPartners": ["CardCode"]})
        .filter("Orders/CardCode eq BusinessPartners/CardCode")
        .execute()
    )
    assert rows == [row]


@pytest.mark.asyncio
async def test_async_stream_follows_next_link():
    page1 = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
    page2 = {"value": [{"Orders": {"DocNum": 3}}]}
    adapter = _mock_async_adapter([page1, page2])
    rows = []
    async for row in (
        AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .stream()
    ):
        rows.append(row)
    assert len(rows) == 3
    assert adapter.get.call_count == 2


@pytest.mark.asyncio
async def test_async_stream_does_not_forward_top_to_sap():
    """Async parity: crossjoin $top is enforced client-side, never sent to SAP."""
    async def fake_get(path, ep_params=None, headers=None, data=None):
        ep_params = ep_params or {}
        r = MagicMock()
        if "$top" in ep_params:
            r.data = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
            r.next_link = None
            return r
        skip = int(ep_params.get("$skip", 0))
        if skip == 0:
            r.data = {"value": [{"Orders": {"DocNum": 1}}, {"Orders": {"DocNum": 2}}]}
            r.next_link = "http://sap/b1s/v1/$crossjoin?$skip=2"
        else:
            r.data = {"value": [{"Orders": {"DocNum": 3}}, {"Orders": {"DocNum": 4}}]}
            r.next_link = None
        return r

    adapter = MagicMock()
    adapter.get = AsyncMock(side_effect=fake_get)
    rows = []
    async for row in (
        AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .top(3)
        .stream(page_size=2)
    ):
        rows.append(row)

    assert [r["Orders"]["DocNum"] for r in rows] == [1, 2, 3]
    for call in adapter.get.call_args_list:
        assert "$top" not in (call.kwargs.get("ep_params") or {})


@pytest.mark.asyncio
async def test_async_apply_aggregation():
    result_row = {"BusinessPartners": {"CardCode": "c001"}, "Orders": {"MaxDocNum": 5}}
    adapter = _mock_async_adapter([{"value": [result_row]}])
    expr = (
        "filter(Orders/CardCode eq BusinessPartners/CardCode)"
        "/groupby((BusinessPartners/CardCode),aggregate(Orders(DocNum with max as MaxDocNum)))"
    )
    rows = await AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners").apply(expr).execute()
    params = adapter.get.call_args[1]["ep_params"]
    assert params["$apply"] == expr
    assert rows[0]["Orders"]["MaxDocNum"] == 5


@pytest.mark.asyncio
async def test_async_first():
    row = {"Orders": {"DocNum": 1}}
    adapter = _mock_async_adapter([{"value": [row]}])
    result = await (
        AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result == row


@pytest.mark.asyncio
async def test_async_bare_crossjoin_raises():
    adapter = MagicMock()
    adapter.get = AsyncMock()
    with pytest.raises(ValueError, match="bare crossjoin"):
        await AsyncCrossJoinQueryBuilder(adapter, "Orders", "BusinessPartners").execute()


# ── QueryServiceBuilder ───────────────────────────────────────────────────────

def _mock_post_adapter(response_data: dict | str) -> MagicMock:
    adapter = MagicMock()
    r = MagicMock()
    r.data = response_data
    adapter.post.return_value = r
    return adapter


def _mock_post_async_adapter(response_data: dict) -> MagicMock:
    adapter = MagicMock()
    r = MagicMock()
    r.data = response_data
    adapter.post = AsyncMock(return_value=r)
    return adapter


def test_query_service_requires_non_empty_path():
    adapter = MagicMock()
    with pytest.raises(ValueError, match="non-empty"):
        from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
        QueryServiceBuilder(adapter, "")


def test_query_service_bare_raises_valueerror():
    adapter = MagicMock()
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    qs = QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
    with pytest.raises(ValueError, match="field projection"):
        qs.execute()


def test_query_service_post_endpoint():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry"], "Orders/DocumentLines": ["ItemCode"]})
        .execute()
    )
    endpoint = adapter.post.call_args[0][0]
    assert endpoint == "QueryService_PostQuery"


def test_query_service_post_body_query_path():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    query_path = "$crossjoin(Orders,Orders/DocumentLines)"
    (
        QueryServiceBuilder(adapter, query_path)
        .expand({"Orders": ["DocEntry"], "Orders/DocumentLines": ["ItemCode"]})
        .execute()
    )
    body = adapter.post.call_args[1]["data"]
    assert body["QueryPath"] == query_path


def test_query_service_post_body_query_option_expand():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry", "DocNum"], "Orders/DocumentLines": ["ItemCode", "LineNum"]})
        .execute()
    )
    body = adapter.post.call_args[1]["data"]
    query_option = body["QueryOption"]
    assert "$expand=Orders($select=DocEntry,DocNum),Orders/DocumentLines($select=ItemCode,LineNum)" in query_option


def test_query_service_post_body_query_option_filter():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    expr = "Orders/DocEntry eq Orders/DocumentLines/DocEntry and Orders/DocumentLines/ItemCode eq 'WIDGET'"
    (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry"]})
        .filter(expr)
        .execute()
    )
    body = adapter.post.call_args[1]["data"]
    assert f"$filter={expr}" in body["QueryOption"]


def test_query_service_query_option_no_url_encoding():
    """QueryOption must NOT percent-encode $, (, ), / — SAP expects raw string."""
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders/DocumentLines": ["ItemCode"]})
        .execute()
    )
    body = adapter.post.call_args[1]["data"]
    query_option = body["QueryOption"]
    assert "%" not in query_option, f"QueryOption must not be URL-encoded: {query_option!r}"
    assert "$expand" in query_option
    assert "($select=" in query_option


def test_query_service_top_skip_in_query_option():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry"]})
        .top(10)
        .skip(5)
        .execute()
    )
    query_option = adapter.post.call_args[1]["data"]["QueryOption"]
    assert "$top=10" in query_option
    assert "$skip=5" in query_option


def test_query_service_apply_no_expand():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": [{"Orders": {"DocNum": 3}}]})
    expr = "filter(Orders/DocEntry eq Orders/DocumentLines/DocEntry)/groupby((Orders/DocNum),aggregate(Orders/$count as Lines))"
    rows = (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .apply(expr)
        .execute()
    )
    query_option = adapter.post.call_args[1]["data"]["QueryOption"]
    assert f"$apply={expr}" in query_option
    assert len(rows) == 1


def test_query_service_execute_returns_list_of_dicts():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    row = {"Orders": {"DocEntry": 3, "DocNum": 1}, "Orders/DocumentLines": {"ItemCode": "W1", "LineNum": 0}}
    adapter = _mock_post_adapter({"value": [row]})
    rows = (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry"], "Orders/DocumentLines": ["ItemCode"]})
        .execute()
    )
    assert rows == [row]
    assert isinstance(rows[0], dict)


def test_query_service_handles_text_plain_double_encoded():
    """Guard: if SAP returns a JSON-encoded string, still parse correctly."""
    import json

    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    inner = {"value": [{"Orders": {"DocNum": 1}}]}
    adapter = _mock_post_adapter(json.dumps(inner))  # simulate text/plain string
    rows = (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocNum"]})
        .execute()
    )
    assert len(rows) == 1
    assert rows[0]["Orders"]["DocNum"] == 1


def test_query_service_first():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    row = {"Orders": {"DocNum": 42}}
    adapter = _mock_post_adapter({"value": [row, {"Orders": {"DocNum": 99}}]})
    result = (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result == row


def test_query_service_first_none_when_empty():
    from b1sl.b1sl.resources.crossjoin import QueryServiceBuilder
    adapter = _mock_post_adapter({"value": []})
    result = (
        QueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result is None


# ── Async QueryService ────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_async_query_service_execute():
    from b1sl.b1sl.resources.crossjoin import AsyncQueryServiceBuilder
    row = {"Orders": {"DocEntry": 5}, "Orders/DocumentLines": {"ItemCode": "X1"}}
    adapter = _mock_post_async_adapter({"value": [row]})
    rows = await (
        AsyncQueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocEntry"], "Orders/DocumentLines": ["ItemCode"]})
        .filter("Orders/DocEntry eq Orders/DocumentLines/DocEntry")
        .execute()
    )
    assert rows == [row]
    endpoint = adapter.post.call_args[0][0]
    assert endpoint == "QueryService_PostQuery"


@pytest.mark.asyncio
async def test_async_query_service_bare_raises():
    from b1sl.b1sl.resources.crossjoin import AsyncQueryServiceBuilder
    adapter = MagicMock()
    adapter.post = AsyncMock()
    with pytest.raises(ValueError, match="field projection"):
        await AsyncQueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)").execute()


@pytest.mark.asyncio
async def test_async_query_service_first():
    from b1sl.b1sl.resources.crossjoin import AsyncQueryServiceBuilder
    row = {"Orders": {"DocNum": 7}}
    adapter = _mock_post_async_adapter({"value": [row]})
    result = await (
        AsyncQueryServiceBuilder(adapter, "$crossjoin(Orders,Orders/DocumentLines)")
        .expand({"Orders": ["DocNum"]})
        .first()
    )
    assert result == row
