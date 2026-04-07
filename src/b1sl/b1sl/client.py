from __future__ import annotations

import logging

from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
from b1sl.b1sl.base_adapter import ObservabilityConfig
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.resources._generated.client_mixin import B1ClientMixin
from b1sl.b1sl.rest_adapter import RestAdapter

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from b1sl.b1sl.resources.udo import UDOResource


class B1Client(B1ClientMixin):
    """
    Main synchronous entry point for the SAP B1 Service Layer SDK.

    This class provides a typed interface to access SAP resources (Items,
    Orders, etc.) and custom UDOs. It orchestrates the underlying RestAdapter
    for session management and HTTP transport.

    AI Role: Primary interface for synchronous scripts and legacy apps.
    Use properties (e.g. client.items) to access SAP entities.

    Example:
        config = B1Config.from_env()
        client = B1Client(config)
        item = client.items.get("A0001")
    """

    def __init__(
        self,
        config: B1Config,
        logger: logging.Logger | None = None,
        version: str = "v2",
        adapter: RestAdapterProtocol | None = None,
        *,
        observability: ObservabilityConfig | None = None,
    ) -> None:
        """
        Initializes the B1Client.

        Args:
            config (B1Config): Validated configuration object.
            logger (logging.Logger, optional): Custom logger; defaults
                to a prefixed 'b1sl.B1Client' logger.
            version (str): Service Layer API version (v1, v2). Defaults to "v2".
            adapter (RestAdapterProtocol, optional): Custom adapter for
                mocking or dependency injection.
        """
        self._logger = logger or logging.getLogger(f"b1sl.{self.__class__.__name__}")
        # Private: consumers use properties from B1ClientMixin
        self._adapter = adapter or RestAdapter(
            config, logger=self._logger, version=version, observability=observability
        )
        self.version = version

    @property
    def session_id(self) -> str | None:
        """
        Retrieves the current SAP session ID.
        """
        return self._adapter.session_id

    def connect(self) -> None:
        """
        No-op for the sync client as connection is per-request,
        provided for parity with AsyncB1Client.
        """
        pass

    def close(self) -> None:
        """
        Logs out and closes the HTTP connection pool.
        Must be called to ensure clean shutdown if not using context manager.
        """
        self._adapter.close()

    def __enter__(self) -> "B1Client":
        """
        Entry point for the context manager.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit point for the context manager.
        Ensures connection pool cleanup.
        """
        self.close()

    def udo(self, table_name: str) -> "UDOResource":
        """
        Access a User Defined Object (UDO) or User Table dynamically.

        AI Role: Use this for any SAP entity not present in the pre-defined
        service properties. Handles @U_ prefixing internally if required
        by specific UDO implementations.

        Args:
            table_name (str): The UDO table name as registered in SAP B1
                (e.g., "CT_SDK_ASSETS").

        Returns:
            UDOResource: A resource object bound to the specified UDO.
        """
        from b1sl.b1sl.resources.udo import UDOResource

        return UDOResource(adapter=self._adapter, table_name=table_name)
