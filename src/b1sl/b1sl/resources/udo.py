from __future__ import annotations

from typing import TypeVar

from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.async_base import AsyncGenericResource
from b1sl.b1sl.resources.base import GenericResource, ODataQuery

T = TypeVar("T", bound=B1Model)


class UDOResource(GenericResource[B1Model]):
    """
    Dynamic resource for any SAP B1 UDO table or User Table.

    Instantiate via ``B1Client.udo(table_name)``.
    """

    def __init__(self, adapter, *, table_name: str) -> None:
        self.endpoint = table_name
        self.model = B1Model
        super().__init__(adapter)
        self._table_name = table_name

    def get(
        self,
        doc_entry: int,
        *,
        select: list[str] | None = None,
    ) -> B1Model:
        """Fetch a single UDO record by DocEntry."""
        return super().get(doc_entry, select=select)

    def list(
        self,
        query: ODataQuery | None = None,
    ) -> list[B1Model]:
        """Paginated list of UDO records."""
        return super().list(query)

    def create(self, data: B1Model) -> B1Model:
        """POST a new UDO record. Returns the created record as a plain B1Model."""
        return super().create(data)

    def update(self, doc_entry: int, data: B1Model) -> None:
        """PATCH a UDO record by DocEntry."""
        super().update(doc_entry, data)

    def delete(self, doc_entry: int) -> None:
        """DELETE a UDO record by DocEntry."""
        super().delete(doc_entry)


class AsyncUDOResource(AsyncGenericResource[B1Model]):
    """
    Versión asíncrona de UDOResource.
    """

    def __init__(self, adapter, *, table_name: str) -> None:
        self.endpoint = table_name
        self.model = B1Model
        super().__init__(adapter)
        self._table_name = table_name

    async def get(self, doc_entry: int, *, select: list[str] | None = None) -> B1Model:
        return await super().get(doc_entry, select=select)

    async def list(self, query: ODataQuery | None = None) -> list[B1Model]:
        return await super().list(query)

    async def create(self, data: B1Model) -> B1Model:
        return await super().create(data)

    async def update(self, doc_entry: int, data: B1Model) -> None:
        await super().update(doc_entry, data)

    async def delete(self, doc_entry: int) -> None:
        await super().delete(doc_entry)
