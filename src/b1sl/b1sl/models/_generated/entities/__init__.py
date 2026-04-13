# AUTO-GENERATED — do not edit by hand.
from __future__ import annotations

from . import businesspartners
from . import finance
from . import general
from . import inventory
from . import production
from . import purchasing
from . import sales

from .general import AccountCategory
from .general import AccountSegmentation
from .general import AccountSegmentationCategory
from .general import AccrualType
from .businesspartners import Activity
from .businesspartners import ActivityLocation
from .businesspartners import ActivityRecipientList
from .businesspartners import ActivityStatus
from .businesspartners import ActivitySubject
from .businesspartners import ActivityType
from .general import AdditionalExpense
from .general import AlertManagement
from .general import AlternateCatNum
from .general import ApprovalRequest
from .general import ApprovalStage
from .general import ApprovalTemplate
from .finance import AssetClass
from .general import AssetDepreciationGroup
from .general import AssetDocument
from .general import AssetGroup
from .general import AssetRevaluation
from .general import Attachments2
from .general import AttributeGroup
from .general import B1Session
from .general import BOEDocumentType
from .general import BOEInstruction
from .general import BOEPortfolio
from .general import BPFiscalRegistryID
from .general import BPPriority
from .general import BPVatExemptions
from .general import Bank
from .general import BankChargesAllocationCode
from .general import BankPage
from .general import BankStatement
from .general import BarCode
from .general import BatchNumberDetail
from .general import BillOfExchangeTransaction
from .general import BinLocation
from .general import BinLocationAttribute
from .general import BinLocationField
from .sales import BlanketAgreement
from .general import Branch
from .general import BrazilBeverageIndexer
from .general import BrazilFuelIndexer
from .general import BrazilMultiIndexer
from .general import BrazilNumericIndexer
from .general import BrazilStringIndexer
from .general import Budget
from .general import BudgetDistribution
from .general import BudgetScenario
from .businesspartners import BusinessPartner
from .businesspartners import BusinessPartnerGroup
from .businesspartners import BusinessPartnerProperty
from .general import BusinessPlace
from .general import CIGCode
from .general import CUPCode
from .general import Campaign
from .general import CampaignResponseType
from .general import CashDiscount
from .general import CashFlowLineItem
from .general import CentralBankIndicator
from .general import CertificateSeries
from .finance import ChartOfAccount
from .general import ChecksforPayment
from .general import ChooseFromList
from .general import ClosingDateProcedure
from .general import Cockpit
from .general import ColumnPreferences
from .general import CommissionGroup
from .general import Contact
from .sales import ContractTemplate
from .finance import CostCenterType
from .general import CostElement
from .general import Country
from .general import County
from .general import CreditCard
from .general import CreditCardPayment
from .general import CreditPaymentMethod
from .finance import Currency
from .general import CustomerEquipmentCard
from .general import CustomsDeclaration
from .general import CustomsGroup
from .inventory import CycleCountDetermination
from .general import DNFCodeSetup
from .general import DeductibleTax
from .general import DeductionTaxGroup
from .general import DeductionTaxHierarchy
from .general import DeductionTaxSubGroup
from .general import DefaultElementsforCR
from .general import Department
from .general import Deposit
from .general import DepreciationArea
from .general import DepreciationType
from .general import DepreciationTypePool
from .general import DeterminationCriteria
from .general import Dimension
from .general import DistributionRule
from .general import Document
from .general import DunningLetter
from .general import DunningTerm
from .general import DynamicSystemString
from .general import EBooks
from .general import EWBTransporter
from .general import ElectronicFileFormat
from .general import EmailGroup
from .general import EmployeeIDType
from .general import EmployeeImage
from .general import EmployeeInfo
from .general import EmployeePosition
from .general import EmployeeRoleSetup
from .general import EmployeeStatus
from .general import EmployeeTransfer
from .general import EmploymentCategory
from .general import EnhancedDiscountGroup
from .general import ExceptionalEvent
from .general import ExpenseTypeData
from .general import ExportDetermination
from .general import ExtendedTranslation
from .general import FAAccountDetermination
from .general import FactoringIndicator
from .general import FinancialYear
from .general import FiscalPrinter
from .general import FormattedSearch
from .general import Forms1099
from .general import GLAccountAdvancedRule
from .general import Gender
from .general import GovPayCode
from .general import Holiday
from .general import HouseBankAccount
from .general import IdentificationCode
from .general import ImportDetermination
from .general import IndiaHsn
from .general import IndiaSacCode
from .general import Industry
from .general import IntegrationPackageConfigure
from .general import InternalReconciliation
from .general import IntrastatConfiguration
from .inventory import InventoryCounting
from .inventory import InventoryCountingDraft
from .general import InventoryCycles
from .inventory import InventoryOpeningBalance
from .inventory import InventoryPosting
from .inventory import Item
from .inventory import ItemGroups
from .inventory import ItemImage
from .inventory import ItemProperty
from .finance import JournalEntry
from .finance import JournalEntryDocumentType
from .general import KPI
from .general import KnowledgeBaseSolution
from .purchasing import LandedCost
from .purchasing import LandedCostsCode
from .general import LegalData
from .general import LengthMeasure
from .general import LocalEra
from .general import Manufacturer
from .general import MaterialGroup
from .inventory import MaterialRevaluation
from .general import Message
from .general import MobileAddOnSetting
from .general import MultiLanguageTranslation
from .general import NCMCodeSetup
from .general import NFModel
from .general import NFTaxCategory
from .general import NatureOfAssessee
from .general import NotaFiscalCFOP
from .general import NotaFiscalCST
from .general import NotaFiscalUsage
from .general import OccurenceCode
from .general import PM_ProjectDocumentData
from .general import PM_TimeSheetData
from .general import POSDailySummary
from .general import PackagesType
from .general import PartnersSetup
from .general import Payment
from .general import PaymentBlock
from .general import PaymentReasonCode
from .general import PaymentRunExport
from .general import PaymentTermsType
from .general import PickList
from .general import Picture
from .general import PostingTemplates
from .general import PredefinedText
from .general import PriceList
from .production import ProductTree
from .production import ProductionOrder
from .finance import ProfitCenter
from .general import Project
from .general import PurchaseTaxInvoice
from .general import QueryAuthGroup
from .general import QueryCategory
from .general import Queue
from .general import RecurringPostings
from .general import Relationship
from .general import ReportType
from .production import Resource
from .production import ResourceCapacity
from .production import ResourceGroup
from .production import ResourceProperty
from .general import RetornoCode
from .general import RouteStage
from .general import SQLQuery
from .general import SQLView
from .general import SalesForecast
from .general import SalesOpportunities
from .general import SalesOpportunityCompetitorSetup
from .general import SalesOpportunityInterestSetup
from .general import SalesOpportunityReasonSetup
from .general import SalesOpportunitySourceSetup
from .general import SalesPerson
from .general import SalesStage
from .general import SalesTaxAuthoritiesType
from .general import SalesTaxAuthority
from .general import SalesTaxCode
from .general import SalesTaxInvoice
from .general import Section
from .general import SerialNumberDetail
from .sales import ServiceCall
from .sales import ServiceCallOrigin
from .sales import ServiceCallProblemSubType
from .sales import ServiceCallProblemType
from .sales import ServiceCallSolutionStatus
from .sales import ServiceCallStatus
from .sales import ServiceCallType
from .general import ServiceContract
from .general import ServiceGroup
from .general import ShippingType
from .general import ShortLinkMapping
from .general import SingleUserConnection
from .general import SpecialPrice
from .general import State
from .general import StockTaking
from .inventory import StockTransfer
from .general import TSRExceptionalEvent
from .general import TargetGroup
from .general import TaxCodeDetermination
from .general import TaxCodeDeterminationTCD
from .general import TaxExemptReason
from .general import TaxInvoiceReport
from .general import TaxReplStateSubData
from .general import TaxReportFilter
from .general import TaxWebSite
from .general import Team
from .general import TerminationReason
from .general import Territory
from .general import TrackingNote
from .general import TransactionCode
from .general import TransportationDocumentData
from .general import UnitOfMeasurement
from .general import UnitOfMeasurementGroup
from .general import User
from .general import UserDefaultGroup
from .general import UserFieldMD
from .general import UserGroup
from .general import UserKeysMD
from .general import UserLanguage
from .general import UserObjectsMD
from .general import UserPermissionTree
from .general import UserQuery
from .general import UserTablesMD
from .general import ValueMappingCommunicationData
from .finance import VatGroup
from .general import WTDCode
from .general import WTaxTypeCode
from .inventory import Warehouse
from .inventory import WarehouseLocation
from .inventory import WarehouseSublevelCode
from .general import WebClientBookmarkTile
from .general import WebClientDashboard
from .general import WebClientFormSetting
from .general import WebClientLaunchpad
from .general import WebClientListviewFilter
from .general import WebClientNotification
from .general import WebClientPreference
from .general import WebClientRecentActivity
from .general import WebClientVariant
from .general import WebClientVariantGroup
from .general import WeightMeasure
from .finance import WithholdingTaxCode
from .general import WizardPaymentMethod

_ALL_MODELS = []
_ALL_MODELS.append(general.AccountCategory)
_ALL_MODELS.append(general.AccountSegmentation)
_ALL_MODELS.append(general.AccountSegmentationCategory)
_ALL_MODELS.append(general.AccrualType)
_ALL_MODELS.append(businesspartners.Activity)
_ALL_MODELS.append(businesspartners.ActivityLocation)
_ALL_MODELS.append(businesspartners.ActivityRecipientList)
_ALL_MODELS.append(businesspartners.ActivityStatus)
_ALL_MODELS.append(businesspartners.ActivitySubject)
_ALL_MODELS.append(businesspartners.ActivityType)
_ALL_MODELS.append(general.AdditionalExpense)
_ALL_MODELS.append(general.AlertManagement)
_ALL_MODELS.append(general.AlternateCatNum)
_ALL_MODELS.append(general.ApprovalRequest)
_ALL_MODELS.append(general.ApprovalStage)
_ALL_MODELS.append(general.ApprovalTemplate)
_ALL_MODELS.append(finance.AssetClass)
_ALL_MODELS.append(general.AssetDepreciationGroup)
_ALL_MODELS.append(general.AssetDocument)
_ALL_MODELS.append(general.AssetGroup)
_ALL_MODELS.append(general.AssetRevaluation)
_ALL_MODELS.append(general.Attachments2)
_ALL_MODELS.append(general.AttributeGroup)
_ALL_MODELS.append(general.B1Session)
_ALL_MODELS.append(general.BOEDocumentType)
_ALL_MODELS.append(general.BOEInstruction)
_ALL_MODELS.append(general.BOEPortfolio)
_ALL_MODELS.append(general.BPFiscalRegistryID)
_ALL_MODELS.append(general.BPPriority)
_ALL_MODELS.append(general.BPVatExemptions)
_ALL_MODELS.append(general.Bank)
_ALL_MODELS.append(general.BankChargesAllocationCode)
_ALL_MODELS.append(general.BankPage)
_ALL_MODELS.append(general.BankStatement)
_ALL_MODELS.append(general.BarCode)
_ALL_MODELS.append(general.BatchNumberDetail)
_ALL_MODELS.append(general.BillOfExchangeTransaction)
_ALL_MODELS.append(general.BinLocation)
_ALL_MODELS.append(general.BinLocationAttribute)
_ALL_MODELS.append(general.BinLocationField)
_ALL_MODELS.append(sales.BlanketAgreement)
_ALL_MODELS.append(general.Branch)
_ALL_MODELS.append(general.BrazilBeverageIndexer)
_ALL_MODELS.append(general.BrazilFuelIndexer)
_ALL_MODELS.append(general.BrazilMultiIndexer)
_ALL_MODELS.append(general.BrazilNumericIndexer)
_ALL_MODELS.append(general.BrazilStringIndexer)
_ALL_MODELS.append(general.Budget)
_ALL_MODELS.append(general.BudgetDistribution)
_ALL_MODELS.append(general.BudgetScenario)
_ALL_MODELS.append(businesspartners.BusinessPartner)
_ALL_MODELS.append(businesspartners.BusinessPartnerGroup)
_ALL_MODELS.append(businesspartners.BusinessPartnerProperty)
_ALL_MODELS.append(general.BusinessPlace)
_ALL_MODELS.append(general.CIGCode)
_ALL_MODELS.append(general.CUPCode)
_ALL_MODELS.append(general.Campaign)
_ALL_MODELS.append(general.CampaignResponseType)
_ALL_MODELS.append(general.CashDiscount)
_ALL_MODELS.append(general.CashFlowLineItem)
_ALL_MODELS.append(general.CentralBankIndicator)
_ALL_MODELS.append(general.CertificateSeries)
_ALL_MODELS.append(finance.ChartOfAccount)
_ALL_MODELS.append(general.ChecksforPayment)
_ALL_MODELS.append(general.ChooseFromList)
_ALL_MODELS.append(general.ClosingDateProcedure)
_ALL_MODELS.append(general.Cockpit)
_ALL_MODELS.append(general.ColumnPreferences)
_ALL_MODELS.append(general.CommissionGroup)
_ALL_MODELS.append(general.Contact)
_ALL_MODELS.append(sales.ContractTemplate)
_ALL_MODELS.append(finance.CostCenterType)
_ALL_MODELS.append(general.CostElement)
_ALL_MODELS.append(general.Country)
_ALL_MODELS.append(general.County)
_ALL_MODELS.append(general.CreditCard)
_ALL_MODELS.append(general.CreditCardPayment)
_ALL_MODELS.append(general.CreditPaymentMethod)
_ALL_MODELS.append(finance.Currency)
_ALL_MODELS.append(general.CustomerEquipmentCard)
_ALL_MODELS.append(general.CustomsDeclaration)
_ALL_MODELS.append(general.CustomsGroup)
_ALL_MODELS.append(inventory.CycleCountDetermination)
_ALL_MODELS.append(general.DNFCodeSetup)
_ALL_MODELS.append(general.DeductibleTax)
_ALL_MODELS.append(general.DeductionTaxGroup)
_ALL_MODELS.append(general.DeductionTaxHierarchy)
_ALL_MODELS.append(general.DeductionTaxSubGroup)
_ALL_MODELS.append(general.DefaultElementsforCR)
_ALL_MODELS.append(general.Department)
_ALL_MODELS.append(general.Deposit)
_ALL_MODELS.append(general.DepreciationArea)
_ALL_MODELS.append(general.DepreciationType)
_ALL_MODELS.append(general.DepreciationTypePool)
_ALL_MODELS.append(general.DeterminationCriteria)
_ALL_MODELS.append(general.Dimension)
_ALL_MODELS.append(general.DistributionRule)
_ALL_MODELS.append(general.Document)
_ALL_MODELS.append(general.DunningLetter)
_ALL_MODELS.append(general.DunningTerm)
_ALL_MODELS.append(general.DynamicSystemString)
_ALL_MODELS.append(general.EBooks)
_ALL_MODELS.append(general.EWBTransporter)
_ALL_MODELS.append(general.ElectronicFileFormat)
_ALL_MODELS.append(general.EmailGroup)
_ALL_MODELS.append(general.EmployeeIDType)
_ALL_MODELS.append(general.EmployeeImage)
_ALL_MODELS.append(general.EmployeeInfo)
_ALL_MODELS.append(general.EmployeePosition)
_ALL_MODELS.append(general.EmployeeRoleSetup)
_ALL_MODELS.append(general.EmployeeStatus)
_ALL_MODELS.append(general.EmployeeTransfer)
_ALL_MODELS.append(general.EmploymentCategory)
_ALL_MODELS.append(general.EnhancedDiscountGroup)
_ALL_MODELS.append(general.ExceptionalEvent)
_ALL_MODELS.append(general.ExpenseTypeData)
_ALL_MODELS.append(general.ExportDetermination)
_ALL_MODELS.append(general.ExtendedTranslation)
_ALL_MODELS.append(general.FAAccountDetermination)
_ALL_MODELS.append(general.FactoringIndicator)
_ALL_MODELS.append(general.FinancialYear)
_ALL_MODELS.append(general.FiscalPrinter)
_ALL_MODELS.append(general.FormattedSearch)
_ALL_MODELS.append(general.Forms1099)
_ALL_MODELS.append(general.GLAccountAdvancedRule)
_ALL_MODELS.append(general.Gender)
_ALL_MODELS.append(general.GovPayCode)
_ALL_MODELS.append(general.Holiday)
_ALL_MODELS.append(general.HouseBankAccount)
_ALL_MODELS.append(general.IdentificationCode)
_ALL_MODELS.append(general.ImportDetermination)
_ALL_MODELS.append(general.IndiaHsn)
_ALL_MODELS.append(general.IndiaSacCode)
_ALL_MODELS.append(general.Industry)
_ALL_MODELS.append(general.IntegrationPackageConfigure)
_ALL_MODELS.append(general.InternalReconciliation)
_ALL_MODELS.append(general.IntrastatConfiguration)
_ALL_MODELS.append(inventory.InventoryCounting)
_ALL_MODELS.append(inventory.InventoryCountingDraft)
_ALL_MODELS.append(general.InventoryCycles)
_ALL_MODELS.append(inventory.InventoryOpeningBalance)
_ALL_MODELS.append(inventory.InventoryPosting)
from ..._overrides.inventory import Item
_ALL_MODELS.append(Item)
_ALL_MODELS.append(inventory.ItemGroups)
_ALL_MODELS.append(inventory.ItemImage)
_ALL_MODELS.append(inventory.ItemProperty)
_ALL_MODELS.append(finance.JournalEntry)
_ALL_MODELS.append(finance.JournalEntryDocumentType)
_ALL_MODELS.append(general.KPI)
_ALL_MODELS.append(general.KnowledgeBaseSolution)
_ALL_MODELS.append(purchasing.LandedCost)
_ALL_MODELS.append(purchasing.LandedCostsCode)
_ALL_MODELS.append(general.LegalData)
_ALL_MODELS.append(general.LengthMeasure)
_ALL_MODELS.append(general.LocalEra)
_ALL_MODELS.append(general.Manufacturer)
_ALL_MODELS.append(general.MaterialGroup)
_ALL_MODELS.append(inventory.MaterialRevaluation)
_ALL_MODELS.append(general.Message)
_ALL_MODELS.append(general.MobileAddOnSetting)
_ALL_MODELS.append(general.MultiLanguageTranslation)
_ALL_MODELS.append(general.NCMCodeSetup)
_ALL_MODELS.append(general.NFModel)
_ALL_MODELS.append(general.NFTaxCategory)
_ALL_MODELS.append(general.NatureOfAssessee)
_ALL_MODELS.append(general.NotaFiscalCFOP)
_ALL_MODELS.append(general.NotaFiscalCST)
_ALL_MODELS.append(general.NotaFiscalUsage)
_ALL_MODELS.append(general.OccurenceCode)
_ALL_MODELS.append(general.PM_ProjectDocumentData)
_ALL_MODELS.append(general.PM_TimeSheetData)
_ALL_MODELS.append(general.POSDailySummary)
_ALL_MODELS.append(general.PackagesType)
_ALL_MODELS.append(general.PartnersSetup)
_ALL_MODELS.append(general.Payment)
_ALL_MODELS.append(general.PaymentBlock)
_ALL_MODELS.append(general.PaymentReasonCode)
_ALL_MODELS.append(general.PaymentRunExport)
_ALL_MODELS.append(general.PaymentTermsType)
_ALL_MODELS.append(general.PickList)
_ALL_MODELS.append(general.Picture)
_ALL_MODELS.append(general.PostingTemplates)
_ALL_MODELS.append(general.PredefinedText)
_ALL_MODELS.append(general.PriceList)
_ALL_MODELS.append(production.ProductTree)
_ALL_MODELS.append(production.ProductionOrder)
_ALL_MODELS.append(finance.ProfitCenter)
_ALL_MODELS.append(general.Project)
_ALL_MODELS.append(general.PurchaseTaxInvoice)
_ALL_MODELS.append(general.QueryAuthGroup)
_ALL_MODELS.append(general.QueryCategory)
_ALL_MODELS.append(general.Queue)
_ALL_MODELS.append(general.RecurringPostings)
_ALL_MODELS.append(general.Relationship)
_ALL_MODELS.append(general.ReportType)
_ALL_MODELS.append(production.Resource)
_ALL_MODELS.append(production.ResourceCapacity)
_ALL_MODELS.append(production.ResourceGroup)
_ALL_MODELS.append(production.ResourceProperty)
_ALL_MODELS.append(general.RetornoCode)
_ALL_MODELS.append(general.RouteStage)
_ALL_MODELS.append(general.SQLQuery)
_ALL_MODELS.append(general.SQLView)
_ALL_MODELS.append(general.SalesForecast)
_ALL_MODELS.append(general.SalesOpportunities)
_ALL_MODELS.append(general.SalesOpportunityCompetitorSetup)
_ALL_MODELS.append(general.SalesOpportunityInterestSetup)
_ALL_MODELS.append(general.SalesOpportunityReasonSetup)
_ALL_MODELS.append(general.SalesOpportunitySourceSetup)
_ALL_MODELS.append(general.SalesPerson)
_ALL_MODELS.append(general.SalesStage)
_ALL_MODELS.append(general.SalesTaxAuthoritiesType)
_ALL_MODELS.append(general.SalesTaxAuthority)
_ALL_MODELS.append(general.SalesTaxCode)
_ALL_MODELS.append(general.SalesTaxInvoice)
_ALL_MODELS.append(general.Section)
_ALL_MODELS.append(general.SerialNumberDetail)
_ALL_MODELS.append(sales.ServiceCall)
_ALL_MODELS.append(sales.ServiceCallOrigin)
_ALL_MODELS.append(sales.ServiceCallProblemSubType)
_ALL_MODELS.append(sales.ServiceCallProblemType)
_ALL_MODELS.append(sales.ServiceCallSolutionStatus)
_ALL_MODELS.append(sales.ServiceCallStatus)
_ALL_MODELS.append(sales.ServiceCallType)
_ALL_MODELS.append(general.ServiceContract)
_ALL_MODELS.append(general.ServiceGroup)
_ALL_MODELS.append(general.ShippingType)
_ALL_MODELS.append(general.ShortLinkMapping)
_ALL_MODELS.append(general.SingleUserConnection)
_ALL_MODELS.append(general.SpecialPrice)
_ALL_MODELS.append(general.State)
_ALL_MODELS.append(general.StockTaking)
_ALL_MODELS.append(inventory.StockTransfer)
_ALL_MODELS.append(general.TSRExceptionalEvent)
_ALL_MODELS.append(general.TargetGroup)
_ALL_MODELS.append(general.TaxCodeDetermination)
_ALL_MODELS.append(general.TaxCodeDeterminationTCD)
_ALL_MODELS.append(general.TaxExemptReason)
_ALL_MODELS.append(general.TaxInvoiceReport)
_ALL_MODELS.append(general.TaxReplStateSubData)
_ALL_MODELS.append(general.TaxReportFilter)
_ALL_MODELS.append(general.TaxWebSite)
_ALL_MODELS.append(general.Team)
_ALL_MODELS.append(general.TerminationReason)
_ALL_MODELS.append(general.Territory)
_ALL_MODELS.append(general.TrackingNote)
_ALL_MODELS.append(general.TransactionCode)
_ALL_MODELS.append(general.TransportationDocumentData)
_ALL_MODELS.append(general.UnitOfMeasurement)
_ALL_MODELS.append(general.UnitOfMeasurementGroup)
_ALL_MODELS.append(general.User)
_ALL_MODELS.append(general.UserDefaultGroup)
_ALL_MODELS.append(general.UserFieldMD)
_ALL_MODELS.append(general.UserGroup)
_ALL_MODELS.append(general.UserKeysMD)
_ALL_MODELS.append(general.UserLanguage)
_ALL_MODELS.append(general.UserObjectsMD)
_ALL_MODELS.append(general.UserPermissionTree)
_ALL_MODELS.append(general.UserQuery)
_ALL_MODELS.append(general.UserTablesMD)
_ALL_MODELS.append(general.ValueMappingCommunicationData)
_ALL_MODELS.append(finance.VatGroup)
_ALL_MODELS.append(general.WTDCode)
_ALL_MODELS.append(general.WTaxTypeCode)
_ALL_MODELS.append(inventory.Warehouse)
_ALL_MODELS.append(inventory.WarehouseLocation)
_ALL_MODELS.append(inventory.WarehouseSublevelCode)
_ALL_MODELS.append(general.WebClientBookmarkTile)
_ALL_MODELS.append(general.WebClientDashboard)
_ALL_MODELS.append(general.WebClientFormSetting)
_ALL_MODELS.append(general.WebClientLaunchpad)
_ALL_MODELS.append(general.WebClientListviewFilter)
_ALL_MODELS.append(general.WebClientNotification)
_ALL_MODELS.append(general.WebClientPreference)
_ALL_MODELS.append(general.WebClientRecentActivity)
_ALL_MODELS.append(general.WebClientVariant)
_ALL_MODELS.append(general.WebClientVariantGroup)
_ALL_MODELS.append(general.WeightMeasure)
_ALL_MODELS.append(finance.WithholdingTaxCode)
_ALL_MODELS.append(general.WizardPaymentMethod)

# Master namespace for cross-domain resolution
_NAMESPACE = {m.__name__: m for m in _ALL_MODELS}

# Rebuild models to resolve circular dependencies
for model in _ALL_MODELS:
    model.model_rebuild(_types_namespace=_NAMESPACE)
