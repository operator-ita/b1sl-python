from __future__ import annotations

from datetime import date, datetime, time
from typing import TYPE_CHECKING, Any, AsyncGenerator, Generator, Generic, TypeVar

if TYPE_CHECKING:
    from b1sl.b1sl.resources.async_base import AsyncGenericResource
    from b1sl.b1sl.resources.base import GenericResource, ODataQuery

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
    __hash__ = str.__hash__


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

    # def __getattr__(self, name: str) -> ODataField:
    #     """Support nested field access: F.DocumentLines.ItemCode -> 'DocumentLines/ItemCode'.
    #
    #     Note: Use the '/' operator (e.g. F.DocumentLines / F.ItemCode) when composing
    #     paths inside select/expand — it is more explicit. This __getattr__ hook is a
    #     convenience shorthand, but it is guarded against dunder names to avoid
    #     interfering with pickle, copy, and framework introspection.
    #     """
    #     if name.startswith("__"):
    #         raise AttributeError(name)
    #     return ODataField(f"{self}/{name}")


class FieldProxy:
    """
    Virtual proxy to create ODataField objects via attribute access.
    Usage: F.ItemCode == 'A001' -> "ItemCode eq 'A001'"
    """
    def __getattr__(self, name: str) -> ODataField:
        return ODataField(name)


F = FieldProxy()

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
        self._schema: str | None = None

    def with_schema(self, name: str) -> QueryBuilder[T]:
        self._schema = name
        return self

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

    def orderby(self, expression: str, desc: bool = False) -> QueryBuilder[T]:
        expr = str(expression)
        if desc:
            expr = f"{expr} desc"
        self._orderby = expr
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

    def _build_query(self) -> ODataQuery:
        """Internal helper to build the ODataQuery object."""
        from b1sl.b1sl.resources.base import ODataQuery
        return ODataQuery(
            filter=self._filter,
            select=self._select or None,
            orderby=self._orderby,
            top=self._top,
            skip=self._skip,
            expand=self._expand
        )

    def execute(self) -> list[T] | T:
        """Execute the query. Returns a list for collections or a single instance if by_id() was used."""
        adapter = self._resource._adapter
        
        # We check if adapter has with_schema method. Some legacy mock adapters might not.
        if self._schema and hasattr(adapter, "with_schema"):
            with adapter.with_schema(self._schema):
                return self._execute_internal()
        return self._execute_internal()

    def _execute_internal(self) -> list[T] | T:
        # If by_id was used, it's a single entity GET
        if self._key is not None:
            return self._resource.get(
                key=self._key, 
                select=self._select or None, 
                expand=self._expand
            )

        return self._resource.list(query=self._build_query())

    def stream(
        self, 
        page_size: int | None = None, 
        max_pages: int | None = None
    ) -> Generator[T, None, None]:
        """
        Execute the query and return a generator that automatically fetches 
        next pages via odata.nextLink.
        """
        adapter = self._resource._adapter
        if self._schema and hasattr(adapter, "with_schema"):
            with adapter.with_schema(self._schema):
                yield from self._resource.stream(
                    query=self._build_query(), 
                    page_size=page_size, 
                    max_pages=max_pages
                )
        else:
            yield from self._resource.stream(
                query=self._build_query(), 
                page_size=page_size, 
                max_pages=max_pages
            )

    def first(self) -> T | None:
        """Execute the query and return the first result, if any."""
        res = self.top(1).execute()
        results = res if isinstance(res, list) else [res]
        return results[0] if results else None


class AsyncQueryBuilder(Generic[T]):
    """
    Asynchronous fluent interface for building OData queries.
    """

    def __init__(self, resource: AsyncGenericResource[T]):
        self._resource = resource
        self._key: Any | None = None
        self._filter: str | None = None
        self._select: list[str] = []
        self._orderby: str | None = None
        self._top: int | None = None
        self._skip: int | None = None
        self._expand: list[str] | dict[str, list[str]] | None = None
        self._schema: str | None = None

    def with_schema(self, name: str) -> AsyncQueryBuilder[T]:
        self._schema = name
        return self

    def by_id(self, key: Any) -> AsyncQueryBuilder[T]:
        self._key = key
        return self

    def filter(self, expression: str) -> AsyncQueryBuilder[T]:
        self._filter = str(expression)
        return self

    def select(self, *fields: str) -> AsyncQueryBuilder[T]:
        self._select.extend(fields)
        return self

    def orderby(self, expression: str | ODataField, desc: bool = False) -> AsyncQueryBuilder[T]:
        expr = str(expression)
        if desc:
            expr = f"{expr} desc"
        self._orderby = expr
        return self

    def top(self, value: int) -> AsyncQueryBuilder[T]:
        self._top = value
        return self

    def skip(self, value: int) -> AsyncQueryBuilder[T]:
        self._skip = value
        return self

    def expand(self, value: list[str] | dict[str, list[str]]) -> AsyncQueryBuilder[T]:
        self._expand = value
        return self

    def _build_query(self) -> ODataQuery:
        """Internal helper to build the ODataQuery object."""
        from b1sl.b1sl.resources.base import ODataQuery
        return ODataQuery(
            filter=self._filter,
            select=self._select or None,
            orderby=self._orderby,
            top=self._top,
            skip=self._skip,
            expand=self._expand
        )

    async def execute(self) -> list[T] | T:
        """Execute the query asynchronously."""
        adapter = self._resource._adapter
        if self._schema and hasattr(adapter, "with_schema"):
            with adapter.with_schema(self._schema):
                return await self._execute_internal()
        return await self._execute_internal()

    async def _execute_internal(self) -> list[T] | T:
        if self._key is not None:
            return await self._resource.get(
                key=self._key,
                select=self._select or None,
                expand=self._expand
            )

        return await self._resource.list(query=self._build_query())

    def stream(
        self, 
        page_size: int | None = None, 
        max_pages: int | None = None
    ) -> AsyncGenerator[T, None]:
        """
        Execute the query and return an async generator that automatically 
        fetches next pages via odata.nextLink.
        """
        adapter = self._resource._adapter
        
        async def _generator_with_context():
            if self._schema and hasattr(adapter, "with_schema"):
                with adapter.with_schema(self._schema):
                    async for item in self._resource.stream(
                        query=self._build_query(), 
                        page_size=page_size, 
                        max_pages=max_pages
                    ):
                        yield item
            else:
                async for item in self._resource.stream(
                    query=self._build_query(), 
                    page_size=page_size, 
                    max_pages=max_pages
                ):
                    yield item

        return _generator_with_context()

    async def first(self) -> T | None:
        """Execute the query and return the first result, if any."""
        res = await self.top(1).execute()
        results = res if isinstance(res, list) else [res]
        return results[0] if results else None
