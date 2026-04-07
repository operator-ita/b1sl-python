from typing import Protocol

from b1sl.b1sl.models.result import Result


class RestAdapterProtocol(Protocol):
    """
    Interface protocol for components that execute HTTP requests
    against SAP B1 Service Layer and return Result objects.

    Implemented statically by both the real RestAdapter and its Fakes.
    """

    def get(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result: ...

    def post(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result: ...

    def patch(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result: ...

    def delete(
        self, endpoint: str, ep_params: dict | None = None, data: dict | None = None
    ) -> Result: ...
