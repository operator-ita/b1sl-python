"""
b1sl.b1sl.models.odata_query_model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Typed container for OData v4 query parameters.

``ODataQueryModel`` is used internally by ``BaseResource._build_odata_params``
to construct validated, serialisable query-parameter dicts.  Using a Pydantic
model here gives us:

* ``extra='forbid'`` — typos in keyword arguments raise a ``ValidationError``
  immediately instead of silently being ignored by the HTTP client.
* A single ``build_query_params()`` method that strips ``None`` values and
  coerces all parameter values to strings as required by ``requests``.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class ODataQueryModel(BaseModel):
    """Typed representation of OData v4 system query options.

    All fields are optional; only non-``None`` fields are included in the
    generated query-parameter dict.
    """

    select: str | None = Field(None, alias="$select")
    filter_: str | None = Field(None, alias="$filter")
    order_by: str | None = Field(None, alias="$orderby")
    top: int | None = Field(None, alias="$top")
    skip: int | None = Field(None, alias="$skip")
    expand: str | None = Field(None, alias="$expand")
    format: str | None = Field(None, alias="$format")
    count: bool | None = Field(None, alias="$count")
    search: str | None = Field(None, alias="$search")

    model_config = ConfigDict(
        extra="forbid",  # reject unknown keys — catches query-param typos
        populate_by_name=True,  # allow both Python name and OData alias
    )

    def build_query_params(self) -> dict[str, str]:
        """Return a ``{str: str}`` dict suitable for ``requests`` ``params=``.

        Only set (non-``None``) fields are included.  OData alias names
        (e.g. ``"$select"``) are used as keys.
        """
        raw = self.model_dump(by_alias=True, exclude_none=True)
        return {k: str(v) for k, v in raw.items()}
