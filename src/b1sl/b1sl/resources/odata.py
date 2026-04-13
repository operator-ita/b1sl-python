from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, Generic, TypeVar

if TYPE_CHECKING:
    from b1sl.b1sl.resources.base import GenericResource

T = TypeVar("T")

def format_odata_value(value: Any) -> str:
    """Formats a Python value for OData query strings."""
    if isinstance(value, str):
        # Escape single quotes and wrap in single quotes
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    if isinstance(value, datetime):
        return f"'{value.strftime('%Y-%m-%dT%H:%M:%S')}'"
    if isinstance(value, date):
        return f"'{value.strftime('%Y-%m-%d')}'"
    if isinstance(value, time):
        return f"'{value.strftime('%H:%M:%S')}'"
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    return str(value)

class ODataExpression(str):
    """Represents a composed OData filter expression."""

    def __and__(self, other: str) -> ODataExpression:
        return ODataExpression(f"({self} and {other})")

    def __or__(self, other: str) -> ODataExpression:
        return ODataExpression(f"({self} or {other})")

    def __invert__(self) -> ODataExpression:
        return ODataExpression(f"not ({self})")

class ODataField(str):
    """
    Represents an OData field name with operator overloading 
    to build ODataExpression strings.
    """

    def __eq__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} eq {format_odata_value(other)}")

    def __ne__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} ne {format_odata_value(other)}")

    def __lt__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} lt {format_odata_value(other)}")

    def __le__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} le {format_odata_value(other)}")

    def __gt__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} gt {format_odata_value(other)}")

    def __ge__(self, other: Any) -> ODataExpression:
        return ODataExpression(f"{self} ge {format_odata_value(other)}")

    def __truediv__(self, other: Any) -> ODataField:
        """Support path-based selection: F.Item / F.ItemChild -> 'Item/ItemChild'."""
        return ODataField(f"{self}/{other}")

    def contains(self, value: str) -> ODataExpression:
        return ODataExpression(f"contains({self}, {format_odata_value(value)})")

    def startswith(self, value: str) -> ODataExpression:
        return ODataExpression(f"startswith({self}, {format_odata_value(value)})")

    def endswith(self, value: str) -> ODataExpression:
        return ODataExpression(f"endswith({self}, {format_odata_value(value)})")

    def desc(self) -> str:
        """Helper for orderby: F.Field.desc() -> 'Field desc'"""
        return f"{self} desc"

    def asc(self) -> str:
        """Helper for orderby: F.Field.asc() -> 'Field asc'"""
        return f"{self} asc"

    def in_(self, values: list[Any]) -> ODataExpression:
        """OData 'in' operator support."""
        vals = ", ".join(format_odata_value(v) for v in values)
        return ODataExpression(f"{self} in ({vals})")

class QueryBuilder(Generic[T]):
    """
    Fluent interface for building OData queries.
    """

    def __init__(self, resource: GenericResource[T]):
        self._resource = resource
        self._key: Any | None = None
        self._filter: str | None = None
        self._select: list[str] = []
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None
        self._expand: list[str] | dict[str, list[str]] | None = None

    def by_id(self, key: Any) -> QueryBuilder[T]:
        """Sets the query to fetch a single entity by its primary key."""
        self._key = key
        return self

    def filter(self, expression: str) -> QueryBuilder[T]:
        self._filter = str(expression)
        return self

    def select(self, *fields: str) -> QueryBuilder[T]:
        self._select.extend(fields)
        return self

    def orderby(self, expression: str) -> QueryBuilder[T]:
        self._orderby = expression
        return self

    def top(self, value: int) -> QueryBuilder[T]:
        self._top = value
        return self

    def skip(self, value: int) -> QueryBuilder[T]:
        self._skip = value
        return self

    def expand(self, value: list[str] | dict[str, list[str]]) -> QueryBuilder[T]:
        self._expand = value
        return self

    def execute(self) -> list[T] | T:
        """Execute the query. Returns a list for collections or a single instance if by_id() was used."""
        from b1sl.b1sl.resources.base import ODataQuery
        
        # If by_id was used, it's a single entity GET
        if self._key is not None:
            return self._resource.get(
                key=self._key, 
                select=self._select or None, 
                expand=self._expand
            )

        query = ODataQuery(
            filter=self._filter,
            select=self._select or None,
            orderby=self._orderby,
            top=self._top,
            skip=self._skip,
            expand=self._expand
        )
        return self._resource.list(query=query)

    def all(self) -> list[T]:
        """Alias for execute() when expecting a collection."""
        res = self.execute()
        return res if isinstance(res, list) else [res]

    def first(self) -> T | None:
        """Execute the query and return the first result, if any."""
        results = self.top(1).all()
        return results[0] if results else None
