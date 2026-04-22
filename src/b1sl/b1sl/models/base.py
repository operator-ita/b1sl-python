"""
b1sl.b1sl.models.base
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Single source of truth for the shared B1Model base class.

All SAP B1 Pydantic models in this SDK must inherit from B1Model, never
directly from pydantic.BaseModel.  This guarantees a consistent config
across the whole model hierarchy:

  - ``extra='allow'``  — unknown UDFs (U_*) returned by SAP are preserved
    instead of causing a ValidationError.
  - ``populate_by_name=True`` — fields can be set by their Python name
    OR by their SAP alias (whichever is more convenient at the call site).

Inbound normalisation contract
-------------------------------
``B1Model`` handles SAP-specific encodings transparently via a
``model_validator(mode='before')`` so every subclass automatically
receives clean Python values:

    * ``"tYES"`` / ``"tNO"``       → ``bool``
    * ``"/Date(1735689600000)/"``   → ISO date string ``"2025-01-01"``

    >>> from b1sl.b1sl.models.base import B1Model
    >>> from pydantic import Field
    >>> class MyModel(B1Model):
    ...     active: bool | None = Field(None, alias="Active")
    ...     created: str | None = Field(None, alias="CreateDate")
    >>> MyModel.model_validate({"Active": "tYES", "CreateDate": "/Date(1735689600000)/"})
    MyModel(active=True, created='2025-01-01')

Outbound serialisation contract
---------------------------------
``to_api_payload()`` reverses the normalisation so SAP receives its native
format, and enforces ``exclude_unset=True`` to prevent accidental null-
overwrites on PATCH requests:

    * ``bool``             → ``"tYES"`` / ``"tNO"``
    * ``datetime.date``    → ISO string ``"YYYY-MM-DD"``
    * ``Valid=True``       → also sets ``Frozen="tNO"`` (SAP invariant)
"""

from __future__ import annotations

import re
import warnings
from collections.abc import Iterator, MutableMapping
from datetime import date, datetime, timezone
from enum import Enum
from typing import Annotated, Any

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, model_validator

# SAP boolean sentinel values — exact set used by the Service Layer.
_SAP_YES: str = "tYES"
_SAP_NO: str = "tNO"

_SAP_BOOL_TRUE = {"boyes", "tyes", "y", "yes", "true", "1"}
_SAP_BOOL_FALSE = {"bono", "tno", "n", "no", "false", "0"}


def _coerce_sap_boolean(v: Any) -> Any:
    if isinstance(v, str):
        vl = v.lower()
        if vl in _SAP_BOOL_TRUE:
            return True
        elif vl in _SAP_BOOL_FALSE:
            return False
    return v


SapBool = Annotated[bool, BeforeValidator(_coerce_sap_boolean)]

# /Date(milliseconds_since_epoch)/ — the OData v2 date format SAP uses.
_SAP_DATE_RE = re.compile(r"^/Date\((\d+)\)/$")


class UDFMapping(MutableMapping):
    """
    A mapping proxy that protects the underlying __pydantic_extra__ dictionary,
    enforcing that all keys must start with "U_".
    """
    def __init__(self, model: "B1Model") -> None:
        self.model = model

    def __getitem__(self, key: str) -> Any:
        if not key.startswith("U_"):
            raise KeyError(f"UDF mapping only supports 'U_' keys, got '{key}'")
        if self.model.__pydantic_extra__ is None:
            raise KeyError(key)
        val = self.model.__pydantic_extra__.get(key)
        if val is None and key not in self.model.__pydantic_extra__:
            raise KeyError(key)
        return val

    def __setitem__(self, key: str, value: Any) -> None:
        if not key.startswith("U_"):
            raise KeyError(f"UDF mapping only supports 'U_' keys, got '{key}'")
        # __pydantic_extra__ is guaranteed non-None at runtime because B1Model
        # always uses extra="allow"; initialise lazily as a safety net.
        if self.model.__pydantic_extra__ is None:
            self.model.__pydantic_extra__ = {}
        self.model.__pydantic_extra__[key] = value

    def __delitem__(self, key: str) -> None:
        if not key.startswith("U_"):
            raise KeyError(f"UDF mapping only supports 'U_' keys, got '{key}'")
        if self.model.__pydantic_extra__ is None or key not in self.model.__pydantic_extra__:
            raise KeyError(key)
        del self.model.__pydantic_extra__[key]

    def __iter__(self) -> Iterator[str]:
        if self.model.__pydantic_extra__ is None:
            return iter([])
        return (k for k in self.model.__pydantic_extra__ if k.startswith("U_"))

    def __len__(self) -> int:
        if self.model.__pydantic_extra__ is None:
            return 0
        return sum(1 for k in self.model.__pydantic_extra__ if k.startswith("U_"))


class B1Model(BaseModel):
    """
    Base for every SAP B1 Pydantic model in the SDK.

    Subclass this instead of ``pydantic.BaseModel`` to inherit:

    * Automatic ``/Date(ms)/`` → ISO date string coercion on ingest.
    * ``extra='allow'`` — unknown UDFs (U_* fields) round-trip cleanly.
    * ``populate_by_name=True`` — both Python name and SAP alias accepted.
    * ``to_api_payload()`` — safe outbound serialisation:
        - ``exclude_unset=True`` to prevent over-posting on PATCH.
        - ``bool`` → ``"tYES"``/``"tNO"``
        - ``date`` → ISO string
        - ``Valid`` presence → auto-sets ``Frozen`` to the inverse.

    UDF Example::

        class MyItem(B1Model):
            item_code: str           = Field(alias="ItemCode")
            custom_field: str | None = Field(None, alias="U_MyCustomField")

    Because ``extra='allow'`` is set, any *additional* UDFs returned by SAP
    that are not explicitly declared on the subclass are stored in
    ``model.__pydantic_extra__`` and round-trip cleanly through
    ``to_api_payload()``.
    """

    model_config = ConfigDict(
        populate_by_name=True,  # accept both field name and alias
        extra="allow",  # preserve unknown SAP UDFs (U_* fields)
        arbitrary_types_allowed=True,
    )

    # Common OData version fields
    # Note: alias is @odata.etag which is standard in SAP B1 v2 (OData V4)
    odata_etag: str | None = Field(None, alias="@odata.etag", repr=False)

    @property
    def etag(self) -> str | None:
        """Returns the ETag (optimistic concurrency token) for this record."""
        return self.odata_etag or self.get("@odata.etag")

    @property
    def udfs(self) -> UDFMapping:
        """
        Provides safe, dictionary-like access to User-Defined Fields (UDFs).
        Enforces that all interactions use the 'U_' prefix.
        
        Example:
            item.udfs["U_MyCustomField"] = "Value"
        """
        return UDFMapping(self)


    # ── Inbound coercion (SAP → Python) ─────────────────────────────────── #

    @model_validator(mode="before")
    @classmethod
    def _coerce_sap_primitives(cls, data: Any) -> Any:
        """
        Coerce SAP string sentinels to native Python types before
        field-level validation runs.

        Conversions applied:
        * "/Date(1735689600000)/"     → "2025-01-01" (ISO date string)
        * "tYES" / "tNO" etc          → bool
        """
        if not isinstance(data, dict):
            return data

        # Work on a shallow copy so we never mutate the caller's dict.
        # Pydantic usually passes a fresh dict in mode='before', but some
        # code paths (model_copy, re-validation) may reuse the same object.
        data = dict(data)
        udfs_arg = data.pop("udfs", None)

        coerced: dict[str, Any] = {}

        for key, val in data.items():
            if isinstance(val, str):
                # 1. Check for Dates
                m = _SAP_DATE_RE.match(val)
                if m:
                    epoch_ms = int(m.group(1))
                    coerced[key] = (
                        datetime.fromtimestamp(epoch_ms / 1000, tz=timezone.utc)
                        .date()
                        .isoformat()
                    )
                else:
                    coerced[key] = val
            else:
                coerced[key] = val

        if isinstance(udfs_arg, dict):
            for k, v in udfs_arg.items():
                if not k.startswith("U_"):
                    raise ValueError(f"UDF keys must start with 'U_', got '{k}'")
                if k in coerced:
                    warnings.warn(
                        f"Constructor conflict: {k} was passed both dynamically and inside `udfs`. The explicit value will be overwritten.",
                        RuntimeWarning,
                        stacklevel=2,
                    )
                coerced[k] = v

        return coerced

    # ── Outbound serialisation (Python → SAP) ───────────────────────────── #

    def get(self, field_alias: str, default: Any = None) -> Any:
        """
        Access a field's value by its SAP alias (e.g. 'CardCode') or Python name.

        This is particularly useful when using the ``F`` (fields) constants to
        read data from a model instance dynamically.

        Args:
            field_alias (str): The SAP alias or Python attribute name.
            default (Any, optional): Value to return if the field is not found.
                Defaults to None.

        Returns:
            Any: The field value if found, else the default.
        """
        # 1. Search in defined Pydantic fields
        for name, field in self.model_fields.items():
            if field.alias == field_alias or name == field_alias:
                return getattr(self, name, default)

        # 2. Search in 'extra' fields (UDFs) if allowed
        if self.model_extra and field_alias in self.model_extra:
            return self.model_extra[field_alias]

        return default

    def to_api_payload(self) -> dict:
        """
        Serialise this model to an API-ready dict safe for SAP Service Layer.

        Behaviour:
        * ``exclude_unset=True`` — only fields the developer *explicitly* set
          are included, preventing accidental null-overwrites on PATCH.
        * ``bool``          → ``"tYES"`` / ``"tNO"``
        * ``datetime.date`` → ISO string ``"YYYY-MM-DD"``
        * If ``Valid`` is in the payload, ``Frozen`` is automatically set to
          the inverse value (SAP requires both fields to be kept in sync).

        Fields explicitly set to ``None`` **are** included (the developer
        intended to clear that SAP field).

        Outputs SAP field aliases (not Python attribute names) and includes
        any extra UDF fields stored in ``__pydantic_extra__``.
        """
        raw: dict[str, Any] = self.model_dump(by_alias=True, exclude_unset=True)

        encoded: dict[str, Any] = {}
        for key, val in raw.items():
            if isinstance(val, bool):
                encoded[key] = _SAP_YES if val else _SAP_NO
            elif isinstance(val, date):
                encoded[key] = val.isoformat()
            elif isinstance(val, Enum):
                # For BoYesNoEnum and others, we might need special handling if they are IntEnums but represent booleans
                if val.name in ("tYES", "boYES"):
                    encoded[key] = _SAP_YES
                elif val.name in ("tNO", "boNO"):
                    encoded[key] = _SAP_NO
                else:
                    encoded[key] = val.value
            else:
                encoded[key] = val

        return encoded
