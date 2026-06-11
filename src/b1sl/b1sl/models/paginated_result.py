"""
b1sl.b1sl.models.paginated_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generic container for a single SAP B1 OData page.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import (
    Any,
    Iterator,
    TypeVar,
    overload,
)

T = TypeVar("T")


class PaginatedResult(Sequence[T]):
    """
    One page of SAP B1 OData results plus pagination metadata.

    Behaves like an immutable list of validated model instances — iteration,
    ``len()``, indexing and slicing all work — while also carrying the OData
    metadata needed to fetch the next page::

        page = client.items.list()
        for item in page:           # iterate
            ...
        page[0], len(page)          # index / count

        while page.next_params:     # manual pagination
            page = client.items.list(params=page.next_params)

    Attributes:
        metadata:    The ``odata.metadata`` URL string returned by SAP, if any.
        next_params: Query-param dict for the next page (derived from
                     ``odata.nextLink``), or ``None`` if this is the last page.
                     Feed it back via ``resource.list(params=...)``.
    """

    def __init__(
        self,
        data: Iterable[T],
        metadata: str | None = None,
        next_params: dict[str, Any] | None = None,
    ) -> None:
        self._data: list[T] = list(data)
        self.metadata = metadata
        self.next_params = next_params

    # ── Sequence protocol ──────────────────────────────────────────────────

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> list[T]: ...

    def __getitem__(self, index: int | slice) -> T | list[T]:
        return self._data[index]

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        more = ", has_more=True" if self.next_params else ""
        return f"PaginatedResult({self._data!r}{more})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PaginatedResult):
            return self._data == other._data
        if isinstance(other, list):
            return self._data == other
        return NotImplemented

    # defining __eq__ implicitly sets __hash__ to None — unhashable, like list

    # ── Convenience ────────────────────────────────────────────────────────

    @property
    def data(self) -> list[T]:
        """The page's records as a plain list (shared, do not mutate)."""
        return self._data

    @property
    def has_more(self) -> bool:
        """``True`` when SAP reported a further page via ``odata.nextLink``."""
        return self.next_params is not None

    def to_list(self) -> list[T]:
        """Return the page's records as a new plain ``list``."""
        return list(self._data)
