"""
b1sl.api_gateway.payload
~~~~~~~~~~~~~~~~~~~~~~~~
Builds the ``ExportPDFData`` request body from ``LoadCR`` parameter
definitions plus caller-supplied values.

Wire shape (a JSON **array**, not an object)::

    [
      {"name": "DocKey@",   "type": "xsd:decimal", "value": [["12345"]]},
      {"name": "ObjectId@", "type": "xsd:decimal", "value": [["23"]]}
    ]

Rules — every one of these was learned by breaking the call, none is in
SAP's manual (see ``docs/20-api-gateway.md``):

* Parameters that are empty **and** nullable are omitted entirely.
* ``xsd:date`` values must be ISO ``YYYY-MM-DD`` strings; a range is two ISO
  strings in the same inner array. ``LoadCR`` echoes dates in a human
  ``Date(2026, 6, 7) to Date(2026, 6, 13)`` form that cannot be sent back,
  so date parameters always need an explicit value.
* ``xsd:decimal`` accepts strings or JSON numbers alike; strings are used.

.. warning:: **Not verified live: multi-value parameters** (``LoadCR``
   ``allowMultiValue: "true"``) and non-date ranges. ``format_value`` emits
   the natural shapes — ``["a", "b"]`` → ``[["a", "b"]]`` and
   ``[["a", "b"], ["c"]]`` passed through — but no layout on the verified
   system declared a multi-value parameter, so the gateway's acceptance of
   those shapes is inferred from the (verified) date-range form, not
   measured. Verify with a real multi-value layout before relying on it.
"""

# TODO(unverified): confirm against a layout with allowMultiValue="true" that
# the gateway accepts [["v1", "v2"]] for discrete multi-value parameters and
# [["from", "to"], ...] for multiple ranges. Only single scalars and one
# xsd:date range have been exercised live (see docs/20-api-gateway.md).

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import date, datetime
from decimal import Decimal
from typing import Any

from b1sl.api_gateway.exceptions import APIGatewayParameterError
from b1sl.api_gateway.models import ReportParameter

_SCALARS = (str, int, float, Decimal)


def format_scalar(value: Any) -> str:
    """Render one scalar the way ``ExportPDFData`` accepts it."""
    if isinstance(value, bool):
        raise APIGatewayParameterError(
            "bool parameter values are ambiguous for Crystal Reports; pass the "
            "literal the layout expects (e.g. 'Y'/'N' or 'true'/'false')."
        )
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, _SCALARS):
        return str(value)
    raise APIGatewayParameterError(
        f"Unsupported parameter value type {type(value).__name__!r}: {value!r}"
    )


def format_value(value: Any) -> list[list[str]]:
    """Normalise a caller value into the ``[[…]]`` wire shape.

    * scalar (``str``/``int``/``Decimal``/``date``…) → ``[["v"]]``
    * flat sequence → ``[["v1", "v2"]]`` (date ranges, multi-value)
    * sequence of sequences → passed through, scalars formatted

    Only the scalar and the ``xsd:date`` range forms are verified against a
    live gateway; multi-value (``allowMultiValue``) and multi-range shapes
    are **unverified** (see the module docstring / TODO).
    """
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        return [[format_scalar(value)]]
    if value and all(
        isinstance(v, Sequence) and not isinstance(v, (str, bytes)) for v in value
    ):
        return [[format_scalar(x) for x in inner] for inner in value]
    return [[format_scalar(v) for v in value]]


def build_export_payload(
    parameters: Sequence[ReportParameter],
    values: Mapping[str, Any] | None = None,
    *,
    strict: bool = True,
) -> list[dict[str, Any]]:
    """Merge ``LoadCR`` definitions with explicit ``values`` into the body.

    Args:
        parameters: What ``LoadCR`` returned for the layout.
        values: ``{param_name: value}`` overrides/fill-ins. Names must match
            the gateway's (``DocKey@``, not ``DocKey``).
        strict: When ``True`` (default), reject unknown names in ``values``
            (typos would otherwise be silently dropped… or silently break
            the call) and parameters that end up with no value but are not
            nullable.

    Returns:
        The JSON-ready list. Order follows ``parameters``.

    Raises:
        APIGatewayParameterError: on unknown names, missing required values,
            or values the gateway cannot accept (dates without an explicit
            value, bools, unsupported types).
    """
    values = dict(values or {})
    known = {p.name for p in parameters}
    unknown = sorted(set(values) - known)
    if unknown and strict:
        raise APIGatewayParameterError(
            f"Unknown parameter(s) {unknown}; layout accepts {sorted(known)}."
        )

    payload: list[dict[str, Any]] = []
    for param in parameters:
        if param.name in values:
            wire_value = format_value(values[param.name])
        elif param.is_optional_empty:
            continue  # gotcha: including it (even as "") breaks the call
        elif param.is_empty:
            if strict:
                raise APIGatewayParameterError(
                    f"Parameter {param.name!r} ({param.type}) is required but has "
                    "no value; supply it via values={...}."
                )
            continue
        elif param.is_date:
            raise APIGatewayParameterError(
                f"Date parameter {param.name!r} needs an explicit value: LoadCR "
                f"echoes {param.current_values!r}, which the gateway cannot "
                "parse back. Pass a date or (start, end) pair."
            )
        else:
            wire_value = format_value(list(param.current_values))
        payload.append({"name": param.name, "type": param.type, "value": wire_value})
    return payload
