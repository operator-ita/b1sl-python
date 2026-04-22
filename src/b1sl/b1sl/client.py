from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from b1sl.b1sl.adapter_protocol import RestAdapterProtocol
from b1sl.b1sl.base_adapter import ObservabilityConfig
from b1sl.b1sl.config import B1Config
from b1sl.b1sl.rest_adapter import RestAdapter

if TYPE_CHECKING:
    from b1sl.b1sl.batch.client import BatchClient
    from b1sl.b1sl.models._generated.entities.businesspartners import (
        Activity,
        BusinessPartner,
    )
    from b1sl.b1sl.models._generated.entities.general import Document
    from b1sl.b1sl.models._generated.entities.inventory import Item
    from b1sl.b1sl.models.base import B1Model
    from b1sl.b1sl.resources.base import GenericResource
    from b1sl.b1sl.resources.udo import UDOResource


class B1Client:
    """
    Main synchronous entry point for the SAP B1 Service Layer SDK.

    This client is designed for synchronous scripts, CLI tools, and legacy apps.
    It uses a context manager for automated session management.

    AI Role: Primary interface for synchronous scripts and legacy apps.
    Use 'with B1Client(config) as b1:' to ensure session cleanup.

    Concurrency-Elite Aliases (Elite Citizens):
        Only entities with ETag support are exposed as direct properties.
        This ensures state-safety and clear architectural boundaries.
        Objects without ETag support must be accessed via 'get_resource()'
        or 'udo()'.

    Example:
        with B1Client(config) as b1:
            item = b1.items.get("A0001")
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

    def dry_run(self, enabled: bool = True):
        """
        Context manager to temporarily enable or disable Dry Run mode
        **for the current thread only** (thread-safe via ContextVar).

        Usage::

            with B1Client(config) as b1:
                # Intercept writes for just this block
                with b1.dry_run():
                    b1.items.create(new_item)  # intercepted

                # Force real execution even if global dry_run is True
                with b1.dry_run(enabled=False):
                    b1.items.update(item)  # sent to SAP

        Note:
            Use ``with`` (sync CM), **not** ``async with``.
        """
        return self._adapter.dry_run(enabled)

    def with_schema(self, name: str):
        """
        Context manager to temporarily set the B1S-Schema header
        **for the current thread only** (thread-safe via ContextVar).
        
        Usage::
        
            with B1Client(config) as b1:
                with b1.with_schema("demo.schema"):
                    b1.items.get("A0001")
        """
        return self._adapter.with_schema(name)

    def batch(self) -> BatchClient:
        """
        Returns a context manager that groups multiple resource operations
        into a single OData $batch HTTP request.

        Use this for high-concurrency scenarios (bulk GETs) or transactional
        integrity (atomic ChangeSets). See :class:`BatchClient` for details.
        """
        from b1sl.b1sl.batch.client import BatchClient
        return BatchClient(self)

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
        """
        self.close()

    def get_resource(
        self, model: type["B1Model"], endpoint: str
    ) -> "GenericResource":
        """
        Instantiates a generic resource accessor for the given SAP entity.

        AI Role: This is the primary, canonical way to map any Pydantic model
        to an arbitrary Service Layer endpoint synchronously.
        """
        from b1sl.b1sl.resources.base import GenericResource

        class DynamicResource(GenericResource):
            pass

        DynamicResource.endpoint = endpoint
        DynamicResource.model = model

        return DynamicResource(self._adapter)

    # --------------------------------------------------------------------------
    # Concurrency-Elite Aliases (First-Class Citizens with ETag support)
    # --------------------------------------------------------------------------

    # --- Master Data ---

    @property
    def items(self) -> "GenericResource[Item]":
        """Access the 'Items' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import Item
        return self.get_resource(Item, "Items")

    @property
    def business_partners(self) -> "GenericResource[BusinessPartner]":
        """Access the 'BusinessPartners' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import BusinessPartner
        return self.get_resource(BusinessPartner, "BusinessPartners")

    @property
    def activities(self) -> "GenericResource[Activity]":
        """Access the 'Activities' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import Activity
        return self.get_resource(Activity, "Activities")

    # --- Sales Documents ---

    @property
    def quotations(self) -> "GenericResource[Document]":
        """Access the 'Quotations' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Quotations")

    @property
    def orders(self) -> "GenericResource[Document]":
        """Access the 'Orders' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Orders")

    @property
    def delivery_notes(self) -> "GenericResource[Document]":
        """Access the 'DeliveryNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "DeliveryNotes")

    @property
    def invoices(self) -> "GenericResource[Document]":
        """Access the 'Invoices' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Invoices")

    @property
    def returns(self) -> "GenericResource[Document]":
        """Access the 'Returns' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Returns")

    @property
    def return_request(self) -> "GenericResource[Document]":
        """Access the 'ReturnRequest' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "ReturnRequest")

    @property
    def credit_notes(self) -> "GenericResource[Document]":
        """Access the 'CreditNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CreditNotes")

    @property
    def down_payments(self) -> "GenericResource[Document]":
        """Access the 'DownPayments' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "DownPayments")

    @property
    def goods_return_request(self) -> "GenericResource[Document]":
        """Access the 'GoodsReturnRequest' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "GoodsReturnRequest")

    # --- Purchasing Documents ---

    @property
    def purchase_requests(self) -> "GenericResource[Document]":
        """Access the 'PurchaseRequests' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseRequests")

    @property
    def purchase_quotations(self) -> "GenericResource[Document]":
        """Access the 'PurchaseQuotations' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseQuotations")

    @property
    def purchase_orders(self) -> "GenericResource[Document]":
        """Access the 'PurchaseOrders' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseOrders")

    @property
    def purchase_delivery_notes(self) -> "GenericResource[Document]":
        """Access the 'PurchaseDeliveryNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseDeliveryNotes")

    @property
    def purchase_invoices(self) -> "GenericResource[Document]":
        """Access the 'PurchaseInvoices' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseInvoices")

    @property
    def purchase_returns(self) -> "GenericResource[Document]":
        """Access the 'PurchaseReturns' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseReturns")

    @property
    def purchase_credit_notes(self) -> "GenericResource[Document]":
        """Access the 'PurchaseCreditNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseCreditNotes")

    @property
    def purchase_down_payments(self) -> "GenericResource[Document]":
        """Access the 'PurchaseDownPayments' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseDownPayments")

    # --- Inventory & Specialized ---

    @property
    def inventory_gen_entries(self) -> "GenericResource[Document]":
        """Access the 'InventoryGenEntries' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "InventoryGenEntries")

    @property
    def inventory_gen_exits(self) -> "GenericResource[Document]":
        """Access the 'InventoryGenExits' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "InventoryGenExits")

    @property
    def drafts(self) -> "GenericResource[Document]":
        """Access the 'Drafts' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Drafts")

    @property
    def additional_expenses(self) -> "GenericResource[B1Model]":
        """Access the 'AdditionalExpenses' entity (supports ETags)."""
        from b1sl.b1sl.models.base import B1Model
        return self.get_resource(B1Model, "AdditionalExpenses")

    # --- Correction marketing documents ---

    @property
    def correction_invoice(self) -> "GenericResource[Document]":
        """Access the 'CorrectionInvoice' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionInvoice")

    @property
    def correction_invoice_reversal(self) -> "GenericResource[Document]":
        """Access the 'CorrectionInvoiceReversal' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionInvoiceReversal")

    @property
    def correction_purchase_invoice(self) -> "GenericResource[Document]":
        """Access the 'CorrectionPurchaseInvoice' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionPurchaseInvoice")

    @property
    def correction_purchase_invoice_reversal(self) -> "GenericResource[Document]":
        """Access the 'CorrectionPurchaseInvoiceReversal' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionPurchaseInvoiceReversal")

    def udo(self, table_name: str) -> "UDOResource":
        """
        Access a User Defined Object (UDO) or User Table dynamically.

        AI Role: Use this for any SAP entity not present in the pre-defined
        service properties.

        Args:
            table_name (str): The UDO table name as registered in SAP B1
                (e.g., "CT_SDK_ASSETS").
        """
        from b1sl.b1sl.resources.udo import UDOResource

        return UDOResource(adapter=self._adapter, table_name=table_name)
