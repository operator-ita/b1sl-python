"""
sap_metadata_generator.mapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Maps EDM types to Python types.
"""
from typing import Optional


EDM_TYPE_MAP: dict[str, str] = {
    "Edm.String":          "str",
    "Edm.Guid":            "str",
    "Edm.Int16":           "int",
    "Edm.Int32":           "int",
    "Edm.Int64":           "int",
    "Edm.Byte":            "int",
    "Edm.SByte":           "int",
    "Edm.Decimal":         "float",
    "Edm.Single":          "float",
    "Edm.Double":          "float",
    "Edm.Date":            "str",
    "Edm.DateTime":        "str",
    "Edm.DateTimeOffset":  "str",
    "Edm.Time":            "str",
    "Edm.TimeOfDay":       "str",
    "Edm.Duration":        "str",
    "Edm.Boolean":         "SapBool",
    "Edm.Binary":          "bytes",
    "Edm.Stream":          "bytes",
}


def map_edm_type(edm_type: str, enum_types: set[str], complex_types: set[str]) -> tuple[str, set[str]]:
    """
    Returns (python_type_string, required_imports_set).
    Python type is wrapped in Optional[] by the generator for non-key fields.
    """
    imports: set[str] = set()

    if edm_type.startswith("Collection(") and edm_type.endswith(")"):
        inner = edm_type[11:-1]
        inner_py, inner_imports = map_edm_type(inner, enum_types, complex_types)
        imports.update(inner_imports)
        return f"list[{inner_py}]", imports

    # Check if it's an enum or complex type
    clean_type = edm_type.split(".")[-1]
    if clean_type in enum_types:
        if clean_type in ("BoYesNoEnum", "BoYesNoNoneEnum"):
            return "SapBool", {"from b1sl.b1sl.models.base import SapBool"}
        return clean_type, {f"from .enums import {clean_type}"}
    if clean_type in complex_types:
        # Use direct class reference for complex types (supported by from __future__ import annotations)
        return clean_type, set()

    # Default to primitive map
    python_type = EDM_TYPE_MAP.get(edm_type, "Any")
    if python_type == "Any":
        imports.add("from typing import Any")
    elif python_type == "SapBool":
        imports.add("from b1sl.b1sl.models.base import SapBool")

    return python_type, imports
