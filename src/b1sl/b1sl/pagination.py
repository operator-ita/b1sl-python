from urllib.parse import parse_qs, urlparse


def extract_skip(next_link: str) -> int | None:
    """
    Extracts the $skip value from an odata.nextLink string.
    
    Args:
        next_link: The raw odata.nextLink URL string returned by SAP.
        
    Returns:
        The integer value of $skip if found, else None.
    """
    parsed_url = urlparse(next_link)
    query_params = parse_qs(parsed_url.query)
    skip_val = query_params.get("$skip")
    if skip_val:
        try:
            return int(skip_val[0])
        except (ValueError, IndexError):
            return None
    return None


def build_next_params(current_params: dict, next_link: str) -> dict:
    """
    Builds the ep_params dictionary for the subsequent page request.
    
    Rule of Precedence (Defensive Implementation):
    1. 'next_link' ONLY wins for the $skip parameter.
    2. 'current_params' wins for everything else ($filter, $select, $orderby, etc.)
       Reason: SAP Service Layer inconsistently omits filters/selections in the 
       odata.nextLink URL. Re-applying current_params ensures the stream doesn't 
       silently "leak" outside its initial scope in page 2+.
    
    Args:
        current_params: The parameters used in the current (or initial) request.
        next_link: The raw odata.nextLink URL string returned by SAP.
        
    Returns:
        A new dictionary with combined parameters.
    """
    parsed_url = urlparse(next_link)
    next_query_params = parse_qs(parsed_url.query)

    # We start with a copy of current_params to preserve filters/selectors
    new_params = current_params.copy()
    
    # We take ONLY $skip from the next_link
    next_skip = next_query_params.get("$skip")
    if next_skip:
        new_params["$skip"] = next_skip[0]
        
    return new_params
