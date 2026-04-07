from __future__ import annotations
from typing import Any, TYPE_CHECKING
from pydantic import Field as PydanticField
from b1sl.b1sl.models.base import B1Model, SapBool
from ..enums import *
from ..complex_types import *
if TYPE_CHECKING:
    from .._types import *
    from .businesspartners import *
    from .finance import *
    from .general import *

class LandedCost(B1Model):
    """SAP LandedCost Entity"""
    doc_entry: int | None = PydanticField(None, alias='DocEntry')
    landed_cost_number: int | None = PydanticField(None, alias='LandedCostNumber')
    posting_date: str | None = PydanticField(None, alias='PostingDate')
    due_date: str | None = PydanticField(None, alias='DueDate')
    vendor_code: str | None = PydanticField(None, alias='VendorCode')
    vendor_name: str | None = PydanticField(None, alias='VendorName')
    broker: str | None = PydanticField(None, alias='Broker')
    broker_name: str | None = PydanticField(None, alias='BrokerName')
    closed_document: LandedCostDocStatusEnum | None = PydanticField(None, alias='ClosedDocument')
    file_number: str | None = PydanticField(None, alias='FileNumber')
    remarks: str | None = PydanticField(None, alias='Remarks')
    reference: str | None = PydanticField(None, alias='Reference')
    document_currency: str | None = PydanticField(None, alias='DocumentCurrency')
    document_rate: float | None = PydanticField(None, alias='DocumentRate')
    projected_customs: float | None = PydanticField(None, alias='ProjectedCustoms')
    actual_customs: float | None = PydanticField(None, alias='ActualCustoms')
    actual_customs_fc: float | None = PydanticField(None, alias='ActualCustomsFC')
    tax1: float | None = PydanticField(None, alias='Tax1')
    tax2: float | None = PydanticField(None, alias='Tax2')
    before_tax: float | None = PydanticField(None, alias='BeforeTax')
    total: float | None = PydanticField(None, alias='Total')
    total_freight_charges: float | None = PydanticField(None, alias='TotalFreightCharges')
    projected_customs_fc: float | None = PydanticField(None, alias='ProjectedCustomsFC')
    tax1_fc: float | None = PydanticField(None, alias='Tax1FC')
    tax2_fc: float | None = PydanticField(None, alias='Tax2FC')
    before_tax_fc: float | None = PydanticField(None, alias='BeforeTaxFC')
    total_fc: float | None = PydanticField(None, alias='TotalFC')
    total_freight_charges_fc: float | None = PydanticField(None, alias='TotalFreightChargesFC')
    series: int | None = PydanticField(None, alias='Series')
    customs_affects_inventory: SapBool | None = PydanticField(None, alias='CustomsAffectsInventory')
    amount_to_balance: float | None = PydanticField(None, alias='AmountToBalance')
    amount_to_balance_fc: float | None = PydanticField(None, alias='AmountToBalanceFC')
    billof_lading_number: str | None = PydanticField(None, alias='BillofLadingNumber')
    transport_type: int | None = PydanticField(None, alias='TransportType')
    transaction_number: int | None = PydanticField(None, alias='TransactionNumber')
    journal_remarks: str | None = PydanticField(None, alias='JournalRemarks')
    attachment_entry: int | None = PydanticField(None, alias='AttachmentEntry')
    landed_cost_item_lines: list[LandedCost_ItemLine] | None = PydanticField(None, alias='LandedCost_ItemLines')
    landed_cost_cost_lines: list[LandedCost_CostLine] | None = PydanticField(None, alias='LandedCost_CostLines')
    business_partner: BusinessPartner | None = PydanticField(None, alias='BusinessPartner')
    shipping_type: ShippingType | None = PydanticField(None, alias='ShippingType')
    journal_entry: JournalEntry | None = PydanticField(None, alias='JournalEntry')
    purchase_delivery_notes: list[Document] | None = PydanticField(None, alias='PurchaseDeliveryNotes')

class LandedCostsCode(B1Model):
    """SAP LandedCostsCode Entity"""
    code: str | None = PydanticField(None, alias='Code')
    name: str | None = PydanticField(None, alias='Name')
    allocation_by: BoAllocationByEnum | None = PydanticField(None, alias='AllocationBy')
    landed_costs_allocation_account: str | None = PydanticField(None, alias='LandedCostsAllocationAccount')
