from b1sl.b1sl.pagination import build_next_params, extract_skip

# ------------------------------------------------------------------------------
# CRITICAL TESTS: Filter and Param Persistence
# ------------------------------------------------------------------------------

def test_build_next_params_ignores_nextlink_filters():
    """
    CRITICAL: As per our implementation rule, we trust current_params for filters
    in case SAP inconsistently drops them in next_link.
    """
    current_params = {"$filter": "Price gt 10"}
    next_link = "https://localhost:50000/b1s/v1/Items?$skip=10&$filter=Price gt 5" # Conflict
    
    new_params = build_next_params(current_params, next_link)
    
    assert new_params["$filter"] == "Price gt 10"
    assert new_params["$skip"] == "10"

def test_build_next_params_preserves_all_original_params():
    """Verifies that $select, $orderby, etc. are carried over."""
    current_params = {
        "$select": "ItemCode,ItemName",
        "$orderby": "ItemCode desc",
        "$filter": "startswith(ItemCode, 'A')",
    }
    next_link = "https://localhost:50000/b1s/v1/Items?$skip=50"
    
    new_params = build_next_params(current_params, next_link)
    
    assert new_params["$select"] == "ItemCode,ItemName"
    assert new_params["$orderby"] == "ItemCode desc"
    assert new_params["$filter"] == "startswith(ItemCode, 'A')"
    assert new_params["$skip"] == "50"

# ------------------------------------------------------------------------------
# UNIT TESTS: Helper functionality
# ------------------------------------------------------------------------------

def test_extract_skip_valid():
    next_link = "https://localhost:50000/b1s/v1/Items?$skip=20"
    assert extract_skip(next_link) == 20

def test_extract_skip_missing():
    next_link = "https://localhost:50000/b1s/v1/Items?$filter=ItemCode eq 'A001'"
    assert extract_skip(next_link) is None

def test_extract_skip_invalid():
    next_link = "https://localhost:50000/b1s/v1/Items?$skip=abc"
    assert extract_skip(next_link) is None

def test_build_next_params_overrides_skip():
    current_params = {"$filter": "ItemCode eq 'abc'", "$skip": "0"}
    next_link = "https://localhost:50000/b1s/v1/Items?$skip=20"
    
    new_params = build_next_params(current_params, next_link)
    
    assert new_params["$filter"] == "ItemCode eq 'abc'"
    assert new_params["$skip"] == "20"
