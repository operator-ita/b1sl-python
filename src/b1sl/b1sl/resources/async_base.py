from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, TypeVar

from b1sl.b1sl.models.base import B1Model
from b1sl.b1sl.resources.base import ODataQuery, _build_expand

if TYPE_CHECKING:
    from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter

T = TypeVar("T", bound=B1Model)


class AsyncGenericResource(Generic[T]):
    """Version asíncrona de GenericResource para uso con AsyncRestAdapter."""

    endpoint: str
    model: type[T]

    def __init__(self, adapter: AsyncRestAdapter) -> None:
        self._adapter = adapter

    async def list(self, query: ODataQuery | None = None) -> list[T]:
        params = query.to_params() if query else {}
        result = await self._adapter.get(f"{self.endpoint}", ep_params=params)
        data = result.data or {}
        return [self.model.model_validate(item) for item in data.get("value", [])]

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

    async def create(self, entity: T) -> T:
        result = await self._adapter.post(
            f"{self.endpoint}", data=entity.model_dump(exclude_none=True, by_alias=True)
        )
        return self.model.model_validate(result.data)

    async def update(self, key: Any, entity: T) -> None:
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        await self._adapter.patch(
            f"{self.endpoint}({id_str})",
            data=entity.model_dump(exclude_none=True, by_alias=True),
        )

    async def delete(self, key: Any) -> None:
        id_str = f"'{key}'" if isinstance(key, str) else str(key)
        await self._adapter.delete(f"{self.endpoint}({id_str})")
