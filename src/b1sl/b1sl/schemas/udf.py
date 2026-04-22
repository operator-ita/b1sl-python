from collections.abc import Iterator, Mapping
from typing import Any

from pydantic import ConfigDict, Field, create_model

from b1sl.b1sl.models.base import B1Model

_SAP_TYPE_MAP: dict[str, type] = {
    "db_Alpha": str,
    "db_Memo": str,
    "db_Numeric": int,
    "db_Float": float,
    "db_Date": str,
}

class UDFSchema(Mapping):
    """User Defined Fields metadata container with introspection and model generation."""

    def __init__(self, table_name: str, udf_list: list) -> None:
        self._table_name = table_name
        self._udfs = {}
        for udf in udf_list:
            # SAP UserFieldsMD returns 'CFDi_UsoCFDi', we need to standardize it as 'U_CFDi_UsoCFDi'
            key = f"U_{udf.name}" if udf.name and not udf.name.startswith("U_") else udf.name
            if key:
                self._udfs[key] = udf

    def __iter__(self) -> Iterator[str]:
        return iter(self._udfs)

    def __len__(self) -> int:
        return len(self._udfs)

    def __getitem__(self, key: str):
        return self._udfs[key]

    def __repr__(self) -> str:
        return f"UDFSchema(table={self._table_name!r}, fields={len(self)})"

    @property
    def names(self) -> list[str]:
        return list(self._udfs.keys())

    # .get() is inherited from Mapping with correct KeyError-safe semantics.

    def to_pydantic_model(
        self,
        model_name: str = "DynamicUDFs",
        base: type = B1Model,
        type_map: dict[str, type] | None = None,
    ) -> type[B1Model]:
        """Build a Pydantic model containing only UDF fields — useful for pre-PATCH validation."""
        fields: dict[str, tuple[type, Any]] = {}
        resolved_map = {**_SAP_TYPE_MAP, **(type_map or {})}

        for key, udf in self._udfs.items():
            py_type = resolved_map.get(udf.type, Any)
            fields[key] = (
                py_type | None,
                Field(default=None, alias=key, description=udf.description or ""),
            )

        # Pydantic v2: cannot pass __config__ alongside __base__.
        # Create an intermediate class that carries the config instead.
        class _DynamicBase(base):  # type: ignore[valid-type]
            model_config = ConfigDict(extra="allow", populate_by_name=True)

        return create_model(model_name, __base__=_DynamicBase, **fields)

    def validate_and_dump(
        self,
        data: dict,
        model_name: str = "DynamicUDFs",
        base: type = B1Model,
        type_map: dict[str, type] | None = None,
    ) -> dict:
        """Shortcut: validate UDFs and return a SAP-ready serialized payload."""
        model = self.to_pydantic_model(model_name, base=base, type_map=type_map)
        return model.model_validate(data).model_dump(by_alias=True, exclude_none=True)
