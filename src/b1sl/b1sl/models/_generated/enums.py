from __future__ import annotations
from enum import Enum, StrEnum
from typing import TYPE_CHECKING, Literal

class AccountCategorySourceEnum(StrEnum):
    acsBalanceSheet = 'acsBalanceSheet'
    acsProfitAndLoss = 'acsProfitAndLoss'
    acsTrialBalance = 'acsTrialBalance'

if TYPE_CHECKING:
    AccountCategorySourceEnumField = AccountCategorySourceEnum | Literal['acsBalanceSheet', 'acsProfitAndLoss', 'acsTrialBalance']
else:
    AccountCategorySourceEnumField = AccountCategorySourceEnum

class AccountSegmentationTypeEnum(StrEnum):
    ast_Alphanumeric = 'ast_Alphanumeric'
    ast_Numeric = 'ast_Numeric'

if TYPE_CHECKING:
    AccountSegmentationTypeEnumField = AccountSegmentationTypeEnum | Literal['ast_Alphanumeric', 'ast_Numeric']
else:
    AccountSegmentationTypeEnumField = AccountSegmentationTypeEnum

class AcquisitionPeriodControlEnum(StrEnum):
    apcProRataTemporis = 'apcProRataTemporis'
    apcFirstYearConvention = 'apcFirstYearConvention'
    apcHalfYear = 'apcHalfYear'
    apcFullYear = 'apcFullYear'

if TYPE_CHECKING:
    AcquisitionPeriodControlEnumField = AcquisitionPeriodControlEnum | Literal['apcProRataTemporis', 'apcFirstYearConvention', 'apcHalfYear', 'apcFullYear']
else:
    AcquisitionPeriodControlEnumField = AcquisitionPeriodControlEnum

class AcquisitionProRataTypeEnum(StrEnum):
    aprtExactlyDailyBase = 'aprtExactlyDailyBase'
    aprtFirstDayOfCurrentPeriod = 'aprtFirstDayOfCurrentPeriod'
    aprtFirstDayOfNextPeriod = 'aprtFirstDayOfNextPeriod'

if TYPE_CHECKING:
    AcquisitionProRataTypeEnumField = AcquisitionProRataTypeEnum | Literal['aprtExactlyDailyBase', 'aprtFirstDayOfCurrentPeriod', 'aprtFirstDayOfNextPeriod']
else:
    AcquisitionProRataTypeEnumField = AcquisitionProRataTypeEnum

class ActivityRecipientObjTypeEnum(StrEnum):
    arotUser = 'arotUser'
    arotEmployee = 'arotEmployee'
    arotRecipientList = 'arotRecipientList'

if TYPE_CHECKING:
    ActivityRecipientObjTypeEnumField = ActivityRecipientObjTypeEnum | Literal['arotUser', 'arotEmployee', 'arotRecipientList']
else:
    ActivityRecipientObjTypeEnumField = ActivityRecipientObjTypeEnum

class AlertManagementDocumentEnum(StrEnum):
    atd_NOB = 'atd_NOB'
    atd_Invoices = 'atd_Invoices'
    atd_RevertInvoice = 'atd_RevertInvoice'
    atd_DeliveryNotes = 'atd_DeliveryNotes'
    atd_Returns = 'atd_Returns'
    atd_Orders = 'atd_Orders'
    atd_PurchaseInvoices = 'atd_PurchaseInvoices'
    atd_PurchaseDeliveryNotes = 'atd_PurchaseDeliveryNotes'
    atd_PurchaseOrders = 'atd_PurchaseOrders'
    atd_Quotations = 'atd_Quotations'
    atd_IncomingPayments = 'atd_IncomingPayments'
    atd_JournalEntries = 'atd_JournalEntries'
    atd_OutgoingPayments = 'atd_OutgoingPayments'
    atd_ChecksForPayment = 'atd_ChecksForPayment'
    atd_CorrectionInvoice = 'atd_CorrectionInvoice'
    atd_DownPaymentIncoming = 'atd_DownPaymentIncoming'
    atd_DownPaymentOutgoing = 'atd_DownPaymentOutgoing'

if TYPE_CHECKING:
    AlertManagementDocumentEnumField = AlertManagementDocumentEnum | Literal['atd_NOB', 'atd_Invoices', 'atd_RevertInvoice', 'atd_DeliveryNotes', 'atd_Returns', 'atd_Orders', 'atd_PurchaseInvoices', 'atd_PurchaseDeliveryNotes', 'atd_PurchaseOrders', 'atd_Quotations', 'atd_IncomingPayments', 'atd_JournalEntries', 'atd_OutgoingPayments', 'atd_ChecksForPayment', 'atd_CorrectionInvoice', 'atd_DownPaymentIncoming', 'atd_DownPaymentOutgoing']
else:
    AlertManagementDocumentEnumField = AlertManagementDocumentEnum

class AlertManagementFrequencyType(StrEnum):
    atfi_Minutes = 'atfi_Minutes'
    atfi_Hours = 'atfi_Hours'
    atfi_Days = 'atfi_Days'
    atfi_Weeks = 'atfi_Weeks'
    atfi_Monthly = 'atfi_Monthly'

if TYPE_CHECKING:
    AlertManagementFrequencyTypeField = AlertManagementFrequencyType | Literal['atfi_Minutes', 'atfi_Hours', 'atfi_Days', 'atfi_Weeks', 'atfi_Monthly']
else:
    AlertManagementFrequencyTypeField = AlertManagementFrequencyType

class AlertManagementPriorityEnum(StrEnum):
    atp_Low = 'atp_Low'
    atp_Normal = 'atp_Normal'
    atp_High = 'atp_High'

if TYPE_CHECKING:
    AlertManagementPriorityEnumField = AlertManagementPriorityEnum | Literal['atp_Low', 'atp_Normal', 'atp_High']
else:
    AlertManagementPriorityEnumField = AlertManagementPriorityEnum

class AlertManagementTypeEnum(StrEnum):
    att_User = 'att_User'
    att_System = 'att_System'

if TYPE_CHECKING:
    AlertManagementTypeEnumField = AlertManagementTypeEnum | Literal['att_User', 'att_System']
else:
    AlertManagementTypeEnumField = AlertManagementTypeEnum

class AmountCatTypeEnum(StrEnum):
    act_Open = 'act_Open'
    act_Invoiced = 'act_Invoiced'

if TYPE_CHECKING:
    AmountCatTypeEnumField = AmountCatTypeEnum | Literal['act_Open', 'act_Invoiced']
else:
    AmountCatTypeEnumField = AmountCatTypeEnum

class ApprovalTemplateConditionTypeEnum(StrEnum):
    atctUndefined = 'atctUndefined'
    atctDeviationFromCreditLine = 'atctDeviationFromCreditLine'
    atctDeviationFromObligo = 'atctDeviationFromObligo'
    atctGrossProfitPercent = 'atctGrossProfitPercent'
    atctDiscountPercent = 'atctDiscountPercent'
    atctDeviationFromBudget = 'atctDeviationFromBudget'
    atctTotalDocument = 'atctTotalDocument'
    atctItemCode = 'atctItemCode'
    atctTotalLine = 'atctTotalLine'
    atctCountedQuantity = 'atctCountedQuantity'
    atctQuantity = 'atctQuantity'
    atctVariance = 'atctVariance'
    atctVariancePercent = 'atctVariancePercent'

if TYPE_CHECKING:
    ApprovalTemplateConditionTypeEnumField = ApprovalTemplateConditionTypeEnum | Literal['atctUndefined', 'atctDeviationFromCreditLine', 'atctDeviationFromObligo', 'atctGrossProfitPercent', 'atctDiscountPercent', 'atctDeviationFromBudget', 'atctTotalDocument', 'atctItemCode', 'atctTotalLine', 'atctCountedQuantity', 'atctQuantity', 'atctVariance', 'atctVariancePercent']
else:
    ApprovalTemplateConditionTypeEnumField = ApprovalTemplateConditionTypeEnum

class ApprovalTemplateOperationTypeEnum(StrEnum):
    opcodeUndefined = 'opcodeUndefined'
    opcodeGreaterThan = 'opcodeGreaterThan'
    opcodeGreaterOrEqual = 'opcodeGreaterOrEqual'
    opcodeLessThan = 'opcodeLessThan'
    opcodeLessOrEqual = 'opcodeLessOrEqual'
    opcodeEqual = 'opcodeEqual'
    opcodeDoesNotEqual = 'opcodeDoesNotEqual'
    opcodeInRange = 'opcodeInRange'
    opcodeNotInRange = 'opcodeNotInRange'

if TYPE_CHECKING:
    ApprovalTemplateOperationTypeEnumField = ApprovalTemplateOperationTypeEnum | Literal['opcodeUndefined', 'opcodeGreaterThan', 'opcodeGreaterOrEqual', 'opcodeLessThan', 'opcodeLessOrEqual', 'opcodeEqual', 'opcodeDoesNotEqual', 'opcodeInRange', 'opcodeNotInRange']
else:
    ApprovalTemplateOperationTypeEnumField = ApprovalTemplateOperationTypeEnum

class ApprovalTemplatesDocumentTypeEnum(StrEnum):
    atdtQuotation = 'atdtQuotation'
    atdtOrder = 'atdtOrder'
    atdtDelivery = 'atdtDelivery'
    atdtReturns = 'atdtReturns'
    atdtArDownPayment = 'atdtArDownPayment'
    atdtArInvoice = 'atdtArInvoice'
    atdtArCreditMemo = 'atdtArCreditMemo'
    atdtCorrectionInvoice = 'atdtCorrectionInvoice'
    atdtPurchaseOrder = 'atdtPurchaseOrder'
    atdtGoodsReceiptPO = 'atdtGoodsReceiptPO'
    atdtGoodsReturns = 'atdtGoodsReturns'
    atdtApDownPayment = 'atdtApDownPayment'
    atdtApInvoice = 'atdtApInvoice'
    atdtApCreditMemo = 'atdtApCreditMemo'
    atdtGoodsReceipt = 'atdtGoodsReceipt'
    atdtGoodsIssue = 'atdtGoodsIssue'
    atdtInventoryTransfer = 'atdtInventoryTransfer'
    atdtPurchaseQuotation = 'atdtPurchaseQuotation'
    atdtInventoryTransferRequest = 'atdtInventoryTransferRequest'
    atdtOutgoingPayment = 'atdtOutgoingPayment'
    atdtInventoryCounting = 'atdtInventoryCounting'
    atdtInventoryPosting = 'atdtInventoryPosting'
    atdtInventoryOpeningBalance = 'atdtInventoryOpeningBalance'
    atdtReturnRequest = 'atdtReturnRequest'
    atdtGoodsReturnRequest = 'atdtGoodsReturnRequest'
    atdtBlanketAgreement = 'atdtBlanketAgreement'
    atdtSalesBlanketAgreement = 'atdtSalesBlanketAgreement'
    atdtPurchaseBlanketAgreement = 'atdtPurchaseBlanketAgreement'
    atdtPurchaseRequest = 'atdtPurchaseRequest'
    atdtSelfInvoice = 'atdtSelfInvoice'
    atdtSelfCreditMemo = 'atdtSelfCreditMemo'

if TYPE_CHECKING:
    ApprovalTemplatesDocumentTypeEnumField = ApprovalTemplatesDocumentTypeEnum | Literal['atdtQuotation', 'atdtOrder', 'atdtDelivery', 'atdtReturns', 'atdtArDownPayment', 'atdtArInvoice', 'atdtArCreditMemo', 'atdtCorrectionInvoice', 'atdtPurchaseOrder', 'atdtGoodsReceiptPO', 'atdtGoodsReturns', 'atdtApDownPayment', 'atdtApInvoice', 'atdtApCreditMemo', 'atdtGoodsReceipt', 'atdtGoodsIssue', 'atdtInventoryTransfer', 'atdtPurchaseQuotation', 'atdtInventoryTransferRequest', 'atdtOutgoingPayment', 'atdtInventoryCounting', 'atdtInventoryPosting', 'atdtInventoryOpeningBalance', 'atdtReturnRequest', 'atdtGoodsReturnRequest', 'atdtBlanketAgreement', 'atdtSalesBlanketAgreement', 'atdtPurchaseBlanketAgreement', 'atdtPurchaseRequest', 'atdtSelfInvoice', 'atdtSelfCreditMemo']
else:
    ApprovalTemplatesDocumentTypeEnumField = ApprovalTemplatesDocumentTypeEnum

class AreaTypeEnum(StrEnum):
    atPostingtoGL = 'atPostingtoGL'
    atAdditionalArea = 'atAdditionalArea'
    atDerivedArea = 'atDerivedArea'

if TYPE_CHECKING:
    AreaTypeEnumField = AreaTypeEnum | Literal['atPostingtoGL', 'atAdditionalArea', 'atDerivedArea']
else:
    AreaTypeEnumField = AreaTypeEnum

class AssesseeTypeEnum(StrEnum):
    atCompany = 'atCompany'
    atOthers = 'atOthers'

if TYPE_CHECKING:
    AssesseeTypeEnumField = AssesseeTypeEnum | Literal['atCompany', 'atOthers']
else:
    AssesseeTypeEnumField = AssesseeTypeEnum

class AssetDocumentStatusEnum(StrEnum):
    adsPosted = 'adsPosted'
    adsDraft = 'adsDraft'
    adsCancelled = 'adsCancelled'

if TYPE_CHECKING:
    AssetDocumentStatusEnumField = AssetDocumentStatusEnum | Literal['adsPosted', 'adsDraft', 'adsCancelled']
else:
    AssetDocumentStatusEnumField = AssetDocumentStatusEnum

class AssetDocumentTypeEnum(StrEnum):
    adtOrdinaryDepreciation = 'adtOrdinaryDepreciation'
    adtUnplannedDepreciation = 'adtUnplannedDepreciation'
    adtSpecialDepreciation = 'adtSpecialDepreciation'
    adtAppreciation = 'adtAppreciation'
    adtAssetTransfer = 'adtAssetTransfer'
    adtSales = 'adtSales'
    adtScrapping = 'adtScrapping'
    adtAssetClassTransfer = 'adtAssetClassTransfer'

if TYPE_CHECKING:
    AssetDocumentTypeEnumField = AssetDocumentTypeEnum | Literal['adtOrdinaryDepreciation', 'adtUnplannedDepreciation', 'adtSpecialDepreciation', 'adtAppreciation', 'adtAssetTransfer', 'adtSales', 'adtScrapping', 'adtAssetClassTransfer']
else:
    AssetDocumentTypeEnumField = AssetDocumentTypeEnum

class AssetOriginalTypeEnum(StrEnum):
    aotARInvoice = 'aotARInvoice'
    aotAPCreditMemo = 'aotAPCreditMemo'
    aotAPInvoice = 'aotAPInvoice'
    aotOutgoingPayment = 'aotOutgoingPayment'
    aotAPCorrectionInvoice = 'aotAPCorrectionInvoice'
    aotCapitalization = 'aotCapitalization'
    aotFixedAssetsCreditMemo = 'aotFixedAssetsCreditMemo'
    aotAllTransactions = 'aotAllTransactions'
    aotManualDepreciation = 'aotManualDepreciation'
    aotFixedAssetsTransfer = 'aotFixedAssetsTransfer'
    aotRetirement = 'aotRetirement'

if TYPE_CHECKING:
    AssetOriginalTypeEnumField = AssetOriginalTypeEnum | Literal['aotARInvoice', 'aotAPCreditMemo', 'aotAPInvoice', 'aotOutgoingPayment', 'aotAPCorrectionInvoice', 'aotCapitalization', 'aotFixedAssetsCreditMemo', 'aotAllTransactions', 'aotManualDepreciation', 'aotFixedAssetsTransfer', 'aotRetirement']
else:
    AssetOriginalTypeEnumField = AssetOriginalTypeEnum

class AssetStatusEnum(StrEnum):
    New = 'New'
    Active = 'Active'
    Inactive = 'Inactive'

if TYPE_CHECKING:
    AssetStatusEnumField = AssetStatusEnum | Literal['New', 'Active', 'Inactive']
else:
    AssetStatusEnumField = AssetStatusEnum

class AssetTransactionTypeEnum(StrEnum):
    att_BeginningOfYear = 'att_BeginningOfYear'
    att_Acquistion = 'att_Acquistion'
    att_Retirement = 'att_Retirement'
    att_Transfer = 'att_Transfer'
    att_WriteUp = 'att_WriteUp'
    att_OrdinaryDepreciation = 'att_OrdinaryDepreciation'
    att_UplannedDepreciation = 'att_UplannedDepreciation'
    att_SpecialDepreciation = 'att_SpecialDepreciation'
    att_EndOfYear = 'att_EndOfYear'

if TYPE_CHECKING:
    AssetTransactionTypeEnumField = AssetTransactionTypeEnum | Literal['att_BeginningOfYear', 'att_Acquistion', 'att_Retirement', 'att_Transfer', 'att_WriteUp', 'att_OrdinaryDepreciation', 'att_UplannedDepreciation', 'att_SpecialDepreciation', 'att_EndOfYear']
else:
    AssetTransactionTypeEnumField = AssetTransactionTypeEnum

class AssetTypeEnum(StrEnum):
    atAssetTypeGeneral = 'atAssetTypeGeneral'
    atAssetTypeLowValueAsset = 'atAssetTypeLowValueAsset'

if TYPE_CHECKING:
    AssetTypeEnumField = AssetTypeEnum | Literal['atAssetTypeGeneral', 'atAssetTypeLowValueAsset']
else:
    AssetTypeEnumField = AssetTypeEnum

class AttributeGroupFieldTypeEnum(StrEnum):
    agftText = 'agftText'
    agftNumeric = 'agftNumeric'
    agftDate = 'agftDate'
    agftAmount = 'agftAmount'
    agftPrice = 'agftPrice'
    agftQuantity = 'agftQuantity'

if TYPE_CHECKING:
    AttributeGroupFieldTypeEnumField = AttributeGroupFieldTypeEnum | Literal['agftText', 'agftNumeric', 'agftDate', 'agftAmount', 'agftPrice', 'agftQuantity']
else:
    AttributeGroupFieldTypeEnumField = AttributeGroupFieldTypeEnum

class AuthenticateUserResultsEnum(StrEnum):
    aturNoUserConnectedToCompany = 'aturNoUserConnectedToCompany'
    aturUsernamePasswordMatched = 'aturUsernamePasswordMatched'
    aturLogOnUserNotAdmin = 'aturLogOnUserNotAdmin'
    aturBadUserOrPassword = 'aturBadUserOrPassword'
    aturUserHasBeenLocked = 'aturUserHasBeenLocked'
    aturPasswordExpired = 'aturPasswordExpired'
    aturDBErrors = 'aturDBErrors'
    aturWrongDomainName = 'aturWrongDomainName'

if TYPE_CHECKING:
    AuthenticateUserResultsEnumField = AuthenticateUserResultsEnum | Literal['aturNoUserConnectedToCompany', 'aturUsernamePasswordMatched', 'aturLogOnUserNotAdmin', 'aturBadUserOrPassword', 'aturUserHasBeenLocked', 'aturPasswordExpired', 'aturDBErrors', 'aturWrongDomainName']
else:
    AuthenticateUserResultsEnumField = AuthenticateUserResultsEnum

class AutoAllocOnReceiptMethodEnum(StrEnum):
    aaormDefaultBin = 'aaormDefaultBin'
    aaormItemCurrentAndHistoricalBins = 'aaormItemCurrentAndHistoricalBins'
    aaormItemCurrentBins = 'aaormItemCurrentBins'
    aaormLastBinReceivedItem = 'aaormLastBinReceivedItem'

if TYPE_CHECKING:
    AutoAllocOnReceiptMethodEnumField = AutoAllocOnReceiptMethodEnum | Literal['aaormDefaultBin', 'aaormItemCurrentAndHistoricalBins', 'aaormItemCurrentBins', 'aaormLastBinReceivedItem']
else:
    AutoAllocOnReceiptMethodEnumField = AutoAllocOnReceiptMethodEnum

class AutomaticPostingEnum(StrEnum):
    apNo = 'apNo'
    apInterestAndFee = 'apInterestAndFee'
    apInterestOnly = 'apInterestOnly'
    apFeeOnly = 'apFeeOnly'

if TYPE_CHECKING:
    AutomaticPostingEnumField = AutomaticPostingEnum | Literal['apNo', 'apInterestAndFee', 'apInterestOnly', 'apFeeOnly']
else:
    AutomaticPostingEnumField = AutomaticPostingEnum

class BADivationAlertLevelEnum(StrEnum):
    badal_NoWarning = 'badal_NoWarning'
    badal_Warning = 'badal_Warning'
    badal_Block = 'badal_Block'

if TYPE_CHECKING:
    BADivationAlertLevelEnumField = BADivationAlertLevelEnum | Literal['badal_NoWarning', 'badal_Warning', 'badal_Block']
else:
    BADivationAlertLevelEnumField = BADivationAlertLevelEnum

class BADocumentStatus(StrEnum):
    bads_Open = 'bads_Open'
    bads_Closed = 'bads_Closed'
    bads_Cancelled = 'bads_Cancelled'

if TYPE_CHECKING:
    BADocumentStatusField = BADocumentStatus | Literal['bads_Open', 'bads_Closed', 'bads_Cancelled']
else:
    BADocumentStatusField = BADocumentStatus

class BankStatementDocTypeEnum(StrEnum):
    bsdtReceipts = 'bsdtReceipts'
    bsdtPaymentToVendor = 'bsdtPaymentToVendor'
    bsdtInvoices = 'bsdtInvoices'
    bsdtPurchases = 'bsdtPurchases'
    bsdtDownPaymentIncoming = 'bsdtDownPaymentIncoming'
    bsdtDownPaymentOutgoing = 'bsdtDownPaymentOutgoing'
    bsdtRevertInvoices = 'bsdtRevertInvoices'
    bsdtRevertPurchases = 'bsdtRevertPurchases'
    bsdtJournalEntry = 'bsdtJournalEntry'

if TYPE_CHECKING:
    BankStatementDocTypeEnumField = BankStatementDocTypeEnum | Literal['bsdtReceipts', 'bsdtPaymentToVendor', 'bsdtInvoices', 'bsdtPurchases', 'bsdtDownPaymentIncoming', 'bsdtDownPaymentOutgoing', 'bsdtRevertInvoices', 'bsdtRevertPurchases', 'bsdtJournalEntry']
else:
    BankStatementDocTypeEnumField = BankStatementDocTypeEnum

class BankStatementRowSourceEnum(StrEnum):
    bsImported = 'bsImported'
    bsImportedAndAmended = 'bsImportedAndAmended'
    bsManuallyEntered = 'bsManuallyEntered'

if TYPE_CHECKING:
    BankStatementRowSourceEnumField = BankStatementRowSourceEnum | Literal['bsImported', 'bsImportedAndAmended', 'bsManuallyEntered']
else:
    BankStatementRowSourceEnumField = BankStatementRowSourceEnum

class BankStatementStatusEnum(StrEnum):
    bssExecuted = 'bssExecuted'
    bssDraft = 'bssDraft'
    bssOld = 'bssOld'

if TYPE_CHECKING:
    BankStatementStatusEnumField = BankStatementStatusEnum | Literal['bssExecuted', 'bssDraft', 'bssOld']
else:
    BankStatementStatusEnumField = BankStatementStatusEnum

class BaseDateSelectEnum(StrEnum):
    bdsFromDueDate = 'bdsFromDueDate'
    bdsFromLastDunningRun = 'bdsFromLastDunningRun'

if TYPE_CHECKING:
    BaseDateSelectEnumField = BaseDateSelectEnum | Literal['bdsFromDueDate', 'bdsFromLastDunningRun']
else:
    BaseDateSelectEnumField = BaseDateSelectEnum

class BatchDetailServiceStatusEnum(StrEnum):
    bdsStatus_Released = 'bdsStatus_Released'
    bdsStatus_NotAccessible = 'bdsStatus_NotAccessible'
    bdsStatus_Locked = 'bdsStatus_Locked'

if TYPE_CHECKING:
    BatchDetailServiceStatusEnumField = BatchDetailServiceStatusEnum | Literal['bdsStatus_Released', 'bdsStatus_NotAccessible', 'bdsStatus_Locked']
else:
    BatchDetailServiceStatusEnumField = BatchDetailServiceStatusEnum

class BinActionTypeEnum(StrEnum):
    batToWarehouse = 'batToWarehouse'
    batFromWarehouse = 'batFromWarehouse'

if TYPE_CHECKING:
    BinActionTypeEnumField = BinActionTypeEnum | Literal['batToWarehouse', 'batFromWarehouse']
else:
    BinActionTypeEnumField = BinActionTypeEnum

class BinLocationFieldTypeEnum(StrEnum):
    blftWarehouseSublevel = 'blftWarehouseSublevel'
    blftBinLocationAttribute = 'blftBinLocationAttribute'

if TYPE_CHECKING:
    BinLocationFieldTypeEnumField = BinLocationFieldTypeEnum | Literal['blftWarehouseSublevel', 'blftBinLocationAttribute']
else:
    BinLocationFieldTypeEnumField = BinLocationFieldTypeEnum

class BinRestrictItemEnum(StrEnum):
    briNone = 'briNone'
    briSpecificItem = 'briSpecificItem'
    briSingleItemOnly = 'briSingleItemOnly'
    briSpecificItemGroup = 'briSpecificItemGroup'
    briSpecificItemGroupOnly = 'briSpecificItemGroupOnly'

if TYPE_CHECKING:
    BinRestrictItemEnumField = BinRestrictItemEnum | Literal['briNone', 'briSpecificItem', 'briSingleItemOnly', 'briSpecificItemGroup', 'briSpecificItemGroupOnly']
else:
    BinRestrictItemEnumField = BinRestrictItemEnum

class BinRestrictTransactionEnum(StrEnum):
    brtNoRestrictions = 'brtNoRestrictions'
    brtAllTrans = 'brtAllTrans'
    brtInboundTrans = 'brtInboundTrans'
    brtOutboundTrans = 'brtOutboundTrans'
    brtAllExceptInventoryTrans = 'brtAllExceptInventoryTrans'

if TYPE_CHECKING:
    BinRestrictTransactionEnumField = BinRestrictTransactionEnum | Literal['brtNoRestrictions', 'brtAllTrans', 'brtInboundTrans', 'brtOutboundTrans', 'brtAllExceptInventoryTrans']
else:
    BinRestrictTransactionEnumField = BinRestrictTransactionEnum

class BinRestrictUoMEnum(StrEnum):
    bruNone = 'bruNone'
    bruSpecificUoM = 'bruSpecificUoM'
    bruSingleUoMOnly = 'bruSingleUoMOnly'
    bruSpecificUoMGroup = 'bruSpecificUoMGroup'
    bruSpecificUoMGroupOnly = 'bruSpecificUoMGroupOnly'

if TYPE_CHECKING:
    BinRestrictUoMEnumField = BinRestrictUoMEnum | Literal['bruNone', 'bruSpecificUoM', 'bruSingleUoMOnly', 'bruSpecificUoMGroup', 'bruSpecificUoMGroupOnly']
else:
    BinRestrictUoMEnumField = BinRestrictUoMEnum

class BinRestrictionBatchEnum(StrEnum):
    brbNoRestrictions = 'brbNoRestrictions'
    brbSingleBatch = 'brbSingleBatch'

if TYPE_CHECKING:
    BinRestrictionBatchEnumField = BinRestrictionBatchEnum | Literal['brbNoRestrictions', 'brbSingleBatch']
else:
    BinRestrictionBatchEnumField = BinRestrictionBatchEnum

class BlanketAgreementBPTypeEnum(StrEnum):
    atCustomer = 'atCustomer'
    atVendor = 'atVendor'

if TYPE_CHECKING:
    BlanketAgreementBPTypeEnumField = BlanketAgreementBPTypeEnum | Literal['atCustomer', 'atVendor']
else:
    BlanketAgreementBPTypeEnumField = BlanketAgreementBPTypeEnum

class BlanketAgreementDatePeriodsEnum(StrEnum):
    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Quarterly = 'Quarterly'
    Semiannually = 'Semiannually'
    Annually = 'Annually'
    OneTime = 'OneTime'

if TYPE_CHECKING:
    BlanketAgreementDatePeriodsEnumField = BlanketAgreementDatePeriodsEnum | Literal['Daily', 'Weekly', 'Monthly', 'Quarterly', 'Semiannually', 'Annually', 'OneTime']
else:
    BlanketAgreementDatePeriodsEnumField = BlanketAgreementDatePeriodsEnum

class BlanketAgreementDocTypeEnum(StrEnum):
    ARInvoice = 'ARInvoice'
    ARCreditMemo = 'ARCreditMemo'
    Delivery = 'Delivery'
    Return = 'Return'
    SalesOrder = 'SalesOrder'
    APInvoice = 'APInvoice'
    APCreditMemo = 'APCreditMemo'
    GoodsReceiptPO = 'GoodsReceiptPO'
    GoodsReturn = 'GoodsReturn'
    PurchaseOrder = 'PurchaseOrder'
    SalesQuotation = 'SalesQuotation'
    APCorrectionInvoice = 'APCorrectionInvoice'
    APCorrectionInvoiceReversal = 'APCorrectionInvoiceReversal'
    ARCorrectionInvoice = 'ARCorrectionInvoice'
    ARCorrectionInvoiceReversal = 'ARCorrectionInvoiceReversal'
    ARDownPayment = 'ARDownPayment'
    APDownPayment = 'APDownPayment'
    PurchaseQuotation = 'PurchaseQuotation'

if TYPE_CHECKING:
    BlanketAgreementDocTypeEnumField = BlanketAgreementDocTypeEnum | Literal['ARInvoice', 'ARCreditMemo', 'Delivery', 'Return', 'SalesOrder', 'APInvoice', 'APCreditMemo', 'GoodsReceiptPO', 'GoodsReturn', 'PurchaseOrder', 'SalesQuotation', 'APCorrectionInvoice', 'APCorrectionInvoiceReversal', 'ARCorrectionInvoice', 'ARCorrectionInvoiceReversal', 'ARDownPayment', 'APDownPayment', 'PurchaseQuotation']
else:
    BlanketAgreementDocTypeEnumField = BlanketAgreementDocTypeEnum

class BlanketAgreementMethodEnum(StrEnum):
    amItem = 'amItem'
    amMonetary = 'amMonetary'

if TYPE_CHECKING:
    BlanketAgreementMethodEnumField = BlanketAgreementMethodEnum | Literal['amItem', 'amMonetary']
else:
    BlanketAgreementMethodEnumField = BlanketAgreementMethodEnum

class BlanketAgreementStatusEnum(StrEnum):
    asApproved = 'asApproved'
    asOnHold = 'asOnHold'
    asDraft = 'asDraft'
    asTerminated = 'asTerminated'
    asCancelled = 'asCancelled'

if TYPE_CHECKING:
    BlanketAgreementStatusEnumField = BlanketAgreementStatusEnum | Literal['asApproved', 'asOnHold', 'asDraft', 'asTerminated', 'asCancelled']
else:
    BlanketAgreementStatusEnumField = BlanketAgreementStatusEnum

class BlanketAgreementTypeEnum(StrEnum):
    atGeneral = 'atGeneral'
    atSpecific = 'atSpecific'

if TYPE_CHECKING:
    BlanketAgreementTypeEnumField = BlanketAgreementTypeEnum | Literal['atGeneral', 'atSpecific']
else:
    BlanketAgreementTypeEnumField = BlanketAgreementTypeEnum

class BoAPARDocumentTypes(StrEnum):
    bodt_Invoice = 'bodt_Invoice'
    bodt_CreditNote = 'bodt_CreditNote'
    bodt_DeliveryNote = 'bodt_DeliveryNote'
    bodt_Return = 'bodt_Return'
    bodt_Order = 'bodt_Order'
    bodt_PurchaseInvoice = 'bodt_PurchaseInvoice'
    bodt_PurchaseCreditNote = 'bodt_PurchaseCreditNote'
    bodt_PurchaseDeliveryNote = 'bodt_PurchaseDeliveryNote'
    bodt_PurchaseReturn = 'bodt_PurchaseReturn'
    bodt_PurchaseOrder = 'bodt_PurchaseOrder'
    bodt_Quotation = 'bodt_Quotation'
    bodt_CorrectionAPInvoice = 'bodt_CorrectionAPInvoice'
    bodt_CorrectionARInvoice = 'bodt_CorrectionARInvoice'
    bodt_Zero = 'bodt_Zero'
    bodt_MinusOne = 'bodt_MinusOne'
    bodt_PurchaseQutation = 'bodt_PurchaseQutation'

if TYPE_CHECKING:
    BoAPARDocumentTypesField = BoAPARDocumentTypes | Literal['bodt_Invoice', 'bodt_CreditNote', 'bodt_DeliveryNote', 'bodt_Return', 'bodt_Order', 'bodt_PurchaseInvoice', 'bodt_PurchaseCreditNote', 'bodt_PurchaseDeliveryNote', 'bodt_PurchaseReturn', 'bodt_PurchaseOrder', 'bodt_Quotation', 'bodt_CorrectionAPInvoice', 'bodt_CorrectionARInvoice', 'bodt_Zero', 'bodt_MinusOne', 'bodt_PurchaseQutation']
else:
    BoAPARDocumentTypesField = BoAPARDocumentTypes

class BoAccountTypes(StrEnum):
    at_Revenues = 'at_Revenues'
    at_Expenses = 'at_Expenses'
    at_Other = 'at_Other'

if TYPE_CHECKING:
    BoAccountTypesField = BoAccountTypes | Literal['at_Revenues', 'at_Expenses', 'at_Other']
else:
    BoAccountTypesField = BoAccountTypes

class BoActivities(StrEnum):
    cn_Conversation = 'cn_Conversation'
    cn_Meeting = 'cn_Meeting'
    cn_Task = 'cn_Task'
    cn_Other = 'cn_Other'
    cn_Note = 'cn_Note'
    cn_Campaign = 'cn_Campaign'

if TYPE_CHECKING:
    BoActivitiesField = BoActivities | Literal['cn_Conversation', 'cn_Meeting', 'cn_Task', 'cn_Other', 'cn_Note', 'cn_Campaign']
else:
    BoActivitiesField = BoActivities

class BoAdEpnsDistribMethods(StrEnum):
    aedm_None = 'aedm_None'
    aedm_Quantity = 'aedm_Quantity'
    aedm_Volume = 'aedm_Volume'
    aedm_Weight = 'aedm_Weight'
    aedm_Equally = 'aedm_Equally'
    aedm_RowTotal = 'aedm_RowTotal'

if TYPE_CHECKING:
    BoAdEpnsDistribMethodsField = BoAdEpnsDistribMethods | Literal['aedm_None', 'aedm_Quantity', 'aedm_Volume', 'aedm_Weight', 'aedm_Equally', 'aedm_RowTotal']
else:
    BoAdEpnsDistribMethodsField = BoAdEpnsDistribMethods

class BoAdEpnsTaxTypes(StrEnum):
    aext_NormalTax = 'aext_NormalTax'
    aext_NoTax = 'aext_NoTax'
    aext_UseTax = 'aext_UseTax'

if TYPE_CHECKING:
    BoAdEpnsTaxTypesField = BoAdEpnsTaxTypes | Literal['aext_NormalTax', 'aext_NoTax', 'aext_UseTax']
else:
    BoAdEpnsTaxTypesField = BoAdEpnsTaxTypes

class BoAddressType(StrEnum):
    bo_ShipTo = 'bo_ShipTo'
    bo_BillTo = 'bo_BillTo'

if TYPE_CHECKING:
    BoAddressTypeField = BoAddressType | Literal['bo_ShipTo', 'bo_BillTo']
else:
    BoAddressTypeField = BoAddressType

class BoAeDistMthd(StrEnum):
    aed_Equally = 'aed_Equally'
    aed_LineTotal = 'aed_LineTotal'
    aed_None = 'aed_None'
    aed_Quantity = 'aed_Quantity'
    aed_Volume = 'aed_Volume'
    aed_Weight = 'aed_Weight'

if TYPE_CHECKING:
    BoAeDistMthdField = BoAeDistMthd | Literal['aed_Equally', 'aed_LineTotal', 'aed_None', 'aed_Quantity', 'aed_Volume', 'aed_Weight']
else:
    BoAeDistMthdField = BoAeDistMthd

class BoAlertTypeforWHStockEnum(StrEnum):
    atfwhs_WarningOnly = 'atfwhs_WarningOnly'
    atfwhs_Block = 'atfwhs_Block'
    atfwhs_NoMessage = 'atfwhs_NoMessage'

if TYPE_CHECKING:
    BoAlertTypeforWHStockEnumField = BoAlertTypeforWHStockEnum | Literal['atfwhs_WarningOnly', 'atfwhs_Block', 'atfwhs_NoMessage']
else:
    BoAlertTypeforWHStockEnumField = BoAlertTypeforWHStockEnum

class BoAllocationByEnum(StrEnum):
    ab_CashValueAfterCustoms = 'ab_CashValueAfterCustoms'
    ab_CashValueBeforeCustoms = 'ab_CashValueBeforeCustoms'
    ab_Equal = 'ab_Equal'
    ab_Quantity = 'ab_Quantity'
    ab_Volume = 'ab_Volume'
    ab_Weight = 'ab_Weight'

if TYPE_CHECKING:
    BoAllocationByEnumField = BoAllocationByEnum | Literal['ab_CashValueAfterCustoms', 'ab_CashValueBeforeCustoms', 'ab_Equal', 'ab_Quantity', 'ab_Volume', 'ab_Weight']
else:
    BoAllocationByEnumField = BoAllocationByEnum

class BoApprovalRequestDecisionEnum(StrEnum):
    ardPending = 'ardPending'
    ardApproved = 'ardApproved'
    ardNotApproved = 'ardNotApproved'

if TYPE_CHECKING:
    BoApprovalRequestDecisionEnumField = BoApprovalRequestDecisionEnum | Literal['ardPending', 'ardApproved', 'ardNotApproved']
else:
    BoApprovalRequestDecisionEnumField = BoApprovalRequestDecisionEnum

class BoApprovalRequestStatusEnum(StrEnum):
    arsPending = 'arsPending'
    arsApproved = 'arsApproved'
    arsNotApproved = 'arsNotApproved'
    arsGenerated = 'arsGenerated'
    arsGeneratedByAuthorizer = 'arsGeneratedByAuthorizer'
    arsCancelled = 'arsCancelled'

if TYPE_CHECKING:
    BoApprovalRequestStatusEnumField = BoApprovalRequestStatusEnum | Literal['arsPending', 'arsApproved', 'arsNotApproved', 'arsGenerated', 'arsGeneratedByAuthorizer', 'arsCancelled']
else:
    BoApprovalRequestStatusEnumField = BoApprovalRequestStatusEnum

class BoBOETypes(StrEnum):
    bobt_Incoming = 'bobt_Incoming'
    bobt_Outgoing = 'bobt_Outgoing'

if TYPE_CHECKING:
    BoBOETypesField = BoBOETypes | Literal['bobt_Incoming', 'bobt_Outgoing']
else:
    BoBOETypesField = BoBOETypes

class BoBOTFromStatus(StrEnum):
    btfs_Sent = 'btfs_Sent'
    btfs_Generated = 'btfs_Generated'
    btfs_Deposited = 'btfs_Deposited'
    btfs_Paid = 'btfs_Paid'

if TYPE_CHECKING:
    BoBOTFromStatusField = BoBOTFromStatus | Literal['btfs_Sent', 'btfs_Generated', 'btfs_Deposited', 'btfs_Paid']
else:
    BoBOTFromStatusField = BoBOTFromStatus

class BoBOTToStatus(StrEnum):
    btts_Canceled = 'btts_Canceled'
    btts_Generated = 'btts_Generated'
    btts_Deposit = 'btts_Deposit'
    btts_Paid = 'btts_Paid'
    btts_Failed = 'btts_Failed'
    btts_Closed = 'btts_Closed'

if TYPE_CHECKING:
    BoBOTToStatusField = BoBOTToStatus | Literal['btts_Canceled', 'btts_Generated', 'btts_Deposit', 'btts_Paid', 'btts_Failed', 'btts_Closed']
else:
    BoBOTToStatusField = BoBOTToStatus

class BoBarCodeStandardEnum(StrEnum):
    rlbsan13 = 'rlbsan13'
    rlbsCode39 = 'rlbsCode39'
    rlbsCode128 = 'rlbsCode128'

if TYPE_CHECKING:
    BoBarCodeStandardEnumField = BoBarCodeStandardEnum | Literal['rlbsan13', 'rlbsCode39', 'rlbsCode128']
else:
    BoBarCodeStandardEnumField = BoBarCodeStandardEnum

class BoBaseDateRateEnum(StrEnum):
    bdr_PostingDate = 'bdr_PostingDate'
    bdr_TaxDate = 'bdr_TaxDate'

if TYPE_CHECKING:
    BoBaseDateRateEnumField = BoBaseDateRateEnum | Literal['bdr_PostingDate', 'bdr_TaxDate']
else:
    BoBaseDateRateEnumField = BoBaseDateRateEnum

class BoBaselineDate(StrEnum):
    bld_PostingDate = 'bld_PostingDate'
    bld_SystemDate = 'bld_SystemDate'
    bld_TaxDate = 'bld_TaxDate'
    bld_ClosingDate = 'bld_ClosingDate'

if TYPE_CHECKING:
    BoBaselineDateField = BoBaselineDate | Literal['bld_PostingDate', 'bld_SystemDate', 'bld_TaxDate', 'bld_ClosingDate']
else:
    BoBaselineDateField = BoBaselineDate

class BoBlockBudget(StrEnum):
    bb_OnlyAnnualAlert = 'bb_OnlyAnnualAlert'
    bb_MonthlyAlertOnly = 'bb_MonthlyAlertOnly'
    bb_Block = 'bb_Block'

if TYPE_CHECKING:
    BoBlockBudgetField = BoBlockBudget | Literal['bb_OnlyAnnualAlert', 'bb_MonthlyAlertOnly', 'bb_Block']
else:
    BoBlockBudgetField = BoBlockBudget

class BoBoeStatus(StrEnum):
    boes_Created = 'boes_Created'
    boes_Sent = 'boes_Sent'
    boes_Deposited = 'boes_Deposited'
    boes_Paid = 'boes_Paid'
    boes_Cancelled = 'boes_Cancelled'
    boes_Closed = 'boes_Closed'
    boes_Failed = 'boes_Failed'

if TYPE_CHECKING:
    BoBoeStatusField = BoBoeStatus | Literal['boes_Created', 'boes_Sent', 'boes_Deposited', 'boes_Paid', 'boes_Cancelled', 'boes_Closed', 'boes_Failed']
else:
    BoBoeStatusField = BoBoeStatus

class BoBpAccountTypes(StrEnum):
    bpat_General = 'bpat_General'
    bpat_DownPayment = 'bpat_DownPayment'
    bpat_AssetsAccount = 'bpat_AssetsAccount'
    bpat_Receivable = 'bpat_Receivable'
    bpat_Payable = 'bpat_Payable'
    bpat_OnCollection = 'bpat_OnCollection'
    bpat_Presentation = 'bpat_Presentation'
    bpat_AssetsPayable = 'bpat_AssetsPayable'
    bpat_Discounted = 'bpat_Discounted'
    bpat_Unpaid = 'bpat_Unpaid'
    bpat_OpenDebts = 'bpat_OpenDebts'
    bpat_Domestic = 'bpat_Domestic'
    bpat_Foreign = 'bpat_Foreign'
    bpat_CashDiscountInterim = 'bpat_CashDiscountInterim'
    bpat_ExchangeRateInterim = 'bpat_ExchangeRateInterim'

if TYPE_CHECKING:
    BoBpAccountTypesField = BoBpAccountTypes | Literal['bpat_General', 'bpat_DownPayment', 'bpat_AssetsAccount', 'bpat_Receivable', 'bpat_Payable', 'bpat_OnCollection', 'bpat_Presentation', 'bpat_AssetsPayable', 'bpat_Discounted', 'bpat_Unpaid', 'bpat_OpenDebts', 'bpat_Domestic', 'bpat_Foreign', 'bpat_CashDiscountInterim', 'bpat_ExchangeRateInterim']
else:
    BoBpAccountTypesField = BoBpAccountTypes

class BoBpsDocTypes(StrEnum):
    bpdt_PaymentReference = 'bpdt_PaymentReference'
    bpdt_ISR = 'bpdt_ISR'
    bpdt_DocNum = 'bpdt_DocNum'

if TYPE_CHECKING:
    BoBpsDocTypesField = BoBpsDocTypes | Literal['bpdt_PaymentReference', 'bpdt_ISR', 'bpdt_DocNum']
else:
    BoBpsDocTypesField = BoBpsDocTypes

class BoBudgetAlert(StrEnum):
    ba_AnnualAlert = 'ba_AnnualAlert'
    ba_MonthlyAlert = 'ba_MonthlyAlert'

if TYPE_CHECKING:
    BoBudgetAlertField = BoBudgetAlert | Literal['ba_AnnualAlert', 'ba_MonthlyAlert']
else:
    BoBudgetAlertField = BoBudgetAlert

class BoBusinessAreaEnum(StrEnum):
    baSales = 'baSales'
    baPurchase = 'baPurchase'
    baSalesAndPurchase = 'baSalesAndPurchase'

if TYPE_CHECKING:
    BoBusinessAreaEnumField = BoBusinessAreaEnum | Literal['baSales', 'baPurchase', 'baSalesAndPurchase']
else:
    BoBusinessAreaEnumField = BoBusinessAreaEnum

class BoBusinessPartnerGroupTypes(StrEnum):
    bbpgt_CustomerGroup = 'bbpgt_CustomerGroup'
    bbpgt_VendorGroup = 'bbpgt_VendorGroup'

if TYPE_CHECKING:
    BoBusinessPartnerGroupTypesField = BoBusinessPartnerGroupTypes | Literal['bbpgt_CustomerGroup', 'bbpgt_VendorGroup']
else:
    BoBusinessPartnerGroupTypesField = BoBusinessPartnerGroupTypes

class BoBusinessPartnerTypes(StrEnum):
    garAll = 'garAll'
    garCompany = 'garCompany'
    garPrivate = 'garPrivate'
    garGovernment = 'garGovernment'

if TYPE_CHECKING:
    BoBusinessPartnerTypesField = BoBusinessPartnerTypes | Literal['garAll', 'garCompany', 'garPrivate', 'garGovernment']
else:
    BoBusinessPartnerTypesField = BoBusinessPartnerTypes

class BoCardCompanyTypes(StrEnum):
    cCompany = 'cCompany'
    cPrivate = 'cPrivate'
    cGovernment = 'cGovernment'
    cEmployee = 'cEmployee'

if TYPE_CHECKING:
    BoCardCompanyTypesField = BoCardCompanyTypes | Literal['cCompany', 'cPrivate', 'cGovernment', 'cEmployee']
else:
    BoCardCompanyTypesField = BoCardCompanyTypes

class BoCardTypes(StrEnum):
    cCustomer = 'cCustomer'
    cSupplier = 'cSupplier'
    cLid = 'cLid'

if TYPE_CHECKING:
    BoCardTypesField = BoCardTypes | Literal['cCustomer', 'cSupplier', 'cLid']
else:
    BoCardTypesField = BoCardTypes

class BoChangeLogEnum(StrEnum):
    clChartOfAccounts = 'clChartOfAccounts'
    clBusinessPartners = 'clBusinessPartners'
    clItems = 'clItems'
    clVatGroups = 'clVatGroups'
    clUsers = 'clUsers'
    clInvoices = 'clInvoices'
    clCreditNotes = 'clCreditNotes'
    clDeliveryNotes = 'clDeliveryNotes'
    clReturns = 'clReturns'
    clOrders = 'clOrders'
    clPurchaseInvoices = 'clPurchaseInvoices'
    clPurchaseCreditNotes = 'clPurchaseCreditNotes'
    clPurchaseDeliveryNotes = 'clPurchaseDeliveryNotes'
    clPurchaseReturns = 'clPurchaseReturns'
    clPurchaseOrders = 'clPurchaseOrders'
    clQuotations = 'clQuotations'
    clIncomingPayments = 'clIncomingPayments'
    clJournalEntries = 'clJournalEntries'
    clCreditCards = 'clCreditCards'
    clAdminInfo = 'clAdminInfo'
    clVendorPayments = 'clVendorPayments'
    clItemGroups = 'clItemGroups'
    clInventoryGeneralEntry = 'clInventoryGeneralEntry'
    clInventoryGeneralExit = 'clInventoryGeneralExit'
    clWarehouses = 'clWarehouses'
    clProductTrees = 'clProductTrees'
    clStockTransfers = 'clStockTransfers'
    clFinancePeriods = 'clFinancePeriods'
    clAdditionalExpenses = 'clAdditionalExpenses'
    clPickLists = 'clPickLists'
    clMaterialRevaluation = 'clMaterialRevaluation'
    clCorrectionPurchaseInvoice = 'clCorrectionPurchaseInvoice'
    clCorrectionPurchaseInvoiceReversal = 'clCorrectionPurchaseInvoiceReversal'
    clCorrectionInvoice = 'clCorrectionInvoice'
    clCorrectionInvoiceReversal = 'clCorrectionInvoiceReversal'
    clEmployeesInfo = 'clEmployeesInfo'
    clCustomerEquipmentCards = 'clCustomerEquipmentCards'
    clWithholdingTaxCodes = 'clWithholdingTaxCodes'
    clBillOfExchange = 'clBillOfExchange'
    clServiceCalls = 'clServiceCalls'
    clProductionOrders = 'clProductionOrders'
    clDownPayments = 'clDownPayments'
    clPurchaseDownPayments = 'clPurchaseDownPayments'
    clPeriodCategory = 'clPeriodCategory'
    clHouseBankAccounts = 'clHouseBankAccounts'
    clSalesTaxInvoice = 'clSalesTaxInvoice'
    clPurchaseTaxInvoice = 'clPurchaseTaxInvoice'
    clExternalBankOperationCodes = 'clExternalBankOperationCodes'
    clInternalBankOperationCodes = 'clInternalBankOperationCodes'
    clOutgoingExciseInvoice = 'clOutgoingExciseInvoice'
    clIncomingExciseInvoice = 'clIncomingExciseInvoice'
    clInventoryTransferRequests = 'clInventoryTransferRequests'
    clPurchaseQuotation = 'clPurchaseQuotation'
    clActivities = 'clActivities'
    clChecksForPayment = 'clChecksForPayment'
    clServiceContract = 'clServiceContract'
    clUDO = 'clUDO'

class BoCheckDepositTypeEnum(StrEnum):
    cdtCashChecks = 'cdtCashChecks'
    cdtPostdatedChecks = 'cdtPostdatedChecks'

if TYPE_CHECKING:
    BoCheckDepositTypeEnumField = BoCheckDepositTypeEnum | Literal['cdtCashChecks', 'cdtPostdatedChecks']
else:
    BoCheckDepositTypeEnumField = BoCheckDepositTypeEnum

class BoClosingDateProcedureBaseDateEnum(StrEnum):
    bocpdbld_BaseSystemDate = 'bocpdbld_BaseSystemDate'
    bocpdbld_PostingDate = 'bocpdbld_PostingDate'

if TYPE_CHECKING:
    BoClosingDateProcedureBaseDateEnumField = BoClosingDateProcedureBaseDateEnum | Literal['bocpdbld_BaseSystemDate', 'bocpdbld_PostingDate']
else:
    BoClosingDateProcedureBaseDateEnumField = BoClosingDateProcedureBaseDateEnum

class BoClosingDateProcedureDueMonthEnum(StrEnum):
    bocpddm_HalfMonth = 'bocpddm_HalfMonth'
    bocpddm_MonthEnd = 'bocpddm_MonthEnd'
    bocpddm_MonthStart = 'bocpddm_MonthStart'
    bocpddm_None = 'bocpddm_None'

if TYPE_CHECKING:
    BoClosingDateProcedureDueMonthEnumField = BoClosingDateProcedureDueMonthEnum | Literal['bocpddm_HalfMonth', 'bocpddm_MonthEnd', 'bocpddm_MonthStart', 'bocpddm_None']
else:
    BoClosingDateProcedureDueMonthEnumField = BoClosingDateProcedureDueMonthEnum

class BoCockpitTypeEnum(StrEnum):
    cptt_UserCockpit = 'cptt_UserCockpit'
    cptt_TemplateCockpit = 'cptt_TemplateCockpit'

if TYPE_CHECKING:
    BoCockpitTypeEnumField = BoCockpitTypeEnum | Literal['cptt_UserCockpit', 'cptt_TemplateCockpit']
else:
    BoCockpitTypeEnumField = BoCockpitTypeEnum

class BoConsumptionMethod(StrEnum):
    cm_BackwardForward = 'cm_BackwardForward'
    cm_ForwardBackward = 'cm_ForwardBackward'

if TYPE_CHECKING:
    BoConsumptionMethodField = BoConsumptionMethod | Literal['cm_BackwardForward', 'cm_ForwardBackward']
else:
    BoConsumptionMethodField = BoConsumptionMethod

class BoContractTypes(StrEnum):
    ct_Customer = 'ct_Customer'
    ct_ItemGroup = 'ct_ItemGroup'
    ct_SerialNumber = 'ct_SerialNumber'

if TYPE_CHECKING:
    BoContractTypesField = BoContractTypes | Literal['ct_Customer', 'ct_ItemGroup', 'ct_SerialNumber']
else:
    BoContractTypesField = BoContractTypes

class BoCorInvItemStatus(StrEnum):
    ciis_Was = 'ciis_Was'
    ciis_ShouldBe = 'ciis_ShouldBe'

if TYPE_CHECKING:
    BoCorInvItemStatusField = BoCorInvItemStatus | Literal['ciis_Was', 'ciis_ShouldBe']
else:
    BoCorInvItemStatusField = BoCorInvItemStatus

class BoCpCardAcct(StrEnum):
    cfp_Card = 'cfp_Card'
    cfp_Account = 'cfp_Account'

if TYPE_CHECKING:
    BoCpCardAcctField = BoCpCardAcct | Literal['cfp_Card', 'cfp_Account']
else:
    BoCpCardAcctField = BoCpCardAcct

class BoCurrencyCheck(StrEnum):
    cc_Block = 'cc_Block'
    cc_NoMessage = 'cc_NoMessage'

if TYPE_CHECKING:
    BoCurrencyCheckField = BoCurrencyCheck | Literal['cc_Block', 'cc_NoMessage']
else:
    BoCurrencyCheckField = BoCurrencyCheck

class BoCurrencySources(StrEnum):
    bocs_LocalCurrency = 'bocs_LocalCurrency'
    bocs_SystemCurrency = 'bocs_SystemCurrency'
    bocs_BPCurrency = 'bocs_BPCurrency'

if TYPE_CHECKING:
    BoCurrencySourcesField = BoCurrencySources | Literal['bocs_LocalCurrency', 'bocs_SystemCurrency', 'bocs_BPCurrency']
else:
    BoCurrencySourcesField = BoCurrencySources

class BoDataOwnershipManageMethodEnum(StrEnum):
    doManageByDocOnly = 'doManageByDocOnly'
    doManageByBPOnly = 'doManageByBPOnly'
    doManageByBPnDoc = 'doManageByBPnDoc'
    doManageByBranch = 'doManageByBranch'

if TYPE_CHECKING:
    BoDataOwnershipManageMethodEnumField = BoDataOwnershipManageMethodEnum | Literal['doManageByDocOnly', 'doManageByBPOnly', 'doManageByBPnDoc', 'doManageByBranch']
else:
    BoDataOwnershipManageMethodEnumField = BoDataOwnershipManageMethodEnum

class BoDataSourceEnum(StrEnum):
    rldsFreeText = 'rldsFreeText'
    rldsSystemVariable = 'rldsSystemVariable'
    rldsDatabase = 'rldsDatabase'
    rldsFormula = 'rldsFormula'

if TYPE_CHECKING:
    BoDataSourceEnumField = BoDataSourceEnum | Literal['rldsFreeText', 'rldsSystemVariable', 'rldsDatabase', 'rldsFormula']
else:
    BoDataSourceEnumField = BoDataSourceEnum

class BoDateTemplate(StrEnum):
    dt_DDMMYY = 'dt_DDMMYY'
    dt_DDMMCCYY = 'dt_DDMMCCYY'
    dt_MMDDYY = 'dt_MMDDYY'
    dt_MMDDCCYY = 'dt_MMDDCCYY'
    dt_CCYYMMDD = 'dt_CCYYMMDD'
    dt_DDMonthYYYY = 'dt_DDMonthYYYY'
    dt_YYMMDD = 'dt_YYMMDD'

if TYPE_CHECKING:
    BoDateTemplateField = BoDateTemplate | Literal['dt_DDMMYY', 'dt_DDMMCCYY', 'dt_MMDDYY', 'dt_MMDDCCYY', 'dt_CCYYMMDD', 'dt_DDMonthYYYY', 'dt_YYMMDD']
else:
    BoDateTemplateField = BoDateTemplate

class BoDeductionTaxGroupCodeEnum(StrEnum):
    dtgcInterestReceivers = 'dtgcInterestReceivers'
    dtgcEmployeeReceivingCommission = 'dtgcEmployeeReceivingCommission'
    dtgcWritersPrice = 'dtgcWritersPrice'
    dtgcPaidServices = 'dtgcPaidServices'
    dtgcPaymentsToForeignCitizens = 'dtgcPaymentsToForeignCitizens'
    dtgcPaymentsForCitizensInForeignCountries = 'dtgcPaymentsForCitizensInForeignCountries'
    dtgcInvalidPaymentFromCompensationFund = 'dtgcInvalidPaymentFromCompensationFund'
    dtgcRepaymentToEmployerFromCompensationFund = 'dtgcRepaymentToEmployerFromCompensationFund'
    dtgcRentalPayments = 'dtgcRentalPayments'
    dtgcPaymentsFromStudyFund = 'dtgcPaymentsFromStudyFund'
    dtgcDividendPayments = 'dtgcDividendPayments'

if TYPE_CHECKING:
    BoDeductionTaxGroupCodeEnumField = BoDeductionTaxGroupCodeEnum | Literal['dtgcInterestReceivers', 'dtgcEmployeeReceivingCommission', 'dtgcWritersPrice', 'dtgcPaidServices', 'dtgcPaymentsToForeignCitizens', 'dtgcPaymentsForCitizensInForeignCountries', 'dtgcInvalidPaymentFromCompensationFund', 'dtgcRepaymentToEmployerFromCompensationFund', 'dtgcRentalPayments', 'dtgcPaymentsFromStudyFund', 'dtgcDividendPayments']
else:
    BoDeductionTaxGroupCodeEnumField = BoDeductionTaxGroupCodeEnum

class BoDefaultBatchStatus(StrEnum):
    dbs_Released = 'dbs_Released'
    dbs_NotAccessible = 'dbs_NotAccessible'
    dbs_Locked = 'dbs_Locked'

if TYPE_CHECKING:
    BoDefaultBatchStatusField = BoDefaultBatchStatus | Literal['dbs_Released', 'dbs_NotAccessible', 'dbs_Locked']
else:
    BoDefaultBatchStatusField = BoDefaultBatchStatus

class BoDepositAccountTypeEnum(StrEnum):
    datBankAccount = 'datBankAccount'
    datBusinessPartner = 'datBusinessPartner'

if TYPE_CHECKING:
    BoDepositAccountTypeEnumField = BoDepositAccountTypeEnum | Literal['datBankAccount', 'datBusinessPartner']
else:
    BoDepositAccountTypeEnumField = BoDepositAccountTypeEnum

class BoDepositCheckEnum(StrEnum):
    dtNo = 'dtNo'
    dcAsCash = 'dcAsCash'
    dtAsPostdated = 'dtAsPostdated'

if TYPE_CHECKING:
    BoDepositCheckEnumField = BoDepositCheckEnum | Literal['dtNo', 'dcAsCash', 'dtAsPostdated']
else:
    BoDepositCheckEnumField = BoDepositCheckEnum

class BoDepositPostingTypes(StrEnum):
    dpt_Collection = 'dpt_Collection'
    dpt_Discounted = 'dpt_Discounted'

if TYPE_CHECKING:
    BoDepositPostingTypesField = BoDepositPostingTypes | Literal['dpt_Collection', 'dpt_Discounted']
else:
    BoDepositPostingTypesField = BoDepositPostingTypes

class BoDepositTypeEnum(StrEnum):
    dtChecks = 'dtChecks'
    dtCredit = 'dtCredit'
    dtCash = 'dtCash'
    dtBOE = 'dtBOE'

if TYPE_CHECKING:
    BoDepositTypeEnumField = BoDepositTypeEnum | Literal['dtChecks', 'dtCredit', 'dtCash', 'dtBOE']
else:
    BoDepositTypeEnumField = BoDepositTypeEnum

class BoDocItemType(StrEnum):
    dit_Item = 'dit_Item'
    dit_Resource = 'dit_Resource'

if TYPE_CHECKING:
    BoDocItemTypeField = BoDocItemType | Literal['dit_Item', 'dit_Resource']
else:
    BoDocItemTypeField = BoDocItemType

class BoDocLineType(StrEnum):
    dlt_Regular = 'dlt_Regular'
    dlt_Alternative = 'dlt_Alternative'
    dlt_Resource = 'dlt_Resource'

if TYPE_CHECKING:
    BoDocLineTypeField = BoDocLineType | Literal['dlt_Regular', 'dlt_Alternative', 'dlt_Resource']
else:
    BoDocLineTypeField = BoDocLineType

class BoDocSpecialLineType(StrEnum):
    dslt_Text = 'dslt_Text'
    dslt_Subtotal = 'dslt_Subtotal'

if TYPE_CHECKING:
    BoDocSpecialLineTypeField = BoDocSpecialLineType | Literal['dslt_Text', 'dslt_Subtotal']
else:
    BoDocSpecialLineTypeField = BoDocSpecialLineType

class BoDocSummaryTypes(StrEnum):
    dNoSummary = 'dNoSummary'
    dByItems = 'dByItems'
    dByDocuments = 'dByDocuments'

if TYPE_CHECKING:
    BoDocSummaryTypesField = BoDocSummaryTypes | Literal['dNoSummary', 'dByItems', 'dByDocuments']
else:
    BoDocSummaryTypesField = BoDocSummaryTypes

class BoDocWhsAutoIssueMethod(StrEnum):
    whsBinSingleChoiceOnly = 'whsBinSingleChoiceOnly'
    whsBinBinCodeOrder = 'whsBinBinCodeOrder'
    whsBinAltSortCodeOrder = 'whsBinAltSortCodeOrder'
    whsBinQtyDescendingOrder = 'whsBinQtyDescendingOrder'
    whsBinQtyAscendingOrder = 'whsBinQtyAscendingOrder'
    whsBinFIFO = 'whsBinFIFO'
    whsBinLIFO = 'whsBinLIFO'
    whsBinSingleBinPreferred = 'whsBinSingleBinPreferred'

if TYPE_CHECKING:
    BoDocWhsAutoIssueMethodField = BoDocWhsAutoIssueMethod | Literal['whsBinSingleChoiceOnly', 'whsBinBinCodeOrder', 'whsBinAltSortCodeOrder', 'whsBinQtyDescendingOrder', 'whsBinQtyAscendingOrder', 'whsBinFIFO', 'whsBinLIFO', 'whsBinSingleBinPreferred']
else:
    BoDocWhsAutoIssueMethodField = BoDocWhsAutoIssueMethod

class BoDocWhsUpdateTypes(StrEnum):
    dwh_No = 'dwh_No'
    dwh_OrdersFromVendors = 'dwh_OrdersFromVendors'
    dwh_CustomerOrders = 'dwh_CustomerOrders'
    dwh_Consignment = 'dwh_Consignment'
    dwh_Stock = 'dwh_Stock'

if TYPE_CHECKING:
    BoDocWhsUpdateTypesField = BoDocWhsUpdateTypes | Literal['dwh_No', 'dwh_OrdersFromVendors', 'dwh_CustomerOrders', 'dwh_Consignment', 'dwh_Stock']
else:
    BoDocWhsUpdateTypesField = BoDocWhsUpdateTypes

class BoDocumentLinePickStatus(StrEnum):
    dlps_Picked = 'dlps_Picked'
    dlps_NotPicked = 'dlps_NotPicked'
    dlps_ReleasedForPicking = 'dlps_ReleasedForPicking'
    dlps_PartiallyPicked = 'dlps_PartiallyPicked'

if TYPE_CHECKING:
    BoDocumentLinePickStatusField = BoDocumentLinePickStatus | Literal['dlps_Picked', 'dlps_NotPicked', 'dlps_ReleasedForPicking', 'dlps_PartiallyPicked']
else:
    BoDocumentLinePickStatusField = BoDocumentLinePickStatus

class BoDocumentSubType(StrEnum):
    bod_None = 'bod_None'
    bod_InvoiceExempt = 'bod_InvoiceExempt'
    bod_DebitMemo = 'bod_DebitMemo'
    bod_Bill = 'bod_Bill'
    bod_ExemptBill = 'bod_ExemptBill'
    bod_PurchaseDebitMemo = 'bod_PurchaseDebitMemo'
    bod_ExportInvoice = 'bod_ExportInvoice'
    bod_GSTTaxInvoice = 'bod_GSTTaxInvoice'
    bod_GSTDebitMemo = 'bod_GSTDebitMemo'
    bod_RefundVoucher = 'bod_RefundVoucher'

if TYPE_CHECKING:
    BoDocumentSubTypeField = BoDocumentSubType | Literal['bod_None', 'bod_InvoiceExempt', 'bod_DebitMemo', 'bod_Bill', 'bod_ExemptBill', 'bod_PurchaseDebitMemo', 'bod_ExportInvoice', 'bod_GSTTaxInvoice', 'bod_GSTDebitMemo', 'bod_RefundVoucher']
else:
    BoDocumentSubTypeField = BoDocumentSubType

class BoDocumentTypes(StrEnum):
    dDocument_Items = 'dDocument_Items'
    dDocument_Service = 'dDocument_Service'

if TYPE_CHECKING:
    BoDocumentTypesField = BoDocumentTypes | Literal['dDocument_Items', 'dDocument_Service']
else:
    BoDocumentTypesField = BoDocumentTypes

class BoDueDateEnum(StrEnum):
    boddDateOfPaymentRun = 'boddDateOfPaymentRun'
    boddDueDateOfInvoice = 'boddDueDateOfInvoice'
    boddPaymentTerms = 'boddPaymentTerms'

if TYPE_CHECKING:
    BoDueDateEnumField = BoDueDateEnum | Literal['boddDateOfPaymentRun', 'boddDueDateOfInvoice', 'boddPaymentTerms']
else:
    BoDueDateEnumField = BoDueDateEnum

class BoDurations(StrEnum):
    du_Seconds = 'du_Seconds'
    du_Minuts = 'du_Minuts'
    du_Hours = 'du_Hours'
    du_Days = 'du_Days'

if TYPE_CHECKING:
    BoDurationsField = BoDurations | Literal['du_Seconds', 'du_Minuts', 'du_Hours', 'du_Days']
else:
    BoDurationsField = BoDurations

class BoEquipmentBPType(StrEnum):
    et_Sales = 'et_Sales'
    et_Purchasing = 'et_Purchasing'
    et_SalesAndPurchasing = 'et_SalesAndPurchasing'

if TYPE_CHECKING:
    BoEquipmentBPTypeField = BoEquipmentBPType | Literal['et_Sales', 'et_Purchasing', 'et_SalesAndPurchasing']
else:
    BoEquipmentBPTypeField = BoEquipmentBPType

class BoExpenseOperationTypeEnum(StrEnum):
    bo_ExpOpType_ProfessionalServices = 'bo_ExpOpType_ProfessionalServices'
    bo_ExpOpType_RentingAssets = 'bo_ExpOpType_RentingAssets'
    bo_ExpOpType_Others = 'bo_ExpOpType_Others'
    bo_ExpOpType_None = 'bo_ExpOpType_None'

if TYPE_CHECKING:
    BoExpenseOperationTypeEnumField = BoExpenseOperationTypeEnum | Literal['bo_ExpOpType_ProfessionalServices', 'bo_ExpOpType_RentingAssets', 'bo_ExpOpType_Others', 'bo_ExpOpType_None']
else:
    BoExpenseOperationTypeEnumField = BoExpenseOperationTypeEnum

class BoExtensionErrorActionEnum(StrEnum):
    eeaStop = 'eeaStop'
    eeaIgnore = 'eeaIgnore'
    eeaPrompt = 'eeaPrompt'

if TYPE_CHECKING:
    BoExtensionErrorActionEnumField = BoExtensionErrorActionEnum | Literal['eeaStop', 'eeaIgnore', 'eeaPrompt']
else:
    BoExtensionErrorActionEnumField = BoExtensionErrorActionEnum

class BoFatherCardTypes(StrEnum):
    cPayments_sum = 'cPayments_sum'
    cDelivery_sum = 'cDelivery_sum'

if TYPE_CHECKING:
    BoFatherCardTypesField = BoFatherCardTypes | Literal['cPayments_sum', 'cDelivery_sum']
else:
    BoFatherCardTypesField = BoFatherCardTypes

class BoFieldTypes(StrEnum):
    db_Alpha = 'db_Alpha'
    db_Memo = 'db_Memo'
    db_Numeric = 'db_Numeric'
    db_Date = 'db_Date'
    db_Float = 'db_Float'

if TYPE_CHECKING:
    BoFieldTypesField = BoFieldTypes | Literal['db_Alpha', 'db_Memo', 'db_Numeric', 'db_Date', 'db_Float']
else:
    BoFieldTypesField = BoFieldTypes

class BoFldSubTypes(StrEnum):
    st_None = 'st_None'
    st_Address = 'st_Address'
    st_Phone = 'st_Phone'
    st_Time = 'st_Time'
    st_Rate = 'st_Rate'
    st_Sum = 'st_Sum'
    st_Price = 'st_Price'
    st_Quantity = 'st_Quantity'
    st_Percentage = 'st_Percentage'
    st_Measurement = 'st_Measurement'
    st_Link = 'st_Link'
    st_Image = 'st_Image'
    st_Checkbox = 'st_Checkbox'

if TYPE_CHECKING:
    BoFldSubTypesField = BoFldSubTypes | Literal['st_None', 'st_Address', 'st_Phone', 'st_Time', 'st_Rate', 'st_Sum', 'st_Price', 'st_Quantity', 'st_Percentage', 'st_Measurement', 'st_Link', 'st_Image', 'st_Checkbox']
else:
    BoFldSubTypesField = BoFldSubTypes

class BoForecastViewType(StrEnum):
    fvtDaily = 'fvtDaily'
    fvtWeekly = 'fvtWeekly'
    fvtMonthly = 'fvtMonthly'

if TYPE_CHECKING:
    BoForecastViewTypeField = BoForecastViewType | Literal['fvtDaily', 'fvtWeekly', 'fvtMonthly']
else:
    BoForecastViewTypeField = BoForecastViewType

class BoFormattedSearchActionEnum(StrEnum):
    bofsaNone = 'bofsaNone'
    bofsaValidValues = 'bofsaValidValues'
    bofsaQuery = 'bofsaQuery'

if TYPE_CHECKING:
    BoFormattedSearchActionEnumField = BoFormattedSearchActionEnum | Literal['bofsaNone', 'bofsaValidValues', 'bofsaQuery']
else:
    BoFormattedSearchActionEnumField = BoFormattedSearchActionEnum

class BoFrequency(StrEnum):
    bof_Daily = 'bof_Daily'
    bof_Weekly = 'bof_Weekly'
    bof_Every4Weeks = 'bof_Every4Weeks'
    bof_Monthly = 'bof_Monthly'
    bof_Quarterly = 'bof_Quarterly'
    bof_HalfYearly = 'bof_HalfYearly'
    bof_Annually = 'bof_Annually'
    bof_OneTime = 'bof_OneTime'
    bof_EveryXDays = 'bof_EveryXDays'

if TYPE_CHECKING:
    BoFrequencyField = BoFrequency | Literal['bof_Daily', 'bof_Weekly', 'bof_Every4Weeks', 'bof_Monthly', 'bof_Quarterly', 'bof_HalfYearly', 'bof_Annually', 'bof_OneTime', 'bof_EveryXDays']
else:
    BoFrequencyField = BoFrequency

class BoFrequencyTypeEnum(StrEnum):
    ftDaily = 'ftDaily'
    ftWeekly = 'ftWeekly'
    ftMonthly = 'ftMonthly'
    ftQuarterly = 'ftQuarterly'
    ftSemiannually = 'ftSemiannually'
    ftAnnually = 'ftAnnually'
    ftOneTime = 'ftOneTime'
    ftTemplate = 'ftTemplate'
    ftNotExecuted = 'ftNotExecuted'

if TYPE_CHECKING:
    BoFrequencyTypeEnumField = BoFrequencyTypeEnum | Literal['ftDaily', 'ftWeekly', 'ftMonthly', 'ftQuarterly', 'ftSemiannually', 'ftAnnually', 'ftOneTime', 'ftTemplate', 'ftNotExecuted']
else:
    BoFrequencyTypeEnumField = BoFrequencyTypeEnum

class BoGLMethods(StrEnum):
    glm_WH = 'glm_WH'
    glm_ItemClass = 'glm_ItemClass'
    glm_ItemLevel = 'glm_ItemLevel'

if TYPE_CHECKING:
    BoGLMethodsField = BoGLMethods | Literal['glm_WH', 'glm_ItemClass', 'glm_ItemLevel']
else:
    BoGLMethodsField = BoGLMethods

class BoGSTRegnTypeEnum(StrEnum):
    invalid = 'invalid'
    gstRegularTDSISD = 'gstRegularTDSISD'
    gstCasualTaxablePerson = 'gstCasualTaxablePerson'
    gstCompositionLevy = 'gstCompositionLevy'
    gstGoverDepartPSU = 'gstGoverDepartPSU'
    gstNonResidentTaxablePerson = 'gstNonResidentTaxablePerson'
    gstUNAgencyEmbassy = 'gstUNAgencyEmbassy'

if TYPE_CHECKING:
    BoGSTRegnTypeEnumField = BoGSTRegnTypeEnum | Literal['invalid', 'gstRegularTDSISD', 'gstCasualTaxablePerson', 'gstCompositionLevy', 'gstGoverDepartPSU', 'gstNonResidentTaxablePerson', 'gstUNAgencyEmbassy']
else:
    BoGSTRegnTypeEnumField = BoGSTRegnTypeEnum

class BoGenderTypes(StrEnum):
    gt_Female = 'gt_Female'
    gt_Male = 'gt_Male'
    gt_Undefined = 'gt_Undefined'
    gt_Masked = 'gt_Masked'
    gt_Invalid = 'gt_Invalid'

if TYPE_CHECKING:
    BoGenderTypesField = BoGenderTypes | Literal['gt_Female', 'gt_Male', 'gt_Undefined', 'gt_Masked', 'gt_Invalid']
else:
    BoGenderTypesField = BoGenderTypes

class BoGridTypeEnum(StrEnum):
    gtCombination = 'gtCombination'
    gtContinuousLine = 'gtContinuousLine'
    gtBrokenLine = 'gtBrokenLine'
    gtDots = 'gtDots'

if TYPE_CHECKING:
    BoGridTypeEnumField = BoGridTypeEnum | Literal['gtCombination', 'gtContinuousLine', 'gtBrokenLine', 'gtDots']
else:
    BoGridTypeEnumField = BoGridTypeEnum

class BoHorizontalAlignmentEnum(StrEnum):
    rlhjRight = 'rlhjRight'
    rlhjLeft = 'rlhjLeft'
    rlhjCentralized = 'rlhjCentralized'
    rlhjLanguageDependent = 'rlhjLanguageDependent'

if TYPE_CHECKING:
    BoHorizontalAlignmentEnumField = BoHorizontalAlignmentEnum | Literal['rlhjRight', 'rlhjLeft', 'rlhjCentralized', 'rlhjLanguageDependent']
else:
    BoHorizontalAlignmentEnumField = BoHorizontalAlignmentEnum

class BoInterimDocTypes(StrEnum):
    boidt_None = 'boidt_None'
    boidt_ExchangeRate = 'boidt_ExchangeRate'
    boidt_CashDiscount = 'boidt_CashDiscount'

if TYPE_CHECKING:
    BoInterimDocTypesField = BoInterimDocTypes | Literal['boidt_None', 'boidt_ExchangeRate', 'boidt_CashDiscount']
else:
    BoInterimDocTypesField = BoInterimDocTypes

class BoInventorySystem(StrEnum):
    bis_MovingAverage = 'bis_MovingAverage'
    bis_Standard = 'bis_Standard'
    bis_FIFO = 'bis_FIFO'
    bis_SNB = 'bis_SNB'

if TYPE_CHECKING:
    BoInventorySystemField = BoInventorySystem | Literal['bis_MovingAverage', 'bis_Standard', 'bis_FIFO', 'bis_SNB']
else:
    BoInventorySystemField = BoInventorySystem

class BoIssueMethod(StrEnum):
    im_Backflush = 'im_Backflush'
    im_Manual = 'im_Manual'

if TYPE_CHECKING:
    BoIssueMethodField = BoIssueMethod | Literal['im_Backflush', 'im_Manual']
else:
    BoIssueMethodField = BoIssueMethod

class BoItemTreeTypes(StrEnum):
    iNotATree = 'iNotATree'
    iAssemblyTree = 'iAssemblyTree'
    iSalesTree = 'iSalesTree'
    iProductionTree = 'iProductionTree'
    iTemplateTree = 'iTemplateTree'
    iIngredient = 'iIngredient'

if TYPE_CHECKING:
    BoItemTreeTypesField = BoItemTreeTypes | Literal['iNotATree', 'iAssemblyTree', 'iSalesTree', 'iProductionTree', 'iTemplateTree', 'iIngredient']
else:
    BoItemTreeTypesField = BoItemTreeTypes

class BoLineBreakEnum(StrEnum):
    rlsAllowOverflow = 'rlsAllowOverflow'
    rlsAdjustToCell = 'rlsAdjustToCell'
    rlsDivideIntoRows = 'rlsDivideIntoRows'

if TYPE_CHECKING:
    BoLineBreakEnumField = BoLineBreakEnum | Literal['rlsAllowOverflow', 'rlsAdjustToCell', 'rlsDivideIntoRows']
else:
    BoLineBreakEnumField = BoLineBreakEnum

class BoMRPComponentWarehouse(StrEnum):
    bomcw_BOM = 'bomcw_BOM'
    bomcw_Parent = 'bomcw_Parent'

if TYPE_CHECKING:
    BoMRPComponentWarehouseField = BoMRPComponentWarehouse | Literal['bomcw_BOM', 'bomcw_Parent']
else:
    BoMRPComponentWarehouseField = BoMRPComponentWarehouse

class BoMYFTypeEnum(StrEnum):
    myft_WholesaleSales = 'myft_WholesaleSales'
    myft_RetailSales = 'myft_RetailSales'
    myft_WholesalePurchases = 'myft_WholesalePurchases'
    myft_OtherExpenseTransactions = 'myft_OtherExpenseTransactions'

if TYPE_CHECKING:
    BoMYFTypeEnumField = BoMYFTypeEnum | Literal['myft_WholesaleSales', 'myft_RetailSales', 'myft_WholesalePurchases', 'myft_OtherExpenseTransactions']
else:
    BoMYFTypeEnumField = BoMYFTypeEnum

class BoManageMethod(StrEnum):
    bomm_OnEveryTransaction = 'bomm_OnEveryTransaction'
    bomm_OnReleaseOnly = 'bomm_OnReleaseOnly'

if TYPE_CHECKING:
    BoManageMethodField = BoManageMethod | Literal['bomm_OnEveryTransaction', 'bomm_OnReleaseOnly']
else:
    BoManageMethodField = BoManageMethod

class BoMaterialTypes(StrEnum):
    mt_GoodsForReseller = 'mt_GoodsForReseller'
    mt_FinishedGoods = 'mt_FinishedGoods'
    mt_GoodsInProcess = 'mt_GoodsInProcess'
    mt_RawMaterial = 'mt_RawMaterial'
    mt_Package = 'mt_Package'
    mt_SubProduct = 'mt_SubProduct'
    mt_IntermediateMaterial = 'mt_IntermediateMaterial'
    mt_ConsumerMaterial = 'mt_ConsumerMaterial'
    mt_FixedAsset = 'mt_FixedAsset'
    mt_Service = 'mt_Service'
    mt_OtherInput = 'mt_OtherInput'
    mt_Other = 'mt_Other'

if TYPE_CHECKING:
    BoMaterialTypesField = BoMaterialTypes | Literal['mt_GoodsForReseller', 'mt_FinishedGoods', 'mt_GoodsInProcess', 'mt_RawMaterial', 'mt_Package', 'mt_SubProduct', 'mt_IntermediateMaterial', 'mt_ConsumerMaterial', 'mt_FixedAsset', 'mt_Service', 'mt_OtherInput', 'mt_Other']
else:
    BoMaterialTypesField = BoMaterialTypes

class BoMeritalStatuses(StrEnum):
    mts_Single = 'mts_Single'
    mts_Married = 'mts_Married'
    mts_Divorced = 'mts_Divorced'
    mts_Widowed = 'mts_Widowed'
    mts_NotSpecified = 'mts_NotSpecified'

if TYPE_CHECKING:
    BoMeritalStatusesField = BoMeritalStatuses | Literal['mts_Single', 'mts_Married', 'mts_Divorced', 'mts_Widowed', 'mts_NotSpecified']
else:
    BoMeritalStatusesField = BoMeritalStatuses

class BoMoneyPrecisionTypes(StrEnum):
    mpt_Sum = 'mpt_Sum'
    mpt_Price = 'mpt_Price'
    mpt_Rate = 'mpt_Rate'
    mpt_Quantity = 'mpt_Quantity'
    mpt_Percent = 'mpt_Percent'
    mpt_Measure = 'mpt_Measure'
    mpt_Tax = 'mpt_Tax'

if TYPE_CHECKING:
    BoMoneyPrecisionTypesField = BoMoneyPrecisionTypes | Literal['mpt_Sum', 'mpt_Price', 'mpt_Rate', 'mpt_Quantity', 'mpt_Percent', 'mpt_Measure', 'mpt_Tax']
else:
    BoMoneyPrecisionTypesField = BoMoneyPrecisionTypes

class BoMsgPriorities(StrEnum):
    pr_Low = 'pr_Low'
    pr_Normal = 'pr_Normal'
    pr_High = 'pr_High'

if TYPE_CHECKING:
    BoMsgPrioritiesField = BoMsgPriorities | Literal['pr_Low', 'pr_Normal', 'pr_High']
else:
    BoMsgPrioritiesField = BoMsgPriorities

class BoMsgRcpTypes(StrEnum):
    rt_RandomUser = 'rt_RandomUser'
    rt_ContactPerson = 'rt_ContactPerson'
    rt_InternalUser = 'rt_InternalUser'

if TYPE_CHECKING:
    BoMsgRcpTypesField = BoMsgRcpTypes | Literal['rt_RandomUser', 'rt_ContactPerson', 'rt_InternalUser']
else:
    BoMsgRcpTypesField = BoMsgRcpTypes

class BoORCTPaymentTypeEnum(StrEnum):
    bopt_None = 'bopt_None'
    bopt_Electronic = 'bopt_Electronic'
    bopt_Post = 'bopt_Post'
    bopt_Telegraph = 'bopt_Telegraph'
    bopt_Express = 'bopt_Express'

if TYPE_CHECKING:
    BoORCTPaymentTypeEnumField = BoORCTPaymentTypeEnum | Literal['bopt_None', 'bopt_Electronic', 'bopt_Post', 'bopt_Telegraph', 'bopt_Express']
else:
    BoORCTPaymentTypeEnumField = BoORCTPaymentTypeEnum

class BoObjectTypes(StrEnum):
    oChartOfAccounts = 'oChartOfAccounts'
    oBusinessPartners = 'oBusinessPartners'
    oBanks = 'oBanks'
    oItems = 'oItems'
    oVatGroups = 'oVatGroups'
    oPriceLists = 'oPriceLists'
    oSpecialPrices = 'oSpecialPrices'
    oItemProperties = 'oItemProperties'
    oBusinessPartnerGroups = 'oBusinessPartnerGroups'
    oUsers = 'oUsers'
    oInvoices = 'oInvoices'
    oCreditNotes = 'oCreditNotes'
    oDeliveryNotes = 'oDeliveryNotes'
    oReturns = 'oReturns'
    oOrders = 'oOrders'
    oPurchaseInvoices = 'oPurchaseInvoices'
    oPurchaseCreditNotes = 'oPurchaseCreditNotes'
    oPurchaseDeliveryNotes = 'oPurchaseDeliveryNotes'
    oPurchaseReturns = 'oPurchaseReturns'
    oPurchaseOrders = 'oPurchaseOrders'
    oQuotations = 'oQuotations'
    oIncomingPayments = 'oIncomingPayments'
    oJournalVouchers = 'oJournalVouchers'
    oJournalEntries = 'oJournalEntries'
    oStockTakings = 'oStockTakings'
    oContacts = 'oContacts'
    oCreditCards = 'oCreditCards'
    oCurrencyCodes = 'oCurrencyCodes'
    oPaymentTermsTypes = 'oPaymentTermsTypes'
    oBankPages = 'oBankPages'
    oManufacturers = 'oManufacturers'
    oVendorPayments = 'oVendorPayments'
    oLandedCostsCodes = 'oLandedCostsCodes'
    oShippingTypes = 'oShippingTypes'
    oLengthMeasures = 'oLengthMeasures'
    oWeightMeasures = 'oWeightMeasures'
    oItemGroups = 'oItemGroups'
    oSalesPersons = 'oSalesPersons'
    oCustomsGroups = 'oCustomsGroups'
    oChecksforPayment = 'oChecksforPayment'
    oInventoryGenEntry = 'oInventoryGenEntry'
    oInventoryGenExit = 'oInventoryGenExit'
    oWarehouses = 'oWarehouses'
    oCommissionGroups = 'oCommissionGroups'
    oProductTrees = 'oProductTrees'
    oStockTransfer = 'oStockTransfer'
    oWorkOrders = 'oWorkOrders'
    oCreditPaymentMethods = 'oCreditPaymentMethods'
    oCreditCardPayments = 'oCreditCardPayments'
    oAlternateCatNum = 'oAlternateCatNum'
    oBudget = 'oBudget'
    oBudgetDistribution = 'oBudgetDistribution'
    oMessages = 'oMessages'
    oBudgetScenarios = 'oBudgetScenarios'
    oUserDefaultGroups = 'oUserDefaultGroups'
    oSalesOpportunities = 'oSalesOpportunities'
    oSalesStages = 'oSalesStages'
    oActivityTypes = 'oActivityTypes'
    oActivityLocations = 'oActivityLocations'
    oDrafts = 'oDrafts'
    oDeductionTaxHierarchies = 'oDeductionTaxHierarchies'
    oDeductionTaxGroups = 'oDeductionTaxGroups'
    oAdditionalExpenses = 'oAdditionalExpenses'
    oSalesTaxAuthorities = 'oSalesTaxAuthorities'
    oSalesTaxAuthoritiesTypes = 'oSalesTaxAuthoritiesTypes'
    oSalesTaxCodes = 'oSalesTaxCodes'
    oQueryCategories = 'oQueryCategories'
    oFactoringIndicators = 'oFactoringIndicators'
    oPaymentsDrafts = 'oPaymentsDrafts'
    oAccountSegmentations = 'oAccountSegmentations'
    oAccountSegmentationCategories = 'oAccountSegmentationCategories'
    oWarehouseLocations = 'oWarehouseLocations'
    oForms1099 = 'oForms1099'
    oInventoryCycles = 'oInventoryCycles'
    oWizardPaymentMethods = 'oWizardPaymentMethods'
    oBPPriorities = 'oBPPriorities'
    oDunningLetters = 'oDunningLetters'
    oUserFields = 'oUserFields'
    oUserTables = 'oUserTables'
    oPickLists = 'oPickLists'
    oPaymentRunExport = 'oPaymentRunExport'
    oUserQueries = 'oUserQueries'
    oMaterialRevaluation = 'oMaterialRevaluation'
    oCorrectionPurchaseInvoice = 'oCorrectionPurchaseInvoice'
    oCorrectionPurchaseInvoiceReversal = 'oCorrectionPurchaseInvoiceReversal'
    oCorrectionInvoice = 'oCorrectionInvoice'
    oCorrectionInvoiceReversal = 'oCorrectionInvoiceReversal'
    oContractTemplates = 'oContractTemplates'
    oEmployeesInfo = 'oEmployeesInfo'
    oCustomerEquipmentCards = 'oCustomerEquipmentCards'
    oWithholdingTaxCodes = 'oWithholdingTaxCodes'
    oBillOfExchangeTransactions = 'oBillOfExchangeTransactions'
    oKnowledgeBaseSolutions = 'oKnowledgeBaseSolutions'
    oServiceContracts = 'oServiceContracts'
    oServiceCalls = 'oServiceCalls'
    oUserKeys = 'oUserKeys'
    oQueue = 'oQueue'
    oSalesForecast = 'oSalesForecast'
    oTerritories = 'oTerritories'
    oIndustries = 'oIndustries'
    oProductionOrders = 'oProductionOrders'
    oDownPayments = 'oDownPayments'
    oPurchaseDownPayments = 'oPurchaseDownPayments'
    oPackagesTypes = 'oPackagesTypes'
    oUserObjectsMD = 'oUserObjectsMD'
    oTeams = 'oTeams'
    oRelationships = 'oRelationships'
    oUserPermissionTree = 'oUserPermissionTree'
    oActivityStatus = 'oActivityStatus'
    oChooseFromList = 'oChooseFromList'
    oFormattedSearches = 'oFormattedSearches'
    oAttachments2 = 'oAttachments2'
    oUserLanguages = 'oUserLanguages'
    oMultiLanguageTranslations = 'oMultiLanguageTranslations'
    oDynamicSystemStrings = 'oDynamicSystemStrings'
    oHouseBankAccounts = 'oHouseBankAccounts'
    oBusinessPlaces = 'oBusinessPlaces'
    oLocalEra = 'oLocalEra'
    oNotaFiscalCFOP = 'oNotaFiscalCFOP'
    oNotaFiscalCST = 'oNotaFiscalCST'
    oNotaFiscalUsage = 'oNotaFiscalUsage'
    oClosingDateProcedure = 'oClosingDateProcedure'
    oBPFiscalRegistryID = 'oBPFiscalRegistryID'
    oSalesTaxInvoice = 'oSalesTaxInvoice'
    oPurchaseTaxInvoice = 'oPurchaseTaxInvoice'
    oPurchaseQuotations = 'oPurchaseQuotations'
    oStockTransferDraft = 'oStockTransferDraft'
    oInventoryTransferRequest = 'oInventoryTransferRequest'
    oPurchaseRequest = 'oPurchaseRequest'
    oReturnRequest = 'oReturnRequest'
    oGoodsReturnRequest = 'oGoodsReturnRequest'
    oSelfInvoice = 'oSelfInvoice'
    oSelfCreditMemo = 'oSelfCreditMemo'

class BoOpenIncPayment(StrEnum):
    oip_No = 'oip_No'
    oip_Cash = 'oip_Cash'
    oip_Checks = 'oip_Checks'
    oip_Credit = 'oip_Credit'
    oip_BankTransfer = 'oip_BankTransfer'

if TYPE_CHECKING:
    BoOpenIncPaymentField = BoOpenIncPayment | Literal['oip_No', 'oip_Cash', 'oip_Checks', 'oip_Credit', 'oip_BankTransfer']
else:
    BoOpenIncPaymentField = BoOpenIncPayment

class BoOperationEnum(StrEnum):
    rloNone = 'rloNone'
    rloAddition = 'rloAddition'
    rloSubtraction = 'rloSubtraction'
    rloMultiplication = 'rloMultiplication'
    rloDivision = 'rloDivision'
    rloPercentage = 'rloPercentage'
    rloLeftPartCharacters = 'rloLeftPartCharacters'
    rloRightPartMantissa = 'rloRightPartMantissa'
    rloRound = 'rloRound'
    rloConcat = 'rloConcat'
    rloRight = 'rloRight'
    rloLeft = 'rloLeft'
    rloSentence = 'rloSentence'
    rloLength = 'rloLength'
    rloCurrency = 'rloCurrency'
    rloNumber = 'rloNumber'
    rloLessThan = 'rloLessThan'
    rloLessOrEqual = 'rloLessOrEqual'
    rloEqual = 'rloEqual'
    rloNotEqual = 'rloNotEqual'
    rloGreaterOrEqual = 'rloGreaterOrEqual'
    rloGreaterThan = 'rloGreaterThan'

if TYPE_CHECKING:
    BoOperationEnumField = BoOperationEnum | Literal['rloNone', 'rloAddition', 'rloSubtraction', 'rloMultiplication', 'rloDivision', 'rloPercentage', 'rloLeftPartCharacters', 'rloRightPartMantissa', 'rloRound', 'rloConcat', 'rloRight', 'rloLeft', 'rloSentence', 'rloLength', 'rloCurrency', 'rloNumber', 'rloLessThan', 'rloLessOrEqual', 'rloEqual', 'rloNotEqual', 'rloGreaterOrEqual', 'rloGreaterThan']
else:
    BoOperationEnumField = BoOperationEnum

class BoOpexStatus(StrEnum):
    bos_Open = 'bos_Open'
    bos_Close = 'bos_Close'

if TYPE_CHECKING:
    BoOpexStatusField = BoOpexStatus | Literal['bos_Open', 'bos_Close']
else:
    BoOpexStatusField = BoOpexStatus

class BoOrientationEnum(StrEnum):
    ortVertical = 'ortVertical'
    ortHorizontal = 'ortHorizontal'

if TYPE_CHECKING:
    BoOrientationEnumField = BoOrientationEnum | Literal['ortVertical', 'ortHorizontal']
else:
    BoOrientationEnumField = BoOrientationEnum

class BoPayTermDueTypes(StrEnum):
    pdt_MonthEnd = 'pdt_MonthEnd'
    pdt_HalfMonth = 'pdt_HalfMonth'
    pdt_MonthStart = 'pdt_MonthStart'
    pdt_None = 'pdt_None'

if TYPE_CHECKING:
    BoPayTermDueTypesField = BoPayTermDueTypes | Literal['pdt_MonthEnd', 'pdt_HalfMonth', 'pdt_MonthStart', 'pdt_None']
else:
    BoPayTermDueTypesField = BoPayTermDueTypes

class BoPaymentMeansEnum(StrEnum):
    bopmCheck = 'bopmCheck'
    bopmBankTransfer = 'bopmBankTransfer'
    bopmBillOfExchange = 'bopmBillOfExchange'

if TYPE_CHECKING:
    BoPaymentMeansEnumField = BoPaymentMeansEnum | Literal['bopmCheck', 'bopmBankTransfer', 'bopmBillOfExchange']
else:
    BoPaymentMeansEnumField = BoPaymentMeansEnum

class BoPaymentPriorities(StrEnum):
    bopp_Priority_1 = 'bopp_Priority_1'
    bopp_Priority_2 = 'bopp_Priority_2'
    bopp_Priority_3 = 'bopp_Priority_3'
    bopp_Priority_4 = 'bopp_Priority_4'
    bopp_Priority_5 = 'bopp_Priority_5'
    bopp_Priority_6 = 'bopp_Priority_6'

if TYPE_CHECKING:
    BoPaymentPrioritiesField = BoPaymentPriorities | Literal['bopp_Priority_1', 'bopp_Priority_2', 'bopp_Priority_3', 'bopp_Priority_4', 'bopp_Priority_5', 'bopp_Priority_6']
else:
    BoPaymentPrioritiesField = BoPaymentPriorities

class BoPaymentTypeEnum(StrEnum):
    boptIncoming = 'boptIncoming'
    boptOutgoing = 'boptOutgoing'

if TYPE_CHECKING:
    BoPaymentTypeEnumField = BoPaymentTypeEnum | Literal['boptIncoming', 'boptOutgoing']
else:
    BoPaymentTypeEnumField = BoPaymentTypeEnum

class BoPaymentsObjectType(StrEnum):
    bopot_IncomingPayments = 'bopot_IncomingPayments'
    bopot_OutgoingPayments = 'bopot_OutgoingPayments'

if TYPE_CHECKING:
    BoPaymentsObjectTypeField = BoPaymentsObjectType | Literal['bopot_IncomingPayments', 'bopot_OutgoingPayments']
else:
    BoPaymentsObjectTypeField = BoPaymentsObjectType

class BoPermission(StrEnum):
    boper_Full = 'boper_Full'
    boper_ReadOnly = 'boper_ReadOnly'
    boper_None = 'boper_None'
    boper_Various = 'boper_Various'
    boper_Undefined = 'boper_Undefined'

if TYPE_CHECKING:
    BoPermissionField = BoPermission | Literal['boper_Full', 'boper_ReadOnly', 'boper_None', 'boper_Various', 'boper_Undefined']
else:
    BoPermissionField = BoPermission

class BoPickStatus(StrEnum):
    ps_Released = 'ps_Released'
    ps_Picked = 'ps_Picked'
    ps_PartiallyPicked = 'ps_PartiallyPicked'
    ps_PartiallyDelivered = 'ps_PartiallyDelivered'
    ps_Closed = 'ps_Closed'

if TYPE_CHECKING:
    BoPickStatusField = BoPickStatus | Literal['ps_Released', 'ps_Picked', 'ps_PartiallyPicked', 'ps_PartiallyDelivered', 'ps_Closed']
else:
    BoPickStatusField = BoPickStatus

class BoPictureSizeEnum(StrEnum):
    rlpsOriginalSize = 'rlpsOriginalSize'
    rlpsFitFieldSizeNonProportionally = 'rlpsFitFieldSizeNonProportionally'
    rlpsFitFieldSizeProportionally = 'rlpsFitFieldSizeProportionally'
    rlpsFitFieldHeight = 'rlpsFitFieldHeight'
    rlpsFitFieldWidth = 'rlpsFitFieldWidth'

if TYPE_CHECKING:
    BoPictureSizeEnumField = BoPictureSizeEnum | Literal['rlpsOriginalSize', 'rlpsFitFieldSizeNonProportionally', 'rlpsFitFieldSizeProportionally', 'rlpsFitFieldHeight', 'rlpsFitFieldWidth']
else:
    BoPictureSizeEnumField = BoPictureSizeEnum

class BoPlanningSystem(StrEnum):
    bop_MRP = 'bop_MRP'
    bop_None = 'bop_None'

if TYPE_CHECKING:
    BoPlanningSystemField = BoPlanningSystem | Literal['bop_MRP', 'bop_None']
else:
    BoPlanningSystemField = BoPlanningSystem

class BoPriceListGroupNum(StrEnum):
    boplgn_Group1 = 'boplgn_Group1'
    boplgn_Group2 = 'boplgn_Group2'
    boplgn_Group3 = 'boplgn_Group3'
    boplgn_Group4 = 'boplgn_Group4'

if TYPE_CHECKING:
    BoPriceListGroupNumField = BoPriceListGroupNum | Literal['boplgn_Group1', 'boplgn_Group2', 'boplgn_Group3', 'boplgn_Group4']
else:
    BoPriceListGroupNumField = BoPriceListGroupNum

class BoPrintReceiptEnum(StrEnum):
    boprcAlways = 'boprcAlways'
    boprcNo = 'boprcNo'
    boprcOnlyWhenAdding = 'boprcOnlyWhenAdding'

if TYPE_CHECKING:
    BoPrintReceiptEnumField = BoPrintReceiptEnum | Literal['boprcAlways', 'boprcNo', 'boprcOnlyWhenAdding']
else:
    BoPrintReceiptEnumField = BoPrintReceiptEnum

class BoProcurementMethod(StrEnum):
    bom_Buy = 'bom_Buy'
    bom_Make = 'bom_Make'

if TYPE_CHECKING:
    BoProcurementMethodField = BoProcurementMethod | Literal['bom_Buy', 'bom_Make']
else:
    BoProcurementMethodField = BoProcurementMethod

class BoProductSources(StrEnum):
    bps_PurchasedFromDomVendor = 'bps_PurchasedFromDomVendor'
    bps_ImportedByCompany = 'bps_ImportedByCompany'
    bps_ImportedGoodsPurchasedFromDomVendor = 'bps_ImportedGoodsPurchasedFromDomVendor'
    bps_ProducedByCompany = 'bps_ProducedByCompany'

if TYPE_CHECKING:
    BoProductSourcesField = BoProductSources | Literal['bps_PurchasedFromDomVendor', 'bps_ImportedByCompany', 'bps_ImportedGoodsPurchasedFromDomVendor', 'bps_ProducedByCompany']
else:
    BoProductSourcesField = BoProductSources

class BoProductionOrderOriginEnum(StrEnum):
    bopooManual = 'bopooManual'
    bopooMRP = 'bopooMRP'
    bopooSalesOrder = 'bopooSalesOrder'
    bopooProductionOrder = 'bopooProductionOrder'

if TYPE_CHECKING:
    BoProductionOrderOriginEnumField = BoProductionOrderOriginEnum | Literal['bopooManual', 'bopooMRP', 'bopooSalesOrder', 'bopooProductionOrder']
else:
    BoProductionOrderOriginEnumField = BoProductionOrderOriginEnum

class BoProductionOrderStatusEnum(StrEnum):
    boposPlanned = 'boposPlanned'
    boposReleased = 'boposReleased'
    boposClosed = 'boposClosed'
    boposCancelled = 'boposCancelled'

if TYPE_CHECKING:
    BoProductionOrderStatusEnumField = BoProductionOrderStatusEnum | Literal['boposPlanned', 'boposReleased', 'boposClosed', 'boposCancelled']
else:
    BoProductionOrderStatusEnumField = BoProductionOrderStatusEnum

class BoProductionOrderTypeEnum(StrEnum):
    bopotStandard = 'bopotStandard'
    bopotSpecial = 'bopotSpecial'
    bopotDisassembly = 'bopotDisassembly'

if TYPE_CHECKING:
    BoProductionOrderTypeEnumField = BoProductionOrderTypeEnum | Literal['bopotStandard', 'bopotSpecial', 'bopotDisassembly']
else:
    BoProductionOrderTypeEnumField = BoProductionOrderTypeEnum

class BoQueryTypeEnum(StrEnum):
    qtRegular = 'qtRegular'
    qtWizard = 'qtWizard'

if TYPE_CHECKING:
    BoQueryTypeEnumField = BoQueryTypeEnum | Literal['qtRegular', 'qtWizard']
else:
    BoQueryTypeEnumField = BoQueryTypeEnum

class BoRcptCredTypes(StrEnum):
    cr_Regular = 'cr_Regular'
    cr_Telephone = 'cr_Telephone'
    cr_InternetTransaction = 'cr_InternetTransaction'

if TYPE_CHECKING:
    BoRcptCredTypesField = BoRcptCredTypes | Literal['cr_Regular', 'cr_Telephone', 'cr_InternetTransaction']
else:
    BoRcptCredTypesField = BoRcptCredTypes

class BoRcptInvTypes(StrEnum):
    it_AllTransactions = 'it_AllTransactions'
    it_OpeningBalance = 'it_OpeningBalance'
    it_ClosingBalance = 'it_ClosingBalance'
    it_Invoice = 'it_Invoice'
    it_CredItnote = 'it_CredItnote'
    it_TaxInvoice = 'it_TaxInvoice'
    it_Return = 'it_Return'
    it_PurchaseInvoice = 'it_PurchaseInvoice'
    it_PurchaseCreditNote = 'it_PurchaseCreditNote'
    it_PurchaseDeliveryNote = 'it_PurchaseDeliveryNote'
    it_PurchaseReturn = 'it_PurchaseReturn'
    it_Receipt = 'it_Receipt'
    it_Deposit = 'it_Deposit'
    it_JournalEntry = 'it_JournalEntry'
    it_PaymentAdvice = 'it_PaymentAdvice'
    it_ChequesForPayment = 'it_ChequesForPayment'
    it_StockReconciliations = 'it_StockReconciliations'
    it_GeneralReceiptToStock = 'it_GeneralReceiptToStock'
    it_GeneralReleaseFromStock = 'it_GeneralReleaseFromStock'
    it_TransferBetweenWarehouses = 'it_TransferBetweenWarehouses'
    it_WorkInstructions = 'it_WorkInstructions'
    it_DeferredDeposit = 'it_DeferredDeposit'
    it_CorrectionInvoice = 'it_CorrectionInvoice'
    it_APCorrectionInvoice = 'it_APCorrectionInvoice'
    it_ARCorrectionInvoice = 'it_ARCorrectionInvoice'
    it_DownPayment = 'it_DownPayment'
    it_PurchaseDownPayment = 'it_PurchaseDownPayment'

if TYPE_CHECKING:
    BoRcptInvTypesField = BoRcptInvTypes | Literal['it_AllTransactions', 'it_OpeningBalance', 'it_ClosingBalance', 'it_Invoice', 'it_CredItnote', 'it_TaxInvoice', 'it_Return', 'it_PurchaseInvoice', 'it_PurchaseCreditNote', 'it_PurchaseDeliveryNote', 'it_PurchaseReturn', 'it_Receipt', 'it_Deposit', 'it_JournalEntry', 'it_PaymentAdvice', 'it_ChequesForPayment', 'it_StockReconciliations', 'it_GeneralReceiptToStock', 'it_GeneralReleaseFromStock', 'it_TransferBetweenWarehouses', 'it_WorkInstructions', 'it_DeferredDeposit', 'it_CorrectionInvoice', 'it_APCorrectionInvoice', 'it_ARCorrectionInvoice', 'it_DownPayment', 'it_PurchaseDownPayment']
else:
    BoRcptInvTypesField = BoRcptInvTypes

class BoRcptTypes(StrEnum):
    rCustomer = 'rCustomer'
    rAccount = 'rAccount'
    rSupplier = 'rSupplier'

if TYPE_CHECKING:
    BoRcptTypesField = BoRcptTypes | Literal['rCustomer', 'rAccount', 'rSupplier']
else:
    BoRcptTypesField = BoRcptTypes

class BoRemindUnits(StrEnum):
    reu_Days = 'reu_Days'
    reu_Weeks = 'reu_Weeks'
    reu_Month = 'reu_Month'

if TYPE_CHECKING:
    BoRemindUnitsField = BoRemindUnits | Literal['reu_Days', 'reu_Weeks', 'reu_Month']
else:
    BoRemindUnitsField = BoRemindUnits

class BoReportLayoutItemTypeEnum(StrEnum):
    rlitPageHeader = 'rlitPageHeader'
    rlitStartOfReport = 'rlitStartOfReport'
    rlitRepetitiveAreaHeader = 'rlitRepetitiveAreaHeader'
    rlitRepetitiveArea = 'rlitRepetitiveArea'
    rlitRepetitiveAreaFooter = 'rlitRepetitiveAreaFooter'
    rlitEndOfReport = 'rlitEndOfReport'
    rlitPageFooter = 'rlitPageFooter'
    rlitTextField = 'rlitTextField'
    rlitPictureField = 'rlitPictureField'
    rlitUserField = 'rlitUserField'

if TYPE_CHECKING:
    BoReportLayoutItemTypeEnumField = BoReportLayoutItemTypeEnum | Literal['rlitPageHeader', 'rlitStartOfReport', 'rlitRepetitiveAreaHeader', 'rlitRepetitiveArea', 'rlitRepetitiveAreaFooter', 'rlitEndOfReport', 'rlitPageFooter', 'rlitTextField', 'rlitPictureField', 'rlitUserField']
else:
    BoReportLayoutItemTypeEnumField = BoReportLayoutItemTypeEnum

class BoResolutionUnits(StrEnum):
    rsu_Days = 'rsu_Days'
    rsu_Hours = 'rsu_Hours'

if TYPE_CHECKING:
    BoResolutionUnitsField = BoResolutionUnits | Literal['rsu_Days', 'rsu_Hours']
else:
    BoResolutionUnitsField = BoResolutionUnits

class BoResponseUnit(StrEnum):
    boru_Day = 'boru_Day'
    boru_Hour = 'boru_Hour'

if TYPE_CHECKING:
    BoResponseUnitField = BoResponseUnit | Literal['boru_Day', 'boru_Hour']
else:
    BoResponseUnitField = BoResponseUnit

class BoRoleInTeam(StrEnum):
    borit_Leader = 'borit_Leader'
    borit_Member = 'borit_Member'

if TYPE_CHECKING:
    BoRoleInTeamField = BoRoleInTeam | Literal['borit_Leader', 'borit_Member']
else:
    BoRoleInTeamField = BoRoleInTeam

class BoRoundingMethod(StrEnum):
    borm_FixedEnding = 'borm_FixedEnding'
    borm_FixedInterval = 'borm_FixedInterval'
    borm_NoRounding = 'borm_NoRounding'
    borm_RoundToFullAmount = 'borm_RoundToFullAmount'
    borm_RoundToFullDecAmount = 'borm_RoundToFullDecAmount'
    borm_RoundToFullTensAmount = 'borm_RoundToFullTensAmount'

if TYPE_CHECKING:
    BoRoundingMethodField = BoRoundingMethod | Literal['borm_FixedEnding', 'borm_FixedInterval', 'borm_NoRounding', 'borm_RoundToFullAmount', 'borm_RoundToFullDecAmount', 'borm_RoundToFullTensAmount']
else:
    BoRoundingMethodField = BoRoundingMethod

class BoRoundingRule(StrEnum):
    borrRoundDown = 'borrRoundDown'
    borrRoundOff = 'borrRoundOff'
    borrRoundUp = 'borrRoundUp'

if TYPE_CHECKING:
    BoRoundingRuleField = BoRoundingRule | Literal['borrRoundDown', 'borrRoundOff', 'borrRoundUp']
else:
    BoRoundingRuleField = BoRoundingRule

class BoSalaryCostUnits(StrEnum):
    scu_Hour = 'scu_Hour'
    scu_Day = 'scu_Day'
    scu_Week = 'scu_Week'
    scu_Month = 'scu_Month'
    scu_Year = 'scu_Year'
    scu_Semimonthly = 'scu_Semimonthly'
    scu_Biweekly = 'scu_Biweekly'

if TYPE_CHECKING:
    BoSalaryCostUnitsField = BoSalaryCostUnits | Literal['scu_Hour', 'scu_Day', 'scu_Week', 'scu_Month', 'scu_Year', 'scu_Semimonthly', 'scu_Biweekly']
else:
    BoSalaryCostUnitsField = BoSalaryCostUnits

class BoSerialNumberStatus(StrEnum):
    sns_Active = 'sns_Active'
    sns_Returned = 'sns_Returned'
    sns_Terminated = 'sns_Terminated'
    sns_Loaned = 'sns_Loaned'
    sns_InLab = 'sns_InLab'

if TYPE_CHECKING:
    BoSerialNumberStatusField = BoSerialNumberStatus | Literal['sns_Active', 'sns_Returned', 'sns_Terminated', 'sns_Loaned', 'sns_InLab']
else:
    BoSerialNumberStatusField = BoSerialNumberStatus

class BoSeriesGroupEnum(StrEnum):
    sg_Group1 = 'sg_Group1'
    sg_Group2 = 'sg_Group2'
    sg_Group3 = 'sg_Group3'
    sg_Group4 = 'sg_Group4'
    sg_Group5 = 'sg_Group5'
    sg_Group6 = 'sg_Group6'
    sg_Group7 = 'sg_Group7'
    sg_Group8 = 'sg_Group8'
    sg_Group9 = 'sg_Group9'
    sg_Group10 = 'sg_Group10'

if TYPE_CHECKING:
    BoSeriesGroupEnumField = BoSeriesGroupEnum | Literal['sg_Group1', 'sg_Group2', 'sg_Group3', 'sg_Group4', 'sg_Group5', 'sg_Group6', 'sg_Group7', 'sg_Group8', 'sg_Group9', 'sg_Group10']
else:
    BoSeriesGroupEnumField = BoSeriesGroupEnum

class BoSeriesTypeEnum(StrEnum):
    stDocument = 'stDocument'
    stBusinessPartner = 'stBusinessPartner'
    stItem = 'stItem'
    stResource = 'stResource'

if TYPE_CHECKING:
    BoSeriesTypeEnumField = BoSeriesTypeEnum | Literal['stDocument', 'stBusinessPartner', 'stItem', 'stResource']
else:
    BoSeriesTypeEnumField = BoSeriesTypeEnum

class BoServicePaymentMethods(StrEnum):
    spmAccreditedToBankAccount = 'spmAccreditedToBankAccount'
    spmBankTransfer = 'spmBankTransfer'
    spmOther = 'spmOther'

if TYPE_CHECKING:
    BoServicePaymentMethodsField = BoServicePaymentMethods | Literal['spmAccreditedToBankAccount', 'spmBankTransfer', 'spmOther']
else:
    BoServicePaymentMethodsField = BoServicePaymentMethods

class BoServiceSupplyMethods(StrEnum):
    ssmImmediate = 'ssmImmediate'
    ssmToMoreResumptions = 'ssmToMoreResumptions'

if TYPE_CHECKING:
    BoServiceSupplyMethodsField = BoServiceSupplyMethods | Literal['ssmImmediate', 'ssmToMoreResumptions']
else:
    BoServiceSupplyMethodsField = BoServiceSupplyMethods

class BoServiceTypes(StrEnum):
    bst_Regular = 'bst_Regular'
    bst_Warranty = 'bst_Warranty'

if TYPE_CHECKING:
    BoServiceTypesField = BoServiceTypes | Literal['bst_Regular', 'bst_Warranty']
else:
    BoServiceTypesField = BoServiceTypes

class BoSoClosedInTypes(StrEnum):
    sos_Months = 'sos_Months'
    sos_Weeks = 'sos_Weeks'
    sos_Days = 'sos_Days'

if TYPE_CHECKING:
    BoSoClosedInTypesField = BoSoClosedInTypes | Literal['sos_Months', 'sos_Weeks', 'sos_Days']
else:
    BoSoClosedInTypesField = BoSoClosedInTypes

class BoSoOsStatus(StrEnum):
    sos_Open = 'sos_Open'
    sos_Missed = 'sos_Missed'
    sos_Sold = 'sos_Sold'

if TYPE_CHECKING:
    BoSoOsStatusField = BoSoOsStatus | Literal['sos_Open', 'sos_Missed', 'sos_Sold']
else:
    BoSoOsStatusField = BoSoOsStatus

class BoSoStatus(StrEnum):
    so_Open = 'so_Open'
    so_Closed = 'so_Closed'

if TYPE_CHECKING:
    BoSoStatusField = BoSoStatus | Literal['so_Open', 'so_Closed']
else:
    BoSoStatusField = BoSoStatus

class BoSortTypeEnum(StrEnum):
    rlstAlpha = 'rlstAlpha'
    rlstNumeric = 'rlstNumeric'
    rlstMoney = 'rlstMoney'
    rlstDate = 'rlstDate'

if TYPE_CHECKING:
    BoSortTypeEnumField = BoSortTypeEnum | Literal['rlstAlpha', 'rlstNumeric', 'rlstMoney', 'rlstDate']
else:
    BoSortTypeEnumField = BoSortTypeEnum

class BoStatus(StrEnum):
    bost_Open = 'bost_Open'
    bost_Close = 'bost_Close'
    bost_Paid = 'bost_Paid'
    bost_Delivered = 'bost_Delivered'

if TYPE_CHECKING:
    BoStatusField = BoStatus | Literal['bost_Open', 'bost_Close', 'bost_Paid', 'bost_Delivered']
else:
    BoStatusField = BoStatus

class BoStckTrnDir(StrEnum):
    bos_TransferToTechnician = 'bos_TransferToTechnician'
    bos_TransferFromTechnician = 'bos_TransferFromTechnician'

if TYPE_CHECKING:
    BoStckTrnDirField = BoStckTrnDir | Literal['bos_TransferToTechnician', 'bos_TransferFromTechnician']
else:
    BoStckTrnDirField = BoStckTrnDir

class BoSubFrequencyTypeEnum(StrEnum):
    sftEmpty = 'sftEmpty'
    sftDailyEvery1 = 'sftDailyEvery1'
    sftDailyEvery2 = 'sftDailyEvery2'
    sftDailyEvery3 = 'sftDailyEvery3'
    sftDailyEvery4 = 'sftDailyEvery4'
    sftDailyEvery5 = 'sftDailyEvery5'
    sftDailyEvery6 = 'sftDailyEvery6'
    sftDailyEvery7 = 'sftDailyEvery7'
    sftDailyEvery8 = 'sftDailyEvery8'
    sftDailyEvery9 = 'sftDailyEvery9'
    sftDailyEvery10 = 'sftDailyEvery10'
    sftDailyEvery15 = 'sftDailyEvery15'
    sftDailyEvery30 = 'sftDailyEvery30'
    sftDailyEvery45 = 'sftDailyEvery45'
    sftDailyEvery60 = 'sftDailyEvery60'
    sftWeeklyOnSunday = 'sftWeeklyOnSunday'
    sftWeeklyOnMonday = 'sftWeeklyOnMonday'
    sftWeeklyOnTuesday = 'sftWeeklyOnTuesday'
    sftWeeklyOnWednesday = 'sftWeeklyOnWednesday'
    sftWeeklyOnThursday = 'sftWeeklyOnThursday'
    sftWeeklyOnFriday = 'sftWeeklyOnFriday'
    sftWeeklyOnSaturday = 'sftWeeklyOnSaturday'
    sftMonthlyOn1 = 'sftMonthlyOn1'
    sftMonthlyOn2 = 'sftMonthlyOn2'
    sftMonthlyOn3 = 'sftMonthlyOn3'
    sftMonthlyOn4 = 'sftMonthlyOn4'
    sftMonthlyOn5 = 'sftMonthlyOn5'
    sftMonthlyOn6 = 'sftMonthlyOn6'
    sftMonthlyOn7 = 'sftMonthlyOn7'
    sftMonthlyOn8 = 'sftMonthlyOn8'
    sftMonthlyOn9 = 'sftMonthlyOn9'
    sftMonthlyOn10 = 'sftMonthlyOn10'
    sftMonthlyOn11 = 'sftMonthlyOn11'
    sftMonthlyOn12 = 'sftMonthlyOn12'
    sftMonthlyOn13 = 'sftMonthlyOn13'
    sftMonthlyOn14 = 'sftMonthlyOn14'
    sftMonthlyOn15 = 'sftMonthlyOn15'
    sftMonthlyOn16 = 'sftMonthlyOn16'
    sftMonthlyOn17 = 'sftMonthlyOn17'
    sftMonthlyOn18 = 'sftMonthlyOn18'
    sftMonthlyOn19 = 'sftMonthlyOn19'
    sftMonthlyOn20 = 'sftMonthlyOn20'
    sftMonthlyOn21 = 'sftMonthlyOn21'
    sftMonthlyOn22 = 'sftMonthlyOn22'
    sftMonthlyOn23 = 'sftMonthlyOn23'
    sftMonthlyOn24 = 'sftMonthlyOn24'
    sftMonthlyOn25 = 'sftMonthlyOn25'
    sftMonthlyOn26 = 'sftMonthlyOn26'
    sftMonthlyOn27 = 'sftMonthlyOn27'
    sftMonthlyOn28 = 'sftMonthlyOn28'
    sftMonthlyOn29 = 'sftMonthlyOn29'
    sftMonthlyOn30 = 'sftMonthlyOn30'
    sftMonthlyOn31 = 'sftMonthlyOn31'

class BoSubPeriodTypeEnum(StrEnum):
    spt_Year = 'spt_Year'
    spt_Quarters = 'spt_Quarters'
    spt_Months = 'spt_Months'
    spt_Days = 'spt_Days'

if TYPE_CHECKING:
    BoSubPeriodTypeEnumField = BoSubPeriodTypeEnum | Literal['spt_Year', 'spt_Quarters', 'spt_Months', 'spt_Days']
else:
    BoSubPeriodTypeEnumField = BoSubPeriodTypeEnum

class BoSuppLangs(StrEnum):
    ln_Null = 'ln_Null'
    ln_Hebrew = 'ln_Hebrew'
    ln_Spanish_Ar = 'ln_Spanish_Ar'
    ln_English = 'ln_English'
    ln_Polish = 'ln_Polish'
    ln_English_Sg = 'ln_English_Sg'
    ln_Spanish_Pa = 'ln_Spanish_Pa'
    ln_English_Gb = 'ln_English_Gb'
    ln_German = 'ln_German'
    ln_Serbian = 'ln_Serbian'
    ln_Danish = 'ln_Danish'
    ln_Norwegian = 'ln_Norwegian'
    ln_Italian = 'ln_Italian'
    ln_Hungarian = 'ln_Hungarian'
    ln_Chinese = 'ln_Chinese'
    ln_Dutch = 'ln_Dutch'
    ln_Finnish = 'ln_Finnish'
    ln_Greek = 'ln_Greek'
    ln_Portuguese = 'ln_Portuguese'
    ln_Swedish = 'ln_Swedish'
    ln_English_Cy = 'ln_English_Cy'
    ln_French = 'ln_French'
    ln_Spanish = 'ln_Spanish'
    ln_Russian = 'ln_Russian'
    ln_Spanish_La = 'ln_Spanish_La'
    ln_Czech_Cz = 'ln_Czech_Cz'
    ln_Slovak_Sk = 'ln_Slovak_Sk'
    ln_Korean_Kr = 'ln_Korean_Kr'
    ln_Portuguese_Br = 'ln_Portuguese_Br'
    ln_Japanese_Jp = 'ln_Japanese_Jp'
    ln_Turkish_Tr = 'ln_Turkish_Tr'
    ln_Arabic = 'ln_Arabic'
    ln_Ukrainian = 'ln_Ukrainian'
    ln_TrdtnlChinese_Hk = 'ln_TrdtnlChinese_Hk'

if TYPE_CHECKING:
    BoSuppLangsField = BoSuppLangs | Literal['ln_Null', 'ln_Hebrew', 'ln_Spanish_Ar', 'ln_English', 'ln_Polish', 'ln_English_Sg', 'ln_Spanish_Pa', 'ln_English_Gb', 'ln_German', 'ln_Serbian', 'ln_Danish', 'ln_Norwegian', 'ln_Italian', 'ln_Hungarian', 'ln_Chinese', 'ln_Dutch', 'ln_Finnish', 'ln_Greek', 'ln_Portuguese', 'ln_Swedish', 'ln_English_Cy', 'ln_French', 'ln_Spanish', 'ln_Russian', 'ln_Spanish_La', 'ln_Czech_Cz', 'ln_Slovak_Sk', 'ln_Korean_Kr', 'ln_Portuguese_Br', 'ln_Japanese_Jp', 'ln_Turkish_Tr', 'ln_Arabic', 'ln_Ukrainian', 'ln_TrdtnlChinese_Hk']
else:
    BoSuppLangsField = BoSuppLangs

class BoSvcCallPriorities(StrEnum):
    scp_Low = 'scp_Low'
    scp_Medium = 'scp_Medium'
    scp_High = 'scp_High'

if TYPE_CHECKING:
    BoSvcCallPrioritiesField = BoSvcCallPriorities | Literal['scp_Low', 'scp_Medium', 'scp_High']
else:
    BoSvcCallPrioritiesField = BoSvcCallPriorities

class BoSvcContractStatus(StrEnum):
    scs_Approved = 'scs_Approved'
    scs_Frozen = 'scs_Frozen'
    scs_Draft = 'scs_Draft'
    scs_Terminated = 'scs_Terminated'

if TYPE_CHECKING:
    BoSvcContractStatusField = BoSvcContractStatus | Literal['scs_Approved', 'scs_Frozen', 'scs_Draft', 'scs_Terminated']
else:
    BoSvcContractStatusField = BoSvcContractStatus

class BoSvcEpxDocTypes(StrEnum):
    edt_Invoice = 'edt_Invoice'
    edt_Delivery = 'edt_Delivery'
    edt_Return = 'edt_Return'
    edt_StockTransfer = 'edt_StockTransfer'
    edt_CreditMemo = 'edt_CreditMemo'
    edt_Order = 'edt_Order'
    edt_Quotation = 'edt_Quotation'
    edt_AP_Invoice = 'edt_AP_Invoice'
    edt_AP_CreditMemo = 'edt_AP_CreditMemo'
    edt_GoodsReceipt = 'edt_GoodsReceipt'
    edt_GoodsReturn = 'edt_GoodsReturn'
    edt_PurchaseOrder = 'edt_PurchaseOrder'
    edt_PurchaseQuotation = 'edt_PurchaseQuotation'
    edt_AR_CorrectionInvoice = 'edt_AR_CorrectionInvoice'
    edt_AP_CorrectionInvoice = 'edt_AP_CorrectionInvoice'
    edt_Return_Request = 'edt_Return_Request'
    edt_Goods_Return_Request = 'edt_Goods_Return_Request'

if TYPE_CHECKING:
    BoSvcEpxDocTypesField = BoSvcEpxDocTypes | Literal['edt_Invoice', 'edt_Delivery', 'edt_Return', 'edt_StockTransfer', 'edt_CreditMemo', 'edt_Order', 'edt_Quotation', 'edt_AP_Invoice', 'edt_AP_CreditMemo', 'edt_GoodsReceipt', 'edt_GoodsReturn', 'edt_PurchaseOrder', 'edt_PurchaseQuotation', 'edt_AR_CorrectionInvoice', 'edt_AP_CorrectionInvoice', 'edt_Return_Request', 'edt_Goods_Return_Request']
else:
    BoSvcEpxDocTypesField = BoSvcEpxDocTypes

class BoSvcExpPartTypes(StrEnum):
    sep_Inventory = 'sep_Inventory'
    sep_NonInventory = 'sep_NonInventory'

if TYPE_CHECKING:
    BoSvcExpPartTypesField = BoSvcExpPartTypes | Literal['sep_Inventory', 'sep_NonInventory']
else:
    BoSvcExpPartTypesField = BoSvcExpPartTypes

class BoTCDConditionEnum(StrEnum):
    tcdcNone = 'tcdcNone'
    tcdcFederalTaxID = 'tcdcFederalTaxID'
    tcdcShipToAddress = 'tcdcShipToAddress'
    tcdcShipToStreePOBox = 'tcdcShipToStreePOBox'
    tcdcShipToCity = 'tcdcShipToCity'
    tcdcShipToZipCode = 'tcdcShipToZipCode'
    tcdcShipToCounty = 'tcdcShipToCounty'
    tcdcShipToState = 'tcdcShipToState'
    tcdcShipToCountry = 'tcdcShipToCountry'
    tcdcItem = 'tcdcItem'
    tcdcItemGroup = 'tcdcItemGroup'
    tcdcBusinessPartner = 'tcdcBusinessPartner'
    tcdcCustomerGroup = 'tcdcCustomerGroup'
    tcdcVendorGroup = 'tcdcVendorGroup'
    tcdcWarehouse = 'tcdcWarehouse'
    tcdcGLAccount = 'tcdcGLAccount'
    tcdcCustomerEquTax = 'tcdcCustomerEquTax'
    tcdcTaxStatus = 'tcdcTaxStatus'
    tcdcFreight = 'tcdcFreight'
    tcdcUDF = 'tcdcUDF'
    tcdcBranchNumber = 'tcdcBranchNumber'
    tcdcTypeOfBusiness = 'tcdcTypeOfBusiness'

if TYPE_CHECKING:
    BoTCDConditionEnumField = BoTCDConditionEnum | Literal['tcdcNone', 'tcdcFederalTaxID', 'tcdcShipToAddress', 'tcdcShipToStreePOBox', 'tcdcShipToCity', 'tcdcShipToZipCode', 'tcdcShipToCounty', 'tcdcShipToState', 'tcdcShipToCountry', 'tcdcItem', 'tcdcItemGroup', 'tcdcBusinessPartner', 'tcdcCustomerGroup', 'tcdcVendorGroup', 'tcdcWarehouse', 'tcdcGLAccount', 'tcdcCustomerEquTax', 'tcdcTaxStatus', 'tcdcFreight', 'tcdcUDF', 'tcdcBranchNumber', 'tcdcTypeOfBusiness']
else:
    BoTCDConditionEnumField = BoTCDConditionEnum

class BoTCDDocumentTypeEnum(StrEnum):
    tcddtItem = 'tcddtItem'
    tcddtService = 'tcddtService'
    tcddtItemAndService = 'tcddtItemAndService'

if TYPE_CHECKING:
    BoTCDDocumentTypeEnumField = BoTCDDocumentTypeEnum | Literal['tcddtItem', 'tcddtService', 'tcddtItemAndService']
else:
    BoTCDDocumentTypeEnumField = BoTCDDocumentTypeEnum

class BoTaxInvoiceTypes(StrEnum):
    botit_AlterationCorrectionInvoice = 'botit_AlterationCorrectionInvoice'
    botit_AlterationInvoice = 'botit_AlterationInvoice'
    botit_CorrectionInvoice = 'botit_CorrectionInvoice'
    botit_Invoice = 'botit_Invoice'
    botit_JournalEntry = 'botit_JournalEntry'
    botit_Payment = 'botit_Payment'

if TYPE_CHECKING:
    BoTaxInvoiceTypesField = BoTaxInvoiceTypes | Literal['botit_AlterationCorrectionInvoice', 'botit_AlterationInvoice', 'botit_CorrectionInvoice', 'botit_Invoice', 'botit_JournalEntry', 'botit_Payment']
else:
    BoTaxInvoiceTypesField = BoTaxInvoiceTypes

class BoTaxOnInstallmentsTypeEnum(StrEnum):
    toiProportionally = 'toiProportionally'
    toiTaxInFirst = 'toiTaxInFirst'
    toiTaxInFirstOnly = 'toiTaxInFirstOnly'

if TYPE_CHECKING:
    BoTaxOnInstallmentsTypeEnumField = BoTaxOnInstallmentsTypeEnum | Literal['toiProportionally', 'toiTaxInFirst', 'toiTaxInFirstOnly']
else:
    BoTaxOnInstallmentsTypeEnumField = BoTaxOnInstallmentsTypeEnum

class BoTaxPostAccEnum(StrEnum):
    tpa_Default = 'tpa_Default'
    tpa_SalesTaxAccount = 'tpa_SalesTaxAccount'
    tpa_PurchaseTaxAccount = 'tpa_PurchaseTaxAccount'

if TYPE_CHECKING:
    BoTaxPostAccEnumField = BoTaxPostAccEnum | Literal['tpa_Default', 'tpa_SalesTaxAccount', 'tpa_PurchaseTaxAccount']
else:
    BoTaxPostAccEnumField = BoTaxPostAccEnum

class BoTaxPostingAccountTypeEnum(StrEnum):
    tpatEmpty = 'tpatEmpty'
    tpatSalesTaxAccount = 'tpatSalesTaxAccount'
    tpatPurchasingTaxAccount = 'tpatPurchasingTaxAccount'

if TYPE_CHECKING:
    BoTaxPostingAccountTypeEnumField = BoTaxPostingAccountTypeEnum | Literal['tpatEmpty', 'tpatSalesTaxAccount', 'tpatPurchasingTaxAccount']
else:
    BoTaxPostingAccountTypeEnumField = BoTaxPostingAccountTypeEnum

class BoTaxRoundingRuleTypes(StrEnum):
    trr_RoundDown = 'trr_RoundDown'
    trr_RoundUp = 'trr_RoundUp'
    trr_RoundOff = 'trr_RoundOff'
    trr_CompanyDefault = 'trr_CompanyDefault'

if TYPE_CHECKING:
    BoTaxRoundingRuleTypesField = BoTaxRoundingRuleTypes | Literal['trr_RoundDown', 'trr_RoundUp', 'trr_RoundOff', 'trr_CompanyDefault']
else:
    BoTaxRoundingRuleTypesField = BoTaxRoundingRuleTypes

class BoTaxTypes(StrEnum):
    tt_Yes = 'tt_Yes'
    tt_No = 'tt_No'
    tt_UseTax = 'tt_UseTax'
    tt_OffsetTax = 'tt_OffsetTax'

if TYPE_CHECKING:
    BoTaxTypesField = BoTaxTypes | Literal['tt_Yes', 'tt_No', 'tt_UseTax', 'tt_OffsetTax']
else:
    BoTaxTypesField = BoTaxTypes

class BoTimeTemplate(StrEnum):
    tt_24H = 'tt_24H'
    tt_12H = 'tt_12H'

if TYPE_CHECKING:
    BoTimeTemplateField = BoTimeTemplate | Literal['tt_24H', 'tt_12H']
else:
    BoTimeTemplateField = BoTimeTemplate

class BoTransactionTypeEnum(StrEnum):
    botrntComplete = 'botrntComplete'
    botrntReject = 'botrntReject'

if TYPE_CHECKING:
    BoTransactionTypeEnumField = BoTransactionTypeEnum | Literal['botrntComplete', 'botrntReject']
else:
    BoTransactionTypeEnumField = BoTransactionTypeEnum

class BoUDOObjType(StrEnum):
    boud_Document = 'boud_Document'
    boud_MasterData = 'boud_MasterData'

if TYPE_CHECKING:
    BoUDOObjTypeField = BoUDOObjType | Literal['boud_Document', 'boud_MasterData']
else:
    BoUDOObjTypeField = BoUDOObjType

class BoUPTOptions(StrEnum):
    bou_FullNone = 'bou_FullNone'
    bou_FullReadNone = 'bou_FullReadNone'

if TYPE_CHECKING:
    BoUPTOptionsField = BoUPTOptions | Literal['bou_FullNone', 'bou_FullReadNone']
else:
    BoUPTOptionsField = BoUPTOptions

class BoUTBTableType(StrEnum):
    bott_Document = 'bott_Document'
    bott_DocumentLines = 'bott_DocumentLines'
    bott_MasterData = 'bott_MasterData'
    bott_MasterDataLines = 'bott_MasterDataLines'
    bott_NoObject = 'bott_NoObject'
    bott_NoObjectAutoIncrement = 'bott_NoObjectAutoIncrement'

if TYPE_CHECKING:
    BoUTBTableTypeField = BoUTBTableType | Literal['bott_Document', 'bott_DocumentLines', 'bott_MasterData', 'bott_MasterDataLines', 'bott_NoObject', 'bott_NoObjectAutoIncrement']
else:
    BoUTBTableTypeField = BoUTBTableType

class BoUniqueSerialNumber(StrEnum):
    usn_None = 'usn_None'
    usn_MfrSerialNumber = 'usn_MfrSerialNumber'
    usn_SerialNumber = 'usn_SerialNumber'
    usn_LotNumber = 'usn_LotNumber'

if TYPE_CHECKING:
    BoUniqueSerialNumberField = BoUniqueSerialNumber | Literal['usn_None', 'usn_MfrSerialNumber', 'usn_SerialNumber', 'usn_LotNumber']
else:
    BoUniqueSerialNumberField = BoUniqueSerialNumber

class BoUpdateAllocationEnum(StrEnum):
    bouaManual = 'bouaManual'
    bouaCalculated = 'bouaCalculated'
    bouaRunCalculation = 'bouaRunCalculation'

if TYPE_CHECKING:
    BoUpdateAllocationEnumField = BoUpdateAllocationEnum | Literal['bouaManual', 'bouaCalculated', 'bouaRunCalculation']
else:
    BoUpdateAllocationEnumField = BoUpdateAllocationEnum

class BoUserGroup(StrEnum):
    ug_Regular = 'ug_Regular'
    ug_Deleted = 'ug_Deleted'

if TYPE_CHECKING:
    BoUserGroupField = BoUserGroup | Literal['ug_Regular', 'ug_Deleted']
else:
    BoUserGroupField = BoUserGroup

class BoVatCategoryEnum(StrEnum):
    bovcInputTax = 'bovcInputTax'
    bovcOutputTax = 'bovcOutputTax'

if TYPE_CHECKING:
    BoVatCategoryEnumField = BoVatCategoryEnum | Literal['bovcInputTax', 'bovcOutputTax']
else:
    BoVatCategoryEnumField = BoVatCategoryEnum

class BoVatStatus(StrEnum):
    vExempted = 'vExempted'
    vLiable = 'vLiable'
    vEC = 'vEC'

if TYPE_CHECKING:
    BoVatStatusField = BoVatStatus | Literal['vExempted', 'vLiable', 'vEC']
else:
    BoVatStatusField = BoVatStatus

class BoVerticalAlignmentEnum(StrEnum):
    rlvaTop = 'rlvaTop'
    rlvaBottom = 'rlvaBottom'
    rlvaCentralized = 'rlvaCentralized'

if TYPE_CHECKING:
    BoVerticalAlignmentEnumField = BoVerticalAlignmentEnum | Literal['rlvaTop', 'rlvaBottom', 'rlvaCentralized']
else:
    BoVerticalAlignmentEnumField = BoVerticalAlignmentEnum

class BoWeekEnum(StrEnum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

if TYPE_CHECKING:
    BoWeekEnumField = BoWeekEnum | Literal['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
else:
    BoWeekEnumField = BoWeekEnum

class BoWeekNoRuleEnum(StrEnum):
    fromJanFirst = 'fromJanFirst'
    fromFirstFourDayWeek = 'fromFirstFourDayWeek'
    fromFirstFullWeek = 'fromFirstFullWeek'

if TYPE_CHECKING:
    BoWeekNoRuleEnumField = BoWeekNoRuleEnum | Literal['fromJanFirst', 'fromFirstFourDayWeek', 'fromFirstFullWeek']
else:
    BoWeekNoRuleEnumField = BoWeekNoRuleEnum

class BoWorkOrderStat(StrEnum):
    wk_ProductComplete = 'wk_ProductComplete'
    wk_WorkInstruction = 'wk_WorkInstruction'
    wk_WorkOrder = 'wk_WorkOrder'

if TYPE_CHECKING:
    BoWorkOrderStatField = BoWorkOrderStat | Literal['wk_ProductComplete', 'wk_WorkInstruction', 'wk_WorkOrder']
else:
    BoWorkOrderStatField = BoWorkOrderStat

class BoYesNoEnum(StrEnum):
    tNO = 'tNO'
    tYES = 'tYES'

if TYPE_CHECKING:
    BoYesNoEnumField = BoYesNoEnum | Literal['tNO', 'tYES']
else:
    BoYesNoEnumField = BoYesNoEnum

class BoYesNoNoneEnum(StrEnum):
    boNO = 'boNO'
    boYES = 'boYES'
    boNONE = 'boNONE'

if TYPE_CHECKING:
    BoYesNoNoneEnumField = BoYesNoNoneEnum | Literal['boNO', 'boYES', 'boNONE']
else:
    BoYesNoNoneEnumField = BoYesNoNoneEnum

class BrazilMultiIndexerTypes(StrEnum):
    bmitInvalid = 'bmitInvalid'
    bmitIncomeNature = 'bmitIncomeNature'

if TYPE_CHECKING:
    BrazilMultiIndexerTypesField = BrazilMultiIndexerTypes | Literal['bmitInvalid', 'bmitIncomeNature']
else:
    BrazilMultiIndexerTypesField = BrazilMultiIndexerTypes

class BrazilNumericIndexerTypes(StrEnum):
    bnitInvalid = 'bnitInvalid'
    bnitBeverageCommercialBrand = 'bnitBeverageCommercialBrand'
    bnitFuelGroup = 'bnitFuelGroup'
    bnitNatureOfCompany = 'bnitNatureOfCompany'
    bnitEconomicActivityType = 'bnitEconomicActivityType'
    bnitCooperativeAssociationType = 'bnitCooperativeAssociationType'
    bnitProfitTaxation = 'bnitProfitTaxation'
    bnitCompanyQualification = 'bnitCompanyQualification'
    bnitDeclarerType = 'bnitDeclarerType'
    bnitEnvironmentType = 'bnitEnvironmentType'
    bnitTributaryType = 'bnitTributaryType'
    bnitTributaryRegimeCode = 'bnitTributaryRegimeCode'
    bnitIncomeNatureTable = 'bnitIncomeNatureTable'
    bnitIncomeNatureCode = 'bnitIncomeNatureCode'
    bnitExportationDocumentType = 'bnitExportationDocumentType'
    bnitExportationNature = 'bnitExportationNature'
    bnitLadingBillType = 'bnitLadingBillType'

if TYPE_CHECKING:
    BrazilNumericIndexerTypesField = BrazilNumericIndexerTypes | Literal['bnitInvalid', 'bnitBeverageCommercialBrand', 'bnitFuelGroup', 'bnitNatureOfCompany', 'bnitEconomicActivityType', 'bnitCooperativeAssociationType', 'bnitProfitTaxation', 'bnitCompanyQualification', 'bnitDeclarerType', 'bnitEnvironmentType', 'bnitTributaryType', 'bnitTributaryRegimeCode', 'bnitIncomeNatureTable', 'bnitIncomeNatureCode', 'bnitExportationDocumentType', 'bnitExportationNature', 'bnitLadingBillType']
else:
    BrazilNumericIndexerTypesField = BrazilNumericIndexerTypes

class BrazilStringIndexerTypes(StrEnum):
    bsitInvalid = 'bsitInvalid'
    bsitBeverageTable = 'bsitBeverageTable'
    bsitNatureOfCalculationBase = 'bsitNatureOfCalculationBase'
    bsitCreditOrigin = 'bsitCreditOrigin'
    bsitBeverageGroup = 'bsitBeverageGroup'
    bsitCreditContributionOrigin = 'bsitCreditContributionOrigin'
    bsitIPIPeriod = 'bsitIPIPeriod'
    bsitSPEDProfile = 'bsitSPEDProfile'
    bsitImportationDocumentType = 'bsitImportationDocumentType'
    bsitReferentialAccountCode = 'bsitReferentialAccountCode'

if TYPE_CHECKING:
    BrazilStringIndexerTypesField = BrazilStringIndexerTypes | Literal['bsitInvalid', 'bsitBeverageTable', 'bsitNatureOfCalculationBase', 'bsitCreditOrigin', 'bsitBeverageGroup', 'bsitCreditContributionOrigin', 'bsitIPIPeriod', 'bsitSPEDProfile', 'bsitImportationDocumentType', 'bsitReferentialAccountCode']
else:
    BrazilStringIndexerTypesField = BrazilStringIndexerTypes

class CalculateInterestMethodEnum(StrEnum):
    cimOnRemainingAmount = 'cimOnRemainingAmount'
    cimOnOriginalSum = 'cimOnOriginalSum'

if TYPE_CHECKING:
    CalculateInterestMethodEnumField = CalculateInterestMethodEnum | Literal['cimOnRemainingAmount', 'cimOnOriginalSum']
else:
    CalculateInterestMethodEnumField = CalculateInterestMethodEnum

class CalculationBaseEnum(StrEnum):
    cbYearly = 'cbYearly'
    cbMonthly = 'cbMonthly'

if TYPE_CHECKING:
    CalculationBaseEnumField = CalculationBaseEnum | Literal['cbYearly', 'cbMonthly']
else:
    CalculationBaseEnumField = CalculationBaseEnum

class CallMessageStatusEnum(StrEnum):
    cmsUnread = 'cmsUnread'
    cmsRead = 'cmsRead'

if TYPE_CHECKING:
    CallMessageStatusEnumField = CallMessageStatusEnum | Literal['cmsUnread', 'cmsRead']
else:
    CallMessageStatusEnumField = CallMessageStatusEnum

class CallMessageTypeEnum(StrEnum):
    cmtInformation = 'cmtInformation'
    cmtWarning = 'cmtWarning'
    cmtError = 'cmtError'

if TYPE_CHECKING:
    CallMessageTypeEnumField = CallMessageTypeEnum | Literal['cmtInformation', 'cmtWarning', 'cmtError']
else:
    CallMessageTypeEnumField = CallMessageTypeEnum

class CampaignAssignToEnum(StrEnum):
    catUser = 'catUser'
    catEmployee = 'catEmployee'

if TYPE_CHECKING:
    CampaignAssignToEnumField = CampaignAssignToEnum | Literal['catUser', 'catEmployee']
else:
    CampaignAssignToEnumField = CampaignAssignToEnum

class CampaignBPStatusEnum(StrEnum):
    cbpsActive = 'cbpsActive'
    cbpsInactive = 'cbpsInactive'

if TYPE_CHECKING:
    CampaignBPStatusEnumField = CampaignBPStatusEnum | Literal['cbpsActive', 'cbpsInactive']
else:
    CampaignBPStatusEnumField = CampaignBPStatusEnum

class CampaignItemTypeEnum(StrEnum):
    citItems = 'citItems'
    citLabel = 'citLabel'
    citTravel = 'citTravel'

if TYPE_CHECKING:
    CampaignItemTypeEnumField = CampaignItemTypeEnum | Literal['citItems', 'citLabel', 'citTravel']
else:
    CampaignItemTypeEnumField = CampaignItemTypeEnum

class CampaignStatusEnum(StrEnum):
    csOpen = 'csOpen'
    csFinished = 'csFinished'
    csCanceled = 'csCanceled'

if TYPE_CHECKING:
    CampaignStatusEnumField = CampaignStatusEnum | Literal['csOpen', 'csFinished', 'csCanceled']
else:
    CampaignStatusEnumField = CampaignStatusEnum

class CampaignTypeEnum(StrEnum):
    ctEmail = 'ctEmail'
    ctMail = 'ctMail'
    ctFax = 'ctFax'
    ctPhoneCall = 'ctPhoneCall'
    ctMeeting = 'ctMeeting'
    ctSMS = 'ctSMS'
    ctWeb = 'ctWeb'
    ctOthers = 'ctOthers'

if TYPE_CHECKING:
    CampaignTypeEnumField = CampaignTypeEnum | Literal['ctEmail', 'ctMail', 'ctFax', 'ctPhoneCall', 'ctMeeting', 'ctSMS', 'ctWeb', 'ctOthers']
else:
    CampaignTypeEnumField = CampaignTypeEnum

class CancelStatusEnum(StrEnum):
    csYes = 'csYes'
    csNo = 'csNo'
    csCancellation = 'csCancellation'

if TYPE_CHECKING:
    CancelStatusEnumField = CancelStatusEnum | Literal['csYes', 'csNo', 'csCancellation']
else:
    CancelStatusEnumField = CancelStatusEnum

class CardOrAccountEnum(StrEnum):
    coaCard = 'coaCard'
    coaAccount = 'coaAccount'

if TYPE_CHECKING:
    CardOrAccountEnumField = CardOrAccountEnum | Literal['coaCard', 'coaAccount']
else:
    CardOrAccountEnumField = CardOrAccountEnum

class ClosingOptionEnum(StrEnum):
    coByCurrentSystemDate = 'coByCurrentSystemDate'
    coByOriginalDocumentDate = 'coByOriginalDocumentDate'
    coBySpecifiedDate = 'coBySpecifiedDate'

if TYPE_CHECKING:
    ClosingOptionEnumField = ClosingOptionEnum | Literal['coByCurrentSystemDate', 'coByOriginalDocumentDate', 'coBySpecifiedDate']
else:
    ClosingOptionEnumField = ClosingOptionEnum

class CommissionTradeTypeEnum(StrEnum):
    ct_Empty = 'ct_Empty'
    ct_SalesAgent = 'ct_SalesAgent'
    ct_PurchaseAgent = 'ct_PurchaseAgent'
    ct_Consignor = 'ct_Consignor'

if TYPE_CHECKING:
    CommissionTradeTypeEnumField = CommissionTradeTypeEnum | Literal['ct_Empty', 'ct_SalesAgent', 'ct_PurchaseAgent', 'ct_Consignor']
else:
    CommissionTradeTypeEnumField = CommissionTradeTypeEnum

class ContractSequenceEnum(StrEnum):
    cs_Monthly = 'cs_Monthly'
    cs_Quarterly = 'cs_Quarterly'
    cs_SemiAnnually = 'cs_SemiAnnually'
    cs_Yearly = 'cs_Yearly'

if TYPE_CHECKING:
    ContractSequenceEnumField = ContractSequenceEnum | Literal['cs_Monthly', 'cs_Quarterly', 'cs_SemiAnnually', 'cs_Yearly']
else:
    ContractSequenceEnumField = ContractSequenceEnum

class CounterTypeEnum(StrEnum):
    ctUser = 'ctUser'
    ctEmployee = 'ctEmployee'

if TYPE_CHECKING:
    CounterTypeEnumField = CounterTypeEnum | Literal['ctUser', 'ctEmployee']
else:
    CounterTypeEnumField = CounterTypeEnum

class CountingDocumentStatusEnum(StrEnum):
    cdsOpen = 'cdsOpen'
    cdsClosed = 'cdsClosed'

if TYPE_CHECKING:
    CountingDocumentStatusEnumField = CountingDocumentStatusEnum | Literal['cdsOpen', 'cdsClosed']
else:
    CountingDocumentStatusEnumField = CountingDocumentStatusEnum

class CountingLineStatusEnum(StrEnum):
    clsOpen = 'clsOpen'
    clsClosed = 'clsClosed'

if TYPE_CHECKING:
    CountingLineStatusEnumField = CountingLineStatusEnum | Literal['clsOpen', 'clsClosed']
else:
    CountingLineStatusEnumField = CountingLineStatusEnum

class CountingTypeEnum(StrEnum):
    ctSingleCounter = 'ctSingleCounter'
    ctMultipleCounters = 'ctMultipleCounters'

if TYPE_CHECKING:
    CountingTypeEnumField = CountingTypeEnum | Literal['ctSingleCounter', 'ctMultipleCounters']
else:
    CountingTypeEnumField = CountingTypeEnum

class CreateMethodEnum(StrEnum):
    cmManual = 'cmManual'
    cmAutomatic = 'cmAutomatic'

if TYPE_CHECKING:
    CreateMethodEnumField = CreateMethodEnum | Literal['cmManual', 'cmAutomatic']
else:
    CreateMethodEnumField = CreateMethodEnum

class CreditOrDebitEnum(StrEnum):
    codCredit = 'codCredit'
    codDebit = 'codDebit'

if TYPE_CHECKING:
    CreditOrDebitEnumField = CreditOrDebitEnum | Literal['codCredit', 'codDebit']
else:
    CreditOrDebitEnumField = CreditOrDebitEnum

class CurrenciesDecimalsEnum(StrEnum):
    cd1Digit = 'cd1Digit'
    cd2Digits = 'cd2Digits'
    cd3Digits = 'cd3Digits'
    cd4Digits = 'cd4Digits'
    cd5Digits = 'cd5Digits'
    cd6Digits = 'cd6Digits'
    cdDefault = 'cdDefault'
    cdWithoutDecimals = 'cdWithoutDecimals'

if TYPE_CHECKING:
    CurrenciesDecimalsEnumField = CurrenciesDecimalsEnum | Literal['cd1Digit', 'cd2Digits', 'cd3Digits', 'cd4Digits', 'cd5Digits', 'cd6Digits', 'cdDefault', 'cdWithoutDecimals']
else:
    CurrenciesDecimalsEnumField = CurrenciesDecimalsEnum

class CycleCountDeterminationCycleByEnum(StrEnum):
    ccdcbItemGroup = 'ccdcbItemGroup'
    ccdcbWarehouseSublevel1 = 'ccdcbWarehouseSublevel1'
    ccdcbWarehouseSublevel2 = 'ccdcbWarehouseSublevel2'
    ccdcbWarehouseSublevel3 = 'ccdcbWarehouseSublevel3'
    ccdcbWarehouseSublevel4 = 'ccdcbWarehouseSublevel4'

if TYPE_CHECKING:
    CycleCountDeterminationCycleByEnumField = CycleCountDeterminationCycleByEnum | Literal['ccdcbItemGroup', 'ccdcbWarehouseSublevel1', 'ccdcbWarehouseSublevel2', 'ccdcbWarehouseSublevel3', 'ccdcbWarehouseSublevel4']
else:
    CycleCountDeterminationCycleByEnumField = CycleCountDeterminationCycleByEnum

class DataPrivacyProtectionEnum(StrEnum):
    dpp_None = 'dpp_None'
    dpp_Erased = 'dpp_Erased'
    dpp_Blocked = 'dpp_Blocked'
    dpp_Unblocked = 'dpp_Unblocked'

if TYPE_CHECKING:
    DataPrivacyProtectionEnumField = DataPrivacyProtectionEnum | Literal['dpp_None', 'dpp_Erased', 'dpp_Blocked', 'dpp_Unblocked']
else:
    DataPrivacyProtectionEnumField = DataPrivacyProtectionEnum

class DataSensitiveStatusEnum(StrEnum):
    dss_FieldNotSentive = 'dss_FieldNotSentive'
    dss_DataSubjectNotNaturalPerson = 'dss_DataSubjectNotNaturalPerson'
    dss_DataSubjectIsBlockedOrErased = 'dss_DataSubjectIsBlockedOrErased'
    dss_DataIsSensitive = 'dss_DataIsSensitive'
    dss_Error = 'dss_Error'
    dss_TransactionIsErased = 'dss_TransactionIsErased'

if TYPE_CHECKING:
    DataSensitiveStatusEnumField = DataSensitiveStatusEnum | Literal['dss_FieldNotSentive', 'dss_DataSubjectNotNaturalPerson', 'dss_DataSubjectIsBlockedOrErased', 'dss_DataIsSensitive', 'dss_Error', 'dss_TransactionIsErased']
else:
    DataSensitiveStatusEnumField = DataSensitiveStatusEnum

class DepreciationCalculationBaseEnum(StrEnum):
    dcbAcquisitionValue = 'dcbAcquisitionValue'
    dcbNetBookValue = 'dcbNetBookValue'

if TYPE_CHECKING:
    DepreciationCalculationBaseEnumField = DepreciationCalculationBaseEnum | Literal['dcbAcquisitionValue', 'dcbNetBookValue']
else:
    DepreciationCalculationBaseEnumField = DepreciationCalculationBaseEnum

class DepreciationMethodEnum(StrEnum):
    dmNoDepreciation = 'dmNoDepreciation'
    dmStraightLine = 'dmStraightLine'
    dmStraightLinePeriodControl = 'dmStraightLinePeriodControl'
    dmDecliningBalance = 'dmDecliningBalance'
    dmMultilevel = 'dmMultilevel'
    dmImmediateWriteOff = 'dmImmediateWriteOff'
    dmSpecialDepreciation = 'dmSpecialDepreciation'
    dmManualDepreciation = 'dmManualDepreciation'
    dmAccelerated = 'dmAccelerated'

if TYPE_CHECKING:
    DepreciationMethodEnumField = DepreciationMethodEnum | Literal['dmNoDepreciation', 'dmStraightLine', 'dmStraightLinePeriodControl', 'dmDecliningBalance', 'dmMultilevel', 'dmImmediateWriteOff', 'dmSpecialDepreciation', 'dmManualDepreciation', 'dmAccelerated']
else:
    DepreciationMethodEnumField = DepreciationMethodEnum

class DepreciationRoundingMethodEnum(StrEnum):
    drmTruncate = 'drmTruncate'
    drmRoundUp = 'drmRoundUp'
    drmRoundDown = 'drmRoundDown'

if TYPE_CHECKING:
    DepreciationRoundingMethodEnumField = DepreciationRoundingMethodEnum | Literal['drmTruncate', 'drmRoundUp', 'drmRoundDown']
else:
    DepreciationRoundingMethodEnumField = DepreciationRoundingMethodEnum

class DirectDebitTypeEnum(StrEnum):
    ddtCORE = 'ddtCORE'
    ddtB2B = 'ddtB2B'
    ddtCOR1 = 'ddtCOR1'

if TYPE_CHECKING:
    DirectDebitTypeEnumField = DirectDebitTypeEnum | Literal['ddtCORE', 'ddtB2B', 'ddtCOR1']
else:
    DirectDebitTypeEnumField = DirectDebitTypeEnum

class DiscountGroupBaseObjectEnum(StrEnum):
    dgboNone = 'dgboNone'
    dgboItemGroups = 'dgboItemGroups'
    dgboItemProperties = 'dgboItemProperties'
    dgboManufacturer = 'dgboManufacturer'
    dgboItems = 'dgboItems'

if TYPE_CHECKING:
    DiscountGroupBaseObjectEnumField = DiscountGroupBaseObjectEnum | Literal['dgboNone', 'dgboItemGroups', 'dgboItemProperties', 'dgboManufacturer', 'dgboItems']
else:
    DiscountGroupBaseObjectEnumField = DiscountGroupBaseObjectEnum

class DiscountGroupDiscountTypeEnum(StrEnum):
    dgdt_Fixed = 'dgdt_Fixed'
    dgdt_Variable = 'dgdt_Variable'

if TYPE_CHECKING:
    DiscountGroupDiscountTypeEnumField = DiscountGroupDiscountTypeEnum | Literal['dgdt_Fixed', 'dgdt_Variable']
else:
    DiscountGroupDiscountTypeEnumField = DiscountGroupDiscountTypeEnum

class DiscountGroupRelationsEnum(StrEnum):
    dgrLowestDiscount = 'dgrLowestDiscount'
    dgrHighestDiscount = 'dgrHighestDiscount'
    dgrAverageDiscount = 'dgrAverageDiscount'
    dgrDiscountTotals = 'dgrDiscountTotals'
    dgrMultipliedDiscount = 'dgrMultipliedDiscount'

if TYPE_CHECKING:
    DiscountGroupRelationsEnumField = DiscountGroupRelationsEnum | Literal['dgrLowestDiscount', 'dgrHighestDiscount', 'dgrAverageDiscount', 'dgrDiscountTotals', 'dgrMultipliedDiscount']
else:
    DiscountGroupRelationsEnumField = DiscountGroupRelationsEnum

class DiscountGroupTypeEnum(StrEnum):
    dgt_AllBPs = 'dgt_AllBPs'
    dgt_CustomerGroup = 'dgt_CustomerGroup'
    dgt_VendorGroup = 'dgt_VendorGroup'
    dgt_SpecificBP = 'dgt_SpecificBP'

if TYPE_CHECKING:
    DiscountGroupTypeEnumField = DiscountGroupTypeEnum | Literal['dgt_AllBPs', 'dgt_CustomerGroup', 'dgt_VendorGroup', 'dgt_SpecificBP']
else:
    DiscountGroupTypeEnumField = DiscountGroupTypeEnum

class DisplayBatchQtyUoMByEnum(StrEnum):
    dispBatchQtyByDocRowUoM = 'dispBatchQtyByDocRowUoM'
    dispBatchQtyByInventoryUoM = 'dispBatchQtyByInventoryUoM'

if TYPE_CHECKING:
    DisplayBatchQtyUoMByEnumField = DisplayBatchQtyUoMByEnum | Literal['dispBatchQtyByDocRowUoM', 'dispBatchQtyByInventoryUoM']
else:
    DisplayBatchQtyUoMByEnumField = DisplayBatchQtyUoMByEnum

class DocumentAuthorizationStatusEnum(StrEnum):
    dasWithout = 'dasWithout'
    dasPending = 'dasPending'
    dasApproved = 'dasApproved'
    dasRejected = 'dasRejected'
    dasGenerated = 'dasGenerated'
    dasGeneratedbyAuthorizer = 'dasGeneratedbyAuthorizer'
    dasCancelled = 'dasCancelled'

if TYPE_CHECKING:
    DocumentAuthorizationStatusEnumField = DocumentAuthorizationStatusEnum | Literal['dasWithout', 'dasPending', 'dasApproved', 'dasRejected', 'dasGenerated', 'dasGeneratedbyAuthorizer', 'dasCancelled']
else:
    DocumentAuthorizationStatusEnumField = DocumentAuthorizationStatusEnum

class DocumentDeliveryTypeEnum(StrEnum):
    ddtNoneSeleted = 'ddtNoneSeleted'
    ddtCreateOnlineDocument = 'ddtCreateOnlineDocument'
    ddtPostToAribaNetwork = 'ddtPostToAribaNetwork'

if TYPE_CHECKING:
    DocumentDeliveryTypeEnumField = DocumentDeliveryTypeEnum | Literal['ddtNoneSeleted', 'ddtCreateOnlineDocument', 'ddtPostToAribaNetwork']
else:
    DocumentDeliveryTypeEnumField = DocumentDeliveryTypeEnum

class DocumentObjectTypeEnum(StrEnum):
    dc_ArInvoice = 'dc_ArInvoice'
    dc_Delivery = 'dc_Delivery'
    dc_GoodsReturn = 'dc_GoodsReturn'
    dc_InventoryTransfer = 'dc_InventoryTransfer'

if TYPE_CHECKING:
    DocumentObjectTypeEnumField = DocumentObjectTypeEnum | Literal['dc_ArInvoice', 'dc_Delivery', 'dc_GoodsReturn', 'dc_InventoryTransfer']
else:
    DocumentObjectTypeEnumField = DocumentObjectTypeEnum

class DocumentPriceSourceEnum(StrEnum):
    dpsSpecialPricesForBusinessPartner = 'dpsSpecialPricesForBusinessPartner'
    dpsManual = 'dpsManual'
    dpsActivePriceListDiscountGroups = 'dpsActivePriceListDiscountGroups'
    dpsActivePriceList = 'dpsActivePriceList'
    dpsInactivePriceList = 'dpsInactivePriceList'
    dpsBlanketAgreement = 'dpsBlanketAgreement'
    dpsPeriodAndVolumeDiscounts = 'dpsPeriodAndVolumeDiscounts'
    dpsPeriodAndVolumeDiscountsDiscountGroups = 'dpsPeriodAndVolumeDiscountsDiscountGroups'
    dpsInactivePriceListDiscountGroups = 'dpsInactivePriceListDiscountGroups'
    dpsNewSpecialPricesForBusinessPartner = 'dpsNewSpecialPricesForBusinessPartner'
    dpsNewActivePriceListDiscountGroups = 'dpsNewActivePriceListDiscountGroups'
    dpsNewActivePriceList = 'dpsNewActivePriceList'
    dpsNewInactivePriceList = 'dpsNewInactivePriceList'
    dpsNewBlanketAgreement = 'dpsNewBlanketAgreement'
    dpsNewPeriodAndVolumeDiscounts = 'dpsNewPeriodAndVolumeDiscounts'
    dpsNewPeriodAndVolumeDiscountsDiscountGroups = 'dpsNewPeriodAndVolumeDiscountsDiscountGroups'
    dpsNewInactivePriceListDiscountGroups = 'dpsNewInactivePriceListDiscountGroups'

if TYPE_CHECKING:
    DocumentPriceSourceEnumField = DocumentPriceSourceEnum | Literal['dpsSpecialPricesForBusinessPartner', 'dpsManual', 'dpsActivePriceListDiscountGroups', 'dpsActivePriceList', 'dpsInactivePriceList', 'dpsBlanketAgreement', 'dpsPeriodAndVolumeDiscounts', 'dpsPeriodAndVolumeDiscountsDiscountGroups', 'dpsInactivePriceListDiscountGroups', 'dpsNewSpecialPricesForBusinessPartner', 'dpsNewActivePriceListDiscountGroups', 'dpsNewActivePriceList', 'dpsNewInactivePriceList', 'dpsNewBlanketAgreement', 'dpsNewPeriodAndVolumeDiscounts', 'dpsNewPeriodAndVolumeDiscountsDiscountGroups', 'dpsNewInactivePriceListDiscountGroups']
else:
    DocumentPriceSourceEnumField = DocumentPriceSourceEnum

class DocumentRemarksIncludeTypeEnum(StrEnum):
    driBaseDocumentNumber = 'driBaseDocumentNumber'
    driBPReferenceNumber = 'driBPReferenceNumber'
    driManualRemarksOnly = 'driManualRemarksOnly'

if TYPE_CHECKING:
    DocumentRemarksIncludeTypeEnumField = DocumentRemarksIncludeTypeEnum | Literal['driBaseDocumentNumber', 'driBPReferenceNumber', 'driManualRemarksOnly']
else:
    DocumentRemarksIncludeTypeEnumField = DocumentRemarksIncludeTypeEnum

class DomesticBankAccountValidationEnum(StrEnum):
    dbavNone = 'dbavNone'
    dbavBelgium = 'dbavBelgium'
    dbavSpain = 'dbavSpain'
    dbavFrance = 'dbavFrance'
    dbavItaly = 'dbavItaly'
    dbavNetherlands = 'dbavNetherlands'
    dbavPortugal = 'dbavPortugal'

if TYPE_CHECKING:
    DomesticBankAccountValidationEnumField = DomesticBankAccountValidationEnum | Literal['dbavNone', 'dbavBelgium', 'dbavSpain', 'dbavFrance', 'dbavItaly', 'dbavNetherlands', 'dbavPortugal']
else:
    DomesticBankAccountValidationEnumField = DomesticBankAccountValidationEnum

class DownPaymentTypeEnum(StrEnum):
    dptRequest = 'dptRequest'
    dptInvoice = 'dptInvoice'

if TYPE_CHECKING:
    DownPaymentTypeEnumField = DownPaymentTypeEnum | Literal['dptRequest', 'dptInvoice']
else:
    DownPaymentTypeEnumField = DownPaymentTypeEnum

class DrawingMethodEnum(StrEnum):
    dmAll = 'dmAll'
    dmNone = 'dmNone'
    dmQuantity = 'dmQuantity'
    dmTotal = 'dmTotal'

if TYPE_CHECKING:
    DrawingMethodEnumField = DrawingMethodEnum | Literal['dmAll', 'dmNone', 'dmQuantity', 'dmTotal']
else:
    DrawingMethodEnumField = DrawingMethodEnum

class DueDateTypesEnum(StrEnum):
    ddtAfterTimePeriod = 'ddtAfterTimePeriod'
    ddtByDates = 'ddtByDates'

if TYPE_CHECKING:
    DueDateTypesEnumField = DueDateTypesEnum | Literal['ddtAfterTimePeriod', 'ddtByDates']
else:
    DueDateTypesEnumField = DueDateTypesEnum

class DunningLetterTypeEnum(StrEnum):
    dltDunningLetter1 = 'dltDunningLetter1'
    dltDunningLetter2 = 'dltDunningLetter2'
    dltDunningLetter3 = 'dltDunningLetter3'
    dltDunningLetter4 = 'dltDunningLetter4'
    dltDunningLetter5 = 'dltDunningLetter5'
    dltDunningLetter6 = 'dltDunningLetter6'
    dltDunningLetter7 = 'dltDunningLetter7'
    dltDunningLetter8 = 'dltDunningLetter8'
    dltDunningLetter9 = 'dltDunningLetter9'
    dltDunningLetter10 = 'dltDunningLetter10'
    dltDunningALL = 'dltDunningALL'

if TYPE_CHECKING:
    DunningLetterTypeEnumField = DunningLetterTypeEnum | Literal['dltDunningLetter1', 'dltDunningLetter2', 'dltDunningLetter3', 'dltDunningLetter4', 'dltDunningLetter5', 'dltDunningLetter6', 'dltDunningLetter7', 'dltDunningLetter8', 'dltDunningLetter9', 'dltDunningLetter10', 'dltDunningALL']
else:
    DunningLetterTypeEnumField = DunningLetterTypeEnum

class ECDPostingTypeEnum(StrEnum):
    ecdNormal = 'ecdNormal'
    ecdStatement = 'ecdStatement'

if TYPE_CHECKING:
    ECDPostingTypeEnumField = ECDPostingTypeEnum | Literal['ecdNormal', 'ecdStatement']
else:
    ECDPostingTypeEnumField = ECDPostingTypeEnum

class EDocGenerationTypeEnum(StrEnum):
    edocGenerate = 'edocGenerate'
    edocGenerateLater = 'edocGenerateLater'
    edocNotRelevant = 'edocNotRelevant'

if TYPE_CHECKING:
    EDocGenerationTypeEnumField = EDocGenerationTypeEnum | Literal['edocGenerate', 'edocGenerateLater', 'edocNotRelevant']
else:
    EDocGenerationTypeEnumField = EDocGenerationTypeEnum

class EDocStatusEnum(StrEnum):
    edoc_New = 'edoc_New'
    edoc_Pending = 'edoc_Pending'
    edoc_Sent = 'edoc_Sent'
    edoc_Error = 'edoc_Error'
    edoc_Ok = 'edoc_Ok'

if TYPE_CHECKING:
    EDocStatusEnumField = EDocStatusEnum | Literal['edoc_New', 'edoc_Pending', 'edoc_Sent', 'edoc_Error', 'edoc_Ok']
else:
    EDocStatusEnumField = EDocStatusEnum

class EDocTypeEnum(StrEnum):
    edocFE = 'edocFE'
    edocFCE = 'edocFCE'

if TYPE_CHECKING:
    EDocTypeEnumField = EDocTypeEnum | Literal['edocFE', 'edocFCE']
else:
    EDocTypeEnumField = EDocTypeEnum

class EWBSupplyTypeEnum(StrEnum):
    ewb_st_Inward = 'ewb_st_Inward'
    ewb_st_Outward = 'ewb_st_Outward'

if TYPE_CHECKING:
    EWBSupplyTypeEnumField = EWBSupplyTypeEnum | Literal['ewb_st_Inward', 'ewb_st_Outward']
else:
    EWBSupplyTypeEnumField = EWBSupplyTypeEnum

class EWBTransactionTypeEnum(StrEnum):
    ewb_tt_Regular = 'ewb_tt_Regular'
    ewb_tt_BillToShipTo = 'ewb_tt_BillToShipTo'
    ewb_tt_BillFromDispathFrom = 'ewb_tt_BillFromDispathFrom'
    ewb_tt_CombinationOfBillAndShip = 'ewb_tt_CombinationOfBillAndShip'

if TYPE_CHECKING:
    EWBTransactionTypeEnumField = EWBTransactionTypeEnum | Literal['ewb_tt_Regular', 'ewb_tt_BillToShipTo', 'ewb_tt_BillFromDispathFrom', 'ewb_tt_CombinationOfBillAndShip']
else:
    EWBTransactionTypeEnumField = EWBTransactionTypeEnum

class EffectivePriceEnum(StrEnum):
    epDefaultPriority = 'epDefaultPriority'
    epLowestPrice = 'epLowestPrice'
    epHighestPrice = 'epHighestPrice'

if TYPE_CHECKING:
    EffectivePriceEnumField = EffectivePriceEnum | Literal['epDefaultPriority', 'epLowestPrice', 'epHighestPrice']
else:
    EffectivePriceEnumField = EffectivePriceEnum

class ElecCommStatusEnum(StrEnum):
    ecsApproved = 'ecsApproved'
    ecsPendingApproval = 'ecsPendingApproval'
    ecsRejected = 'ecsRejected'

if TYPE_CHECKING:
    ElecCommStatusEnumField = ElecCommStatusEnum | Literal['ecsApproved', 'ecsPendingApproval', 'ecsRejected']
else:
    ElecCommStatusEnumField = ElecCommStatusEnum

class ElectronicDocGenTypeEnum(StrEnum):
    edgt_NotRelevant = 'edgt_NotRelevant'
    edgt_Generate = 'edgt_Generate'
    edgt_GenerateLater = 'edgt_GenerateLater'

if TYPE_CHECKING:
    ElectronicDocGenTypeEnumField = ElectronicDocGenTypeEnum | Literal['edgt_NotRelevant', 'edgt_Generate', 'edgt_GenerateLater']
else:
    ElectronicDocGenTypeEnumField = ElectronicDocGenTypeEnum

class ElectronicDocProcessingTargetEnum(StrEnum):
    edpt_Invalid = 'edpt_Invalid'
    edpt_All = 'edpt_All'
    edpt_None = 'edpt_None'
    edpt_LegacyB1iSender = 'edpt_LegacyB1iSender'
    edpt_B1iEventSender = 'edpt_B1iEventSender'
    edpt_LegacyXMLFile = 'edpt_LegacyXMLFile'
    edpt_ConnectorXML = 'edpt_ConnectorXML'
    edpt_ConnectorB1iWS = 'edpt_ConnectorB1iWS'
    edpt_ConnectorPEPPOL = 'edpt_ConnectorPEPPOL'
    edpt_ConnectorEET = 'edpt_ConnectorEET'
    edpt_ConnectorEETv2 = 'edpt_ConnectorEETv2'
    edpt_ConnectorCFDi = 'edpt_ConnectorCFDi'
    edpt_ConnectorEBooks = 'edpt_ConnectorEBooks'
    edpt_ConnectorDOX = 'edpt_ConnectorDOX'
    edpt_ConnectorDigipoort = 'edpt_ConnectorDigipoort'
    edpt_ImportWizardManualFile = 'edpt_ImportWizardManualFile'
    edpt_ImportWizardAutomaticFile = 'edpt_ImportWizardAutomaticFile'
    edpt_ImportWizardWebService = 'edpt_ImportWizardWebService'
    edpt_ConnectorFPA = 'edpt_ConnectorFPA'
    edpt_ConnectorDocSign = 'edpt_ConnectorDocSign'
    edpt_ConnectorAFE = 'edpt_ConnectorAFE'
    edpt_ConnectorGSTReturn = 'edpt_ConnectorGSTReturn'
    edpt_ConnectorKSeF = 'edpt_ConnectorKSeF'
    edpt_ConnectorPTDocSign = 'edpt_ConnectorPTDocSign'
    edpt_ConnectorSkatDK = 'edpt_ConnectorSkatDK'
    edpt_ConnectorEII = 'edpt_ConnectorEII'
    edpt_ConnectorPTeInvoicing = 'edpt_ConnectorPTeInvoicing'
    edpt_ConnectorEBilling = 'edpt_ConnectorEBilling'
    edpt_ConnectorEDSHOI = 'edpt_ConnectorEDSHOI'
    edpt_ConnectorPTeCom = 'edpt_ConnectorPTeCom'
    edpt_ConnectorVeriFactu = 'edpt_ConnectorVeriFactu'
    edpt_ManualImport = 'edpt_ManualImport'

if TYPE_CHECKING:
    ElectronicDocProcessingTargetEnumField = ElectronicDocProcessingTargetEnum | Literal['edpt_Invalid', 'edpt_All', 'edpt_None', 'edpt_LegacyB1iSender', 'edpt_B1iEventSender', 'edpt_LegacyXMLFile', 'edpt_ConnectorXML', 'edpt_ConnectorB1iWS', 'edpt_ConnectorPEPPOL', 'edpt_ConnectorEET', 'edpt_ConnectorEETv2', 'edpt_ConnectorCFDi', 'edpt_ConnectorEBooks', 'edpt_ConnectorDOX', 'edpt_ConnectorDigipoort', 'edpt_ImportWizardManualFile', 'edpt_ImportWizardAutomaticFile', 'edpt_ImportWizardWebService', 'edpt_ConnectorFPA', 'edpt_ConnectorDocSign', 'edpt_ConnectorAFE', 'edpt_ConnectorGSTReturn', 'edpt_ConnectorKSeF', 'edpt_ConnectorPTDocSign', 'edpt_ConnectorSkatDK', 'edpt_ConnectorEII', 'edpt_ConnectorPTeInvoicing', 'edpt_ConnectorEBilling', 'edpt_ConnectorEDSHOI', 'edpt_ConnectorPTeCom', 'edpt_ConnectorVeriFactu', 'edpt_ManualImport']
else:
    ElectronicDocProcessingTargetEnumField = ElectronicDocProcessingTargetEnum

class ElectronicDocProtocolCodeEnum(StrEnum):
    edpc_Invalid = 'edpc_Invalid'
    edpc_GEN = 'edpc_GEN'
    edpc_EET = 'edpc_EET'
    edpc_CFDI = 'edpc_CFDI'
    edpc_FPA = 'edpc_FPA'
    edpc_MTD = 'edpc_MTD'
    edpc_EWB = 'edpc_EWB'
    edpc_PEPPOL = 'edpc_PEPPOL'
    edpc_HOI = 'edpc_HOI'
    edpc_MYF = 'edpc_MYF'
    edpc_EIS = 'edpc_EIS'
    edpc_IIS = 'edpc_IIS'
    edpc_IIS_Annual = 'edpc_IIS_Annual'
    edpc_DIGIPOORT = 'edpc_DIGIPOORT'
    edpc_EBooks = 'edpc_EBooks'
    edpc_DOX = 'edpc_DOX'
    edpc_RTIE = 'edpc_RTIE'
    edpc_EBilling = 'edpc_EBilling'
    edpc_TaxService = 'edpc_TaxService'
    edpc_AFE = 'edpc_AFE'
    edpc_DocSign = 'edpc_DocSign'
    edpc_KSeF = 'edpc_KSeF'
    edpc_GSTReturn = 'edpc_GSTReturn'
    edpc_PTDocSign = 'edpc_PTDocSign'
    edpc_SkatDK = 'edpc_SkatDK'
    edpc_EII = 'edpc_EII'
    edpc_NFe = 'edpc_NFe'
    edpc_PTeInvoicing = 'edpc_PTeInvoicing'
    edpc_PTeCom = 'edpc_PTeCom'
    edpc_VeriFactu = 'edpc_VeriFactu'
    edpc_BAS = 'edpc_BAS'

if TYPE_CHECKING:
    ElectronicDocProtocolCodeEnumField = ElectronicDocProtocolCodeEnum | Literal['edpc_Invalid', 'edpc_GEN', 'edpc_EET', 'edpc_CFDI', 'edpc_FPA', 'edpc_MTD', 'edpc_EWB', 'edpc_PEPPOL', 'edpc_HOI', 'edpc_MYF', 'edpc_EIS', 'edpc_IIS', 'edpc_IIS_Annual', 'edpc_DIGIPOORT', 'edpc_EBooks', 'edpc_DOX', 'edpc_RTIE', 'edpc_EBilling', 'edpc_TaxService', 'edpc_AFE', 'edpc_DocSign', 'edpc_KSeF', 'edpc_GSTReturn', 'edpc_PTDocSign', 'edpc_SkatDK', 'edpc_EII', 'edpc_NFe', 'edpc_PTeInvoicing', 'edpc_PTeCom', 'edpc_VeriFactu', 'edpc_BAS']
else:
    ElectronicDocProtocolCodeEnumField = ElectronicDocProtocolCodeEnum

class ElectronicDocProtocolCodeStrEnum(StrEnum):
    edpcs_Invalid = 'edpcs_Invalid'
    edpcs_GEN = 'edpcs_GEN'
    edpcs_EET = 'edpcs_EET'
    edpcs_CFDI = 'edpcs_CFDI'
    edpcs_FPA = 'edpcs_FPA'
    edpcs_MTD = 'edpcs_MTD'
    edpcs_EWB = 'edpcs_EWB'
    edpcs_PEPPOL = 'edpcs_PEPPOL'
    edpcs_HOI = 'edpcs_HOI'
    edpcs_MYF = 'edpcs_MYF'
    edpcs_EIS = 'edpcs_EIS'
    edpcs_IIS = 'edpcs_IIS'
    edpcs_IIS_Annual = 'edpcs_IIS_Annual'
    edpcs_DIGIPOORT = 'edpcs_DIGIPOORT'
    edpcs_EBooks = 'edpcs_EBooks'
    edpcs_DOX = 'edpcs_DOX'
    edpcs_RTIE = 'edpcs_RTIE'
    edpcs_EBilling = 'edpcs_EBilling'
    edpcs_TaxService = 'edpcs_TaxService'
    edpcs_AFE = 'edpcs_AFE'
    edpcs_DocSign = 'edpcs_DocSign'
    edpcs_KSeF = 'edpcs_KSeF'
    edpcs_GSTReturn = 'edpcs_GSTReturn'
    edpcs_PTDocSign = 'edpcs_PTDocSign'
    edpcs_SkatDK = 'edpcs_SkatDK'
    edpcs_EII = 'edpcs_EII'
    edpcs_NFe = 'edpcs_NFe'
    edpcs_PTeInvoicing = 'edpcs_PTeInvoicing'
    edpcs_PTeCom = 'edpcs_PTeCom'
    edpcs_VeriFactu = 'edpcs_VeriFactu'
    edpcs_BAS = 'edpcs_BAS'

if TYPE_CHECKING:
    ElectronicDocProtocolCodeStrEnumField = ElectronicDocProtocolCodeStrEnum | Literal['edpcs_Invalid', 'edpcs_GEN', 'edpcs_EET', 'edpcs_CFDI', 'edpcs_FPA', 'edpcs_MTD', 'edpcs_EWB', 'edpcs_PEPPOL', 'edpcs_HOI', 'edpcs_MYF', 'edpcs_EIS', 'edpcs_IIS', 'edpcs_IIS_Annual', 'edpcs_DIGIPOORT', 'edpcs_EBooks', 'edpcs_DOX', 'edpcs_RTIE', 'edpcs_EBilling', 'edpcs_TaxService', 'edpcs_AFE', 'edpcs_DocSign', 'edpcs_KSeF', 'edpcs_GSTReturn', 'edpcs_PTDocSign', 'edpcs_SkatDK', 'edpcs_EII', 'edpcs_NFe', 'edpcs_PTeInvoicing', 'edpcs_PTeCom', 'edpcs_VeriFactu', 'edpcs_BAS']
else:
    ElectronicDocProtocolCodeStrEnumField = ElectronicDocProtocolCodeStrEnum

class ElectronicDocumentAuthorityProcessEnum(StrEnum):
    edapNone = 'edapNone'
    edapApproval = 'edapApproval'
    edapRejection = 'edapRejection'

if TYPE_CHECKING:
    ElectronicDocumentAuthorityProcessEnumField = ElectronicDocumentAuthorityProcessEnum | Literal['edapNone', 'edapApproval', 'edapRejection']
else:
    ElectronicDocumentAuthorityProcessEnumField = ElectronicDocumentAuthorityProcessEnum

class ElectronicDocumentBlobContentTypeEnum(StrEnum):
    edbctDefault = 'edbctDefault'
    edbctXML = 'edbctXML'
    edbctZippedXML = 'edbctZippedXML'
    edbctJSON = 'edbctJSON'
    edbctZippedJSON = 'edbctZippedJSON'
    edbctText = 'edbctText'
    edbctZippedP7M = 'edbctZippedP7M'
    edbctP7M = 'edbctP7M'
    edbctZippedPDF = 'edbctZippedPDF'

if TYPE_CHECKING:
    ElectronicDocumentBlobContentTypeEnumField = ElectronicDocumentBlobContentTypeEnum | Literal['edbctDefault', 'edbctXML', 'edbctZippedXML', 'edbctJSON', 'edbctZippedJSON', 'edbctText', 'edbctZippedP7M', 'edbctP7M', 'edbctZippedPDF']
else:
    ElectronicDocumentBlobContentTypeEnumField = ElectronicDocumentBlobContentTypeEnum

class ElectronicDocumentEntryCancellationStatusEnum(StrEnum):
    edecsInvalid = 'edecsInvalid'
    edecsNotSet = 'edecsNotSet'
    edecsNewRequest = 'edecsNewRequest'
    edecsRequestSent = 'edecsRequestSent'
    edecsApproved = 'edecsApproved'
    edecsRejected = 'edecsRejected'
    edecsError = 'edecsError'
    edecsCancelled = 'edecsCancelled'
    edecsInProcess = 'edecsInProcess'
    edecsSentToAuthority = 'edecsSentToAuthority'
    edescCancelledWOApproval = 'edescCancelledWOApproval'

if TYPE_CHECKING:
    ElectronicDocumentEntryCancellationStatusEnumField = ElectronicDocumentEntryCancellationStatusEnum | Literal['edecsInvalid', 'edecsNotSet', 'edecsNewRequest', 'edecsRequestSent', 'edecsApproved', 'edecsRejected', 'edecsError', 'edecsCancelled', 'edecsInProcess', 'edecsSentToAuthority', 'edescCancelledWOApproval']
else:
    ElectronicDocumentEntryCancellationStatusEnumField = ElectronicDocumentEntryCancellationStatusEnum

class ElectronicDocumentEntryLogTypeEnum(StrEnum):
    edeltNone = 'edeltNone'
    edeltSend = 'edeltSend'
    edeltReceive = 'edeltReceive'
    edeltImport = 'edeltImport'
    edeltNote = 'edeltNote'
    edeltWarning = 'edeltWarning'
    edeltError = 'edeltError'
    edeltWSData = 'edeltWSData'
    edeltAuthorityProcessBegins = 'edeltAuthorityProcessBegins'
    edeltAuthorityProcessFinished = 'edeltAuthorityProcessFinished'

if TYPE_CHECKING:
    ElectronicDocumentEntryLogTypeEnumField = ElectronicDocumentEntryLogTypeEnum | Literal['edeltNone', 'edeltSend', 'edeltReceive', 'edeltImport', 'edeltNote', 'edeltWarning', 'edeltError', 'edeltWSData', 'edeltAuthorityProcessBegins', 'edeltAuthorityProcessFinished']
else:
    ElectronicDocumentEntryLogTypeEnumField = ElectronicDocumentEntryLogTypeEnum

class ElectronicDocumentEntryPeriodTypeEnum(StrEnum):
    edeptIgnore = 'edeptIgnore'
    edeptYear = 'edeptYear'
    edeptQuarter = 'edeptQuarter'
    edeptMonth = 'edeptMonth'
    edeptDateRange = 'edeptDateRange'

if TYPE_CHECKING:
    ElectronicDocumentEntryPeriodTypeEnumField = ElectronicDocumentEntryPeriodTypeEnum | Literal['edeptIgnore', 'edeptYear', 'edeptQuarter', 'edeptMonth', 'edeptDateRange']
else:
    ElectronicDocumentEntryPeriodTypeEnumField = ElectronicDocumentEntryPeriodTypeEnum

class ElectronicDocumentEntryStatusEnum(StrEnum):
    edesNone = 'edesNone'
    edesNew = 'edesNew'
    edesReadyToProcess = 'edesReadyToProcess'
    edesPending = 'edesPending'
    edesError = 'edesError'
    edesOK = 'edesOK'
    edesSent = 'edesSent'
    edesDocError = 'edesDocError'
    edesTempError = 'edesTempError'
    edesWarning = 'edesWarning'
    edesWaiting = 'edesWaiting'
    edesAuthorized = 'edesAuthorized'
    edesInProcess = 'edesInProcess'
    edesRejected = 'edesRejected'
    edesDenied = 'edesDenied'
    edesCanceled = 'edesCanceled'
    edesAborted = 'edesAborted'
    edesUnused = 'edesUnused'
    edesQueued = 'edesQueued'
    edesImported = 'edesImported'
    edesApproved = 'edesApproved'
    edesApproving = 'edesApproving'
    edesRejecting = 'edesRejecting'
    edesGenerated = 'edesGenerated'
    edesDetermined = 'edesDetermined'
    edesImporting = 'edesImporting'
    edesInProcessToIntermediary = 'edesInProcessToIntermediary'
    edesSentToIntermediary = 'edesSentToIntermediary'
    edesApprovedByIntermediary = 'edesApprovedByIntermediary'
    edesNotIntegratedCustomer = 'edesNotIntegratedCustomer'
    edesNotSentToCustomer = 'edesNotSentToCustomer'
    edesErrorSendingToCustomer = 'edesErrorSendingToCustomer'
    edesSentToCustomer = 'edesSentToCustomer'
    edesReceivedByCustomer = 'edesReceivedByCustomer'
    edesRejectedByCustomer = 'edesRejectedByCustomer'
    edesPaidByCustomer = 'edesPaidByCustomer'
    edesCheckingIntegrationStatus = 'edesCheckingIntegrationStatus'
    edesNotApproved = 'edesNotApproved'
    edesChargeReversal = 'edesChargeReversal'
    edesCanceling = 'edesCanceling'
    edesContinuing = 'edesContinuing'
    edesContinued = 'edesContinued'
    edesFurtherObjecting = 'edesFurtherObjecting'
    edesFurtherObjection = 'edesFurtherObjection'
    edesResending = 'edesResending'

if TYPE_CHECKING:
    ElectronicDocumentEntryStatusEnumField = ElectronicDocumentEntryStatusEnum | Literal['edesNone', 'edesNew', 'edesReadyToProcess', 'edesPending', 'edesError', 'edesOK', 'edesSent', 'edesDocError', 'edesTempError', 'edesWarning', 'edesWaiting', 'edesAuthorized', 'edesInProcess', 'edesRejected', 'edesDenied', 'edesCanceled', 'edesAborted', 'edesUnused', 'edesQueued', 'edesImported', 'edesApproved', 'edesApproving', 'edesRejecting', 'edesGenerated', 'edesDetermined', 'edesImporting', 'edesInProcessToIntermediary', 'edesSentToIntermediary', 'edesApprovedByIntermediary', 'edesNotIntegratedCustomer', 'edesNotSentToCustomer', 'edesErrorSendingToCustomer', 'edesSentToCustomer', 'edesReceivedByCustomer', 'edesRejectedByCustomer', 'edesPaidByCustomer', 'edesCheckingIntegrationStatus', 'edesNotApproved', 'edesChargeReversal', 'edesCanceling', 'edesContinuing', 'edesContinued', 'edesFurtherObjecting', 'edesFurtherObjection', 'edesResending']
else:
    ElectronicDocumentEntryStatusEnumField = ElectronicDocumentEntryStatusEnum

class ElectronicDocumentEntryTypeEnum(StrEnum):
    edetNone = 'edetNone'
    edetSetup = 'edetSetup'
    edetReport = 'edetReport'
    edetDocumentAR = 'edetDocumentAR'
    edetDocumentAP = 'edetDocumentAP'
    edetDraftAR = 'edetDraftAR'
    edetDraftAP = 'edetDraftAP'
    edetOther = 'edetOther'
    edetSkip = 'edetSkip'
    edetContingency = 'edetContingency'
    edetBpCheck = 'edetBpCheck'
    edetIncomingPayment = 'edetIncomingPayment'
    edetOutgoingPayment = 'edetOutgoingPayment'
    edetInternalReconciliation = 'edetInternalReconciliation'
    edetTransportationDocument = 'edetTransportationDocument'
    edetInventoryTransfer = 'edetInventoryTransfer'
    edetVATObligations = 'edetVATObligations'
    edetVATDeclarations = 'edetVATDeclarations'
    edetVATLiabilities = 'edetVATLiabilities'
    edetVATPayments = 'edetVATPayments'
    edetDelivery = 'edetDelivery'
    edetReturn = 'edetReturn'
    edetARInvoice = 'edetARInvoice'
    edetARCreditMemo = 'edetARCreditMemo'
    edetGoodsReceiptPO = 'edetGoodsReceiptPO'
    edetGoodsReturn = 'edetGoodsReturn'
    edetAPInvoice = 'edetAPInvoice'
    edetAPCreditMemo = 'edetAPCreditMemo'
    edetDraftIncomingPayment = 'edetDraftIncomingPayment'
    edetDraftOutgoingPayment = 'edetDraftOutgoingPayment'
    edetJournalEntry = 'edetJournalEntry'
    edetEBooksExpense = 'edetEBooksExpense'
    edetSkatDKPeriod = 'edetSkatDKPeriod'
    edetSkatDKDraftReport = 'edetSkatDKDraftReport'
    edetSkatDKReport = 'edetSkatDKReport'
    edetINV = 'edetINV'
    edetRIN = 'edetRIN'
    edetDLN = 'edetDLN'
    edetINVBasedOnDLN = 'edetINVBasedOnDLN'
    edetSeries = 'edetSeries'
    edetInvoices = 'edetInvoices'
    edetGoodsTransfers = 'edetGoodsTransfers'

if TYPE_CHECKING:
    ElectronicDocumentEntryTypeEnumField = ElectronicDocumentEntryTypeEnum | Literal['edetNone', 'edetSetup', 'edetReport', 'edetDocumentAR', 'edetDocumentAP', 'edetDraftAR', 'edetDraftAP', 'edetOther', 'edetSkip', 'edetContingency', 'edetBpCheck', 'edetIncomingPayment', 'edetOutgoingPayment', 'edetInternalReconciliation', 'edetTransportationDocument', 'edetInventoryTransfer', 'edetVATObligations', 'edetVATDeclarations', 'edetVATLiabilities', 'edetVATPayments', 'edetDelivery', 'edetReturn', 'edetARInvoice', 'edetARCreditMemo', 'edetGoodsReceiptPO', 'edetGoodsReturn', 'edetAPInvoice', 'edetAPCreditMemo', 'edetDraftIncomingPayment', 'edetDraftOutgoingPayment', 'edetJournalEntry', 'edetEBooksExpense', 'edetSkatDKPeriod', 'edetSkatDKDraftReport', 'edetSkatDKReport', 'edetINV', 'edetRIN', 'edetDLN', 'edetINVBasedOnDLN', 'edetSeries', 'edetInvoices', 'edetGoodsTransfers']
else:
    ElectronicDocumentEntryTypeEnumField = ElectronicDocumentEntryTypeEnum

class EmployeeExemptionUnitEnum(StrEnum):
    eeu_None = 'eeu_None'
    eeu_Yearly = 'eeu_Yearly'
    eeu_Monthly = 'eeu_Monthly'
    eeu_Weekly = 'eeu_Weekly'
    eeu_Daily = 'eeu_Daily'

if TYPE_CHECKING:
    EmployeeExemptionUnitEnumField = EmployeeExemptionUnitEnum | Literal['eeu_None', 'eeu_Yearly', 'eeu_Monthly', 'eeu_Weekly', 'eeu_Daily']
else:
    EmployeeExemptionUnitEnumField = EmployeeExemptionUnitEnum

class EmployeePaymentMethodEnum(StrEnum):
    epm_None = 'epm_None'
    epm_BankTransfer = 'epm_BankTransfer'

if TYPE_CHECKING:
    EmployeePaymentMethodEnumField = EmployeePaymentMethodEnum | Literal['epm_None', 'epm_BankTransfer']
else:
    EmployeePaymentMethodEnumField = EmployeePaymentMethodEnum

class EmployeeTransferProcessingStatusEnum(StrEnum):
    etps_New = 'etps_New'
    etps_Sent = 'etps_Sent'
    etps_Accepted = 'etps_Accepted'
    etps_Error = 'etps_Error'

if TYPE_CHECKING:
    EmployeeTransferProcessingStatusEnumField = EmployeeTransferProcessingStatusEnum | Literal['etps_New', 'etps_Sent', 'etps_Accepted', 'etps_Error']
else:
    EmployeeTransferProcessingStatusEnumField = EmployeeTransferProcessingStatusEnum

class EmployeeTransferStatusEnum(StrEnum):
    ets_New = 'ets_New'
    ets_Processing = 'ets_Processing'
    ets_Sent = 'ets_Sent'
    ets_Received = 'ets_Received'
    ets_Accepted = 'ets_Accepted'
    ets_Error = 'ets_Error'

if TYPE_CHECKING:
    EmployeeTransferStatusEnumField = EmployeeTransferStatusEnum | Literal['ets_New', 'ets_Processing', 'ets_Sent', 'ets_Received', 'ets_Accepted', 'ets_Error']
else:
    EmployeeTransferStatusEnumField = EmployeeTransferStatusEnum

class EndTypeEnum(StrEnum):
    etNoEndDate = 'etNoEndDate'
    etByCounter = 'etByCounter'
    etByDate = 'etByDate'

if TYPE_CHECKING:
    EndTypeEnumField = EndTypeEnum | Literal['etNoEndDate', 'etByCounter', 'etByDate']
else:
    EndTypeEnumField = EndTypeEnum

class ExchangeRateSelectEnum(StrEnum):
    ierFromInovice = 'ierFromInovice'
    ierCurrentRate = 'ierCurrentRate'

if TYPE_CHECKING:
    ExchangeRateSelectEnumField = ExchangeRateSelectEnum | Literal['ierFromInovice', 'ierCurrentRate']
else:
    ExchangeRateSelectEnumField = ExchangeRateSelectEnum

class ExemptionMaxAmountValidationTypeEnum(StrEnum):
    emaIndividual = 'emaIndividual'
    emaAccumulated = 'emaAccumulated'

if TYPE_CHECKING:
    ExemptionMaxAmountValidationTypeEnumField = ExemptionMaxAmountValidationTypeEnum | Literal['emaIndividual', 'emaAccumulated']
else:
    ExemptionMaxAmountValidationTypeEnumField = ExemptionMaxAmountValidationTypeEnum

class ExternalCallStatusEnum(StrEnum):
    ecsNew = 'ecsNew'
    ecsInProcess = 'ecsInProcess'
    ecsCompleted = 'ecsCompleted'
    ecsConfirmed = 'ecsConfirmed'
    ecsFailed = 'ecsFailed'

if TYPE_CHECKING:
    ExternalCallStatusEnumField = ExternalCallStatusEnum | Literal['ecsNew', 'ecsInProcess', 'ecsCompleted', 'ecsConfirmed', 'ecsFailed']
else:
    ExternalCallStatusEnumField = ExternalCallStatusEnum

class FolioLetterEnum(StrEnum):
    fLetterA = 'fLetterA'
    fLetterB = 'fLetterB'
    fLetterC = 'fLetterC'
    fLetterE = 'fLetterE'
    fLetterM = 'fLetterM'
    fLetterR = 'fLetterR'
    fLetterT = 'fLetterT'
    fLetterX = 'fLetterX'
    fLetterEMPTY = 'fLetterEMPTY'

if TYPE_CHECKING:
    FolioLetterEnumField = FolioLetterEnum | Literal['fLetterA', 'fLetterB', 'fLetterC', 'fLetterE', 'fLetterM', 'fLetterR', 'fLetterT', 'fLetterX', 'fLetterEMPTY']
else:
    FolioLetterEnumField = FolioLetterEnum

class FormattedSearchByFieldEnum(StrEnum):
    fsbfWhenExitingAlteredColumn = 'fsbfWhenExitingAlteredColumn'
    fsbfWhenFieldChanges = 'fsbfWhenFieldChanges'
    fsbfWhenColumnValueChanges = 'fsbfWhenColumnValueChanges'

if TYPE_CHECKING:
    FormattedSearchByFieldEnumField = FormattedSearchByFieldEnum | Literal['fsbfWhenExitingAlteredColumn', 'fsbfWhenFieldChanges', 'fsbfWhenColumnValueChanges']
else:
    FormattedSearchByFieldEnumField = FormattedSearchByFieldEnum

class FreightTypeEnum(StrEnum):
    ftShipping = 'ftShipping'
    ftInsurance = 'ftInsurance'
    ftOther = 'ftOther'
    ftSpecial = 'ftSpecial'

if TYPE_CHECKING:
    FreightTypeEnumField = FreightTypeEnum | Literal['ftShipping', 'ftInsurance', 'ftOther', 'ftSpecial']
else:
    FreightTypeEnumField = FreightTypeEnum

class FreightTypeForBolloEnum(StrEnum):
    ftStandard = 'ftStandard'
    ftBollo = 'ftBollo'

if TYPE_CHECKING:
    FreightTypeForBolloEnumField = FreightTypeForBolloEnum | Literal['ftStandard', 'ftBollo']
else:
    FreightTypeForBolloEnumField = FreightTypeForBolloEnum

class GSTTaxCategoryEnum(StrEnum):
    gtc_Regular = 'gtc_Regular'
    gtc_NilRated = 'gtc_NilRated'
    gtc_Exempt = 'gtc_Exempt'

if TYPE_CHECKING:
    GSTTaxCategoryEnumField = GSTTaxCategoryEnum | Literal['gtc_Regular', 'gtc_NilRated', 'gtc_Exempt']
else:
    GSTTaxCategoryEnumField = GSTTaxCategoryEnum

class GSTTransactionTypeEnum(StrEnum):
    gsttrantyp_BillOfSupply = 'gsttrantyp_BillOfSupply'
    gsttrantyp_GSTTaxInvoice = 'gsttrantyp_GSTTaxInvoice'
    gsttrantyp_GSTDebitMemo = 'gsttrantyp_GSTDebitMemo'

if TYPE_CHECKING:
    GSTTransactionTypeEnumField = GSTTransactionTypeEnum | Literal['gsttrantyp_BillOfSupply', 'gsttrantyp_GSTTaxInvoice', 'gsttrantyp_GSTDebitMemo']
else:
    GSTTransactionTypeEnumField = GSTTransactionTypeEnum

class GTSResponseToExceedingEnum(StrEnum):
    Block = 'Block'
    Split = 'Split'

if TYPE_CHECKING:
    GTSResponseToExceedingEnumField = GTSResponseToExceedingEnum | Literal['Block', 'Split']
else:
    GTSResponseToExceedingEnumField = GTSResponseToExceedingEnum

class GeneratedAssetStatusEnum(StrEnum):
    gasOpen = 'gasOpen'
    gasClosed = 'gasClosed'

if TYPE_CHECKING:
    GeneratedAssetStatusEnumField = GeneratedAssetStatusEnum | Literal['gasOpen', 'gasClosed']
else:
    GeneratedAssetStatusEnumField = GeneratedAssetStatusEnum

class GetGLAccountByEnum(StrEnum):
    gglab_General = 'gglab_General'
    gglab_Warehouse = 'gglab_Warehouse'
    gglab_ItemGroup = 'gglab_ItemGroup'

if TYPE_CHECKING:
    GetGLAccountByEnumField = GetGLAccountByEnum | Literal['gglab_General', 'gglab_Warehouse', 'gglab_ItemGroup']
else:
    GetGLAccountByEnumField = GetGLAccountByEnum

class GovPayCodePeriodicityEnum(StrEnum):
    gpcpMonth = 'gpcpMonth'
    gpcpQuarter = 'gpcpQuarter'
    gpcpHalfMonth = 'gpcpHalfMonth'
    gpcpTenDays = 'gpcpTenDays'

if TYPE_CHECKING:
    GovPayCodePeriodicityEnumField = GovPayCodePeriodicityEnum | Literal['gpcpMonth', 'gpcpQuarter', 'gpcpHalfMonth', 'gpcpTenDays']
else:
    GovPayCodePeriodicityEnumField = GovPayCodePeriodicityEnum

class GovPayCodeSPEDCategoryEnum(StrEnum):
    gpcscICMS = 'gpcscICMS'
    gpcscICMSST = 'gpcscICMSST'
    gpcscIPI = 'gpcscIPI'
    gpcscISS = 'gpcscISS'
    gpcscPIS = 'gpcscPIS'
    gpcscCOFINS = 'gpcscCOFINS'
    gpcsPISST = 'gpcsPISST'
    gpcsCONFINSST = 'gpcsCONFINSST'

if TYPE_CHECKING:
    GovPayCodeSPEDCategoryEnumField = GovPayCodeSPEDCategoryEnum | Literal['gpcscICMS', 'gpcscICMSST', 'gpcscIPI', 'gpcscISS', 'gpcscPIS', 'gpcscCOFINS', 'gpcsPISST', 'gpcsCONFINSST']
else:
    GovPayCodeSPEDCategoryEnumField = GovPayCodeSPEDCategoryEnum

class GroupingMethodEnum(StrEnum):
    gmPerInvoice = 'gmPerInvoice'
    gmPerDunningLevel = 'gmPerDunningLevel'
    gmPerBP = 'gmPerBP'

if TYPE_CHECKING:
    GroupingMethodEnumField = GroupingMethodEnum | Literal['gmPerInvoice', 'gmPerDunningLevel', 'gmPerBP']
else:
    GroupingMethodEnumField = GroupingMethodEnum

class IdentificationCodeTypeEnum(StrEnum):
    idctOrder = 'idctOrder'
    idctDelivery = 'idctDelivery'
    idctInvoice = 'idctInvoice'
    idctCreditNote = 'idctCreditNote'
    idctStandardItemTypeIdentification = 'idctStandardItemTypeIdentification'
    idctItemCommodityClassification = 'idctItemCommodityClassification'

if TYPE_CHECKING:
    IdentificationCodeTypeEnumField = IdentificationCodeTypeEnum | Literal['idctOrder', 'idctDelivery', 'idctInvoice', 'idctCreditNote', 'idctStandardItemTypeIdentification', 'idctItemCommodityClassification']
else:
    IdentificationCodeTypeEnumField = IdentificationCodeTypeEnum

class ImportFieldTypeEnum(StrEnum):
    iftInvalid = 'iftInvalid'
    iftFederalTaxID = 'iftFederalTaxID'
    iftAdditionalID = 'iftAdditionalID'
    iftUnifiedFederalTaxID = 'iftUnifiedFederalTaxID'
    iftCNPJ = 'iftCNPJ'
    iftAliasName = 'iftAliasName'
    iftIBAN = 'iftIBAN'
    iftBPName = 'iftBPName'

if TYPE_CHECKING:
    ImportFieldTypeEnumField = ImportFieldTypeEnum | Literal['iftInvalid', 'iftFederalTaxID', 'iftAdditionalID', 'iftUnifiedFederalTaxID', 'iftCNPJ', 'iftAliasName', 'iftIBAN', 'iftBPName']
else:
    ImportFieldTypeEnumField = ImportFieldTypeEnum

class ImportOrExportTypeEnum(StrEnum):
    et_IpmortsOrExports = 'et_IpmortsOrExports'
    et_SEZ_Developer = 'et_SEZ_Developer'
    et_SEZ_Unit = 'et_SEZ_Unit'
    et_Deemed_ImportsOrExports = 'et_Deemed_ImportsOrExports'

if TYPE_CHECKING:
    ImportOrExportTypeEnumField = ImportOrExportTypeEnum | Literal['et_IpmortsOrExports', 'et_SEZ_Developer', 'et_SEZ_Unit', 'et_Deemed_ImportsOrExports']
else:
    ImportOrExportTypeEnumField = ImportOrExportTypeEnum

class InstallmentPaymentsPossiblityEnum(StrEnum):
    ippCr = 'ippCr'
    ippNo = 'ippNo'
    ippRd = 'ippRd'
    ippYes = 'ippYes'

if TYPE_CHECKING:
    InstallmentPaymentsPossiblityEnumField = InstallmentPaymentsPossiblityEnum | Literal['ippCr', 'ippNo', 'ippRd', 'ippYes']
else:
    InstallmentPaymentsPossiblityEnumField = InstallmentPaymentsPossiblityEnum

class IntrastatConfigurationEnum(StrEnum):
    enAdditionalMeasureUnit = 'enAdditionalMeasureUnit'
    enCommodityCodes = 'enCommodityCodes'
    enCustomProcedures = 'enCustomProcedures'
    enIncoterms = 'enIncoterms'
    enNatureOfTransactions = 'enNatureOfTransactions'
    enPortsOfEntryAndExit = 'enPortsOfEntryAndExit'
    enServiceCodes = 'enServiceCodes'
    enStatisticalProcedures = 'enStatisticalProcedures'
    enTransportModes = 'enTransportModes'
    enRegions = 'enRegions'

if TYPE_CHECKING:
    IntrastatConfigurationEnumField = IntrastatConfigurationEnum | Literal['enAdditionalMeasureUnit', 'enCommodityCodes', 'enCustomProcedures', 'enIncoterms', 'enNatureOfTransactions', 'enPortsOfEntryAndExit', 'enServiceCodes', 'enStatisticalProcedures', 'enTransportModes', 'enRegions']
else:
    IntrastatConfigurationEnumField = IntrastatConfigurationEnum

class IntrastatConfigurationTriangDealEnum(StrEnum):
    enNone = 'enNone'
    enType11 = 'enType11'
    enType21 = 'enType21'
    enType31 = 'enType31'

if TYPE_CHECKING:
    IntrastatConfigurationTriangDealEnumField = IntrastatConfigurationTriangDealEnum | Literal['enNone', 'enType11', 'enType21', 'enType31']
else:
    IntrastatConfigurationTriangDealEnumField = IntrastatConfigurationTriangDealEnum

class InvBaseDocTypeEnum(StrEnum):
    Default = 'Default'
    Empty = 'Empty'
    PurchaseDeliveryNotes = 'PurchaseDeliveryNotes'
    InventoryGeneralEntry = 'InventoryGeneralEntry'
    WarehouseTransfers = 'WarehouseTransfers'
    InventoryTransferRequest = 'InventoryTransferRequest'

if TYPE_CHECKING:
    InvBaseDocTypeEnumField = InvBaseDocTypeEnum | Literal['Default', 'Empty', 'PurchaseDeliveryNotes', 'InventoryGeneralEntry', 'WarehouseTransfers', 'InventoryTransferRequest']
else:
    InvBaseDocTypeEnumField = InvBaseDocTypeEnum

class InventoryAccountTypeEnum(StrEnum):
    iatExpenses = 'iatExpenses'
    iatRevenues = 'iatRevenues'
    iatExemptIncome = 'iatExemptIncome'
    iatInventory = 'iatInventory'
    iatCost = 'iatCost'
    iatTransfer = 'iatTransfer'
    iatVarience = 'iatVarience'
    iatPriceDifference = 'iatPriceDifference'
    iatNegativeInventoryAdjustment = 'iatNegativeInventoryAdjustment'
    iatDecreasing = 'iatDecreasing'
    iatIncreasing = 'iatIncreasing'
    iatReturning = 'iatReturning'
    iatEURevenues = 'iatEURevenues'
    iatEUExpenses = 'iatEUExpenses'
    iatForeignRevenue = 'iatForeignRevenue'
    iatForeignExpens = 'iatForeignExpens'
    iatPurchase = 'iatPurchase'
    iatPAReturn = 'iatPAReturn'
    iatPurchaseOffset = 'iatPurchaseOffset'
    iatExchangeRateDifferences = 'iatExchangeRateDifferences'
    iatGoodsClearing = 'iatGoodsClearing'
    iatGLDecrease = 'iatGLDecrease'
    iatGLIncrease = 'iatGLIncrease'
    iatWip = 'iatWip'
    iatWipVariance = 'iatWipVariance'
    iatWipOffsetProfitAndLoss = 'iatWipOffsetProfitAndLoss'
    iatInventoryOffsetProfitAndLoss = 'iatInventoryOffsetProfitAndLoss'
    iatStockInflationAdjust = 'iatStockInflationAdjust'
    iatStockInflationOffset = 'iatStockInflationOffset'
    iatCostInflation = 'iatCostInflation'
    iatCostInflationOffset = 'iatCostInflationOffset'
    iatExpenseClearing = 'iatExpenseClearing'
    iatExpenseOffsetting = 'iatExpenseOffsetting'
    iatStockInTransit = 'iatStockInTransit'
    iatShippedGoods = 'iatShippedGoods'
    iatVATInRevenue = 'iatVATInRevenue'
    iatSalesCredit = 'iatSalesCredit'
    iatPurchaseCredit = 'iatPurchaseCredit'
    iatExemptedCredits = 'iatExemptedCredits'
    iatSalesCreditForeign = 'iatSalesCreditForeign'
    iatForeignPurchaseCredit = 'iatForeignPurchaseCredit'
    iatSalesCreditEU = 'iatSalesCreditEU'
    iatEUPurchaseCredit = 'iatEUPurchaseCredit'
    iatPurchaseBalance = 'iatPurchaseBalance'
    iatWHIncomingCenvat = 'iatWHIncomingCenvat'
    iatWHOutgoingCenvat = 'iatWHOutgoingCenvat'
    iatFreeOfChargeSales = 'iatFreeOfChargeSales'
    iatFreeOfChargePurchase = 'iatFreeOfChargePurchase'

if TYPE_CHECKING:
    InventoryAccountTypeEnumField = InventoryAccountTypeEnum | Literal['iatExpenses', 'iatRevenues', 'iatExemptIncome', 'iatInventory', 'iatCost', 'iatTransfer', 'iatVarience', 'iatPriceDifference', 'iatNegativeInventoryAdjustment', 'iatDecreasing', 'iatIncreasing', 'iatReturning', 'iatEURevenues', 'iatEUExpenses', 'iatForeignRevenue', 'iatForeignExpens', 'iatPurchase', 'iatPAReturn', 'iatPurchaseOffset', 'iatExchangeRateDifferences', 'iatGoodsClearing', 'iatGLDecrease', 'iatGLIncrease', 'iatWip', 'iatWipVariance', 'iatWipOffsetProfitAndLoss', 'iatInventoryOffsetProfitAndLoss', 'iatStockInflationAdjust', 'iatStockInflationOffset', 'iatCostInflation', 'iatCostInflationOffset', 'iatExpenseClearing', 'iatExpenseOffsetting', 'iatStockInTransit', 'iatShippedGoods', 'iatVATInRevenue', 'iatSalesCredit', 'iatPurchaseCredit', 'iatExemptedCredits', 'iatSalesCreditForeign', 'iatForeignPurchaseCredit', 'iatSalesCreditEU', 'iatEUPurchaseCredit', 'iatPurchaseBalance', 'iatWHIncomingCenvat', 'iatWHOutgoingCenvat', 'iatFreeOfChargeSales', 'iatFreeOfChargePurchase']
else:
    InventoryAccountTypeEnumField = InventoryAccountTypeEnum

class InventoryCycleTypeEnum(StrEnum):
    ictCylce = 'ictCylce'
    ictMRP = 'ictMRP'

if TYPE_CHECKING:
    InventoryCycleTypeEnumField = InventoryCycleTypeEnum | Literal['ictCylce', 'ictMRP']
else:
    InventoryCycleTypeEnumField = InventoryCycleTypeEnum

class InventoryOpeningBalancePriceSourceEnum(StrEnum):
    iobpsByPriceList = 'iobpsByPriceList'
    iobpsLastEvaluatedPrice = 'iobpsLastEvaluatedPrice'
    iobpsItemCost = 'iobpsItemCost'

if TYPE_CHECKING:
    InventoryOpeningBalancePriceSourceEnumField = InventoryOpeningBalancePriceSourceEnum | Literal['iobpsByPriceList', 'iobpsLastEvaluatedPrice', 'iobpsItemCost']
else:
    InventoryOpeningBalancePriceSourceEnumField = InventoryOpeningBalancePriceSourceEnum

class InventoryPostingCopyOptionEnum(StrEnum):
    ipcoNoCountersDiff = 'ipcoNoCountersDiff'
    ipcoIndividual1CountedQuantity = 'ipcoIndividual1CountedQuantity'
    ipcoIndividual2CountedQuantity = 'ipcoIndividual2CountedQuantity'
    ipcoIndividual3CountedQuantity = 'ipcoIndividual3CountedQuantity'
    ipcoIndividual4CountedQuantity = 'ipcoIndividual4CountedQuantity'
    ipcoIndividual5CountedQuantity = 'ipcoIndividual5CountedQuantity'
    ipcoTeamCountedQuantity = 'ipcoTeamCountedQuantity'

if TYPE_CHECKING:
    InventoryPostingCopyOptionEnumField = InventoryPostingCopyOptionEnum | Literal['ipcoNoCountersDiff', 'ipcoIndividual1CountedQuantity', 'ipcoIndividual2CountedQuantity', 'ipcoIndividual3CountedQuantity', 'ipcoIndividual4CountedQuantity', 'ipcoIndividual5CountedQuantity', 'ipcoTeamCountedQuantity']
else:
    InventoryPostingCopyOptionEnumField = InventoryPostingCopyOptionEnum

class InventoryPostingPriceSourceEnum(StrEnum):
    ippsByPriceList = 'ippsByPriceList'
    ippsLastEvaluatedPrice = 'ippsLastEvaluatedPrice'
    ippsItemCost = 'ippsItemCost'

if TYPE_CHECKING:
    InventoryPostingPriceSourceEnumField = InventoryPostingPriceSourceEnum | Literal['ippsByPriceList', 'ippsLastEvaluatedPrice', 'ippsItemCost']
else:
    InventoryPostingPriceSourceEnumField = InventoryPostingPriceSourceEnum

class IssuePrimarilyByEnum(StrEnum):
    ipbSerialAndBatchNumbers = 'ipbSerialAndBatchNumbers'
    ipbBinLocations = 'ipbBinLocations'

if TYPE_CHECKING:
    IssuePrimarilyByEnumField = IssuePrimarilyByEnum | Literal['ipbSerialAndBatchNumbers', 'ipbBinLocations']
else:
    IssuePrimarilyByEnumField = IssuePrimarilyByEnum

class ItemClassEnum(StrEnum):
    itcService = 'itcService'
    itcMaterial = 'itcMaterial'

if TYPE_CHECKING:
    ItemClassEnumField = ItemClassEnum | Literal['itcService', 'itcMaterial']
else:
    ItemClassEnumField = ItemClassEnum

class ItemTypeEnum(StrEnum):
    itItems = 'itItems'
    itLabor = 'itLabor'
    itTravel = 'itTravel'
    itFixedAssets = 'itFixedAssets'

if TYPE_CHECKING:
    ItemTypeEnumField = ItemTypeEnum | Literal['itItems', 'itLabor', 'itTravel', 'itFixedAssets']
else:
    ItemTypeEnumField = ItemTypeEnum

class ItemUoMTypeEnum(StrEnum):
    iutPurchasing = 'iutPurchasing'
    iutSales = 'iutSales'
    iutInventory = 'iutInventory'

if TYPE_CHECKING:
    ItemUoMTypeEnumField = ItemUoMTypeEnum | Literal['iutPurchasing', 'iutSales', 'iutInventory']
else:
    ItemUoMTypeEnumField = ItemUoMTypeEnum

class KPITypeEnum(StrEnum):
    asSingle = 'asSingle'
    asQuarterly = 'asQuarterly'
    asMonthly = 'asMonthly'
    asMultiple = 'asMultiple'

if TYPE_CHECKING:
    KPITypeEnumField = KPITypeEnum | Literal['asSingle', 'asQuarterly', 'asMonthly', 'asMultiple']
else:
    KPITypeEnumField = KPITypeEnum

class LCCostTypeEnum(StrEnum):
    asFixedCosts = 'asFixedCosts'
    asVariableCosts = 'asVariableCosts'
    asLegalCosts = 'asLegalCosts'

if TYPE_CHECKING:
    LCCostTypeEnumField = LCCostTypeEnum | Literal['asFixedCosts', 'asVariableCosts', 'asLegalCosts']
else:
    LCCostTypeEnumField = LCCostTypeEnum

class LandedCostAllocationByEnum(StrEnum):
    asCashValueBeforeCustoms = 'asCashValueBeforeCustoms'
    asCashValueAfterCustoms = 'asCashValueAfterCustoms'
    asQuantity = 'asQuantity'
    asWeight = 'asWeight'
    asVolume = 'asVolume'
    asEqual = 'asEqual'
    asLegalCost = 'asLegalCost'

if TYPE_CHECKING:
    LandedCostAllocationByEnumField = LandedCostAllocationByEnum | Literal['asCashValueBeforeCustoms', 'asCashValueAfterCustoms', 'asQuantity', 'asWeight', 'asVolume', 'asEqual', 'asLegalCost']
else:
    LandedCostAllocationByEnumField = LandedCostAllocationByEnum

class LandedCostBaseDocumentTypeEnum(StrEnum):
    asDefault = 'asDefault'
    asEmpty = 'asEmpty'
    asGoodsReceiptPO = 'asGoodsReceiptPO'
    asLandedCosts = 'asLandedCosts'
    asPurchaseInvoice = 'asPurchaseInvoice'

if TYPE_CHECKING:
    LandedCostBaseDocumentTypeEnumField = LandedCostBaseDocumentTypeEnum | Literal['asDefault', 'asEmpty', 'asGoodsReceiptPO', 'asLandedCosts', 'asPurchaseInvoice']
else:
    LandedCostBaseDocumentTypeEnumField = LandedCostBaseDocumentTypeEnum

class LandedCostCostCategoryEnum(StrEnum):
    lccc_CustomsVAT = 'lccc_CustomsVAT'
    lccc_ExciseCost = 'lccc_ExciseCost'
    lccc_CustomsDuty = 'lccc_CustomsDuty'

if TYPE_CHECKING:
    LandedCostCostCategoryEnumField = LandedCostCostCategoryEnum | Literal['lccc_CustomsVAT', 'lccc_ExciseCost', 'lccc_CustomsDuty']
else:
    LandedCostCostCategoryEnumField = LandedCostCostCategoryEnum

class LandedCostDocStatusEnum(StrEnum):
    lcOpen = 'lcOpen'
    lcClosed = 'lcClosed'

if TYPE_CHECKING:
    LandedCostDocStatusEnumField = LandedCostDocStatusEnum | Literal['lcOpen', 'lcClosed']
else:
    LandedCostDocStatusEnumField = LandedCostDocStatusEnum

class LegalDataLineTypeEnum(StrEnum):
    ldlt_DocumentTotal = 'ldlt_DocumentTotal'
    ldlt_TaxPerLine = 'ldlt_TaxPerLine'
    ldlt_TotalTax = 'ldlt_TotalTax'

if TYPE_CHECKING:
    LegalDataLineTypeEnumField = LegalDataLineTypeEnum | Literal['ldlt_DocumentTotal', 'ldlt_TaxPerLine', 'ldlt_TotalTax']
else:
    LegalDataLineTypeEnumField = LegalDataLineTypeEnum

class LicenseTypeEnum(StrEnum):
    lkIdirect = 'lkIdirect'
    lkSOAIndirect = 'lkSOAIndirect'
    lkSOA = 'lkSOA'
    lkB1iIndirect = 'lkB1iIndirect'
    lkB1i = 'lkB1i'

if TYPE_CHECKING:
    LicenseTypeEnumField = LicenseTypeEnum | Literal['lkIdirect', 'lkSOAIndirect', 'lkSOA', 'lkB1iIndirect', 'lkB1i']
else:
    LicenseTypeEnumField = LicenseTypeEnum

class LicenseUpdateTypeEnum(StrEnum):
    ultAssign = 'ultAssign'
    ultRemove = 'ultRemove'

if TYPE_CHECKING:
    LicenseUpdateTypeEnumField = LicenseUpdateTypeEnum | Literal['ultAssign', 'ultRemove']
else:
    LicenseUpdateTypeEnumField = LicenseUpdateTypeEnum

class LineStatusTypeEnum(StrEnum):
    lst_Open = 'lst_Open'
    lst_Closed = 'lst_Closed'

if TYPE_CHECKING:
    LineStatusTypeEnumField = LineStatusTypeEnum | Literal['lst_Open', 'lst_Closed']
else:
    LineStatusTypeEnumField = LineStatusTypeEnum

class LineTypeEnum(StrEnum):
    ltDocument = 'ltDocument'
    ltRounding = 'ltRounding'
    ltVat = 'ltVat'

if TYPE_CHECKING:
    LineTypeEnumField = LineTypeEnum | Literal['ltDocument', 'ltRounding', 'ltVat']
else:
    LineTypeEnumField = LineTypeEnum

class LinkReferenceTypeEnum(StrEnum):
    lrt_00 = 'lrt_00'
    lrt_01 = 'lrt_01'
    lrt_02 = 'lrt_02'
    lrt_03 = 'lrt_03'
    lrt_04 = 'lrt_04'
    lrt_05 = 'lrt_05'
    lrt_06 = 'lrt_06'
    lrt_07 = 'lrt_07'
    lrt_08 = 'lrt_08'
    lrt_MX_08 = 'lrt_MX_08'
    lrt_MX_09 = 'lrt_MX_09'

if TYPE_CHECKING:
    LinkReferenceTypeEnumField = LinkReferenceTypeEnum | Literal['lrt_00', 'lrt_01', 'lrt_02', 'lrt_03', 'lrt_04', 'lrt_05', 'lrt_06', 'lrt_07', 'lrt_08', 'lrt_MX_08', 'lrt_MX_09']
else:
    LinkReferenceTypeEnumField = LinkReferenceTypeEnum

class LinkedDocTypeEnum(StrEnum):
    ldtEmptyLink = 'ldtEmptyLink'
    ldtSalesOpportunitiesLink = 'ldtSalesOpportunitiesLink'
    ldtSalesQuotationsLink = 'ldtSalesQuotationsLink'
    ldtSalesOrdersLink = 'ldtSalesOrdersLink'
    ldtDeliveriesLink = 'ldtDeliveriesLink'
    ldtARInvoicesLink = 'ldtARInvoicesLink'

if TYPE_CHECKING:
    LinkedDocTypeEnumField = LinkedDocTypeEnum | Literal['ldtEmptyLink', 'ldtSalesOpportunitiesLink', 'ldtSalesQuotationsLink', 'ldtSalesOrdersLink', 'ldtDeliveriesLink', 'ldtARInvoicesLink']
else:
    LinkedDocTypeEnumField = LinkedDocTypeEnum

class LogonMethodEnum(StrEnum):
    lmBOneIntegrationFramework = 'lmBOneIntegrationFramework'
    lmStandardLogon = 'lmStandardLogon'
    lmNoControl = 'lmNoControl'

if TYPE_CHECKING:
    LogonMethodEnumField = LogonMethodEnum | Literal['lmBOneIntegrationFramework', 'lmStandardLogon', 'lmNoControl']
else:
    LogonMethodEnumField = LogonMethodEnum

class MobileAddonSettingTypeEnum(StrEnum):
    mastModule = 'mastModule'
    mastHome = 'mastHome'

if TYPE_CHECKING:
    MobileAddonSettingTypeEnumField = MobileAddonSettingTypeEnum | Literal['mastModule', 'mastHome']
else:
    MobileAddonSettingTypeEnumField = MobileAddonSettingTypeEnum

class MobileAppReportChoiceEnum(StrEnum):
    marSystemReport = 'marSystemReport'
    marCustomizedReport = 'marCustomizedReport'

if TYPE_CHECKING:
    MobileAppReportChoiceEnumField = MobileAppReportChoiceEnum | Literal['marSystemReport', 'marCustomizedReport']
else:
    MobileAppReportChoiceEnumField = MobileAppReportChoiceEnum

class MultipleCounterRoleEnum(StrEnum):
    mcrTeamCounter = 'mcrTeamCounter'
    mcrIndividualCounter = 'mcrIndividualCounter'

if TYPE_CHECKING:
    MultipleCounterRoleEnumField = MultipleCounterRoleEnum | Literal['mcrTeamCounter', 'mcrIndividualCounter']
else:
    MultipleCounterRoleEnumField = MultipleCounterRoleEnum

class OperationCode347Enum(StrEnum):
    ocGoodsOrServiciesAcquisitions = 'ocGoodsOrServiciesAcquisitions'
    ocPublicEntitiesAcquisitions = 'ocPublicEntitiesAcquisitions'
    ocTravelAgenciesPurchases = 'ocTravelAgenciesPurchases'
    ocSalesOrServicesRevenues = 'ocSalesOrServicesRevenues'
    ocPublicSubsidies = 'ocPublicSubsidies'
    ocTravelAgenciesSales = 'ocTravelAgenciesSales'

if TYPE_CHECKING:
    OperationCode347EnumField = OperationCode347Enum | Literal['ocGoodsOrServiciesAcquisitions', 'ocPublicEntitiesAcquisitions', 'ocTravelAgenciesPurchases', 'ocSalesOrServicesRevenues', 'ocPublicSubsidies', 'ocTravelAgenciesSales']
else:
    OperationCode347EnumField = OperationCode347Enum

class OperationCodeTypeEnum(StrEnum):
    octSummaryInvoicesEntry = 'octSummaryInvoicesEntry'
    octSummaryReceiptsEntry = 'octSummaryReceiptsEntry'
    octInvoicewithSeveralVATRates = 'octInvoicewithSeveralVATRates'
    octCorrectionInvoice = 'octCorrectionInvoice'
    octDueVATPendingInvoiceIssuance = 'octDueVATPendingInvoiceIssuance'
    octExpensesIncurredbyTravelAgentforCustomers = 'octExpensesIncurredbyTravelAgentforCustomers'
    octSpecialRegulationforVATGroup = 'octSpecialRegulationforVATGroup'
    octSpecialRegulationforGoldInvestment = 'octSpecialRegulationforGoldInvestment'
    octReverseChargeProcedure = 'octReverseChargeProcedure'
    octUnsummarizedReceipts = 'octUnsummarizedReceipts'
    octIdentificationofErrorTransactions = 'octIdentificationofErrorTransactions'
    octTransactionswithEntrepreneursIssuingReceiptsforAgriculturalCompensation = 'octTransactionswithEntrepreneursIssuingReceiptsforAgriculturalCompensation'
    octServiceInvoicingbyTravelAgenciesonBehalfofThirdParties = 'octServiceInvoicingbyTravelAgenciesonBehalfofThirdParties'
    octBusinessOfficeRental = 'octBusinessOfficeRental'
    octSubsidies = 'octSubsidies'
    octIncomingPaymentsforIndustrialandIntellectualPropertyRights = 'octIncomingPaymentsforIndustrialandIntellectualPropertyRights'
    octInsuranceTransactions = 'octInsuranceTransactions'
    octPurchasesfromTravelAgencies = 'octPurchasesfromTravelAgencies'
    octTransactionsSubjecttoProductionServiceandImportTaxesinCeutaandMelilla = 'octTransactionsSubjecttoProductionServiceandImportTaxesinCeutaandMelilla'

if TYPE_CHECKING:
    OperationCodeTypeEnumField = OperationCodeTypeEnum | Literal['octSummaryInvoicesEntry', 'octSummaryReceiptsEntry', 'octInvoicewithSeveralVATRates', 'octCorrectionInvoice', 'octDueVATPendingInvoiceIssuance', 'octExpensesIncurredbyTravelAgentforCustomers', 'octSpecialRegulationforVATGroup', 'octSpecialRegulationforGoldInvestment', 'octReverseChargeProcedure', 'octUnsummarizedReceipts', 'octIdentificationofErrorTransactions', 'octTransactionswithEntrepreneursIssuingReceiptsforAgriculturalCompensation', 'octServiceInvoicingbyTravelAgenciesonBehalfofThirdParties', 'octBusinessOfficeRental', 'octSubsidies', 'octIncomingPaymentsforIndustrialandIntellectualPropertyRights', 'octInsuranceTransactions', 'octPurchasesfromTravelAgencies', 'octTransactionsSubjecttoProductionServiceandImportTaxesinCeutaandMelilla']
else:
    OperationCodeTypeEnumField = OperationCodeTypeEnum

class OpportunityTypeEnum(StrEnum):
    boOpSales = 'boOpSales'
    boOpPurchasing = 'boOpPurchasing'

if TYPE_CHECKING:
    OpportunityTypeEnumField = OpportunityTypeEnum | Literal['boOpSales', 'boOpPurchasing']
else:
    OpportunityTypeEnumField = OpportunityTypeEnum

class PMCategorizeTypeEnum(StrEnum):
    pm_cat_Ignore = 'pm_cat_Ignore'
    pm_cat_OpenAmountAP = 'pm_cat_OpenAmountAP'
    pm_cat_OpenAmountAR = 'pm_cat_OpenAmountAR'
    pm_cat_InvoicedAP = 'pm_cat_InvoicedAP'
    pm_cat_InvoicedAR = 'pm_cat_InvoicedAR'

if TYPE_CHECKING:
    PMCategorizeTypeEnumField = PMCategorizeTypeEnum | Literal['pm_cat_Ignore', 'pm_cat_OpenAmountAP', 'pm_cat_OpenAmountAR', 'pm_cat_InvoicedAP', 'pm_cat_InvoicedAR']
else:
    PMCategorizeTypeEnumField = PMCategorizeTypeEnum

class PMDocumentTypeEnum(StrEnum):
    pmdt_DocumentDraft = 'pmdt_DocumentDraft'
    pmdt_ManualJournalEntry = 'pmdt_ManualJournalEntry'
    pmdt_SalesQuotation = 'pmdt_SalesQuotation'
    pmdt_SalesOrder = 'pmdt_SalesOrder'
    pmdt_Delivery = 'pmdt_Delivery'
    pmdt_Return = 'pmdt_Return'
    pmdt_ReturnRequest = 'pmdt_ReturnRequest'
    pmdt_ARDownPaymentRequest = 'pmdt_ARDownPaymentRequest'
    pmdt_ARDownPaymentInvoice = 'pmdt_ARDownPaymentInvoice'
    pmdt_ARInvoice = 'pmdt_ARInvoice'
    pmdt_ARCreditMemo = 'pmdt_ARCreditMemo'
    pmdt_ARReserveInvoice = 'pmdt_ARReserveInvoice'
    pmdt_PurchaseQuotation = 'pmdt_PurchaseQuotation'
    pmdt_PurchaseOrder = 'pmdt_PurchaseOrder'
    pmdt_PurchaseRequest = 'pmdt_PurchaseRequest'
    pmdt_GoodsReceiptPO = 'pmdt_GoodsReceiptPO'
    pmdt_GoodsReturn = 'pmdt_GoodsReturn'
    pmdt_GoodsReturnRequest = 'pmdt_GoodsReturnRequest'
    pmdt_APDownPaymentRequest = 'pmdt_APDownPaymentRequest'
    pmdt_APDownPaymentInvoice = 'pmdt_APDownPaymentInvoice'
    pmdt_APInvoice = 'pmdt_APInvoice'
    pmdt_APCreditMemo = 'pmdt_APCreditMemo'
    pmdt_APReserveInvoice = 'pmdt_APReserveInvoice'
    pmdt_ServiceCall = 'pmdt_ServiceCall'
    pmdt_GoodsReceipt = 'pmdt_GoodsReceipt'
    pmdt_GoodsIssue = 'pmdt_GoodsIssue'
    pmdt_ARCorrectionInvoice = 'pmdt_ARCorrectionInvoice'
    pmdt_ARCorrectionInvoiceReversal = 'pmdt_ARCorrectionInvoiceReversal'
    pmdt_APCorrectionInvoice = 'pmdt_APCorrectionInvoice'
    pmdt_APCorrectionInvoiceReversal = 'pmdt_APCorrectionInvoiceReversal'

if TYPE_CHECKING:
    PMDocumentTypeEnumField = PMDocumentTypeEnum | Literal['pmdt_DocumentDraft', 'pmdt_ManualJournalEntry', 'pmdt_SalesQuotation', 'pmdt_SalesOrder', 'pmdt_Delivery', 'pmdt_Return', 'pmdt_ReturnRequest', 'pmdt_ARDownPaymentRequest', 'pmdt_ARDownPaymentInvoice', 'pmdt_ARInvoice', 'pmdt_ARCreditMemo', 'pmdt_ARReserveInvoice', 'pmdt_PurchaseQuotation', 'pmdt_PurchaseOrder', 'pmdt_PurchaseRequest', 'pmdt_GoodsReceiptPO', 'pmdt_GoodsReturn', 'pmdt_GoodsReturnRequest', 'pmdt_APDownPaymentRequest', 'pmdt_APDownPaymentInvoice', 'pmdt_APInvoice', 'pmdt_APCreditMemo', 'pmdt_APReserveInvoice', 'pmdt_ServiceCall', 'pmdt_GoodsReceipt', 'pmdt_GoodsIssue', 'pmdt_ARCorrectionInvoice', 'pmdt_ARCorrectionInvoiceReversal', 'pmdt_APCorrectionInvoice', 'pmdt_APCorrectionInvoiceReversal']
else:
    PMDocumentTypeEnumField = PMDocumentTypeEnum

class PMOperationTypeEnum(StrEnum):
    pm_op_Ignore = 'pm_op_Ignore'
    pm_op_Add = 'pm_op_Add'
    pm_op_Subtract = 'pm_op_Subtract'

if TYPE_CHECKING:
    PMOperationTypeEnumField = PMOperationTypeEnum | Literal['pm_op_Ignore', 'pm_op_Add', 'pm_op_Subtract']
else:
    PMOperationTypeEnumField = PMOperationTypeEnum

class PaymentInvoiceTypeEnum(StrEnum):
    itARInvoice = 'itARInvoice'
    itARDownPaymentInvoice = 'itARDownPaymentInvoice'

if TYPE_CHECKING:
    PaymentInvoiceTypeEnumField = PaymentInvoiceTypeEnum | Literal['itARInvoice', 'itARDownPaymentInvoice']
else:
    PaymentInvoiceTypeEnumField = PaymentInvoiceTypeEnum

class PaymentMeansTypeEnum(StrEnum):
    pmtNotAssigned = 'pmtNotAssigned'
    pmtChecks = 'pmtChecks'
    pmtBankTransfer = 'pmtBankTransfer'
    pmtCash = 'pmtCash'
    pmtCreditCard = 'pmtCreditCard'

if TYPE_CHECKING:
    PaymentMeansTypeEnumField = PaymentMeansTypeEnum | Literal['pmtNotAssigned', 'pmtChecks', 'pmtBankTransfer', 'pmtCash', 'pmtCreditCard']
else:
    PaymentMeansTypeEnumField = PaymentMeansTypeEnum

class PaymentRunExportRowTypeEnum(StrEnum):
    prtGeneral = 'prtGeneral'
    prtPayOnAccount = 'prtPayOnAccount'
    prtPayToAccount = 'prtPayToAccount'

if TYPE_CHECKING:
    PaymentRunExportRowTypeEnumField = PaymentRunExportRowTypeEnum | Literal['prtGeneral', 'prtPayOnAccount', 'prtPayToAccount']
else:
    PaymentRunExportRowTypeEnumField = PaymentRunExportRowTypeEnum

class PaymentsAuthorizationStatusEnum(StrEnum):
    pasWithout = 'pasWithout'
    pasPending = 'pasPending'
    pasApproved = 'pasApproved'
    pasRejected = 'pasRejected'
    pasGenerated = 'pasGenerated'
    pasGeneratedbyAuthorizer = 'pasGeneratedbyAuthorizer'
    pasCancelled = 'pasCancelled'

if TYPE_CHECKING:
    PaymentsAuthorizationStatusEnumField = PaymentsAuthorizationStatusEnum | Literal['pasWithout', 'pasPending', 'pasApproved', 'pasRejected', 'pasGenerated', 'pasGeneratedbyAuthorizer', 'pasCancelled']
else:
    PaymentsAuthorizationStatusEnumField = PaymentsAuthorizationStatusEnum

class PeriodStatusEnum(StrEnum):
    ltUnlocked = 'ltUnlocked'
    ltUnlockedExceptSales = 'ltUnlockedExceptSales'
    ltPeriodClosing = 'ltPeriodClosing'
    ltLocked = 'ltLocked'

if TYPE_CHECKING:
    PeriodStatusEnumField = PeriodStatusEnum | Literal['ltUnlocked', 'ltUnlockedExceptSales', 'ltPeriodClosing', 'ltLocked']
else:
    PeriodStatusEnumField = PeriodStatusEnum

class PostingMethodEnum(StrEnum):
    pmGLAccountBankAccount = 'pmGLAccountBankAccount'
    pmBussinessPartnerBankAccount = 'pmBussinessPartnerBankAccount'
    pmInterimAccountBankAccount = 'pmInterimAccountBankAccount'
    pmExternalReconciliation = 'pmExternalReconciliation'
    pmIgnore = 'pmIgnore'

if TYPE_CHECKING:
    PostingMethodEnumField = PostingMethodEnum | Literal['pmGLAccountBankAccount', 'pmBussinessPartnerBankAccount', 'pmInterimAccountBankAccount', 'pmExternalReconciliation', 'pmIgnore']
else:
    PostingMethodEnumField = PostingMethodEnum

class PostingOfDepreciationEnum(StrEnum):
    podDirectPosting = 'podDirectPosting'
    podIndirectPosting = 'podIndirectPosting'

if TYPE_CHECKING:
    PostingOfDepreciationEnumField = PostingOfDepreciationEnum | Literal['podDirectPosting', 'podIndirectPosting']
else:
    PostingOfDepreciationEnumField = PostingOfDepreciationEnum

class PriceModeDocumentEnum(StrEnum):
    pmdNet = 'pmdNet'
    pmdGross = 'pmdGross'
    pmdNetAndGross = 'pmdNetAndGross'

if TYPE_CHECKING:
    PriceModeDocumentEnumField = PriceModeDocumentEnum | Literal['pmdNet', 'pmdGross', 'pmdNetAndGross']
else:
    PriceModeDocumentEnumField = PriceModeDocumentEnum

class PriceModeEnum(StrEnum):
    pmNet = 'pmNet'
    pmGross = 'pmGross'

if TYPE_CHECKING:
    PriceModeEnumField = PriceModeEnum | Literal['pmNet', 'pmGross']
else:
    PriceModeEnumField = PriceModeEnum

class PriceProceedMethodEnum(StrEnum):
    ppmRemove = 'ppmRemove'
    ppmUpdate = 'ppmUpdate'
    ppmKeepCorresponding = 'ppmKeepCorresponding'
    ppmKeepAll = 'ppmKeepAll'

if TYPE_CHECKING:
    PriceProceedMethodEnumField = PriceProceedMethodEnum | Literal['ppmRemove', 'ppmUpdate', 'ppmKeepCorresponding', 'ppmKeepAll']
else:
    PriceProceedMethodEnumField = PriceProceedMethodEnum

class PrintOnEnum(StrEnum):
    poBlankPaper = 'poBlankPaper'
    poDefault = 'poDefault'
    poOverflowBlankPaper = 'poOverflowBlankPaper'
    poOverflowCheckStock = 'poOverflowCheckStock'

if TYPE_CHECKING:
    PrintOnEnumField = PrintOnEnum | Literal['poBlankPaper', 'poDefault', 'poOverflowBlankPaper', 'poOverflowCheckStock']
else:
    PrintOnEnumField = PrintOnEnum

class PrintStatusEnum(StrEnum):
    psNo = 'psNo'
    psYes = 'psYes'
    psAmended = 'psAmended'

if TYPE_CHECKING:
    PrintStatusEnumField = PrintStatusEnum | Literal['psNo', 'psYes', 'psAmended']
else:
    PrintStatusEnumField = PrintStatusEnum

class ProductionItemType(StrEnum):
    pit_Item = 'pit_Item'
    pit_Resource = 'pit_Resource'
    pit_Text = 'pit_Text'

if TYPE_CHECKING:
    ProductionItemTypeField = ProductionItemType | Literal['pit_Item', 'pit_Resource', 'pit_Text']
else:
    ProductionItemTypeField = ProductionItemType

class ProjectStatusTypeEnum(StrEnum):
    pst_Started = 'pst_Started'
    pst_Paused = 'pst_Paused'
    pst_Stopped = 'pst_Stopped'
    pst_Finished = 'pst_Finished'
    pst_Canceled = 'pst_Canceled'

if TYPE_CHECKING:
    ProjectStatusTypeEnumField = ProjectStatusTypeEnum | Literal['pst_Started', 'pst_Paused', 'pst_Stopped', 'pst_Finished', 'pst_Canceled']
else:
    ProjectStatusTypeEnumField = ProjectStatusTypeEnum

class ProjectTypeEnum(StrEnum):
    pt_External = 'pt_External'
    pt_Internal = 'pt_Internal'

if TYPE_CHECKING:
    ProjectTypeEnumField = ProjectTypeEnum | Literal['pt_External', 'pt_Internal']
else:
    ProjectTypeEnumField = ProjectTypeEnum

class RclRecurringExecutionHandlingEnum(StrEnum):
    rehStopOnError = 'rehStopOnError'
    rehSkipTransaction = 'rehSkipTransaction'

if TYPE_CHECKING:
    RclRecurringExecutionHandlingEnumField = RclRecurringExecutionHandlingEnum | Literal['rehStopOnError', 'rehSkipTransaction']
else:
    RclRecurringExecutionHandlingEnumField = RclRecurringExecutionHandlingEnum

class RclRecurringTransactionStatusEnum(StrEnum):
    rtsNotExecuted = 'rtsNotExecuted'
    rtsExecuted = 'rtsExecuted'
    rtsRemoved = 'rtsRemoved'

if TYPE_CHECKING:
    RclRecurringTransactionStatusEnumField = RclRecurringTransactionStatusEnum | Literal['rtsNotExecuted', 'rtsExecuted', 'rtsRemoved']
else:
    RclRecurringTransactionStatusEnumField = RclRecurringTransactionStatusEnum

class ReceivingBinLocationsMethodEnum(StrEnum):
    rblmBinLocationCodeOrder = 'rblmBinLocationCodeOrder'
    rblmAlternativeSortCodeOrder = 'rblmAlternativeSortCodeOrder'

if TYPE_CHECKING:
    ReceivingBinLocationsMethodEnumField = ReceivingBinLocationsMethodEnum | Literal['rblmBinLocationCodeOrder', 'rblmAlternativeSortCodeOrder']
else:
    ReceivingBinLocationsMethodEnumField = ReceivingBinLocationsMethodEnum

class ReceivingUpToMethodEnum(StrEnum):
    rutmBothMaxQtyAndWeight = 'rutmBothMaxQtyAndWeight'
    rutmMaximumQty = 'rutmMaximumQty'
    rutmMaximumWeight = 'rutmMaximumWeight'

if TYPE_CHECKING:
    ReceivingUpToMethodEnumField = ReceivingUpToMethodEnum | Literal['rutmBothMaxQtyAndWeight', 'rutmMaximumQty', 'rutmMaximumWeight']
else:
    ReceivingUpToMethodEnumField = ReceivingUpToMethodEnum

class RecipientTypeEnum(StrEnum):
    rtUser = 'rtUser'
    rtEmployee = 'rtEmployee'

if TYPE_CHECKING:
    RecipientTypeEnumField = RecipientTypeEnum | Literal['rtUser', 'rtEmployee']
else:
    RecipientTypeEnumField = RecipientTypeEnum

class ReconSelectDateTypeEnum(StrEnum):
    rsdtPostDate = 'rsdtPostDate'
    rsdtDueDate = 'rsdtDueDate'
    rsdtDocDate = 'rsdtDocDate'

if TYPE_CHECKING:
    ReconSelectDateTypeEnumField = ReconSelectDateTypeEnum | Literal['rsdtPostDate', 'rsdtDueDate', 'rsdtDocDate']
else:
    ReconSelectDateTypeEnumField = ReconSelectDateTypeEnum

class ReconTypeEnum(StrEnum):
    rtManual = 'rtManual'
    rtAutomatic = 'rtAutomatic'
    rtSemiAutomatic = 'rtSemiAutomatic'
    rtPayment = 'rtPayment'
    rtCreditMemo = 'rtCreditMemo'
    rtReversal = 'rtReversal'
    rtZeroValue = 'rtZeroValue'
    rtCancellation = 'rtCancellation'
    rtBoE = 'rtBoE'
    rtDeposit = 'rtDeposit'
    rtBankStatementProcess = 'rtBankStatementProcess'
    rtPeriodClosing = 'rtPeriodClosing'
    rtCorrectionInvoice = 'rtCorrectionInvoice'
    rtInventoryOrExpenseAllocation = 'rtInventoryOrExpenseAllocation'
    rtWIP = 'rtWIP'
    rtDeferredTaxInterimAccount = 'rtDeferredTaxInterimAccount'
    rtDownPaymentAllocation = 'rtDownPaymentAllocation'
    rtAutoConversionDifference = 'rtAutoConversionDifference'
    rtInterimDocument = 'rtInterimDocument'

if TYPE_CHECKING:
    ReconTypeEnumField = ReconTypeEnum | Literal['rtManual', 'rtAutomatic', 'rtSemiAutomatic', 'rtPayment', 'rtCreditMemo', 'rtReversal', 'rtZeroValue', 'rtCancellation', 'rtBoE', 'rtDeposit', 'rtBankStatementProcess', 'rtPeriodClosing', 'rtCorrectionInvoice', 'rtInventoryOrExpenseAllocation', 'rtWIP', 'rtDeferredTaxInterimAccount', 'rtDownPaymentAllocation', 'rtAutoConversionDifference', 'rtInterimDocument']
else:
    ReconTypeEnumField = ReconTypeEnum

class ReconciliationAccountTypeEnum(StrEnum):
    rat_GLAccount = 'rat_GLAccount'
    rat_BusinessPartner = 'rat_BusinessPartner'

if TYPE_CHECKING:
    ReconciliationAccountTypeEnumField = ReconciliationAccountTypeEnum | Literal['rat_GLAccount', 'rat_BusinessPartner']
else:
    ReconciliationAccountTypeEnumField = ReconciliationAccountTypeEnum

class RecurrenceDayOfWeekEnum(StrEnum):
    rdowDay = 'rdowDay'
    rdowWeekDay = 'rdowWeekDay'
    rdowWeekendDay = 'rdowWeekendDay'
    rdowSun = 'rdowSun'
    rdowMon = 'rdowMon'
    rdowTue = 'rdowTue'
    rdowWed = 'rdowWed'
    rdowThu = 'rdowThu'
    rdowFri = 'rdowFri'
    rdowSat = 'rdowSat'

if TYPE_CHECKING:
    RecurrenceDayOfWeekEnumField = RecurrenceDayOfWeekEnum | Literal['rdowDay', 'rdowWeekDay', 'rdowWeekendDay', 'rdowSun', 'rdowMon', 'rdowTue', 'rdowWed', 'rdowThu', 'rdowFri', 'rdowSat']
else:
    RecurrenceDayOfWeekEnumField = RecurrenceDayOfWeekEnum

class RecurrencePatternEnum(StrEnum):
    rpNone = 'rpNone'
    rpDaily = 'rpDaily'
    rpWeekly = 'rpWeekly'
    rpMonthly = 'rpMonthly'
    rpAnnually = 'rpAnnually'

if TYPE_CHECKING:
    RecurrencePatternEnumField = RecurrencePatternEnum | Literal['rpNone', 'rpDaily', 'rpWeekly', 'rpMonthly', 'rpAnnually']
else:
    RecurrencePatternEnumField = RecurrencePatternEnum

class RecurrenceSequenceEnum(StrEnum):
    rsFirst = 'rsFirst'
    rsSecond = 'rsSecond'
    rsThird = 'rsThird'
    rsFourth = 'rsFourth'
    rsLast = 'rsLast'

if TYPE_CHECKING:
    RecurrenceSequenceEnumField = RecurrenceSequenceEnum | Literal['rsFirst', 'rsSecond', 'rsThird', 'rsFourth', 'rsLast']
else:
    RecurrenceSequenceEnumField = RecurrenceSequenceEnum

class ReferencedObjectTypeEnum(StrEnum):
    rot_ExternalDocument = 'rot_ExternalDocument'
    rot_SalesQuotation = 'rot_SalesQuotation'
    rot_SalesOrder = 'rot_SalesOrder'
    rot_DeliveryNotes = 'rot_DeliveryNotes'
    rot_ReturnRequest = 'rot_ReturnRequest'
    rot_Return = 'rot_Return'
    rot_DownPaymentIncoming = 'rot_DownPaymentIncoming'
    rot_SalesInvoice = 'rot_SalesInvoice'
    rot_SalesCreditNote = 'rot_SalesCreditNote'
    rot_CorrectionSalesInvoice = 'rot_CorrectionSalesInvoice'
    rot_SalesTaxInvoice = 'rot_SalesTaxInvoice'
    rot_PurchaseQuotation = 'rot_PurchaseQuotation'
    rot_PurchaseOrder = 'rot_PurchaseOrder'
    rot_GoodsReceiptPO = 'rot_GoodsReceiptPO'
    rot_GoodsReturnRequest = 'rot_GoodsReturnRequest'
    rot_GoodsReturn = 'rot_GoodsReturn'
    rot_DownPaymentOutgoing = 'rot_DownPaymentOutgoing'
    rot_PurchaseInvoice = 'rot_PurchaseInvoice'
    rot_PurchaseCreditNote = 'rot_PurchaseCreditNote'
    rot_CorrectionPurchaseInvoice = 'rot_CorrectionPurchaseInvoice'
    rot_PurchaseTaxInvoice = 'rot_PurchaseTaxInvoice'
    rot_LandedCosts = 'rot_LandedCosts'
    rot_IncomingPayments = 'rot_IncomingPayments'
    rot_JournalEntry = 'rot_JournalEntry'
    rot_ProductionOrder = 'rot_ProductionOrder'
    rot_InternalReconciliation = 'rot_InternalReconciliation'
    rot_OriginalInvoice = 'rot_OriginalInvoice'
    rot_OriginalARDownPayment = 'rot_OriginalARDownPayment'
    rot_PurchaseRequest = 'rot_PurchaseRequest'
    rot_GoodsReceipt = 'rot_GoodsReceipt'
    rot_GoodsIssue = 'rot_GoodsIssue'
    rot_InventoryTransferRequest = 'rot_InventoryTransferRequest'
    rot_InventoryTransfer = 'rot_InventoryTransfer'
    rot_ChecksforPayment = 'rot_ChecksforPayment'
    rot_MaterialRevaluation = 'rot_MaterialRevaluation'
    rot_InventoryCounting = 'rot_InventoryCounting'
    rot_InventoryPosting = 'rot_InventoryPosting'
    rot_OutgoingPayments = 'rot_OutgoingPayments'

if TYPE_CHECKING:
    ReferencedObjectTypeEnumField = ReferencedObjectTypeEnum | Literal['rot_ExternalDocument', 'rot_SalesQuotation', 'rot_SalesOrder', 'rot_DeliveryNotes', 'rot_ReturnRequest', 'rot_Return', 'rot_DownPaymentIncoming', 'rot_SalesInvoice', 'rot_SalesCreditNote', 'rot_CorrectionSalesInvoice', 'rot_SalesTaxInvoice', 'rot_PurchaseQuotation', 'rot_PurchaseOrder', 'rot_GoodsReceiptPO', 'rot_GoodsReturnRequest', 'rot_GoodsReturn', 'rot_DownPaymentOutgoing', 'rot_PurchaseInvoice', 'rot_PurchaseCreditNote', 'rot_CorrectionPurchaseInvoice', 'rot_PurchaseTaxInvoice', 'rot_LandedCosts', 'rot_IncomingPayments', 'rot_JournalEntry', 'rot_ProductionOrder', 'rot_InternalReconciliation', 'rot_OriginalInvoice', 'rot_OriginalARDownPayment', 'rot_PurchaseRequest', 'rot_GoodsReceipt', 'rot_GoodsIssue', 'rot_InventoryTransferRequest', 'rot_InventoryTransfer', 'rot_ChecksforPayment', 'rot_MaterialRevaluation', 'rot_InventoryCounting', 'rot_InventoryPosting', 'rot_OutgoingPayments']
else:
    ReferencedObjectTypeEnumField = ReferencedObjectTypeEnum

class RelatedDocumentTypeEnum(StrEnum):
    rdt_Payment = 'rdt_Payment'
    rdt_Reconciliation = 'rdt_Reconciliation'

if TYPE_CHECKING:
    RelatedDocumentTypeEnumField = RelatedDocumentTypeEnum | Literal['rdt_Payment', 'rdt_Reconciliation']
else:
    RelatedDocumentTypeEnumField = RelatedDocumentTypeEnum

class RepeatOptionEnum(StrEnum):
    roByDate = 'roByDate'
    roByWeekDay = 'roByWeekDay'

if TYPE_CHECKING:
    RepeatOptionEnumField = RepeatOptionEnum | Literal['roByDate', 'roByWeekDay']
else:
    RepeatOptionEnumField = RepeatOptionEnum

class Report349CodeListEnum(StrEnum):
    r349cA = 'r349cA'
    r349cE = 'r349cE'
    r349cEmpty = 'r349cEmpty'
    r349cH = 'r349cH'
    r349cI = 'r349cI'
    r349cM = 'r349cM'
    r349cS = 'r349cS'
    r349cT = 'r349cT'

if TYPE_CHECKING:
    Report349CodeListEnumField = Report349CodeListEnum | Literal['r349cA', 'r349cE', 'r349cEmpty', 'r349cH', 'r349cI', 'r349cM', 'r349cS', 'r349cT']
else:
    Report349CodeListEnumField = Report349CodeListEnum

class ReportLayoutCategoryEnum(StrEnum):
    rlcPLD = 'rlcPLD'
    rlcCrystal = 'rlcCrystal'
    rlcLegalList = 'rlcLegalList'
    rlcUserDefinedType = 'rlcUserDefinedType'

if TYPE_CHECKING:
    ReportLayoutCategoryEnumField = ReportLayoutCategoryEnum | Literal['rlcPLD', 'rlcCrystal', 'rlcLegalList', 'rlcUserDefinedType']
else:
    ReportLayoutCategoryEnumField = ReportLayoutCategoryEnum

class ResidenceNumberTypeEnum(StrEnum):
    rntSpanishFiscalID = 'rntSpanishFiscalID'
    rntVATRegistrationNumber = 'rntVATRegistrationNumber'
    rntPassport = 'rntPassport'
    rntFiscalIDIssuedbytheResidenceCountry = 'rntFiscalIDIssuedbytheResidenceCountry'
    rntCertificateofFiscalResidence = 'rntCertificateofFiscalResidence'
    rntOtherDocument = 'rntOtherDocument'

if TYPE_CHECKING:
    ResidenceNumberTypeEnumField = ResidenceNumberTypeEnum | Literal['rntSpanishFiscalID', 'rntVATRegistrationNumber', 'rntPassport', 'rntFiscalIDIssuedbytheResidenceCountry', 'rntCertificateofFiscalResidence', 'rntOtherDocument']
else:
    ResidenceNumberTypeEnumField = ResidenceNumberTypeEnum

class ResourceAllocationEnum(StrEnum):
    raOnStartDate = 'raOnStartDate'
    raOnEndDate = 'raOnEndDate'
    raStartDateForwards = 'raStartDateForwards'
    raEndDateBackwards = 'raEndDateBackwards'

if TYPE_CHECKING:
    ResourceAllocationEnumField = ResourceAllocationEnum | Literal['raOnStartDate', 'raOnEndDate', 'raStartDateForwards', 'raEndDateBackwards']
else:
    ResourceAllocationEnumField = ResourceAllocationEnum

class ResourceCapacityActionEnum(StrEnum):
    rcaUnknown = 'rcaUnknown'
    rcaProductionOrderCreate = 'rcaProductionOrderCreate'
    rcaProductionOrderClose = 'rcaProductionOrderClose'
    rcaProductionOrderReschedule = 'rcaProductionOrderReschedule'
    rcaProductionOrderAddLine = 'rcaProductionOrderAddLine'
    rcaProductionOrderDeleteLine = 'rcaProductionOrderDeleteLine'
    rcaProductionOrderUpdateLine = 'rcaProductionOrderUpdateLine'
    rcaIssueForProductionCreate = 'rcaIssueForProductionCreate'
    rcaReceiptFromProductionCreate = 'rcaReceiptFromProductionCreate'

if TYPE_CHECKING:
    ResourceCapacityActionEnumField = ResourceCapacityActionEnum | Literal['rcaUnknown', 'rcaProductionOrderCreate', 'rcaProductionOrderClose', 'rcaProductionOrderReschedule', 'rcaProductionOrderAddLine', 'rcaProductionOrderDeleteLine', 'rcaProductionOrderUpdateLine', 'rcaIssueForProductionCreate', 'rcaReceiptFromProductionCreate']
else:
    ResourceCapacityActionEnumField = ResourceCapacityActionEnum

class ResourceCapacityBaseTypeEnum(StrEnum):
    rcbtNone = 'rcbtNone'
    rcbtProductionOrder = 'rcbtProductionOrder'

if TYPE_CHECKING:
    ResourceCapacityBaseTypeEnumField = ResourceCapacityBaseTypeEnum | Literal['rcbtNone', 'rcbtProductionOrder']
else:
    ResourceCapacityBaseTypeEnumField = ResourceCapacityBaseTypeEnum

class ResourceCapacityMemoSourceEnum(StrEnum):
    rcmsUnknown = 'rcmsUnknown'
    rcmsResourceCapacityForm = 'rcmsResourceCapacityForm'
    rcmsSetDailyInternalCapacitiesForm = 'rcmsSetDailyInternalCapacitiesForm'

if TYPE_CHECKING:
    ResourceCapacityMemoSourceEnumField = ResourceCapacityMemoSourceEnum | Literal['rcmsUnknown', 'rcmsResourceCapacityForm', 'rcmsSetDailyInternalCapacitiesForm']
else:
    ResourceCapacityMemoSourceEnumField = ResourceCapacityMemoSourceEnum

class ResourceCapacityOwningTypeEnum(StrEnum):
    rcotNone = 'rcotNone'
    rcotProductionOrder = 'rcotProductionOrder'
    rcotIssueForProduction = 'rcotIssueForProduction'
    rcotReceiptFromProduction = 'rcotReceiptFromProduction'

if TYPE_CHECKING:
    ResourceCapacityOwningTypeEnumField = ResourceCapacityOwningTypeEnum | Literal['rcotNone', 'rcotProductionOrder', 'rcotIssueForProduction', 'rcotReceiptFromProduction']
else:
    ResourceCapacityOwningTypeEnumField = ResourceCapacityOwningTypeEnum

class ResourceCapacityRevertedTypeEnum(StrEnum):
    rcrtNone = 'rcrtNone'
    rcrtIssueForProduction = 'rcrtIssueForProduction'

if TYPE_CHECKING:
    ResourceCapacityRevertedTypeEnumField = ResourceCapacityRevertedTypeEnum | Literal['rcrtNone', 'rcrtIssueForProduction']
else:
    ResourceCapacityRevertedTypeEnumField = ResourceCapacityRevertedTypeEnum

class ResourceCapacitySourceTypeEnum(StrEnum):
    rcstNone = 'rcstNone'
    rcstProductionOrder = 'rcstProductionOrder'
    rcstIssueForProduction = 'rcstIssueForProduction'
    rcstReceiptFromProduction = 'rcstReceiptFromProduction'

if TYPE_CHECKING:
    ResourceCapacitySourceTypeEnumField = ResourceCapacitySourceTypeEnum | Literal['rcstNone', 'rcstProductionOrder', 'rcstIssueForProduction', 'rcstReceiptFromProduction']
else:
    ResourceCapacitySourceTypeEnumField = ResourceCapacitySourceTypeEnum

class ResourceCapacityTypeEnum(StrEnum):
    rctInternal = 'rctInternal'
    rctOrdered = 'rctOrdered'
    rctCommitted = 'rctCommitted'
    rctConsumed = 'rctConsumed'

if TYPE_CHECKING:
    ResourceCapacityTypeEnumField = ResourceCapacityTypeEnum | Literal['rctInternal', 'rctOrdered', 'rctCommitted', 'rctConsumed']
else:
    ResourceCapacityTypeEnumField = ResourceCapacityTypeEnum

class ResourceDailyCapacityWeekdayEnum(StrEnum):
    rdcwFirst = 'rdcwFirst'
    rdcwSecond = 'rdcwSecond'
    rdcwThird = 'rdcwThird'
    rdcwFourth = 'rdcwFourth'
    rdcwFifth = 'rdcwFifth'
    rdcwSixth = 'rdcwSixth'
    rdcwSeventh = 'rdcwSeventh'

if TYPE_CHECKING:
    ResourceDailyCapacityWeekdayEnumField = ResourceDailyCapacityWeekdayEnum | Literal['rdcwFirst', 'rdcwSecond', 'rdcwThird', 'rdcwFourth', 'rdcwFifth', 'rdcwSixth', 'rdcwSeventh']
else:
    ResourceDailyCapacityWeekdayEnumField = ResourceDailyCapacityWeekdayEnum

class ResourceIssueMethodEnum(StrEnum):
    rimBackflush = 'rimBackflush'
    rimManual = 'rimManual'

if TYPE_CHECKING:
    ResourceIssueMethodEnumField = ResourceIssueMethodEnum | Literal['rimBackflush', 'rimManual']
else:
    ResourceIssueMethodEnumField = ResourceIssueMethodEnum

class ResourceTypeEnum(StrEnum):
    rtMachine = 'rtMachine'
    rtLabor = 'rtLabor'
    rtOther = 'rtOther'

if TYPE_CHECKING:
    ResourceTypeEnumField = ResourceTypeEnum | Literal['rtMachine', 'rtLabor', 'rtOther']
else:
    ResourceTypeEnumField = ResourceTypeEnum

class RetirementMethodEnum(StrEnum):
    rmGross = 'rmGross'
    rmNet = 'rmNet'

if TYPE_CHECKING:
    RetirementMethodEnumField = RetirementMethodEnum | Literal['rmGross', 'rmNet']
else:
    RetirementMethodEnumField = RetirementMethodEnum

class RetirementPeriodControlEnum(StrEnum):
    rpcProRataTemporis = 'rpcProRataTemporis'
    rpcHalfYearConvention = 'rpcHalfYearConvention'
    rpcOnlyAfterEndOfUsefulLife = 'rpcOnlyAfterEndOfUsefulLife'

if TYPE_CHECKING:
    RetirementPeriodControlEnumField = RetirementPeriodControlEnum | Literal['rpcProRataTemporis', 'rpcHalfYearConvention', 'rpcOnlyAfterEndOfUsefulLife']
else:
    RetirementPeriodControlEnumField = RetirementPeriodControlEnum

class RetirementProRataTypeEnum(StrEnum):
    rprtExactlyDailyBase = 'rprtExactlyDailyBase'
    rprtLastDayOfPriorPeriod = 'rprtLastDayOfPriorPeriod'
    rprtLastDayOfCurrentPeriod = 'rprtLastDayOfCurrentPeriod'

if TYPE_CHECKING:
    RetirementProRataTypeEnumField = RetirementProRataTypeEnum | Literal['rprtExactlyDailyBase', 'rprtLastDayOfPriorPeriod', 'rprtLastDayOfCurrentPeriod']
else:
    RetirementProRataTypeEnumField = RetirementProRataTypeEnum

class ReturnTypeEnum(StrEnum):
    rt26Q = 'rt26Q'
    rt27Q = 'rt27Q'
    rt27EQ = 'rt27EQ'

if TYPE_CHECKING:
    ReturnTypeEnumField = ReturnTypeEnum | Literal['rt26Q', 'rt27Q', 'rt27EQ']
else:
    ReturnTypeEnumField = ReturnTypeEnum

class RiskLevelTypeEnum(StrEnum):
    rlt_Low = 'rlt_Low'
    rlt_Medium = 'rlt_Medium'
    rlt_High = 'rlt_High'

if TYPE_CHECKING:
    RiskLevelTypeEnumField = RiskLevelTypeEnum | Literal['rlt_Low', 'rlt_Medium', 'rlt_High']
else:
    RiskLevelTypeEnumField = RiskLevelTypeEnum

class RoundingContextEnum(StrEnum):
    rcSum = 'rcSum'
    rcPrice = 'rcPrice'
    rcRate = 'rcRate'
    rcQuantity = 'rcQuantity'
    rcMeasure = 'rcMeasure'
    rcPercent = 'rcPercent'
    rcTax = 'rcTax'
    rcTaxPerGroup = 'rcTaxPerGroup'
    rcBudgetSum = 'rcBudgetSum'
    rcPriceListSum = 'rcPriceListSum'
    rcRealAmountInPayment = 'rcRealAmountInPayment'
    rcStockSumRoundUp = 'rcStockSumRoundUp'
    rcDocHeaderTotal = 'rcDocHeaderTotal'
    rcVatReportAmount = 'rcVatReportAmount'
    rcLineGrossTotal = 'rcLineGrossTotal'
    rcExpenseTotal = 'rcExpenseTotal'
    rcWTax = 'rcWTax'
    rcBASCode = 'rcBASCode'
    rcTaxForPrice = 'rcTaxForPrice'

if TYPE_CHECKING:
    RoundingContextEnumField = RoundingContextEnum | Literal['rcSum', 'rcPrice', 'rcRate', 'rcQuantity', 'rcMeasure', 'rcPercent', 'rcTax', 'rcTaxPerGroup', 'rcBudgetSum', 'rcPriceListSum', 'rcRealAmountInPayment', 'rcStockSumRoundUp', 'rcDocHeaderTotal', 'rcVatReportAmount', 'rcLineGrossTotal', 'rcExpenseTotal', 'rcWTax', 'rcBASCode', 'rcTaxForPrice']
else:
    RoundingContextEnumField = RoundingContextEnum

class RoundingSysEnum(StrEnum):
    rsNoRounding = 'rsNoRounding'
    rsRoundToFiveHundredth = 'rsRoundToFiveHundredth'
    rsRoundToOne = 'rsRoundToOne'
    rsRoundToTen = 'rsRoundToTen'
    rsRoundToTenHundredth = 'rsRoundToTenHundredth'

if TYPE_CHECKING:
    RoundingSysEnumField = RoundingSysEnum | Literal['rsNoRounding', 'rsRoundToFiveHundredth', 'rsRoundToOne', 'rsRoundToTen', 'rsRoundToTenHundredth']
else:
    RoundingSysEnumField = RoundingSysEnum

class RoundingTypeEnum(StrEnum):
    rt_TruncatedAU = 'rt_TruncatedAU'
    rt_CommercialValues = 'rt_CommercialValues'
    rt_NoRounding = 'rt_NoRounding'

if TYPE_CHECKING:
    RoundingTypeEnumField = RoundingTypeEnum | Literal['rt_TruncatedAU', 'rt_CommercialValues', 'rt_NoRounding']
else:
    RoundingTypeEnumField = RoundingTypeEnum

class SAFTProductTypeEnum(StrEnum):
    saftpt_Products = 'saftpt_Products'
    saftpt_Services = 'saftpt_Services'
    saftpt_Other = 'saftpt_Other'
    saftpt_Taxes = 'saftpt_Taxes'
    saftpt_NonSystem = 'saftpt_NonSystem'

if TYPE_CHECKING:
    SAFTProductTypeEnumField = SAFTProductTypeEnum | Literal['saftpt_Products', 'saftpt_Services', 'saftpt_Other', 'saftpt_Taxes', 'saftpt_NonSystem']
else:
    SAFTProductTypeEnumField = SAFTProductTypeEnum

class SAFTTaxCodeEnum(StrEnum):
    safttc_ReducedTax = 'safttc_ReducedTax'
    safttc_MiddleTax = 'safttc_MiddleTax'
    safttc_NormalTax = 'safttc_NormalTax'
    safttc_Exempt = 'safttc_Exempt'
    safttt_Others = 'safttt_Others'
    safttc_NonSystem = 'safttc_NonSystem'

if TYPE_CHECKING:
    SAFTTaxCodeEnumField = SAFTTaxCodeEnum | Literal['safttc_ReducedTax', 'safttc_MiddleTax', 'safttc_NormalTax', 'safttc_Exempt', 'safttt_Others', 'safttc_NonSystem']
else:
    SAFTTaxCodeEnumField = SAFTTaxCodeEnum

class SAFTTransactionTypeEnum(StrEnum):
    safttt_Default = 'safttt_Default'
    safttt_Normal = 'safttt_Normal'
    safttt_AdjustmentsofTheTaxPeriod = 'safttt_AdjustmentsofTheTaxPeriod'
    safttt_MeasurementofResults = 'safttt_MeasurementofResults'
    safttt_Adjustment = 'safttt_Adjustment'
    safttt_DoNotExport = 'safttt_DoNotExport'
    safttt_NonSystem = 'safttt_NonSystem'

if TYPE_CHECKING:
    SAFTTransactionTypeEnumField = SAFTTransactionTypeEnum | Literal['safttt_Default', 'safttt_Normal', 'safttt_AdjustmentsofTheTaxPeriod', 'safttt_MeasurementofResults', 'safttt_Adjustment', 'safttt_DoNotExport', 'safttt_NonSystem']
else:
    SAFTTransactionTypeEnumField = SAFTTransactionTypeEnum

class SEPASequenceTypeEnum(StrEnum):
    sstOOFF = 'sstOOFF'
    sstFRST = 'sstFRST'
    sstRCUR = 'sstRCUR'
    sstFNAL = 'sstFNAL'

if TYPE_CHECKING:
    SEPASequenceTypeEnumField = SEPASequenceTypeEnum | Literal['sstOOFF', 'sstFRST', 'sstRCUR', 'sstFNAL']
else:
    SEPASequenceTypeEnumField = SEPASequenceTypeEnum

class SOIExcisableTypeEnum(StrEnum):
    se_Excisable = 'se_Excisable'
    se_Exemption = 'se_Exemption'
    se_PaidToOther = 'se_PaidToOther'
    se_NotExcisable = 'se_NotExcisable'

if TYPE_CHECKING:
    SOIExcisableTypeEnumField = SOIExcisableTypeEnum | Literal['se_Excisable', 'se_Exemption', 'se_PaidToOther', 'se_NotExcisable']
else:
    SOIExcisableTypeEnumField = SOIExcisableTypeEnum

class SPEDContabilAccountPurposeCode(StrEnum):
    spedContasDeAtivo = 'spedContasDeAtivo'
    spedContasDePassivo = 'spedContasDePassivo'
    spedPatrimonioLiquido = 'spedPatrimonioLiquido'
    spedContasDeResultado = 'spedContasDeResultado'
    spedContasDeCompensacao = 'spedContasDeCompensacao'
    spedOutras = 'spedOutras'

if TYPE_CHECKING:
    SPEDContabilAccountPurposeCodeField = SPEDContabilAccountPurposeCode | Literal['spedContasDeAtivo', 'spedContasDePassivo', 'spedPatrimonioLiquido', 'spedContasDeResultado', 'spedContasDeCompensacao', 'spedOutras']
else:
    SPEDContabilAccountPurposeCodeField = SPEDContabilAccountPurposeCode

class SPEDContabilQualificationCodeEnum(StrEnum):
    spedNA = 'spedNA'
    spedDiretor = 'spedDiretor'
    spedConselheiroDeAdministracao = 'spedConselheiroDeAdministracao'
    spedAdministrador = 'spedAdministrador'
    spedAdministradorDoGrupo = 'spedAdministradorDoGrupo'
    spedAdministradorDeSociedadeFiliada = 'spedAdministradorDeSociedadeFiliada'
    spedAdministradorJudicialPessoaFisica = 'spedAdministradorJudicialPessoaFisica'
    spedAdministradorJudicialPessoaJuridicaProfissionalResponsavel = 'spedAdministradorJudicialPessoaJuridicaProfissionalResponsavel'
    spedAdministradorJudicialGestor = 'spedAdministradorJudicialGestor'
    spedGestorJudicial = 'spedGestorJudicial'
    spedProcurador = 'spedProcurador'
    spedInventariante = 'spedInventariante'
    spedLiquidante = 'spedLiquidante'
    spedInterventor = 'spedInterventor'
    spedEmpresario = 'spedEmpresario'
    spedContador = 'spedContador'
    spedOutros = 'spedOutros'

if TYPE_CHECKING:
    SPEDContabilQualificationCodeEnumField = SPEDContabilQualificationCodeEnum | Literal['spedNA', 'spedDiretor', 'spedConselheiroDeAdministracao', 'spedAdministrador', 'spedAdministradorDoGrupo', 'spedAdministradorDeSociedadeFiliada', 'spedAdministradorJudicialPessoaFisica', 'spedAdministradorJudicialPessoaJuridicaProfissionalResponsavel', 'spedAdministradorJudicialGestor', 'spedGestorJudicial', 'spedProcurador', 'spedInventariante', 'spedLiquidante', 'spedInterventor', 'spedEmpresario', 'spedContador', 'spedOutros']
else:
    SPEDContabilQualificationCodeEnumField = SPEDContabilQualificationCodeEnum

class ServiceTypeEnum(StrEnum):
    srvcSales = 'srvcSales'
    srvcPurchasing = 'srvcPurchasing'

if TYPE_CHECKING:
    ServiceTypeEnumField = ServiceTypeEnum | Literal['srvcSales', 'srvcPurchasing']
else:
    ServiceTypeEnumField = ServiceTypeEnum

class Services(StrEnum):
    MessagesService = 'MessagesService'
    CompanyService = 'CompanyService'
    SeriesService = 'SeriesService'
    ReportLayoutsService = 'ReportLayoutsService'
    FormPreferencesService = 'FormPreferencesService'
    AccountsService = 'AccountsService'
    BusinessPartnersService = 'BusinessPartnersService'

if TYPE_CHECKING:
    ServicesField = Services | Literal['MessagesService', 'CompanyService', 'SeriesService', 'ReportLayoutsService', 'FormPreferencesService', 'AccountsService', 'BusinessPartnersService']
else:
    ServicesField = Services

class ShaamGroupEnum(StrEnum):
    sgServicesAndAsset = 'sgServicesAndAsset'
    sgAgriculturalProducts = 'sgAgriculturalProducts'
    sgInsuranceCommissions = 'sgInsuranceCommissions'
    sgWHTaxInstructions = 'sgWHTaxInstructions'
    sgInterestExchangeRateDiffs = 'sgInterestExchangeRateDiffs'
    sgRentalFees = 'sgRentalFees'

if TYPE_CHECKING:
    ShaamGroupEnumField = ShaamGroupEnum | Literal['sgServicesAndAsset', 'sgAgriculturalProducts', 'sgInsuranceCommissions', 'sgWHTaxInstructions', 'sgInterestExchangeRateDiffs', 'sgRentalFees']
else:
    ShaamGroupEnumField = ShaamGroupEnum

class SingleUserConnectionActionEnum(StrEnum):
    sucaWarning = 'sucaWarning'
    sucaBlock = 'sucaBlock'

if TYPE_CHECKING:
    SingleUserConnectionActionEnumField = SingleUserConnectionActionEnum | Literal['sucaWarning', 'sucaBlock']
else:
    SingleUserConnectionActionEnumField = SingleUserConnectionActionEnum

class SortOrderEnum(StrEnum):
    soAscending = 'soAscending'
    soDescending = 'soDescending'

if TYPE_CHECKING:
    SortOrderEnumField = SortOrderEnum | Literal['soAscending', 'soDescending']
else:
    SortOrderEnumField = SortOrderEnum

class SourceCurrencyEnum(StrEnum):
    sc_PrimaryCurrency = 'sc_PrimaryCurrency'
    sc_AdditionalCurrency1 = 'sc_AdditionalCurrency1'
    sc_AdditionalCurrency2 = 'sc_AdditionalCurrency2'

if TYPE_CHECKING:
    SourceCurrencyEnumField = SourceCurrencyEnum | Literal['sc_PrimaryCurrency', 'sc_AdditionalCurrency1', 'sc_AdditionalCurrency2']
else:
    SourceCurrencyEnumField = SourceCurrencyEnum

class SpecialDepreciationCalculationMethodEnum(StrEnum):
    spcmAdditional = 'spcmAdditional'
    spcmAlternative = 'spcmAlternative'

if TYPE_CHECKING:
    SpecialDepreciationCalculationMethodEnumField = SpecialDepreciationCalculationMethodEnum | Literal['spcmAdditional', 'spcmAlternative']
else:
    SpecialDepreciationCalculationMethodEnumField = SpecialDepreciationCalculationMethodEnum

class SpecialDepreciationMaximumFlagEnum(StrEnum):
    spmfPercentage = 'spmfPercentage'
    spmfAmount = 'spmfAmount'

if TYPE_CHECKING:
    SpecialDepreciationMaximumFlagEnumField = SpecialDepreciationMaximumFlagEnum | Literal['spmfPercentage', 'spmfAmount']
else:
    SpecialDepreciationMaximumFlagEnumField = SpecialDepreciationMaximumFlagEnum

class SpecialProductTypeEnum(StrEnum):
    sptMT = 'sptMT'
    sptIO = 'sptIO'

if TYPE_CHECKING:
    SpecialProductTypeEnumField = SpecialProductTypeEnum | Literal['sptMT', 'sptIO']
else:
    SpecialProductTypeEnumField = SpecialProductTypeEnum

class StageDepTypeEnum(StrEnum):
    sdt_Project = 'sdt_Project'
    sdt_Subproject = 'sdt_Subproject'

if TYPE_CHECKING:
    StageDepTypeEnumField = StageDepTypeEnum | Literal['sdt_Project', 'sdt_Subproject']
else:
    StageDepTypeEnumField = StageDepTypeEnum

class StockTransferAuthorizationStatusEnum(StrEnum):
    sasWithout = 'sasWithout'
    sasPending = 'sasPending'
    sasApproved = 'sasApproved'
    sasRejected = 'sasRejected'
    sasGenerated = 'sasGenerated'
    sasGeneratedbyAuthorizer = 'sasGeneratedbyAuthorizer'
    sasCancelled = 'sasCancelled'

if TYPE_CHECKING:
    StockTransferAuthorizationStatusEnumField = StockTransferAuthorizationStatusEnum | Literal['sasWithout', 'sasPending', 'sasApproved', 'sasRejected', 'sasGenerated', 'sasGeneratedbyAuthorizer', 'sasCancelled']
else:
    StockTransferAuthorizationStatusEnumField = StockTransferAuthorizationStatusEnum

class StraightLineCalculationMethodEnum(StrEnum):
    slcmAuquisitionValueDividedByTotalUsefulLife = 'slcmAuquisitionValueDividedByTotalUsefulLife'
    slcmPercentageOfAcquisitionValue = 'slcmPercentageOfAcquisitionValue'
    slcmNetBookValueDividedByRemainingLife = 'slcmNetBookValueDividedByRemainingLife'

if TYPE_CHECKING:
    StraightLineCalculationMethodEnumField = StraightLineCalculationMethodEnum | Literal['slcmAuquisitionValueDividedByTotalUsefulLife', 'slcmPercentageOfAcquisitionValue', 'slcmNetBookValueDividedByRemainingLife']
else:
    StraightLineCalculationMethodEnumField = StraightLineCalculationMethodEnum

class StraightLinePeriodControlDepreciationPeriodsEnum(StrEnum):
    slpcdpStandard = 'slpcdpStandard'
    slpcdpIndividual = 'slpcdpIndividual'
    slpcdpIndividualUsage = 'slpcdpIndividualUsage'

if TYPE_CHECKING:
    StraightLinePeriodControlDepreciationPeriodsEnumField = StraightLinePeriodControlDepreciationPeriodsEnum | Literal['slpcdpStandard', 'slpcdpIndividual', 'slpcdpIndividualUsage']
else:
    StraightLinePeriodControlDepreciationPeriodsEnumField = StraightLinePeriodControlDepreciationPeriodsEnum

class SubprojectStatusTypeEnum(StrEnum):
    sst_Open = 'sst_Open'
    sst_Closed = 'sst_Closed'

if TYPE_CHECKING:
    SubprojectStatusTypeEnumField = SubprojectStatusTypeEnum | Literal['sst_Open', 'sst_Closed']
else:
    SubprojectStatusTypeEnumField = SubprojectStatusTypeEnum

class SubsequentAcquisitionPeriodControlEnum(StrEnum):
    sapcProRataTemporis = 'sapcProRataTemporis'
    sapcHalfYearConvention = 'sapcHalfYearConvention'
    sapcFullYear = 'sapcFullYear'

if TYPE_CHECKING:
    SubsequentAcquisitionPeriodControlEnumField = SubsequentAcquisitionPeriodControlEnum | Literal['sapcProRataTemporis', 'sapcHalfYearConvention', 'sapcFullYear']
else:
    SubsequentAcquisitionPeriodControlEnumField = SubsequentAcquisitionPeriodControlEnum

class SubsequentAcquisitionProRataTypeEnum(StrEnum):
    saprtExactlyDailyBase = 'saprtExactlyDailyBase'
    saprtFirstDayOfCurrentPeriod = 'saprtFirstDayOfCurrentPeriod'
    saprtFirstDayOfNextPeriod = 'saprtFirstDayOfNextPeriod'

if TYPE_CHECKING:
    SubsequentAcquisitionProRataTypeEnumField = SubsequentAcquisitionProRataTypeEnum | Literal['saprtExactlyDailyBase', 'saprtFirstDayOfCurrentPeriod', 'saprtFirstDayOfNextPeriod']
else:
    SubsequentAcquisitionProRataTypeEnumField = SubsequentAcquisitionProRataTypeEnum

class SupportUserLoginRecordLogReasonTypeEnum(StrEnum):
    reasonTransIssueAnaly = 'reasonTransIssueAnaly'
    reasonSetupIssueAnaly = 'reasonSetupIssueAnaly'
    reasonDataIssueAnaly = 'reasonDataIssueAnaly'
    reasonAddonIssueAnaly = 'reasonAddonIssueAnaly'
    reasonCustomerIssueAnaly = 'reasonCustomerIssueAnaly'
    reasonSystemMaint = 'reasonSystemMaint'
    reasonConsulting = 'reasonConsulting'
    reasonOther = 'reasonOther'
    reasonAddonAccess = 'reasonAddonAccess'
    reasonRootCauseAnaly = 'reasonRootCauseAnaly'
    reasonConsultSupport = 'reasonConsultSupport'

if TYPE_CHECKING:
    SupportUserLoginRecordLogReasonTypeEnumField = SupportUserLoginRecordLogReasonTypeEnum | Literal['reasonTransIssueAnaly', 'reasonSetupIssueAnaly', 'reasonDataIssueAnaly', 'reasonAddonIssueAnaly', 'reasonCustomerIssueAnaly', 'reasonSystemMaint', 'reasonConsulting', 'reasonOther', 'reasonAddonAccess', 'reasonRootCauseAnaly', 'reasonConsultSupport']
else:
    SupportUserLoginRecordLogReasonTypeEnumField = SupportUserLoginRecordLogReasonTypeEnum

class TCSAccumulationBaseEnum(StrEnum):
    tcsAccumulationOnInvoice = 'tcsAccumulationOnInvoice'
    tcsAccumulationOnPayment = 'tcsAccumulationOnPayment'

if TYPE_CHECKING:
    TCSAccumulationBaseEnumField = TCSAccumulationBaseEnum | Literal['tcsAccumulationOnInvoice', 'tcsAccumulationOnPayment']
else:
    TCSAccumulationBaseEnumField = TCSAccumulationBaseEnum

class TargetGroupTypeEnum(StrEnum):
    tgtCustomer = 'tgtCustomer'
    tgtVendor = 'tgtVendor'

if TYPE_CHECKING:
    TargetGroupTypeEnumField = TargetGroupTypeEnum | Literal['tgtCustomer', 'tgtVendor']
else:
    TargetGroupTypeEnumField = TargetGroupTypeEnum

class TargetGroupsDetailStatusEnum(StrEnum):
    tdsActive = 'tdsActive'
    tdsInactive = 'tdsInactive'

if TYPE_CHECKING:
    TargetGroupsDetailStatusEnumField = TargetGroupsDetailStatusEnum | Literal['tdsActive', 'tdsInactive']
else:
    TargetGroupsDetailStatusEnumField = TargetGroupsDetailStatusEnum

class TaxCalcSysEnum(StrEnum):
    PreconfiguredFormulaWithJurisdictionSupport = 'PreconfiguredFormulaWithJurisdictionSupport'
    UserDefinedFormula = 'UserDefinedFormula'
    PreconfiguredFormula = 'PreconfiguredFormula'

if TYPE_CHECKING:
    TaxCalcSysEnumField = TaxCalcSysEnum | Literal['PreconfiguredFormulaWithJurisdictionSupport', 'UserDefinedFormula', 'PreconfiguredFormula']
else:
    TaxCalcSysEnumField = TaxCalcSysEnum

class TaxCodeDeterminationTCDByUsageTypeEnum(StrEnum):
    tcdbutDefaultSales = 'tcdbutDefaultSales'
    tcdbutDefaultPurchase = 'tcdbutDefaultPurchase'
    tcdbutLine = 'tcdbutLine'

if TYPE_CHECKING:
    TaxCodeDeterminationTCDByUsageTypeEnumField = TaxCodeDeterminationTCDByUsageTypeEnum | Literal['tcdbutDefaultSales', 'tcdbutDefaultPurchase', 'tcdbutLine']
else:
    TaxCodeDeterminationTCDByUsageTypeEnumField = TaxCodeDeterminationTCDByUsageTypeEnum

class TaxCodeDeterminationTCDDefaultWTTypeEnum(StrEnum):
    tcddwttDefaultSales = 'tcddwttDefaultSales'
    tcddwttDefaultPurchase = 'tcddwttDefaultPurchase'
    tcddwttLine = 'tcddwttLine'

if TYPE_CHECKING:
    TaxCodeDeterminationTCDDefaultWTTypeEnumField = TaxCodeDeterminationTCDDefaultWTTypeEnum | Literal['tcddwttDefaultSales', 'tcddwttDefaultPurchase', 'tcddwttLine']
else:
    TaxCodeDeterminationTCDDefaultWTTypeEnumField = TaxCodeDeterminationTCDDefaultWTTypeEnum

class TaxCodeDeterminationTCDTypeEnum(StrEnum):
    tcdtMaterialItem = 'tcdtMaterialItem'
    tcdtServiceItem = 'tcdtServiceItem'
    tcdtServiceDocument = 'tcdtServiceDocument'
    tcdtWithholdingTax = 'tcdtWithholdingTax'

if TYPE_CHECKING:
    TaxCodeDeterminationTCDTypeEnumField = TaxCodeDeterminationTCDTypeEnum | Literal['tcdtMaterialItem', 'tcdtServiceItem', 'tcdtServiceDocument', 'tcdtWithholdingTax']
else:
    TaxCodeDeterminationTCDTypeEnumField = TaxCodeDeterminationTCDTypeEnum

class TaxInvoiceReportLineTypeEnum(StrEnum):
    LineOfBusinessPlace = 'LineOfBusinessPlace'
    LineOfBusinessPartner = 'LineOfBusinessPartner'
    LineOfDocument = 'LineOfDocument'
    LineOfItem = 'LineOfItem'

if TYPE_CHECKING:
    TaxInvoiceReportLineTypeEnumField = TaxInvoiceReportLineTypeEnum | Literal['LineOfBusinessPlace', 'LineOfBusinessPartner', 'LineOfDocument', 'LineOfItem']
else:
    TaxInvoiceReportLineTypeEnumField = TaxInvoiceReportLineTypeEnum

class TaxInvoiceReportNTSApprovedEnum(StrEnum):
    NotApproved = 'NotApproved'
    Approved = 'Approved'

if TYPE_CHECKING:
    TaxInvoiceReportNTSApprovedEnumField = TaxInvoiceReportNTSApprovedEnum | Literal['NotApproved', 'Approved']
else:
    TaxInvoiceReportNTSApprovedEnumField = TaxInvoiceReportNTSApprovedEnum

class TaxRateDeterminationEnum(StrEnum):
    trd_PostingDate = 'trd_PostingDate'
    trd_DocumentDate = 'trd_DocumentDate'

if TYPE_CHECKING:
    TaxRateDeterminationEnumField = TaxRateDeterminationEnum | Literal['trd_PostingDate', 'trd_DocumentDate']
else:
    TaxRateDeterminationEnumField = TaxRateDeterminationEnum

class TaxReportFilterApArDocumentType(StrEnum):
    trfadt_APDocuments = 'trfadt_APDocuments'
    trfadt_ARDocuments = 'trfadt_ARDocuments'

if TYPE_CHECKING:
    TaxReportFilterApArDocumentTypeField = TaxReportFilterApArDocumentType | Literal['trfadt_APDocuments', 'trfadt_ARDocuments']
else:
    TaxReportFilterApArDocumentTypeField = TaxReportFilterApArDocumentType

class TaxReportFilterDeclarationType(StrEnum):
    trfdt_Original = 'trfdt_Original'
    trfdt_Substitute = 'trfdt_Substitute'
    trfdt_Complementary = 'trfdt_Complementary'

if TYPE_CHECKING:
    TaxReportFilterDeclarationTypeField = TaxReportFilterDeclarationType | Literal['trfdt_Original', 'trfdt_Substitute', 'trfdt_Complementary']
else:
    TaxReportFilterDeclarationTypeField = TaxReportFilterDeclarationType

class TaxReportFilterDocumentType(StrEnum):
    trfdt_ARInvoices = 'trfdt_ARInvoices'
    trfdt_ARCreditMemos = 'trfdt_ARCreditMemos'
    trfdt_APInvoices = 'trfdt_APInvoices'
    trfdt_APCreditMemos = 'trfdt_APCreditMemos'
    trfdt_IncomingPayments = 'trfdt_IncomingPayments'
    trfdt_JournalEntries = 'trfdt_JournalEntries'
    trfdt_OutgoingPayments = 'trfdt_OutgoingPayments'
    trfdt_ChecksforPayment = 'trfdt_ChecksforPayment'
    trfdt_InventoryTransfers = 'trfdt_InventoryTransfers'
    trfdt_ARDownPayment = 'trfdt_ARDownPayment'
    trfdt_APDownPayment = 'trfdt_APDownPayment'

if TYPE_CHECKING:
    TaxReportFilterDocumentTypeField = TaxReportFilterDocumentType | Literal['trfdt_ARInvoices', 'trfdt_ARCreditMemos', 'trfdt_APInvoices', 'trfdt_APCreditMemos', 'trfdt_IncomingPayments', 'trfdt_JournalEntries', 'trfdt_OutgoingPayments', 'trfdt_ChecksforPayment', 'trfdt_InventoryTransfers', 'trfdt_ARDownPayment', 'trfdt_APDownPayment']
else:
    TaxReportFilterDocumentTypeField = TaxReportFilterDocumentType

class TaxReportFilterPeriod(StrEnum):
    trfP_Quarter = 'trfP_Quarter'
    trfP_Year = 'trfP_Year'
    trfP_Month = 'trfP_Month'
    trfP_NULL = 'trfP_NULL'

if TYPE_CHECKING:
    TaxReportFilterPeriodField = TaxReportFilterPeriod | Literal['trfP_Quarter', 'trfP_Year', 'trfP_Month', 'trfP_NULL']
else:
    TaxReportFilterPeriodField = TaxReportFilterPeriod

class TaxReportFilterQuarterOrDates(StrEnum):
    trfqd_Interval = 'trfqd_Interval'
    trfqd_Date = 'trfqd_Date'

if TYPE_CHECKING:
    TaxReportFilterQuarterOrDatesField = TaxReportFilterQuarterOrDates | Literal['trfqd_Interval', 'trfqd_Date']
else:
    TaxReportFilterQuarterOrDatesField = TaxReportFilterQuarterOrDates

class TaxReportFilterReportLayoutType(StrEnum):
    trfrlt_RegisterBookLayout = 'trfrlt_RegisterBookLayout'
    trfrlt_DeclarationLayout = 'trfrlt_DeclarationLayout'

if TYPE_CHECKING:
    TaxReportFilterReportLayoutTypeField = TaxReportFilterReportLayoutType | Literal['trfrlt_RegisterBookLayout', 'trfrlt_DeclarationLayout']
else:
    TaxReportFilterReportLayoutTypeField = TaxReportFilterReportLayoutType

class TaxReportFilterType(StrEnum):
    trft_TaxReport = 'trft_TaxReport'
    trft_WTReport = 'trft_WTReport'
    trft_Report347 = 'trft_Report347'
    trft_Report349 = 'trft_Report349'
    trft_ReconciliationReport = 'trft_ReconciliationReport'
    trft_StampTax = 'trft_StampTax'
    trft_SalesReport = 'trft_SalesReport'
    trft_None = 'trft_None'
    trft_BoxReport = 'trft_BoxReport'
    trft_AppendixOP = 'trft_AppendixOP'
    trft_AnnualSalesReport = 'trft_AnnualSalesReport'
    trft_VATRefundReport = 'trft_VATRefundReport'

if TYPE_CHECKING:
    TaxReportFilterTypeField = TaxReportFilterType | Literal['trft_TaxReport', 'trft_WTReport', 'trft_Report347', 'trft_Report349', 'trft_ReconciliationReport', 'trft_StampTax', 'trft_SalesReport', 'trft_None', 'trft_BoxReport', 'trft_AppendixOP', 'trft_AnnualSalesReport', 'trft_VATRefundReport']
else:
    TaxReportFilterTypeField = TaxReportFilterType

class TaxTypeBlackListEnum(StrEnum):
    ttblExcluded = 'ttblExcluded'
    ttblExempt = 'ttblExempt'
    ttblNonSubject = 'ttblNonSubject'
    ttblNotTaxable = 'ttblNotTaxable'
    ttblTaxable = 'ttblTaxable'

if TYPE_CHECKING:
    TaxTypeBlackListEnumField = TaxTypeBlackListEnum | Literal['ttblExcluded', 'ttblExempt', 'ttblNonSubject', 'ttblNotTaxable', 'ttblTaxable']
else:
    TaxTypeBlackListEnumField = TaxTypeBlackListEnum

class TdsTypeEnum(StrEnum):
    wtETds = 'wtETds'
    wtGstTds = 'wtGstTds'
    wtGstTcs = 'wtGstTcs'
    wtTcs = 'wtTcs'

if TYPE_CHECKING:
    TdsTypeEnumField = TdsTypeEnum | Literal['wtETds', 'wtGstTds', 'wtGstTcs', 'wtTcs']
else:
    TdsTypeEnumField = TdsTypeEnum

class ThreatLevelEnum(StrEnum):
    tlLow = 'tlLow'
    tlMedium = 'tlMedium'
    tlHigh = 'tlHigh'

if TYPE_CHECKING:
    ThreatLevelEnumField = ThreatLevelEnum | Literal['tlLow', 'tlMedium', 'tlHigh']
else:
    ThreatLevelEnumField = ThreatLevelEnum

class TimeSheetTypeEnum(StrEnum):
    tsh_Employee = 'tsh_Employee'
    tsh_User = 'tsh_User'
    tsh_Other = 'tsh_Other'

if TYPE_CHECKING:
    TimeSheetTypeEnumField = TimeSheetTypeEnum | Literal['tsh_Employee', 'tsh_User', 'tsh_Other']
else:
    TimeSheetTypeEnumField = TimeSheetTypeEnum

class TransTypesEnum(StrEnum):
    ttAllTransactions = 'ttAllTransactions'
    ttOpeningBalance = 'ttOpeningBalance'
    ttClosingBalance = 'ttClosingBalance'
    ttARInvoice = 'ttARInvoice'
    ttARCredItnote = 'ttARCredItnote'
    ttDelivery = 'ttDelivery'
    ttReturn = 'ttReturn'
    ttAPInvoice = 'ttAPInvoice'
    ttAPCreditNote = 'ttAPCreditNote'
    ttPurchaseDeliveryNote = 'ttPurchaseDeliveryNote'
    ttPurchaseReturn = 'ttPurchaseReturn'
    ttReceipt = 'ttReceipt'
    ttDeposit = 'ttDeposit'
    ttJournalEntry = 'ttJournalEntry'
    ttVendorPayment = 'ttVendorPayment'
    ttChequesForPayment = 'ttChequesForPayment'
    ttStockList = 'ttStockList'
    ttGeneralReceiptToStock = 'ttGeneralReceiptToStock'
    ttGeneralReleaseFromStock = 'ttGeneralReleaseFromStock'
    ttTransferBetweenWarehouses = 'ttTransferBetweenWarehouses'
    ttWorkInstructions = 'ttWorkInstructions'
    ttLandedCosts = 'ttLandedCosts'
    ttDeferredDeposit = 'ttDeferredDeposit'
    ttCorrectionInvoice = 'ttCorrectionInvoice'
    ttInventoryValuation = 'ttInventoryValuation'
    ttAPCorrectionInvoice = 'ttAPCorrectionInvoice'
    ttAPCorrectionInvoiceReversal = 'ttAPCorrectionInvoiceReversal'
    ttARCorrectionInvoice = 'ttARCorrectionInvoice'
    ttARCorrectionInvoiceReversal = 'ttARCorrectionInvoiceReversal'
    ttBoETransaction = 'ttBoETransaction'
    ttProductionOrder = 'ttProductionOrder'
    ttDownPayment = 'ttDownPayment'
    ttPurchaseDownPayment = 'ttPurchaseDownPayment'
    ttInternalReconciliation = 'ttInternalReconciliation'
    ttInventoryPosting = 'ttInventoryPosting'
    ttInventoryOpeningBalance = 'ttInventoryOpeningBalance'

if TYPE_CHECKING:
    TransTypesEnumField = TransTypesEnum | Literal['ttAllTransactions', 'ttOpeningBalance', 'ttClosingBalance', 'ttARInvoice', 'ttARCredItnote', 'ttDelivery', 'ttReturn', 'ttAPInvoice', 'ttAPCreditNote', 'ttPurchaseDeliveryNote', 'ttPurchaseReturn', 'ttReceipt', 'ttDeposit', 'ttJournalEntry', 'ttVendorPayment', 'ttChequesForPayment', 'ttStockList', 'ttGeneralReceiptToStock', 'ttGeneralReleaseFromStock', 'ttTransferBetweenWarehouses', 'ttWorkInstructions', 'ttLandedCosts', 'ttDeferredDeposit', 'ttCorrectionInvoice', 'ttInventoryValuation', 'ttAPCorrectionInvoice', 'ttAPCorrectionInvoiceReversal', 'ttARCorrectionInvoice', 'ttARCorrectionInvoiceReversal', 'ttBoETransaction', 'ttProductionOrder', 'ttDownPayment', 'ttPurchaseDownPayment', 'ttInternalReconciliation', 'ttInventoryPosting', 'ttInventoryOpeningBalance']
else:
    TransTypesEnumField = TransTypesEnum

class TransferSourcePeriodControlEnum(StrEnum):
    tspcProRataTemporis = 'tspcProRataTemporis'

if TYPE_CHECKING:
    TransferSourcePeriodControlEnumField = TransferSourcePeriodControlEnum | Literal['tspcProRataTemporis']
else:
    TransferSourcePeriodControlEnumField = TransferSourcePeriodControlEnum

class TransferSourceProRataTypeEnum(StrEnum):
    tsprtExactlyDailyBase = 'tsprtExactlyDailyBase'
    tsprtLastDayOfPriorPeriod = 'tsprtLastDayOfPriorPeriod'
    tsprtLastDayofCurrentPeriod = 'tsprtLastDayofCurrentPeriod'

if TYPE_CHECKING:
    TransferSourceProRataTypeEnumField = TransferSourceProRataTypeEnum | Literal['tsprtExactlyDailyBase', 'tsprtLastDayOfPriorPeriod', 'tsprtLastDayofCurrentPeriod']
else:
    TransferSourceProRataTypeEnumField = TransferSourceProRataTypeEnum

class TransferTargetPeriodControlEnum(StrEnum):
    ttpcProRataTemporis = 'ttpcProRataTemporis'

if TYPE_CHECKING:
    TransferTargetPeriodControlEnumField = TransferTargetPeriodControlEnum | Literal['ttpcProRataTemporis']
else:
    TransferTargetPeriodControlEnumField = TransferTargetPeriodControlEnum

class TransferTargetProRataTypeEnum(StrEnum):
    ttprtExactlyDailyBase = 'ttprtExactlyDailyBase'
    ttprtFirstDayOfCurrentPeriod = 'ttprtFirstDayOfCurrentPeriod'
    ttprtFirstDayOfNextPeriod = 'ttprtFirstDayOfNextPeriod'

if TYPE_CHECKING:
    TransferTargetProRataTypeEnumField = TransferTargetProRataTypeEnum | Literal['ttprtExactlyDailyBase', 'ttprtFirstDayOfCurrentPeriod', 'ttprtFirstDayOfNextPeriod']
else:
    TransferTargetProRataTypeEnumField = TransferTargetProRataTypeEnum

class TranslationCategoryEnum(StrEnum):
    asCRReport = 'asCRReport'
    asMenuItem = 'asMenuItem'
    asEFMItem = 'asEFMItem'

if TYPE_CHECKING:
    TranslationCategoryEnumField = TranslationCategoryEnum | Literal['asCRReport', 'asMenuItem', 'asEFMItem']
else:
    TranslationCategoryEnumField = TranslationCategoryEnum

class TypeOfAdvancedRulesEnum(StrEnum):
    toarGeneral = 'toarGeneral'
    toarWarehouse = 'toarWarehouse'
    toarItemGroup = 'toarItemGroup'

if TYPE_CHECKING:
    TypeOfAdvancedRulesEnumField = TypeOfAdvancedRulesEnum | Literal['toarGeneral', 'toarWarehouse', 'toarItemGroup']
else:
    TypeOfAdvancedRulesEnumField = TypeOfAdvancedRulesEnum

class TypeOfOperationEnum(StrEnum):
    tooProfessionalServices = 'tooProfessionalServices'
    tooRentingAssets = 'tooRentingAssets'
    tooOthers = 'tooOthers'

if TYPE_CHECKING:
    TypeOfOperationEnumField = TypeOfOperationEnum | Literal['tooProfessionalServices', 'tooRentingAssets', 'tooOthers']
else:
    TypeOfOperationEnumField = TypeOfOperationEnum

class UDFLinkedSystemObjectTypesEnum(StrEnum):
    ulNone = 'ulNone'
    ulChartOfAccounts = 'ulChartOfAccounts'
    ulBusinessPartners = 'ulBusinessPartners'
    ulBanks = 'ulBanks'
    ulItems = 'ulItems'
    ulUsers = 'ulUsers'
    ulInvoices = 'ulInvoices'
    ulCreditNotes = 'ulCreditNotes'
    ulDeliveryNotes = 'ulDeliveryNotes'
    ulReturns = 'ulReturns'
    ulOrders = 'ulOrders'
    ulPurchaseInvoices = 'ulPurchaseInvoices'
    ulPurchaseCreditNotes = 'ulPurchaseCreditNotes'
    ulPurchaseDeliveryNotes = 'ulPurchaseDeliveryNotes'
    ulPurchaseReturns = 'ulPurchaseReturns'
    ulPurchaseOrders = 'ulPurchaseOrders'
    ulQuotations = 'ulQuotations'
    ulIncomingPayments = 'ulIncomingPayments'
    ulDepositsService = 'ulDepositsService'
    ulJournalEntries = 'ulJournalEntries'
    ulContacts = 'ulContacts'
    ulVendorPayments = 'ulVendorPayments'
    ulChecksforPayment = 'ulChecksforPayment'
    ulInventoryGenEntry = 'ulInventoryGenEntry'
    ulInventoryGenExit = 'ulInventoryGenExit'
    ulWarehouses = 'ulWarehouses'
    ulProductTrees = 'ulProductTrees'
    ulStockTransfer = 'ulStockTransfer'
    ulSalesOpportunities = 'ulSalesOpportunities'
    ulDrafts = 'ulDrafts'
    ulMaterialRevaluation = 'ulMaterialRevaluation'
    ulEmployeesInfo = 'ulEmployeesInfo'
    ulCustomerEquipmentCards = 'ulCustomerEquipmentCards'
    ulServiceContracts = 'ulServiceContracts'
    ulServiceCalls = 'ulServiceCalls'
    ulProductionOrders = 'ulProductionOrders'
    ulInventoryTransferRequest = 'ulInventoryTransferRequest'
    ulBlanketAgreementsService = 'ulBlanketAgreementsService'
    ulProjectManagementService = 'ulProjectManagementService'
    ulReturnRequest = 'ulReturnRequest'
    ulGoodsReturnRequest = 'ulGoodsReturnRequest'
    ulSalesEmployee = 'ulSalesEmployee'
    ulLocations = 'ulLocations'
    ulStates = 'ulStates'
    ulResources = 'ulResources'
    ulUnitsofMeasure = 'ulUnitsofMeasure'
    ulPaymentTerms = 'ulPaymentTerms'
    ulPriceLists = 'ulPriceLists'

if TYPE_CHECKING:
    UDFLinkedSystemObjectTypesEnumField = UDFLinkedSystemObjectTypesEnum | Literal['ulNone', 'ulChartOfAccounts', 'ulBusinessPartners', 'ulBanks', 'ulItems', 'ulUsers', 'ulInvoices', 'ulCreditNotes', 'ulDeliveryNotes', 'ulReturns', 'ulOrders', 'ulPurchaseInvoices', 'ulPurchaseCreditNotes', 'ulPurchaseDeliveryNotes', 'ulPurchaseReturns', 'ulPurchaseOrders', 'ulQuotations', 'ulIncomingPayments', 'ulDepositsService', 'ulJournalEntries', 'ulContacts', 'ulVendorPayments', 'ulChecksforPayment', 'ulInventoryGenEntry', 'ulInventoryGenExit', 'ulWarehouses', 'ulProductTrees', 'ulStockTransfer', 'ulSalesOpportunities', 'ulDrafts', 'ulMaterialRevaluation', 'ulEmployeesInfo', 'ulCustomerEquipmentCards', 'ulServiceContracts', 'ulServiceCalls', 'ulProductionOrders', 'ulInventoryTransferRequest', 'ulBlanketAgreementsService', 'ulProjectManagementService', 'ulReturnRequest', 'ulGoodsReturnRequest', 'ulSalesEmployee', 'ulLocations', 'ulStates', 'ulResources', 'ulUnitsofMeasure', 'ulPaymentTerms', 'ulPriceLists']
else:
    UDFLinkedSystemObjectTypesEnumField = UDFLinkedSystemObjectTypesEnum

class UserAccessLogReasonIDTypeEnum(StrEnum):
    reasonPlanInitialSystConf = 'reasonPlanInitialSystConf'
    reasonPlanSystConfChang = 'reasonPlanSystConfChang'
    reasonPlanSystMaint = 'reasonPlanSystMaint'
    reasonPlanKnowlTrans2EndUsr = 'reasonPlanKnowlTrans2EndUsr'
    reasonUnplanRootCauseAnaly = 'reasonUnplanRootCauseAnaly'
    reasonUnplanKnowlTrans2EndUsr = 'reasonUnplanKnowlTrans2EndUsr'
    reasonUnplanSystMaint = 'reasonUnplanSystMaint'
    reasonUnplanSystConfChang = 'reasonUnplanSystConfChang'
    reasonSystMaint = 'reasonSystMaint'
    reasonRootCauseAnaly = 'reasonRootCauseAnaly'
    reasonConsultSupport = 'reasonConsultSupport'
    reasonOther = 'reasonOther'

if TYPE_CHECKING:
    UserAccessLogReasonIDTypeEnumField = UserAccessLogReasonIDTypeEnum | Literal['reasonPlanInitialSystConf', 'reasonPlanSystConfChang', 'reasonPlanSystMaint', 'reasonPlanKnowlTrans2EndUsr', 'reasonUnplanRootCauseAnaly', 'reasonUnplanKnowlTrans2EndUsr', 'reasonUnplanSystMaint', 'reasonUnplanSystConfChang', 'reasonSystMaint', 'reasonRootCauseAnaly', 'reasonConsultSupport', 'reasonOther']
else:
    UserAccessLogReasonIDTypeEnumField = UserAccessLogReasonIDTypeEnum

class UserActionTypeEnum(StrEnum):
    actionLogin = 'actionLogin'
    actionLoginFail = 'actionLoginFail'
    actionLogoff = 'actionLogoff'
    actionCreateUser = 'actionCreateUser'
    actionRemoveUser = 'actionRemoveUser'
    actionSelectSU = 'actionSelectSU'
    actionDeselectSU = 'actionDeselectSU'
    actionLock = 'actionLock'
    actionUnlock = 'actionUnlock'
    actionChPasswd = 'actionChPasswd'
    actionUnlockFail = 'actionUnlockFail'

if TYPE_CHECKING:
    UserActionTypeEnumField = UserActionTypeEnum | Literal['actionLogin', 'actionLoginFail', 'actionLogoff', 'actionCreateUser', 'actionRemoveUser', 'actionSelectSU', 'actionDeselectSU', 'actionLock', 'actionUnlock', 'actionChPasswd', 'actionUnlockFail']
else:
    UserActionTypeEnumField = UserActionTypeEnum

class UserGroupCategoryEnum(StrEnum):
    gc_Authorization = 'gc_Authorization'
    gc_Formsetting = 'gc_Formsetting'
    gc_Alert = 'gc_Alert'
    gc_UITmplate = 'gc_UITmplate'
    gc_All = 'gc_All'

if TYPE_CHECKING:
    UserGroupCategoryEnumField = UserGroupCategoryEnum | Literal['gc_Authorization', 'gc_Formsetting', 'gc_Alert', 'gc_UITmplate', 'gc_All']
else:
    UserGroupCategoryEnumField = UserGroupCategoryEnum

class UserMenuItemTypeEnum(StrEnum):
    umitForm = 'umitForm'
    umitQuery = 'umitQuery'
    umitFolder = 'umitFolder'
    umitReport = 'umitReport'
    umitLink = 'umitLink'

if TYPE_CHECKING:
    UserMenuItemTypeEnumField = UserMenuItemTypeEnum | Literal['umitForm', 'umitQuery', 'umitFolder', 'umitReport', 'umitLink']
else:
    UserMenuItemTypeEnumField = UserMenuItemTypeEnum

class UserQueryTypeEnum(StrEnum):
    uqtRegular = 'uqtRegular'
    uqtWizard = 'uqtWizard'
    uqtGenerator = 'uqtGenerator'
    uqtStoredProcedure = 'uqtStoredProcedure'

if TYPE_CHECKING:
    UserQueryTypeEnumField = UserQueryTypeEnum | Literal['uqtRegular', 'uqtWizard', 'uqtGenerator', 'uqtStoredProcedure']
else:
    UserQueryTypeEnumField = UserQueryTypeEnum

class VMCommunicationStatusEnum(StrEnum):
    vmcs_Pending = 'vmcs_Pending'
    vmcs_Error = 'vmcs_Error'
    vmcs_Successful = 'vmcs_Successful'
    vmcs_New = 'vmcs_New'
    vmcs_Rejected = 'vmcs_Rejected'

if TYPE_CHECKING:
    VMCommunicationStatusEnumField = VMCommunicationStatusEnum | Literal['vmcs_Pending', 'vmcs_Error', 'vmcs_Successful', 'vmcs_New', 'vmcs_Rejected']
else:
    VMCommunicationStatusEnumField = VMCommunicationStatusEnum

class VMCommunicationTypeEnum(StrEnum):
    vmct_MasterData = 'vmct_MasterData'
    vmct_Transaction = 'vmct_Transaction'

if TYPE_CHECKING:
    VMCommunicationTypeEnumField = VMCommunicationTypeEnum | Literal['vmct_MasterData', 'vmct_Transaction']
else:
    VMCommunicationTypeEnumField = VMCommunicationTypeEnum

class VatGroupsTaxRegionEnum(StrEnum):
    vgtrPT = 'vgtrPT'
    vgtrPT_AC = 'vgtrPT_AC'
    vgtrPT_MA = 'vgtrPT_MA'

if TYPE_CHECKING:
    VatGroupsTaxRegionEnumField = VatGroupsTaxRegionEnum | Literal['vgtrPT', 'vgtrPT_AC', 'vgtrPT_MA']
else:
    VatGroupsTaxRegionEnumField = VatGroupsTaxRegionEnum

class ViewStyleTypeEnum(StrEnum):
    vstPage = 'vstPage'
    vstFullScreen = 'vstFullScreen'
    vstLandscape = 'vstLandscape'

if TYPE_CHECKING:
    ViewStyleTypeEnumField = ViewStyleTypeEnum | Literal['vstPage', 'vstFullScreen', 'vstLandscape']
else:
    ViewStyleTypeEnumField = ViewStyleTypeEnum

class WTDDetailType(StrEnum):
    Allowed = 'Allowed'
    SpecialRate = 'SpecialRate'
    Exemption = 'Exemption'

if TYPE_CHECKING:
    WTDDetailTypeField = WTDDetailType | Literal['Allowed', 'SpecialRate', 'Exemption']
else:
    WTDDetailTypeField = WTDDetailType

class WithholdingTaxCodeBaseTypeEnum(StrEnum):
    wtcbt_Gross = 'wtcbt_Gross'
    wtcbt_Net = 'wtcbt_Net'
    wtcbt_VAT = 'wtcbt_VAT'
    wtcbt_Gross_VAT = 'wtcbt_Gross_VAT'
    wtcbt_UoM = 'wtcbt_UoM'

if TYPE_CHECKING:
    WithholdingTaxCodeBaseTypeEnumField = WithholdingTaxCodeBaseTypeEnum | Literal['wtcbt_Gross', 'wtcbt_Net', 'wtcbt_VAT', 'wtcbt_Gross_VAT', 'wtcbt_UoM']
else:
    WithholdingTaxCodeBaseTypeEnumField = WithholdingTaxCodeBaseTypeEnum

class WithholdingTaxCodeCategoryEnum(StrEnum):
    wtcc_Invoice = 'wtcc_Invoice'
    wtcc_Payment = 'wtcc_Payment'

if TYPE_CHECKING:
    WithholdingTaxCodeCategoryEnumField = WithholdingTaxCodeCategoryEnum | Literal['wtcc_Invoice', 'wtcc_Payment']
else:
    WithholdingTaxCodeCategoryEnumField = WithholdingTaxCodeCategoryEnum

class WithholdingTypeEnum(StrEnum):
    wt_VatWithholding = 'wt_VatWithholding'
    wt_IncomeTaxWithholding = 'wt_IncomeTaxWithholding'

if TYPE_CHECKING:
    WithholdingTypeEnumField = WithholdingTypeEnum | Literal['wt_VatWithholding', 'wt_IncomeTaxWithholding']
else:
    WithholdingTypeEnumField = WithholdingTypeEnum
