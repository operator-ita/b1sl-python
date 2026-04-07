"""
b1sl.b1sl.models.paginated_result
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generic container for a single SAP B1 OData page.
"""

from __future__ import annotations

from typing import (
    Any,
    Generic,
    Iterator,
)

from b1sl.b1sl._types import T


class PaginatedResult(Generic[T]):
    """
    Wraps one page of SAP B1 OData results together with pagination metadata.

    Attributes:
        data:        An **iterator** yielding validated model instances for
                     this page.  See the warning below.
        metadata:    The ``odata.metadata`` URL string returned by SAP, if any.
        next_params: Query-param dict for the next page (from ``odata.nextLink``),
                     or ``None`` if this is the last page.

    .. warning:: ``data`` is a **one-shot generator**.

        Iterating over ``data`` a second time returns nothing::

            result = client.items.list()
            first  = list(result.data)   # ✅ correct
            second = list(result.data)   # ❌ empty — generator exhausted!

        To consume the page multiple times, call :meth:`to_list` **once** and
        keep a reference to the returned list::

            items = result.to_list()
            print(items[0])   # ✅ safe — list is cached internally
            print(items[-1])  # ✅ still fine
    """

    def __init__(
        self,
        data: Iterator[T],
        metadata: str | None = None,
        next_params: dict[str, Any] | None = None,
    ) -> None:
        self._data_iter: Iterator[T] = data
        self._data_cache: list[T] | None = None
        self.metadata = metadata
        self.next_params = next_params

    @property
    def data(self) -> Iterator[T]:
        """
        One-shot iterator over this page's records.

        If you have already called :meth:`to_list`, subsequent accesses to
        ``data`` will replay the cached list so it is not empty.
        """
        if self._data_cache is not None:
            return iter(self._data_cache)
        return self._data_iter

    def to_list(self) -> list[T]:
        """
        Materialise the page into a list and cache it.

        Safe to call multiple times — the generator is consumed only once and
        the result is stored in ``_data_cache`` for all future accesses via
        either ``to_list()`` or the ``data`` property.

        Returns:
            A list of validated model instances for this page.
        """
        if self._data_cache is None:
            self._data_cache = list(self._data_iter)
        return self._data_cache

    def __iter__(self) -> Iterator[T]:
        """Allow ``for item in paginated_result`` to work transparently."""
        return self.data
