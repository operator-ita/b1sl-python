"""Unit tests for b1sl.contrib.mcp — schemas and formatters.

All tests are pure unit tests (no network, no SAP connection).
"""


from b1sl.b1sl.exceptions.exceptions import (
    B1NotFoundError,
    B1SqlNotAllowedError,
    B1SqlParamError,
    B1SqlSyntaxError,
)
from b1sl.b1sl.resources.sql_queries import (
    DEFAULT_ACCESSIBLE_TABLES,
    KNOWN_INACCESSIBLE_PATTERNS,
    SQLQueryInfo,
    SQLRunResult,
)
from b1sl.contrib.mcp.formatters import format_sql_error, format_sql_result
from b1sl.contrib.mcp.grammar import (
    SUPPORTED_FUNCTIONS,
    SUPPORTED_KEYWORDS,
    UNSUPPORTED_COMMON,
    sql_grammar_system_prompt,
)
from b1sl.contrib.mcp.schemas import (
    accessible_tables_description,
    sql_query_input_schema,
    sql_query_tool_definition,
)

# ── Helpers ────────────────────────────────────────────────────────────────────

def _make_info(
    sql_code: str = "sql04",
    sql_name: str = "queryOnItem",
    sql_text: str = 'SELECT "ItemCode" FROM "OITM"',
    params: list[str] | None = None,
) -> SQLQueryInfo:
    return SQLQueryInfo(
        sql_code=sql_code,
        sql_name=sql_name,
        sql_text=sql_text,
        params=params or [],
    )


def _make_result(rows: list[dict], next_link: str | None = None) -> SQLRunResult:
    return SQLRunResult(rows=rows, sql_text="SELECT ...", next_link=next_link)


# ── sql_query_input_schema ─────────────────────────────────────────────────────

class TestSqlQueryInputSchema:
    def test_no_params_has_no_required(self):
        schema = sql_query_input_schema([])
        assert "required" not in schema
        assert "page_size" in schema["properties"]
        assert "max_pages" in schema["properties"]

    def test_params_appear_in_properties(self):
        schema = sql_query_input_schema(["docTotal", "cardCode"])
        assert "docTotal" in schema["properties"]
        assert "cardCode" in schema["properties"]

    def test_params_are_required(self):
        schema = sql_query_input_schema(["docTotal", "cardCode"])
        assert schema["required"] == ["docTotal", "cardCode"]

    def test_pagination_controls_not_required(self):
        schema = sql_query_input_schema(["docTotal"])
        assert "page_size" not in schema.get("required", [])
        assert "max_pages" not in schema.get("required", [])

    def test_param_type_allows_multiple(self):
        schema = sql_query_input_schema(["p1"])
        assert schema["properties"]["p1"]["type"] == ["string", "number", "boolean"]


# ── sql_query_tool_definition ──────────────────────────────────────────────────

class TestSqlQueryToolDefinition:
    def test_name_prefixed_with_sql_(self):
        tool = sql_query_tool_definition(_make_info(sql_code="sql04"))
        assert tool["name"] == "sql_sql04"

    def test_hyphens_replaced_in_name(self):
        tool = sql_query_tool_definition(_make_info(sql_code="my-query.v2"))
        assert tool["name"] == "sql_my_query_v2"

    def test_description_includes_sql_name(self):
        tool = sql_query_tool_definition(_make_info(sql_name="Items Report"))
        assert "Items Report" in tool["description"]

    def test_description_includes_param_hints(self):
        info = _make_info(params=["docTotal", "cardCode"])
        tool = sql_query_tool_definition(info)
        assert ":docTotal" in tool["description"]
        assert ":cardCode" in tool["description"]

    def test_description_includes_sql_snippet(self):
        tool = sql_query_tool_definition(_make_info(sql_text='SELECT "ItemCode" FROM "OITM"'))
        assert "ItemCode" in tool["description"]

    def test_long_sql_is_truncated(self):
        long_sql = "SELECT " + "x" * 200 + " FROM OITM"
        tool = sql_query_tool_definition(_make_info(sql_text=long_sql))
        assert tool["description"].endswith("...")

    def test_input_schema_is_included(self):
        tool = sql_query_tool_definition(_make_info(params=["docTotal"]))
        assert "inputSchema" in tool
        assert "docTotal" in tool["inputSchema"]["properties"]

    def test_no_params_tool_has_no_required(self):
        tool = sql_query_tool_definition(_make_info(params=[]))
        assert "required" not in tool["inputSchema"]


# ── format_sql_result ──────────────────────────────────────────────────────────

class TestFormatSqlResult:
    def test_empty_result(self):
        result = _make_result([])
        text = format_sql_result(result)
        assert "No rows returned" in text

    def test_table_headers(self):
        result = _make_result([{"ItemCode": "A001", "OnHand": 10.0}])
        text = format_sql_result(result)
        assert "ItemCode" in text
        assert "OnHand" in text

    def test_table_values(self):
        result = _make_result([{"ItemCode": "A001"}])
        text = format_sql_result(result)
        assert "A001" in text

    def test_title_included(self):
        result = _make_result([{"X": 1}])
        text = format_sql_result(result, title="My Report")
        assert "## My Report" in text

    def test_truncation_noted(self):
        rows = [{"X": i} for i in range(10)]
        result = _make_result(rows)
        text = format_sql_result(result, max_rows=3)
        assert "omitted" in text
        assert "7" in text

    def test_has_more_noted(self):
        result = _make_result([{"X": 1}], next_link="SQLQueries('q')/List?$skip=20")
        text = format_sql_result(result)
        assert "More pages" in text

    def test_no_has_more_message_when_single_page(self):
        result = _make_result([{"X": 1}])
        text = format_sql_result(result)
        assert "More pages" not in text


# ── format_sql_error ───────────────────────────────────────────────────────────

class TestFormatSqlError:
    def test_701_mentions_error_code(self):
        exc = B1SqlSyntaxError("Invalid SQL syntax: select * from ORDR, Cannot support asterisk(*)")
        text = format_sql_error(exc)
        assert "701" in text

    def test_701_mentions_select_star(self):
        exc = B1SqlSyntaxError("Invalid SQL syntax: asterisk not allowed")
        text = format_sql_error(exc)
        assert "SELECT *" in text

    def test_701_mentions_dml(self):
        exc = B1SqlSyntaxError("Invalid SQL syntax: UPDATE not expected")
        text = format_sql_error(exc)
        assert "UPDATE" in text or "DML" in text

    def test_701_mentions_unsupported_function(self):
        exc = B1SqlSyntaxError("Cannot support this function: length")
        text = format_sql_error(exc)
        assert "CASE WHEN" in text or "UNSUPPORTED_COMMON" in text or "Unsupported function" in text

    def test_701_includes_sql_code_context(self):
        exc = B1SqlSyntaxError("Invalid SQL syntax: ...")
        text = format_sql_error(exc, sql_code="sql01")
        assert "sql01" in text

    def test_702_mentions_allowlist(self):
        exc = B1SqlNotAllowedError("Table blocked", sap_code="702")
        text = format_sql_error(exc)
        assert "allowlist" in text
        assert "702" in text

    def test_702_lists_common_accessible_tables(self):
        exc = B1SqlNotAllowedError("Table blocked", sap_code="702")
        text = format_sql_error(exc)
        assert "OITM" in text
        assert "ORDR" in text
        assert "OCRD" in text

    def test_702_references_default_accessible_tables_constant(self):
        exc = B1SqlNotAllowedError("Table blocked", sap_code="702")
        text = format_sql_error(exc)
        assert "DEFAULT_ACCESSIBLE_TABLES" in text

    def test_702_sbocommon_gives_specific_hint(self):
        exc = B1SqlNotAllowedError("Table 'SBOCOMMON' not accessible", sap_code="702")
        text = format_sql_error(exc)
        assert "SBOCOMMON" in text
        assert "never" in text.lower() or "not queryable" in text.lower()

    def test_702_log_table_shows_generic_702_message(self):
        # No A-prefix heuristic — too fragile (ADM1, ATC1 are accessible and start with A).
        # AITM gets the same generic 702 message as any other blocked table.
        exc = B1SqlNotAllowedError("Table 'AITM' not accessible", sap_code="702")
        text = format_sql_error(exc)
        assert "702" in text
        assert "allowlist" in text

    def test_703_mentions_column_exclude(self):
        exc = B1SqlNotAllowedError("Column blocked", sap_code="703")
        text = format_sql_error(exc)
        assert "ColumnExcludeList" in text or "column" in text.lower()

    def test_704_includes_sql_code_context(self):
        exc = B1SqlParamError("Parameter error.")
        text = format_sql_error(exc, sql_code="sql04")
        assert "sql04" in text

    def test_704_lists_expected_params_from_exception(self):
        exc = B1SqlParamError("Parameter error.", expected_params=["docTotal", "cardCode"])
        text = format_sql_error(exc)
        assert ":docTotal" in text
        assert ":cardCode" in text

    def test_704_lists_expected_params_from_describe(self):
        exc = B1SqlParamError("Parameter error.")
        info = _make_info(params=["docTotal"])
        text = format_sql_error(exc, describe_result=info)
        assert ":docTotal" in text

    def test_not_found_mentions_sql_code(self):
        exc = B1NotFoundError("No matching records")
        text = format_sql_error(exc, sql_code="sql04")
        assert "sql04" in text
        assert "not found" in text.lower()

    def test_generic_exception_passthrough(self):
        exc = ValueError("something went wrong")
        text = format_sql_error(exc, sql_code="sql04")
        assert "sql04" in text
        assert "something went wrong" in text


# ── DEFAULT_ACCESSIBLE_TABLES ──────────────────────────────────────────────────

class TestDefaultAccessibleTables:
    def test_is_frozenset(self):
        assert isinstance(DEFAULT_ACCESSIBLE_TABLES, frozenset)

    def test_contains_core_inventory_tables(self):
        for table in ("OITM", "OITW", "OIBQ"):
            assert table in DEFAULT_ACCESSIBLE_TABLES

    def test_contains_sales_tables(self):
        for table in ("ORDR", "OINV", "ODLN", "OQUT"):
            assert table in DEFAULT_ACCESSIBLE_TABLES

    def test_contains_numbered_line_tables(self):
        # RDR1-14, INV1-14, etc.
        for i in range(1, 15):
            assert f"RDR{i}" in DEFAULT_ACCESSIBLE_TABLES
            assert f"INV{i}" in DEFAULT_ACCESSIBLE_TABLES

    def test_contains_gl_tables(self):
        assert "OJDT" in DEFAULT_ACCESSIBLE_TABLES
        assert "JDT1" in DEFAULT_ACCESSIBLE_TABLES

    def test_does_not_contain_restricted_tables(self):
        # OSRI (serial numbers by item) is not in the default allowlist
        assert "OSRI" not in DEFAULT_ACCESSIBLE_TABLES

    def test_does_not_contain_log_tables(self):
        # Audit log tables (A-prefixed) are always inaccessible
        for log_table in ("AITM", "ACRD", "AINV", "AORDR"):
            assert log_table not in DEFAULT_ACCESSIBLE_TABLES, \
                f"LOG table {log_table} should not be in DEFAULT_ACCESSIBLE_TABLES"

    def test_contains_over_100_tables(self):
        # With 1-14 line tables for 18 doc families = 252 + parent tables
        assert len(DEFAULT_ACCESSIBLE_TABLES) > 100


class TestKnownInaccessiblePatterns:
    def test_is_dict(self):
        assert isinstance(KNOWN_INACCESSIBLE_PATTERNS, dict)

    def test_contains_log_tables_key(self):
        assert "log_tables" in KNOWN_INACCESSIBLE_PATTERNS

    def test_contains_sbocommon_key(self):
        assert "sbocommon" in KNOWN_INACCESSIBLE_PATTERNS

    def test_contains_udt_key(self):
        assert "udt_old_tenants" in KNOWN_INACCESSIBLE_PATTERNS

    def test_descriptions_are_strings(self):
        for key, val in KNOWN_INACCESSIBLE_PATTERNS.items():
            assert isinstance(val, str), f"Expected str for key '{key}', got {type(val)}"


# ── accessible_tables_description ─────────────────────────────────────────────

class TestAccessibleTablesDescription:
    def test_returns_string(self):
        text = accessible_tables_description()
        assert isinstance(text, str)

    def test_contains_key_tables(self):
        text = accessible_tables_description()
        assert "OITM" in text
        assert "ORDR" in text

    def test_contains_category_headers(self):
        text = accessible_tables_description()
        assert "Items" in text or "Inventory" in text
        assert "Sales" in text

    def test_references_full_constant(self):
        text = accessible_tables_description()
        assert "DEFAULT_ACCESSIBLE_TABLES" in text


# ── Grammar constants ──────────────────────────────────────────────────────────

class TestGrammarConstants:
    def test_supported_keywords_is_frozenset(self):
        assert isinstance(SUPPORTED_KEYWORDS, frozenset)

    def test_supported_keywords_contains_core(self):
        for kw in ("SELECT", "FROM", "WHERE", "ORDER BY", "GROUP BY", "INNER JOIN"):
            assert kw in SUPPORTED_KEYWORDS

    def test_supported_functions_is_frozenset(self):
        assert isinstance(SUPPORTED_FUNCTIONS, frozenset)

    def test_supported_functions_contains_aggregates(self):
        for fn in ("SUM", "AVG", "MAX", "MIN", "COUNT"):
            assert fn in SUPPORTED_FUNCTIONS

    def test_supported_functions_contains_null_handlers(self):
        assert "ISNULL" in SUPPORTED_FUNCTIONS
        assert "IFNULL" in SUPPORTED_FUNCTIONS

    def test_unsupported_common_is_frozenset(self):
        assert isinstance(UNSUPPORTED_COMMON, frozenset)

    def test_unsupported_contains_case_when(self):
        assert "CASE WHEN" in UNSUPPORTED_COMMON

    def test_unsupported_contains_coalesce(self):
        assert "COALESCE" in UNSUPPORTED_COMMON

    def test_unsupported_contains_cte(self):
        assert "WITH" in UNSUPPORTED_COMMON

    def test_unsupported_contains_window_functions(self):
        for fn in ("OVER", "PARTITION BY", "ROW_NUMBER", "RANK"):
            assert fn in UNSUPPORTED_COMMON

    def test_unsupported_contains_dml(self):
        for stmt in ("UPDATE", "INSERT", "DELETE", "ALTER", "DROP", "TRUNCATE"):
            assert stmt in UNSUPPORTED_COMMON, f"{stmt} missing from UNSUPPORTED_COMMON"

    def test_no_overlap_supported_unsupported_keywords(self):
        # Sanity: a keyword cannot be both supported and unsupported
        overlap = SUPPORTED_KEYWORDS & UNSUPPORTED_COMMON
        assert not overlap, f"Overlap found: {overlap}"

    def test_no_overlap_supported_functions_unsupported(self):
        overlap = SUPPORTED_FUNCTIONS & UNSUPPORTED_COMMON
        assert not overlap, f"Overlap found: {overlap}"


# ── sql_grammar_system_prompt ──────────────────────────────────────────────────

class TestSqlGrammarSystemPrompt:
    def test_returns_string(self):
        text = sql_grammar_system_prompt()
        assert isinstance(text, str)

    def test_mentions_supported_keywords(self):
        text = sql_grammar_system_prompt()
        assert "SELECT" in text
        assert "GROUP BY" in text
        assert "UNION" in text

    def test_mentions_supported_functions(self):
        text = sql_grammar_system_prompt()
        assert "ISNULL" in text
        assert "IFNULL" in text
        assert "SUM" in text

    def test_warns_about_case_when(self):
        text = sql_grammar_system_prompt()
        assert "CASE WHEN" in text

    def test_warns_about_coalesce(self):
        text = sql_grammar_system_prompt()
        assert "COALESCE" in text

    def test_warns_about_cte(self):
        text = sql_grammar_system_prompt()
        assert "CTE" in text or "WITH" in text

    def test_mentions_param_syntax(self):
        text = sql_grammar_system_prompt()
        assert ":paramName" in text or ":docTotal" in text

    def test_includes_tables_by_default(self):
        text = sql_grammar_system_prompt()
        assert "OITM" in text
        assert "DEFAULT_ACCESSIBLE_TABLES" in text

    def test_exclude_tables_when_flag_false(self):
        text = sql_grammar_system_prompt(include_tables=False)
        # The table-list section should be absent; DEFAULT_ACCESSIBLE_TABLES
        # is the unique marker for that section (OITM may appear in examples)
        assert "DEFAULT_ACCESSIBLE_TABLES" not in text
        assert "Accessible tables" not in text

    def test_mentions_normalisation_rule(self):
        text = sql_grammar_system_prompt()
        # SL auto-normalises identifiers
        assert "normaliz" in text.lower() or "HANA" in text

    def test_warns_about_select_star(self):
        text = sql_grammar_system_prompt()
        assert "SELECT *" in text

    def test_warns_about_dml(self):
        text = sql_grammar_system_prompt()
        assert "UPDATE" in text or "DML" in text

    def test_mentions_alias_requirement(self):
        text = sql_grammar_system_prompt()
        assert "alias" in text.lower() or "AS" in text

    def test_includes_injection_safety_warning(self):
        text = sql_grammar_system_prompt()
        assert "inject" in text.lower() or "interpolat" in text.lower() or "ParamList" in text

    def test_warns_about_log_tables(self):
        text = sql_grammar_system_prompt()
        assert "AITM" in text or "LOG table" in text or "audit" in text.lower()

    def test_warns_about_sbocommon(self):
        text = sql_grammar_system_prompt()
        assert "SBOCOMMON" in text
