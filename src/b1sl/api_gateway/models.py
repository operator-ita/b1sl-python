"""
b1sl.api_gateway.models
~~~~~~~~~~~~~~~~~~~~~~~
Typed views over the API Gateway's JSON. The gateway's wire format is loose
(booleans as ``"true"``/``"false"`` strings, twenty-odd keys per parameter),
so each model keeps the untouched dict in ``raw`` and exposes only the
fields the client relies on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


def _as_bool(value: Any) -> bool:
    """Coerce the gateway's stringly booleans (``"true"``/``"false"``)."""
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, (list, tuple)):
        return list(value)
    return [value]


@dataclass(frozen=True)
class ReportInfo:
    """One entry of ``LoadAuthorizedCRList`` (general-catalog reports only).

    Document-bound print layouts (``QUT200xx``, ``INV200xx``…) are **not**
    listed by the gateway; their codes come from Print Layout Designer.
    """

    code: str
    name: str
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_wire(cls, data: Mapping[str, Any]) -> ReportInfo:
        return cls(
            code=str(data.get("code", "")),
            name=str(data.get("name", "")),
            raw=dict(data),
        )


@dataclass(frozen=True)
class ReportParameter:
    """One parameter definition returned by ``LoadCR?DocCode=…``.

    Attributes:
        name: Parameter name as SAP/Crystal expects it (``DocKey@``,
            ``ObjectId@``, ``RangeDate@``, ``Pm-<Table>.<Field>`` formula params…).
        type: XSD type string (``xsd:decimal``, ``xsd:string``, ``xsd:date``).
        current_values: The values SAP preloads. Flat list of strings.
            **Do not trust ``DocKey@``'s preloaded value** — it travels with
            the layout definition and may point at an arbitrary document.
        allow_null: Whether the parameter may be omitted from the export.
        allow_multi_value: ``allowMultiValue`` on the wire. **Unverified**:
            no layout on the verified system declared one, so how the
            gateway accepts multi-value payloads is inferred, not measured
            (see the TODO in ``payload.py``).
        parameter_type: ``ReportParameter`` / ``StoredProcedureParameter``.
        raw: Full wire dict.
    """

    name: str
    type: str
    current_values: list[Any] = field(default_factory=list)
    allow_null: bool = False
    allow_multi_value: bool = False
    parameter_type: str = ""
    raw: Mapping[str, Any] = field(default_factory=dict, repr=False, compare=False)

    @classmethod
    def from_wire(cls, data: Mapping[str, Any]) -> ReportParameter:
        return cls(
            name=str(data.get("name", "")),
            type=str(data.get("type", "")),
            current_values=_as_list(data.get("currentvalues")),
            allow_null=_as_bool(data.get("allowNullValue", False)),
            allow_multi_value=_as_bool(data.get("allowMultiValue", False)),
            parameter_type=str(data.get("parameterType", "")),
            raw=dict(data),
        )

    @property
    def is_date(self) -> bool:
        return self.type.lower() in {"xsd:date", "xsd:datetime"}

    @property
    def is_empty(self) -> bool:
        return not self.current_values

    @property
    def is_optional_empty(self) -> bool:
        """Empty **and** nullable — must be omitted from the export payload.

        Sending it (even as ``""``) makes ``ExportPDFData`` fail silently.
        """
        return self.is_empty and self.allow_null
