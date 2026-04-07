from typing import Any

from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
from b1sl.b1sl.models.result import Result


class SAPErrorFactory:
    """Static generator for structured SAP B1 error responses."""

    @staticmethod
    def generic_error(code: str, message: str) -> dict[str, Any]:
        return {"error": {"code": code, "message": {"value": message}}}

    @staticmethod
    def invalid_session() -> dict[str, Any]:
        return SAPErrorFactory.generic_error(
            "301", "Invalid session or session already timeout."
        )

    @staticmethod
    def insufficient_stock() -> dict[str, Any]:
        return SAPErrorFactory.generic_error(
            "-2035", "Fall below zero stock not allowed"
        )


class FakeRestAdapter(RestAdapterProtocol):
    """Concrete implementation of RestAdapterProtocol for unit testing.

    This class provides a fast, network-less alternative to the real SAP B1 adapter.
    It allows registering expected responses for specific routes and methods.
    """

    def __init__(self) -> None:
        """Initialize the fake adapter with empty routes and call history."""
        # Maps (method, endpoint) -> list of responses (Payloads or Exceptions)
        self._routes: dict[tuple[str, str], list[Any]] = {}
        # History of calls made for verification in tests
        self.calls: list[dict[str, Any]] = []

    def register(
        self,
        method: str,
        endpoint: str,
        response_data: Any = None,
        status: int = 200,
        raises: Exception | None = None,
    ) -> None:
        """Register a mock response for a specific HTTP method and endpoint.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE).
            endpoint: The resource endpoint (e.g., "Items", "BusinessPartners('C1')").
            response_data: The JSON-serializable data to return.
            status: HTTP status code to simulate.
            raises: If provided, this exception will be raised when the route is hit.
        """
        # Normalize endpoint by removing leading slash for storage
        normalized_ep = endpoint.lstrip("/")
        key = (method.upper(), normalized_ep)

        if key not in self._routes:
            self._routes[key] = []

        if raises:
            self._routes[key].append(raises)
        else:
            self._routes[key].append(
                Result(
                    status_code=status,
                    message="OK" if status < 400 else "Error",
                    data=response_data,
                )
            )

    def register_collection(self, endpoint: str, items: list[dict[str, Any]]) -> None:
        """Helper to register an OData collection response.

        Args:
            endpoint: Target resource endpoint.
            items: List of entities to wrap in {"value": [...]}.
        """
        self.register("GET", endpoint, response_data={"value": items})

    def register_entity(self, endpoint: str, data: dict[str, Any]) -> None:
        """Helper to register a single entity response.

        Args:
            endpoint: Target resource endpoint (e.g., "Items('A001')").
            data: The entity data.
        """
        self.register("GET", endpoint, response_data=data)

    def _handle_request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Result:
        """Internal router to record the call and return the next queued response.

        Args:
            method: HTTP method.
            endpoint: Target endpoint.
            params: Query parameters.
            data: Request body.

        Returns:
            The next Result registered for this route.

        Raises:
            ValueError: If no response is registered for the given route.
        """
        self.calls.append(
            {"method": method, "endpoint": endpoint, "params": params, "data": data}
        )

        # Normalize for lookup
        normalized_ep = endpoint.lstrip("/")
        key = (method.upper(), normalized_ep)

        if key not in self._routes or not self._routes[key]:
            # Try matching with a leading slash just in case (fallback for some legacy registration styles)
            key_alt = (method.upper(), "/" + normalized_ep)
            if key_alt in self._routes and self._routes[key_alt]:
                key = key_alt
            else:
                raise ValueError(
                    f"FakeRestAdapter: No response registered for {method} {endpoint}. "
                    f"Registered routes: {list(self._routes.keys())}"
                )

        response = self._routes[key].pop(0)
        if isinstance(response, Exception):
            raise response

        return response

    def get(
        self,
        endpoint: str,
        ep_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Result:
        """Simulate a GET request."""
        return self._handle_request("GET", endpoint, ep_params, data)

    def post(
        self,
        endpoint: str,
        ep_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Result:
        """Simulate a POST request."""
        return self._handle_request("POST", endpoint, ep_params, data)

    def patch(
        self,
        endpoint: str,
        ep_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Result:
        """Simulate a PATCH request."""
        return self._handle_request("PATCH", endpoint, ep_params, data)

    def delete(
        self,
        endpoint: str,
        ep_params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Result:
        """Simulate a DELETE request."""
        return self._handle_request("DELETE", endpoint, ep_params, data)
