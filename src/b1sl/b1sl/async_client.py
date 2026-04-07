from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.base_adapter import ObservabilityConfig
from b1sl.b1sl.config import B1Config

if TYPE_CHECKING:
    from b1sl.b1sl.models.base import B1Model
    from b1sl.b1sl.resources.async_base import AsyncGenericResource
    from b1sl.b1sl.resources.udo import AsyncUDOResource
    
    # Models for typing convenience aliases
    from b1sl.b1sl.models._generated.entities.inventory import Item
    from b1sl.b1sl.models._generated.entities.businesspartners import BusinessPartner, Activity
    from b1sl.b1sl.models._generated.entities.general import Document, Payment, User
    from b1sl.b1sl.models._generated.entities.production import ProductionOrder
    from b1sl.b1sl.models._generated.entities.finance import JournalEntry
    from b1sl.b1sl.models._generated.entities.sales import ServiceCall


class AsyncB1Client:
    """
    Main asynchronous entry point for the SAP B1 Service Layer SDK.

    This client is designed for high-concurrency environments like FastAPI,
    Temporal, or Sanic. It uses an asynchronous context manager for automated
    session management and httpx for non-blocking I/O.

    AI Role: Recommended for modern web apps.
    Use 'async with AsyncB1Client(config) as b1:' to ensure session cleanup.

    Example:
        async with AsyncB1Client(config) as b1:
            item = await b1.items.get("A0001")
    """

    def __init__(
        self,
        config: B1Config,
        logger: logging.Logger | None = None,
        version: str = "v2",
        *,
        observability: ObservabilityConfig | None = None,
        session_id: str | None = None,
    ) -> None:
        """
        Initializes the AsyncB1Client.

        Args:
            config (B1Config): Validated configuration object.
            logger (logging.Logger, optional): Custom logger; defaults
                to a prefixed 'b1sl.AsyncB1Client' logger.
            version (str): API version (defaults to 'v2').
            session_id (str, optional): An existing B1SESSION cookie to reuse.
        """
        self._adapter = AsyncRestAdapter(
            config,
            logger=logger,
            version=version,
            observability=observability,
            session_id=session_id,
        )
        self.version = version

    @property
    def session_id(self) -> str | None:
        """
        Retrieves the current SAP session ID.

        Returns:
            str: B1SESSION cookie value or None.
        """
        return self._adapter.session_id

    async def connect(self) -> None:
        """
        Initializes the underlying HTTP client and logs in.
        Must be called if not using the async context manager.
        """
        await self._adapter.connect()

    async def aclose(self) -> None:
        """
        Logs out and closes the HTTP connection pool.
        Must be called to ensure clean shutdown if not using context manager.
        """
        await self._adapter.aclose()

    async def __aenter__(self) -> AsyncB1Client:
        """
        Entry point for the async context manager.
        Logins and prepares the session.
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit point for the async context manager.
        Ensures logout and connection pool cleanup.
        """
        await self.aclose()

    def get_resource(
        self, model: type["B1Model"], endpoint: str
    ) -> "AsyncGenericResource":
        """
        Instantiates a generic resource accessor for the given SAP entity.

        AI Role: This is the primary, canonical way to map any Pydantic model
        to an arbitrary Service Layer endpoint concurrently.
        """
        from b1sl.b1sl.resources.async_base import AsyncGenericResource

        class DynamicResource(AsyncGenericResource):
            pass

        DynamicResource.endpoint = endpoint
        DynamicResource.model = model

        return DynamicResource(self._adapter)

    # --------------------------------------------------------------------------
    # Thin Aliases for common endpoints (Developer Experience)
    # --------------------------------------------------------------------------

    @property
    def items(self) -> "AsyncGenericResource[Item]":
        """Convenience alias for get_resource(Item, 'Items')."""
        from b1sl.b1sl.models._generated.entities.inventory import Item

        return self.get_resource(Item, "Items")

    @property
    def business_partners(self) -> "AsyncGenericResource[BusinessPartner]":
        """Convenience alias for get_resource(BusinessPartner, 'BusinessPartners')."""
        from b1sl.b1sl.models._generated.entities.businesspartners import (
            BusinessPartner,
        )

        return self.get_resource(BusinessPartner, "BusinessPartners")

    @property
    def invoices(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'Invoices')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "Invoices")

    @property
    def quotations(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'Quotations')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "Quotations")

    @property
    def orders(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'Orders')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "Orders")

    @property
    def delivery_notes(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'DeliveryNotes')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "DeliveryNotes")

    @property
    def purchase_orders(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'PurchaseOrders')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "PurchaseOrders")

    @property
    def purchase_delivery_notes(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'PurchaseDeliveryNotes')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "PurchaseDeliveryNotes")

    @property
    def purchase_invoices(self) -> "AsyncGenericResource[Document]":
        """Convenience alias for get_resource(Document, 'PurchaseInvoices')."""
        from b1sl.b1sl.models._generated.entities.general import Document

        return self.get_resource(Document, "PurchaseInvoices")

    @property
    def incoming_payments(self) -> "AsyncGenericResource[Payment]":
        """Convenience alias for get_resource(Payment, 'IncomingPayments')."""
        from b1sl.b1sl.models._generated.entities.general import Payment

        return self.get_resource(Payment, "IncomingPayments")

    @property
    def vendor_payments(self) -> "AsyncGenericResource[Payment]":
        """Convenience alias for get_resource(Payment, 'VendorPayments')."""
        from b1sl.b1sl.models._generated.entities.general import Payment

        return self.get_resource(Payment, "VendorPayments")

    @property
    def users(self) -> "AsyncGenericResource[User]":
        """Convenience alias for get_resource(User, 'Users')."""
        from b1sl.b1sl.models._generated.entities.general import User

        return self.get_resource(User, "Users")

    # --- Producción & Operaciones ---

    @property
    def production_orders(self) -> "AsyncGenericResource[ProductionOrder]":
        """Convenience alias for get_resource(ProductionOrder, 'ProductionOrders')."""
        from b1sl.b1sl.models._generated.entities.production import ProductionOrder

        return self.get_resource(ProductionOrder, "ProductionOrders")

    # --- Contabilidad & Finanzas ---

    @property
    def journal_entries(self) -> "AsyncGenericResource[JournalEntry]":
        """Convenience alias for get_resource(JournalEntry, 'JournalEntries')."""
        from b1sl.b1sl.models._generated.entities.finance import JournalEntry

        return self.get_resource(JournalEntry, "JournalEntries")

    # --- Servicio Post-Venta ---

    @property
    def service_calls(self) -> "AsyncGenericResource[ServiceCall]":
        """Convenience alias for get_resource(ServiceCall, 'ServiceCalls')."""
        from b1sl.b1sl.models._generated.entities.sales import ServiceCall

        return self.get_resource(ServiceCall, "ServiceCalls")

    # --- CRM & Seguimiento ---

    @property
    def activities(self) -> "AsyncGenericResource[Activity]":
        """Convenience alias for get_resource(Activity, 'Activities')."""
        from b1sl.b1sl.models._generated.entities.businesspartners import Activity

        return self.get_resource(Activity, "Activities")

    def udo(self, table_name: str) -> "AsyncUDOResource":
        """
        Asynchronously access a User Defined Object (UDO) or User Table.

        AI Role: Dynamic accessor for entities not pre-defined in the client.

        Args:
            table_name (str): The UDO name in SAP B1.

        Returns:
            AsyncUDOResource: A resource object bound to the UDO.
        """
        from b1sl.b1sl.resources.udo import AsyncUDOResource

        return AsyncUDOResource(adapter=self._adapter, table_name=table_name)


