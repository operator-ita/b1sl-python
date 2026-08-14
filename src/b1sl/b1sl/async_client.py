from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Self

from b1sl.b1sl.async_rest_adapter import AsyncRestAdapter
from b1sl.b1sl.base_adapter import ObservabilityConfig
from b1sl.b1sl.config import B1Config

if TYPE_CHECKING:
    from collections.abc import Sequence

    from b1sl.b1sl.batch.client import BatchClient
    from b1sl.b1sl.models._generated.entities.businesspartners import (
        Activity,
        BusinessPartner,
    )
    from b1sl.b1sl.models._generated.entities.general import Document
    from b1sl.b1sl.models._generated.entities.inventory import Item
    from b1sl.b1sl.models.base import B1Model
    from b1sl.b1sl.models.multipart import MultipartFile
    from b1sl.b1sl.resources.async_base import AsyncGenericResource
    from b1sl.b1sl.resources.attachments import AsyncAttachmentsResource
    from b1sl.b1sl.resources.crossjoin import (
        AsyncCrossJoinQueryBuilder,
        AsyncQueryServiceBuilder,
    )
    from b1sl.b1sl.resources.sql_queries import AsyncSQLQueriesResource
    from b1sl.b1sl.resources.udo import AsyncUDOResource


class AsyncB1Client:
    """
    Main asynchronous entry point for the SAP B1 Service Layer SDK.

    This client is designed for high-concurrency environments like FastAPI,
    Temporal, or Sanic. It uses an asynchronous context manager for automated
    session management and httpx for non-blocking I/O.

    AI Role: Recommended for modern web apps.
    Use 'async with AsyncB1Client(config) as b1:' to ensure session cleanup.

    Concurrency-Elite Aliases (Elite Citizens):
        Only entities with ETag support are exposed as direct properties.
        This ensures state-safety and clear architectural boundaries.
        Objects without ETag support must be accessed via 'get_resource()'
        or 'udo()'.

    Example:
        async with AsyncB1Client(config) as b1:
            item = await b1.items.get("A0001")
    """

    def __init__(
        self,
        config: B1Config,
        logger: logging.Logger | None = None,
        version: str = "v2",
        adapter: AsyncRestAdapter | None = None,
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
            adapter (AsyncRestAdapter, optional): Custom adapter for
                mocking or dependency injection (parity with B1Client).
            session_id (str, optional): An existing B1SESSION cookie to reuse.
        """
        self._logger = logger or logging.getLogger(f"b1sl.{self.__class__.__name__}")
        self._adapter = adapter or AsyncRestAdapter(
            config,
            logger=self._logger,
            version=version,
            observability=observability,
            session_id=session_id,
        )
        self.version = version

    @property
    def session_id(self) -> str | None:
        """
        Retrieves the current SAP session ID.
        """
        return self._adapter.session_id

    @property
    def base_url(self) -> str:
        """The fully normalized Service Layer base URL (including /b1s/<version>)."""
        return self._adapter.url

    def dry_run(self, enabled: bool = True):
        """
        Context manager to temporarily enable or disable Dry Run mode
        **for the current asyncio task only** (task-safe via ContextVar).

        Usage::

            async with AsyncB1Client(config) as b1:
                # Intercept writes for just this block
                with b1.dry_run():
                    await b1.items.create(new_item)  # intercepted

                # Force real execution even if global dry_run is True
                with b1.dry_run(enabled=False):
                    await b1.items.update(item)  # sent to SAP

        Note:
            Use ``with`` (sync CM), **not** ``async with``, even in async code.
        """
        return self._adapter.dry_run(enabled)

    def with_schema(self, name: str):
        """
        Context manager to temporarily set the B1S-Schema header
        **for the current asyncio.Task only** (task-safe via ContextVar).
        
        Usage::
        
            async with AsyncB1Client(config) as b1:
                async with b1.with_schema("demo.schema"):
                    await b1.items.get("A0001")
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

    async def __aenter__(self) -> Self:
        """
        Entry point for the async context manager.
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit point for the async context manager.
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

    async def call_service_method(self, name: str, payload: dict | None = None) -> Any:
        """Invoke an unbound Service Layer service method at the service root.

        Covers SAP's ``*Service_*`` operations, e.g.
        ``SBOBobService_SetCurrencyRate`` or ``SBOBobService_GetCurrencyRate``.
        The Service Layer invokes both "actions" and "functions" of this kind
        as POST with a JSON body, so a single entry point covers both.

        This is the low-level escape hatch for the ~1000 service operations
        without an Elite alias. No ETag concurrency applies to unbound
        operations. The call goes through the adapter, so dry-run interception
        and semantic exception mapping behave as usual.

        Example::

            await b1.call_service_method(
                "SBOBobService_SetCurrencyRate",
                {"Currency": "EUR", "Rate": "4.8", "RateDate": "20260811"},
            )
        """
        result = await self._adapter.post(name, data=payload or {})
        return result.data if result else None

    async def post_multipart(
        self, endpoint: str, files: "Sequence[MultipartFile] | MultipartFile"
    ) -> Any:
        """POST ``multipart/form-data`` to any Service Layer endpoint.

        The public file-upload escape hatch: the typed builder and
        ``call_service_method`` only speak JSON, while SAP's file endpoints
        need a multipart body. For ``Attachments2`` prefer the typed
        ``client.attachments.upload()``.

        Dry-run interception and semantic exception mapping behave as usual.

        Example::

            await b1.post_multipart("Attachments2", MultipartFile("a.pdf", data))
        """
        from b1sl.b1sl.models.multipart import MultipartFile

        parts = [files] if isinstance(files, MultipartFile) else list(files)
        result = await self._adapter.post_multipart(endpoint, parts)
        return result.data if result else None

    async def get_binary(self, endpoint: str, params: dict | None = None) -> bytes:
        """GET a raw binary body from any Service Layer endpoint.

        The download counterpart of :meth:`post_multipart`. Ordinary reads
        decode every body as JSON (falling back to text), which corrupts binary
        payloads. For ``Attachments2`` prefer ``client.attachments.download()``.

        Example::

            await b1.get_binary("Attachments2(12)/$value",
                                {"filename": "'invoice.pdf'"})
        """
        return await self._adapter.get_binary(endpoint, ep_params=params)

    # --------------------------------------------------------------------------
    # Concurrency-Elite Aliases (First-Class Citizens with ETag support)
    # --------------------------------------------------------------------------

    # --- Master Data ---

    @property
    def items(self) -> "AsyncGenericResource[Item]":
        """Access the 'Items' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import Item
        return self.get_resource(Item, "Items")

    @property
    def business_partners(self) -> "AsyncGenericResource[BusinessPartner]":
        """Access the 'BusinessPartners' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import BusinessPartner
        return self.get_resource(BusinessPartner, "BusinessPartners")

    @property
    def activities(self) -> "AsyncGenericResource[Activity]":
        """Access the 'Activities' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities import Activity
        return self.get_resource(Activity, "Activities")

    # --- Sales Documents ---

    @property
    def quotations(self) -> "AsyncGenericResource[Document]":
        """Access the 'Quotations' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Quotations")

    @property
    def orders(self) -> "AsyncGenericResource[Document]":
        """Access the 'Orders' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Orders")

    @property
    def delivery_notes(self) -> "AsyncGenericResource[Document]":
        """Access the 'DeliveryNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "DeliveryNotes")

    @property
    def invoices(self) -> "AsyncGenericResource[Document]":
        """Access the 'Invoices' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Invoices")

    @property
    def returns(self) -> "AsyncGenericResource[Document]":
        """Access the 'Returns' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Returns")

    @property
    def return_request(self) -> "AsyncGenericResource[Document]":
        """Access the 'ReturnRequest' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "ReturnRequest")

    @property
    def credit_notes(self) -> "AsyncGenericResource[Document]":
        """Access the 'CreditNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CreditNotes")

    @property
    def down_payments(self) -> "AsyncGenericResource[Document]":
        """Access the 'DownPayments' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "DownPayments")

    @property
    def goods_return_request(self) -> "AsyncGenericResource[Document]":
        """Access the 'GoodsReturnRequest' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "GoodsReturnRequest")

    # --- Purchasing Documents ---

    @property
    def purchase_requests(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseRequests' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseRequests")

    @property
    def purchase_quotations(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseQuotations' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseQuotations")

    @property
    def purchase_orders(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseOrders' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseOrders")

    @property
    def purchase_delivery_notes(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseDeliveryNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseDeliveryNotes")

    @property
    def purchase_invoices(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseInvoices' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseInvoices")

    @property
    def purchase_returns(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseReturns' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseReturns")

    @property
    def purchase_credit_notes(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseCreditNotes' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseCreditNotes")

    @property
    def purchase_down_payments(self) -> "AsyncGenericResource[Document]":
        """Access the 'PurchaseDownPayments' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "PurchaseDownPayments")

    # --- Inventory & Specialized ---

    @property
    def inventory_gen_entries(self) -> "AsyncGenericResource[Document]":
        """Access the 'InventoryGenEntries' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "InventoryGenEntries")

    @property
    def inventory_gen_exits(self) -> "AsyncGenericResource[Document]":
        """Access the 'InventoryGenExits' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "InventoryGenExits")

    @property
    def drafts(self) -> "AsyncGenericResource[Document]":
        """Access the 'Drafts' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "Drafts")

    @property
    def additional_expenses(self) -> "AsyncGenericResource[B1Model]":
        """Access the 'AdditionalExpenses' entity (supports ETags)."""
        from b1sl.b1sl.models.base import B1Model
        return self.get_resource(B1Model, "AdditionalExpenses")

    # --- Correction marketing documents ---

    @property
    def correction_invoice(self) -> "AsyncGenericResource[Document]":
        """Access the 'CorrectionInvoice' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionInvoice")

    @property
    def correction_invoice_reversal(self) -> "AsyncGenericResource[Document]":
        """Access the 'CorrectionInvoiceReversal' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionInvoiceReversal")

    @property
    def correction_purchase_invoice(self) -> "AsyncGenericResource[Document]":
        """Access the 'CorrectionPurchaseInvoice' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionPurchaseInvoice")

    @property
    def correction_purchase_invoice_reversal(self) -> "AsyncGenericResource[Document]":
        """Access the 'CorrectionPurchaseInvoiceReversal' entity (supports ETags)."""
        from b1sl.b1sl.models._generated.entities.general import Document
        return self.get_resource(Document, "CorrectionPurchaseInvoiceReversal")

    # --- SQL Queries ---

    @property
    def sql_queries(self) -> "AsyncSQLQueriesResource":
        """Access the 'SQLQueries' endpoint (supports ETags, run() / run_stream())."""
        from b1sl.b1sl.resources.sql_queries import AsyncSQLQueriesResource
        resource = AsyncSQLQueriesResource(self._adapter)
        return resource

    # --- Attachments ---

    @property
    def attachments(self) -> "AsyncAttachmentsResource":
        """Access the 'Attachments2' endpoint (upload() / download()).

        Specialized resource, not an Elite alias: SAP offers no ETag
        concurrency here, and ``delete()`` is unsupported server-side.
        """
        from b1sl.b1sl.resources.attachments import AsyncAttachmentsResource
        resource = AsyncAttachmentsResource(self._adapter)
        return resource

    def udo(self, table_name: str) -> "AsyncUDOResource":
        """
        Asynchronously access a User Defined Object (UDO) or User Table.

        AI Role: Dynamic accessor for entities not pre-defined in the client.
        """
        from b1sl.b1sl.resources.udo import AsyncUDOResource
        return AsyncUDOResource(adapter=self._adapter, table_name=table_name)

    def crossjoin(self, *entities: str) -> "AsyncCrossJoinQueryBuilder":
        """Build an async ``$crossjoin`` query (SAP HANA only, B1 9.2 patch 07+).

        At least 2 entity names are required.  A bare crossjoin without
        ``$expand`` or ``$apply`` will raise ``ValueError`` before the request.

        Example::

            rows = await (
                client.crossjoin("Orders", "BusinessPartners")
                .expand({"Orders": ["DocEntry", "DocNum"], "BusinessPartners": ["CardCode"]})
                .filter("Orders/CardCode eq BusinessPartners/CardCode")
                .execute()
            )
        """
        from b1sl.b1sl.resources.crossjoin import AsyncCrossJoinQueryBuilder

        return AsyncCrossJoinQueryBuilder(self._adapter, *entities)

    def query_service(self, query_path: str) -> "AsyncQueryServiceBuilder":
        """Async ``QueryService_PostQuery`` row-level filter (SAP HANA only, B1 9.2 PL11+).

        Example::

            rows = await (
                client.query_service("$crossjoin(Orders,Orders/DocumentLines)")
                .expand({
                    "Orders": ["DocEntry", "DocNum"],
                    "Orders/DocumentLines": ["ItemCode", "LineNum"],
                })
                .filter(
                    "Orders/DocEntry eq Orders/DocumentLines/DocEntry"
                    " and Orders/DocumentLines/ItemCode eq 'WIDGET'"
                )
                .execute()
            )
        """
        from b1sl.b1sl.resources.crossjoin import AsyncQueryServiceBuilder

        return AsyncQueryServiceBuilder(self._adapter, query_path)


