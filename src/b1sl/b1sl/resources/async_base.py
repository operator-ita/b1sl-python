from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from b1sl.b1sl.exceptions.exceptions import B1NotFoundError
from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.base import ODataQuery, _build_expand

if TYPE_CHECKING:
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
    from b1sl.b1sl.resources.odata import AsyncQueryBuilder, ODataField

T = TypeVar("T", bound=B1Model)


class AsyncGenericResource(Generic[T]):
    """Version asíncrona de GenericResource para uso con AsyncRestAdapter."""

    endpoint: str
    model: type[T]

    def __init__(self, adapter: AsyncRestAdapter) -> None:
        self._adapter = adapter

    # ── fluent query builder ────────────────────────────────────────────────

    def by_id(self, key: Any) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).by_id(key)

    def filter(self, expression: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).filter(expression)

    def select(self, *fields: str) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).select(*fields)

    def top(self, value: int) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).top(value)

    def skip(self, value: int) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).skip(value)

    def orderby(
        self, expression: str | ODataField, desc: bool = False
    ) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).orderby(expression, desc=desc)

    def expand(self, value: list[str] | dict[str, list[str]]) -> AsyncQueryBuilder[T]:
        from b1sl.b1sl.resources.odata import AsyncQueryBuilder

        return AsyncQueryBuilder(self).expand(value)

    async def list(self, query: ODataQuery | None = None) -> list[T]:
        params = query.to_params() if query else {}
        result = await self._adapter.get(f"{self.endpoint}", ep_params=params)
        data = result.data or {}
        return [self.model.model_validate(item) for item in data.get("value", [])]

    async def count(self) -> int:
        """GET Endpoint/$count"""
        result = await self._adapter.get(f"{self.endpoint}/$count")
        return int(result.data)

    async def get(
        self,
        key: Any,
        select: list[str] | None = None,
        expand: list[str] | dict[str, list[str]] | None = None,
    ) -> T:
        params: dict[str, str] = {}
        if select:
            params["$select"] = ",".join(str(f) for f in select)
        if expand:
            params["$expand"] = _build_expand(expand)

        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        result = await self._adapter.get(f"{self.endpoint}({id_str})", ep_params=params)
        return self.model.model_validate(result.data)

    async def exists(self, key: Any) -> bool:
        """Check if an entity exists by attempting to fetch it."""
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        try:
            await self._adapter.get(f"{self.endpoint}({id_str})")
            return True
        except B1NotFoundError:
            return False

    async def create(self, entity: T) -> T:
        # POST: send all fields that are not None (SAP requires complete payloads on create).
        # to_api_payload() uses exclude_unset, which is wrong for create — use model_dump
        # but still encode booleans by delegating through B1Model serialisation.
        payload = entity.model_dump(exclude_none=True, by_alias=True)
        # Re-encode booleans (model_dump returns Python bools, SAP needs tYES/tNO)
        from b1sl.b1sl.models.base import _SAP_NO, _SAP_YES
        encoded = {
            k: (_SAP_YES if v is True else _SAP_NO if v is False else v)
            for k, v in payload.items()
        }
        result = await self._adapter.post(f"{self.endpoint}", data=encoded)
        return self.model.model_validate(result.data)

    async def update(self, key: Any, entity: T) -> None:
        # PATCH: to_api_payload() is correct here — exclude_unset means only the
        # fields explicitly set by the developer are sent, which is the proper
        # delta semantics for a partial update. Booleans are also encoded.
        #
        # After a successful PATCH, the server-side ETag changes but SAP SL
        # returns 204 No Content without a new ETag header. We proactively
        # invalidate the stale cache entry so the next PATCH or DELETE does not
        # hit a predictable 412 conflict.
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        endpoint_path = f"/{self.endpoint}({id_str})"
        await self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=entity.to_api_payload(),
        )
        # Proactively invalidate the stale ETag: SAP issued a 204 with no
        # new ETag header, so anything in cache is now a lie.
        self._adapter._clear_etag(endpoint_path)

    async def delete(self, key: Any) -> None:
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        await self._adapter.delete(f"{self.endpoint}({id_str})")

    # ── Actions / Functions ───────────────────────────────────────────────────

    async def _action(self, key: Any, name: str, payload: dict | None = None) -> Any:
        """POST Endpoint(key)/ActionName"""
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        result = await self._adapter.post(
            f"{self.endpoint}({id_str})/{name}", data=payload or {}
        )
        return result.data if result else None

    async def _function(self, name: str, params: dict | None = None) -> Any:
        """GET Endpoint/FunctionName(params)"""
        result = await self._adapter.get(f"{self.endpoint}/{name}", ep_params=params or {})
        return result.data if result else None
