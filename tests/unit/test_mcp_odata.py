"""Unit tests for b1sl.contrib.mcp OData helpers — grammar + crossjoin tool def.

All tests are pure unit tests (no network, no SAP connection).
"""

from __future__ import annotations

from b1sl.contrib.mcp.odata_grammar import (
    ODATA_FUNCTIONS,
    ODATA_OPERATORS,
    ODATA_SYSTEM_OPTIONS,
    odata_query_system_prompt,
)
from b1sl.contrib.mcp.odata_schemas import odata_crossjoin_tool_definition

# ── ODATA_OPERATORS ────────────────────────────────────────────────────────────

def test_odata_operators_contains_comparison_ops():
    for op in ("eq", "ne", "gt", "ge", "lt", "le"):
        assert op in ODATA_OPERATORS


def test_odata_operators_contains_logical_ops():
    for op in ("and", "or", "not"):
        assert op in ODATA_OPERATORS


def test_odata_operators_is_frozenset():
    assert isinstance(ODATA_OPERATORS, frozenset)


def test_odata_operators_lowercase():
    for op in ODATA_OPERATORS:
        assert op == op.lower(), f"Operator {op!r} is not lowercase"


# ── ODATA_FUNCTIONS ────────────────────────────────────────────────────────────

def test_odata_functions_contains_v4_style():
    for fn in ("contains", "startswith", "endswith"):
        assert fn in ODATA_FUNCTIONS


def test_odata_functions_contains_v3_substringof():
    assert "substringof" in ODATA_FUNCTIONS


def test_odata_functions_is_frozenset():
    assert isinstance(ODATA_FUNCTIONS, frozenset)


def test_odata_functions_no_unsupported_entries():
    unsupported = {"tolower", "toupper", "trim", "concat", "length", "indexof"}
    overlap = ODATA_FUNCTIONS & unsupported
    assert not overlap, f"Unsupported functions in ODATA_FUNCTIONS: {overlap}"


# ── ODATA_SYSTEM_OPTIONS ───────────────────────────────────────────────────────

def test_odata_system_options_contains_core_options():
    for opt in ("$filter", "$select", "$orderby", "$expand", "$top", "$skip"):
        assert opt in ODATA_SYSTEM_OPTIONS


def test_odata_system_options_contains_count_options():
    assert "$count" in ODATA_SYSTEM_OPTIONS
    assert "$inlinecount" in ODATA_SYSTEM_OPTIONS


def test_odata_system_options_is_frozenset():
    assert isinstance(ODATA_SYSTEM_OPTIONS, frozenset)


def test_odata_system_options_all_start_with_dollar():
    for opt in ODATA_SYSTEM_OPTIONS:
        assert opt.startswith("$"), f"System option {opt!r} does not start with '$'"


# ── odata_query_system_prompt ──────────────────────────────────────────────────

def test_odata_query_system_prompt_returns_string():
    prompt = odata_query_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 200


def test_odata_query_system_prompt_covers_boolean_quirk():
    prompt = odata_query_system_prompt()
    assert "tYES" in prompt
    assert "tNO" in prompt


def test_odata_query_system_prompt_covers_date_encoding():
    prompt = odata_query_system_prompt()
    assert "/Date(" in prompt


def test_odata_query_system_prompt_covers_string_quoting():
    prompt = odata_query_system_prompt()
    assert "single quote" in prompt.lower() or "single quotes" in prompt.lower()


def test_odata_query_system_prompt_covers_select_discipline():
    prompt = odata_query_system_prompt()
    assert "$select" in prompt


def test_odata_query_system_prompt_covers_expand():
    prompt = odata_query_system_prompt()
    assert "$expand" in prompt


def test_odata_query_system_prompt_mentions_case_sensitivity():
    prompt = odata_query_system_prompt()
    assert "case-sensitive" in prompt.lower()


def test_odata_query_system_prompt_covers_substringof_argument_order():
    prompt = odata_query_system_prompt()
    # The v3 reversed-argument-order gotcha must be mentioned
    assert "substringof" in prompt
    assert "reversed" in prompt.lower() or "reverse" in prompt.lower()


def test_odata_query_system_prompt_covers_time_fields():
    prompt = odata_query_system_prompt()
    # DocTime and time-field formats must be documented
    assert "DocTime" in prompt or "time field" in prompt.lower()
    # SAP ignores date parts for time fields — that caveat must be mentioned
    assert "ignores" in prompt.lower()


def test_odata_query_system_prompt_covers_null_comparison():
    prompt = odata_query_system_prompt()
    # Null comparison (eq null without quotes) must be documented
    assert "eq null" in prompt


def test_odata_query_system_prompt_covers_enum_name_and_value():
    prompt = odata_query_system_prompt()
    # Both enum value short code and full name must be mentioned
    assert "cCustomer" in prompt or ("enum" in prompt.lower() and "name" in prompt.lower())
    assert "'C'" in prompt or "value" in prompt.lower()


def test_odata_query_system_prompt_skip_before_top():
    prompt = odata_query_system_prompt()
    # The $skip-applied-before-$top ordering rule must be documented
    lower = prompt.lower()
    assert "$skip" in prompt
    assert "first" in lower or "before" in lower or "applied" in lower


def test_odata_system_options_contains_apply():
    assert "$apply" in ODATA_SYSTEM_OPTIONS


def test_odata_query_system_prompt_covers_apply_aggregation():
    prompt = odata_query_system_prompt()
    assert "$apply" in prompt
    # Core aggregation methods must be listed
    for method in ("sum", "min", "max", "countdistinct"):
        assert method in prompt


def test_odata_query_system_prompt_apply_alias_required():
    prompt = odata_query_system_prompt()
    # The alias requirement must be documented
    lower = prompt.lower()
    assert "alias" in lower or "as Alias" in prompt or "required" in lower


def test_odata_query_system_prompt_apply_count_virtual_property():
    prompt = odata_query_system_prompt()
    # $count virtual property form (no field name) must be shown
    assert "$count as" in prompt or "aggregate($count" in prompt


def test_odata_query_system_prompt_covers_inlinecount_allpages():
    prompt = odata_query_system_prompt()
    assert "$inlinecount" in prompt
    assert "allpages" in prompt
    # The odata.count response field must be mentioned
    assert "odata.count" in prompt


def test_odata_query_system_prompt_covers_groupby():
    prompt = odata_query_system_prompt()
    assert "groupby" in prompt
    # Chained filter/groupby transform must be mentioned
    lower = prompt.lower()
    assert "filter" in lower and "groupby" in prompt


def test_odata_query_system_prompt_groupby_with_aggregation():
    prompt = odata_query_system_prompt()
    # groupby + aggregate combined syntax must be shown
    assert "groupby" in prompt and "aggregate" in prompt


def test_odata_query_system_prompt_covers_crossjoin():
    prompt = odata_query_system_prompt()
    assert "$crossjoin" in prompt
    # The bare-crossjoin-returns-error constraint is critical
    lower = prompt.lower()
    assert "400" in prompt or "error" in lower or "always" in lower


def test_odata_query_system_prompt_crossjoin_navigation_paths():
    prompt = odata_query_system_prompt()
    # EntityName/FieldName navigation path syntax for crossjoin must be documented
    assert "EntityName/FieldName" in prompt or "Orders/CardCode" in prompt


def test_odata_query_system_prompt_crossjoin_arithmetic():
    prompt = odata_query_system_prompt()
    # Arithmetic operators in $expand must be documented
    for op in ("mul", "sub", "add", "div"):
        assert op in prompt


# ── odata_crossjoin_tool_definition ───────────────────────────────────────────

def test_crossjoin_tool_definition_structure():
    tool = odata_crossjoin_tool_definition()
    assert tool["name"] == "crossjoin"
    assert "description" in tool
    assert "inputSchema" in tool
    schema = tool["inputSchema"]
    assert schema["type"] == "object"
    assert "entities" in schema["properties"]
    assert schema["required"] == ["entities"]


def test_crossjoin_tool_entities_param_is_array():
    tool = odata_crossjoin_tool_definition()
    entities_param = tool["inputSchema"]["properties"]["entities"]
    assert entities_param["type"] == "array"
    assert entities_param["items"]["type"] == "string"
    assert entities_param["minItems"] == 2


def test_crossjoin_tool_has_expand_param():
    tool = odata_crossjoin_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "expand" in props
    expand = props["expand"]
    assert expand["type"] == "object"
    # Arithmetic hint must be present
    assert "mul" in expand["description"] or "arithmetic" in expand["description"].lower()


def test_crossjoin_tool_has_filter_param():
    tool = odata_crossjoin_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "filter" in props
    # Navigation path syntax hint
    assert "EntityName/FieldName" in props["filter"]["description"] or "Orders/CardCode" in props["filter"]["description"]


def test_crossjoin_tool_has_apply_param():
    tool = odata_crossjoin_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "apply" in props
    desc = props["apply"]["description"]
    assert "aggregate" in desc
    assert "groupby" in desc


def test_crossjoin_tool_has_top_skip_orderby():
    tool = odata_crossjoin_tool_definition()
    props = tool["inputSchema"]["properties"]
    for param in ("top", "skip", "orderby"):
        assert param in props, f"Missing param: {param}"
    assert props["top"]["type"] == "integer"
    assert props["skip"]["type"] == "integer"


def test_crossjoin_tool_description_warns_bare_crossjoin():
    tool = odata_crossjoin_tool_definition()
    desc = tool["description"].lower()
    # Must communicate that bare crossjoin returns 400
    assert "400" in desc or "bare" in desc or "always" in desc


def test_crossjoin_tool_is_exported_from_package():
    from b1sl.contrib.mcp import odata_crossjoin_tool_definition as fn
    assert callable(fn)
    tool = fn()
    assert tool["name"] == "crossjoin"


# ── query_service_tool_definition ─────────────────────────────────────────────

def test_query_service_tool_definition_structure():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    assert tool["name"] == "query_service"
    assert "description" in tool
    assert "inputSchema" in tool
    schema = tool["inputSchema"]
    assert schema["type"] == "object"
    assert schema["required"] == ["query_path"]


def test_query_service_has_query_path_param():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "query_path" in props
    assert props["query_path"]["type"] == "string"
    # Must mention navigation path syntax
    desc = props["query_path"]["description"]
    assert "DocumentLines" in desc or "NavProperty" in desc or "navigation" in desc.lower()


def test_query_service_has_expand_param():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "expand" in props
    assert props["expand"]["type"] == "object"


def test_query_service_has_filter_param():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "filter" in props
    # Navigation path hint must be present
    assert "Entity" in props["filter"]["description"] or "DocEntry" in props["filter"]["description"]


def test_query_service_has_apply_param():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    props = tool["inputSchema"]["properties"]
    assert "apply" in props


def test_query_service_has_top_skip_orderby():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    props = tool["inputSchema"]["properties"]
    for param in ("top", "skip", "orderby"):
        assert param in props
    assert props["top"]["type"] == "integer"
    assert props["skip"]["type"] == "integer"


def test_query_service_description_warns_no_expand_apply():
    from b1sl.contrib.mcp.odata_schemas import query_service_tool_definition
    tool = query_service_tool_definition()
    desc = tool["description"].lower()
    assert "400" in desc or "requires" in desc or "expand or apply" in desc


def test_query_service_is_exported_from_package():
    from b1sl.contrib.mcp import query_service_tool_definition
    assert callable(query_service_tool_definition)
    tool = query_service_tool_definition()
    assert tool["name"] == "query_service"


# ── Grammar: $expand nested $select + QueryService ────────────────────────────

def test_grammar_expand_nested_select_syntax():
    prompt = odata_query_system_prompt()
    # Nested $select inside $expand must be documented (B1 10.0 FP 2105+)
    assert "($select=" in prompt


def test_grammar_expand_dict_sdk_note():
    prompt = odata_query_system_prompt()
    # SDK dict shorthand that generates Nav($select=...) must be mentioned
    lower = prompt.lower()
    assert "dict" in lower or "sdk" in lower or "automatically" in lower


def test_grammar_covers_query_service():
    prompt = odata_query_system_prompt()
    assert "QueryService_PostQuery" in prompt


def test_grammar_query_service_post_method():
    prompt = odata_query_system_prompt()
    assert "POST" in prompt


def test_grammar_query_service_no_nextlink():
    prompt = odata_query_system_prompt()
    # Must warn that odata.nextLink is not supported for QueryService
    lower = prompt.lower()
    assert "nextlink" in lower or "pagination" in lower or "$skip" in prompt


def test_grammar_query_service_navigation_path_example():
    prompt = odata_query_system_prompt()
    # Must show a navigation path example like Orders/DocumentLines
    assert "DocumentLines" in prompt or "Orders/DocumentLines" in prompt
