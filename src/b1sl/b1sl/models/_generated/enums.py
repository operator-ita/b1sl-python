from __future__ import annotations
from enum import Enum, StrEnum

class AccountCategorySourceEnum(StrEnum):
    acsBalanceSheet = 'acsBalanceSheet'
    acsProfitAndLoss = 'acsProfitAndLoss'
    acsTrialBalance = 'acsTrialBalance'

class AccountSegmentationTypeEnum(StrEnum):
    ast_Alphanumeric = 'ast_Alphanumeric'
    ast_Numeric = 'ast_Numeric'

class AcquisitionPeriodControlEnum(StrEnum):
    apcProRataTemporis = 'apcProRataTemporis'
    apcFirstYearConvention = 'apcFirstYearConvention'
    apcHalfYear = 'apcHalfYear'
    apcFullYear = 'apcFullYear'

class AcquisitionProRataTypeEnum(StrEnum):
    aprtExactlyDailyBase = 'aprtExactlyDailyBase'
    aprtFirstDayOfCurrentPeriod = 'aprtFirstDayOfCurrentPeriod'
    aprtFirstDayOfNextPeriod = 'aprtFirstDayOfNextPeriod'

class ActivityRecipientObjTypeEnum(StrEnum):
    arotUser = 'arotUser'
    arotEmployee = 'arotEmployee'
    arotRecipientList = 'arotRecipientList'

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

class AlertManagementFrequencyType(StrEnum):
    atfi_Minutes = 'atfi_Minutes'
    atfi_Hours = 'atfi_Hours'
    atfi_Days = 'atfi_Days'
    atfi_Weeks = 'atfi_Weeks'
    atfi_Monthly = 'atfi_Monthly'

class AlertManagementPriorityEnum(StrEnum):
    atp_Low = 'atp_Low'
    atp_Normal = 'atp_Normal'
    atp_High = 'atp_High'

class AlertManagementTypeEnum(StrEnum):
    att_User = 'att_User'
    att_System = 'att_System'

class AmountCatTypeEnum(StrEnum):
    act_Open = 'act_Open'
    act_Invoiced = 'act_Invoiced'

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

class AreaTypeEnum(StrEnum):
    atPostingtoGL = 'atPostingtoGL'
    atAdditionalArea = 'atAdditionalArea'
    atDerivedArea = 'atDerivedArea'

class AssesseeTypeEnum(StrEnum):
    atCompany = 'atCompany'
    atOthers = 'atOthers'

class AssetDocumentStatusEnum(StrEnum):
    adsPosted = 'adsPosted'
    adsDraft = 'adsDraft'
    adsCancelled = 'adsCancelled'

class AssetDocumentTypeEnum(StrEnum):
    adtOrdinaryDepreciation = 'adtOrdinaryDepreciation'
    adtUnplannedDepreciation = 'adtUnplannedDepreciation'
    adtSpecialDepreciation = 'adtSpecialDepreciation'
    adtAppreciation = 'adtAppreciation'
    adtAssetTransfer = 'adtAssetTransfer'
    adtSales = 'adtSales'
    adtScrapping = 'adtScrapping'
    adtAssetClassTransfer = 'adtAssetClassTransfer'

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

class AssetStatusEnum(StrEnum):
    New = 'New'
    Active = 'Active'
    Inactive = 'Inactive'

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

class AssetTypeEnum(StrEnum):
    atAssetTypeGeneral = 'atAssetTypeGeneral'
    atAssetTypeLowValueAsset = 'atAssetTypeLowValueAsset'

class AttributeGroupFieldTypeEnum(StrEnum):
    agftText = 'agftText'
    agftNumeric = 'agftNumeric'
    agftDate = 'agftDate'
    agftAmount = 'agftAmount'
    agftPrice = 'agftPrice'
    agftQuantity = 'agftQuantity'

class AuthenticateUserResultsEnum(StrEnum):
    aturNoUserConnectedToCompany = 'aturNoUserConnectedToCompany'
    aturUsernamePasswordMatched = 'aturUsernamePasswordMatched'
    aturLogOnUserNotAdmin = 'aturLogOnUserNotAdmin'
    aturBadUserOrPassword = 'aturBadUserOrPassword'
    aturUserHasBeenLocked = 'aturUserHasBeenLocked'
    aturPasswordExpired = 'aturPasswordExpired'
    aturDBErrors = 'aturDBErrors'
    aturWrongDomainName = 'aturWrongDomainName'

class AutoAllocOnReceiptMethodEnum(StrEnum):
    aaormDefaultBin = 'aaormDefaultBin'
    aaormItemCurrentAndHistoricalBins = 'aaormItemCurrentAndHistoricalBins'
    aaormItemCurrentBins = 'aaormItemCurrentBins'
    aaormLastBinReceivedItem = 'aaormLastBinReceivedItem'

class AutomaticPostingEnum(StrEnum):
    apNo = 'apNo'
    apInterestAndFee = 'apInterestAndFee'
    apInterestOnly = 'apInterestOnly'
    apFeeOnly = 'apFeeOnly'

class BADivationAlertLevelEnum(StrEnum):
    badal_NoWarning = 'badal_NoWarning'
    badal_Warning = 'badal_Warning'
    badal_Block = 'badal_Block'

class BADocumentStatus(StrEnum):
    bads_Open = 'bads_Open'
    bads_Closed = 'bads_Closed'
    bads_Cancelled = 'bads_Cancelled'

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

class BankStatementRowSourceEnum(StrEnum):
    bsImported = 'bsImported'
    bsImportedAndAmended = 'bsImportedAndAmended'
    bsManuallyEntered = 'bsManuallyEntered'

class BankStatementStatusEnum(StrEnum):
    bssExecuted = 'bssExecuted'
    bssDraft = 'bssDraft'
    bssOld = 'bssOld'

class BaseDateSelectEnum(StrEnum):
    bdsFromDueDate = 'bdsFromDueDate'
    bdsFromLastDunningRun = 'bdsFromLastDunningRun'

class BatchDetailServiceStatusEnum(StrEnum):
    bdsStatus_Released = 'bdsStatus_Released'
    bdsStatus_NotAccessible = 'bdsStatus_NotAccessible'
    bdsStatus_Locked = 'bdsStatus_Locked'

class BinActionTypeEnum(StrEnum):
    batToWarehouse = 'batToWarehouse'
    batFromWarehouse = 'batFromWarehouse'

class BinLocationFieldTypeEnum(StrEnum):
    blftWarehouseSublevel = 'blftWarehouseSublevel'
    blftBinLocationAttribute = 'blftBinLocationAttribute'

class BinRestrictItemEnum(StrEnum):
    briNone = 'briNone'
    briSpecificItem = 'briSpecificItem'
    briSingleItemOnly = 'briSingleItemOnly'
    briSpecificItemGroup = 'briSpecificItemGroup'
    briSpecificItemGroupOnly = 'briSpecificItemGroupOnly'

class BinRestrictTransactionEnum(StrEnum):
    brtNoRestrictions = 'brtNoRestrictions'
    brtAllTrans = 'brtAllTrans'
    brtInboundTrans = 'brtInboundTrans'
    brtOutboundTrans = 'brtOutboundTrans'
    brtAllExceptInventoryTrans = 'brtAllExceptInventoryTrans'

class BinRestrictUoMEnum(StrEnum):
    bruNone = 'bruNone'
    bruSpecificUoM = 'bruSpecificUoM'
    bruSingleUoMOnly = 'bruSingleUoMOnly'
    bruSpecificUoMGroup = 'bruSpecificUoMGroup'
    bruSpecificUoMGroupOnly = 'bruSpecificUoMGroupOnly'

class BinRestrictionBatchEnum(StrEnum):
    brbNoRestrictions = 'brbNoRestrictions'
    brbSingleBatch = 'brbSingleBatch'

class BlanketAgreementBPTypeEnum(StrEnum):
    atCustomer = 'atCustomer'
    atVendor = 'atVendor'

class BlanketAgreementDatePeriodsEnum(StrEnum):
    Daily = 'Daily'
    Weekly = 'Weekly'
    Monthly = 'Monthly'
    Quarterly = 'Quarterly'
    Semiannually = 'Semiannually'
    Annually = 'Annually'
    OneTime = 'OneTime'

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

class BlanketAgreementMethodEnum(StrEnum):
    amItem = 'amItem'
    amMonetary = 'amMonetary'

class BlanketAgreementStatusEnum(StrEnum):
    asApproved = 'asApproved'
    asOnHold = 'asOnHold'
    asDraft = 'asDraft'
    asTerminated = 'asTerminated'
    asCancelled = 'asCancelled'

class BlanketAgreementTypeEnum(StrEnum):
    atGeneral = 'atGeneral'
    atSpecific = 'atSpecific'

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

class BoAccountTypes(StrEnum):
    at_Revenues = 'at_Revenues'
    at_Expenses = 'at_Expenses'
    at_Other = 'at_Other'

class BoActivities(StrEnum):
    cn_Conversation = 'cn_Conversation'
    cn_Meeting = 'cn_Meeting'
    cn_Task = 'cn_Task'
    cn_Other = 'cn_Other'
    cn_Note = 'cn_Note'
    cn_Campaign = 'cn_Campaign'

class BoAdEpnsDistribMethods(StrEnum):
    aedm_None = 'aedm_None'
    aedm_Quantity = 'aedm_Quantity'
    aedm_Volume = 'aedm_Volume'
    aedm_Weight = 'aedm_Weight'
    aedm_Equally = 'aedm_Equally'
    aedm_RowTotal = 'aedm_RowTotal'

class BoAdEpnsTaxTypes(StrEnum):
    aext_NormalTax = 'aext_NormalTax'
    aext_NoTax = 'aext_NoTax'
    aext_UseTax = 'aext_UseTax'

class BoAddressType(StrEnum):
    bo_ShipTo = 'bo_ShipTo'
    bo_BillTo = 'bo_BillTo'

class BoAeDistMthd(StrEnum):
    aed_Equally = 'aed_Equally'
    aed_LineTotal = 'aed_LineTotal'
    aed_None = 'aed_None'
    aed_Quantity = 'aed_Quantity'
    aed_Volume = 'aed_Volume'
    aed_Weight = 'aed_Weight'

class BoAlertTypeforWHStockEnum(StrEnum):
    atfwhs_WarningOnly = 'atfwhs_WarningOnly'
    atfwhs_Block = 'atfwhs_Block'
    atfwhs_NoMessage = 'atfwhs_NoMessage'

class BoAllocationByEnum(StrEnum):
    ab_CashValueAfterCustoms = 'ab_CashValueAfterCustoms'
    ab_CashValueBeforeCustoms = 'ab_CashValueBeforeCustoms'
    ab_Equal = 'ab_Equal'
    ab_Quantity = 'ab_Quantity'
    ab_Volume = 'ab_Volume'
    ab_Weight = 'ab_Weight'

class BoApprovalRequestDecisionEnum(StrEnum):
    ardPending = 'ardPending'
    ardApproved = 'ardApproved'
    ardNotApproved = 'ardNotApproved'

class BoApprovalRequestStatusEnum(StrEnum):
    arsPending = 'arsPending'
    arsApproved = 'arsApproved'
    arsNotApproved = 'arsNotApproved'
    arsGenerated = 'arsGenerated'
    arsGeneratedByAuthorizer = 'arsGeneratedByAuthorizer'
    arsCancelled = 'arsCancelled'

class BoBOETypes(StrEnum):
    bobt_Incoming = 'bobt_Incoming'
    bobt_Outgoing = 'bobt_Outgoing'

class BoBOTFromStatus(StrEnum):
    btfs_Sent = 'btfs_Sent'
    btfs_Generated = 'btfs_Generated'
    btfs_Deposited = 'btfs_Deposited'
    btfs_Paid = 'btfs_Paid'

class BoBOTToStatus(StrEnum):
    btts_Canceled = 'btts_Canceled'
    btts_Generated = 'btts_Generated'
    btts_Deposit = 'btts_Deposit'
    btts_Paid = 'btts_Paid'
    btts_Failed = 'btts_Failed'
    btts_Closed = 'btts_Closed'

class BoBarCodeStandardEnum(StrEnum):
    rlbsan13 = 'rlbsan13'
    rlbsCode39 = 'rlbsCode39'
    rlbsCode128 = 'rlbsCode128'

class BoBaseDateRateEnum(StrEnum):
    bdr_PostingDate = 'bdr_PostingDate'
    bdr_TaxDate = 'bdr_TaxDate'

class BoBaselineDate(StrEnum):
    bld_PostingDate = 'bld_PostingDate'
    bld_SystemDate = 'bld_SystemDate'
    bld_TaxDate = 'bld_TaxDate'
    bld_ClosingDate = 'bld_ClosingDate'

class BoBlockBudget(StrEnum):
    bb_OnlyAnnualAlert = 'bb_OnlyAnnualAlert'
    bb_MonthlyAlertOnly = 'bb_MonthlyAlertOnly'
    bb_Block = 'bb_Block'

class BoBoeStatus(StrEnum):
    boes_Created = 'boes_Created'
    boes_Sent = 'boes_Sent'
    boes_Deposited = 'boes_Deposited'
    boes_Paid = 'boes_Paid'
    boes_Cancelled = 'boes_Cancelled'
    boes_Closed = 'boes_Closed'
    boes_Failed = 'boes_Failed'

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

class BoBpsDocTypes(StrEnum):
    bpdt_PaymentReference = 'bpdt_PaymentReference'
    bpdt_ISR = 'bpdt_ISR'
    bpdt_DocNum = 'bpdt_DocNum'

class BoBudgetAlert(StrEnum):
    ba_AnnualAlert = 'ba_AnnualAlert'
    ba_MonthlyAlert = 'ba_MonthlyAlert'

class BoBusinessAreaEnum(StrEnum):
    baSales = 'baSales'
    baPurchase = 'baPurchase'
    baSalesAndPurchase = 'baSalesAndPurchase'

class BoBusinessPartnerGroupTypes(StrEnum):
    bbpgt_CustomerGroup = 'bbpgt_CustomerGroup'
    bbpgt_VendorGroup = 'bbpgt_VendorGroup'

class BoBusinessPartnerTypes(StrEnum):
    garAll = 'garAll'
    garCompany = 'garCompany'
    garPrivate = 'garPrivate'
    garGovernment = 'garGovernment'

class BoCardCompanyTypes(StrEnum):
    cCompany = 'cCompany'
    cPrivate = 'cPrivate'
    cGovernment = 'cGovernment'
    cEmployee = 'cEmployee'

class BoCardTypes(StrEnum):
    cCustomer = 'cCustomer'
    cSupplier = 'cSupplier'
    cLid = 'cLid'

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

class BoClosingDateProcedureBaseDateEnum(StrEnum):
    bocpdbld_BaseSystemDate = 'bocpdbld_BaseSystemDate'
    bocpdbld_PostingDate = 'bocpdbld_PostingDate'

class BoClosingDateProcedureDueMonthEnum(StrEnum):
    bocpddm_HalfMonth = 'bocpddm_HalfMonth'
    bocpddm_MonthEnd = 'bocpddm_MonthEnd'
    bocpddm_MonthStart = 'bocpddm_MonthStart'
    bocpddm_None = 'bocpddm_None'

class BoCockpitTypeEnum(StrEnum):
    cptt_UserCockpit = 'cptt_UserCockpit'
    cptt_TemplateCockpit = 'cptt_TemplateCockpit'

class BoConsumptionMethod(StrEnum):
    cm_BackwardForward = 'cm_BackwardForward'
    cm_ForwardBackward = 'cm_ForwardBackward'

class BoContractTypes(StrEnum):
    ct_Customer = 'ct_Customer'
    ct_ItemGroup = 'ct_ItemGroup'
    ct_SerialNumber = 'ct_SerialNumber'

class BoCorInvItemStatus(StrEnum):
    ciis_Was = 'ciis_Was'
    ciis_ShouldBe = 'ciis_ShouldBe'

class BoCpCardAcct(StrEnum):
    cfp_Card = 'cfp_Card'
    cfp_Account = 'cfp_Account'

class BoCurrencyCheck(StrEnum):
    cc_Block = 'cc_Block'
    cc_NoMessage = 'cc_NoMessage'

class BoCurrencySources(StrEnum):
    bocs_LocalCurrency = 'bocs_LocalCurrency'
    bocs_SystemCurrency = 'bocs_SystemCurrency'
    bocs_BPCurrency = 'bocs_BPCurrency'

class BoDataOwnershipManageMethodEnum(StrEnum):
    doManageByDocOnly = 'doManageByDocOnly'
    doManageByBPOnly = 'doManageByBPOnly'
    doManageByBPnDoc = 'doManageByBPnDoc'
    doManageByBranch = 'doManageByBranch'

class BoDataSourceEnum(StrEnum):
    rldsFreeText = 'rldsFreeText'
    rldsSystemVariable = 'rldsSystemVariable'
    rldsDatabase = 'rldsDatabase'
    rldsFormula = 'rldsFormula'

class BoDateTemplate(StrEnum):
    dt_DDMMYY = 'dt_DDMMYY'
    dt_DDMMCCYY = 'dt_DDMMCCYY'
    dt_MMDDYY = 'dt_MMDDYY'
    dt_MMDDCCYY = 'dt_MMDDCCYY'
    dt_CCYYMMDD = 'dt_CCYYMMDD'
    dt_DDMonthYYYY = 'dt_DDMonthYYYY'
    dt_YYMMDD = 'dt_YYMMDD'

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

class BoDefaultBatchStatus(StrEnum):
    dbs_Released = 'dbs_Released'
    dbs_NotAccessible = 'dbs_NotAccessible'
    dbs_Locked = 'dbs_Locked'

class BoDepositAccountTypeEnum(StrEnum):
    datBankAccount = 'datBankAccount'
    datBusinessPartner = 'datBusinessPartner'

class BoDepositCheckEnum(StrEnum):
    dtNo = 'dtNo'
    dcAsCash = 'dcAsCash'
    dtAsPostdated = 'dtAsPostdated'

class BoDepositPostingTypes(StrEnum):
    dpt_Collection = 'dpt_Collection'
    dpt_Discounted = 'dpt_Discounted'

class BoDepositTypeEnum(StrEnum):
    dtChecks = 'dtChecks'
    dtCredit = 'dtCredit'
    dtCash = 'dtCash'
    dtBOE = 'dtBOE'

class BoDocItemType(StrEnum):
    dit_Item = 'dit_Item'
    dit_Resource = 'dit_Resource'

class BoDocLineType(StrEnum):
    dlt_Regular = 'dlt_Regular'
    dlt_Alternative = 'dlt_Alternative'
    dlt_Resource = 'dlt_Resource'

class BoDocSpecialLineType(StrEnum):
    dslt_Text = 'dslt_Text'
    dslt_Subtotal = 'dslt_Subtotal'

class BoDocSummaryTypes(StrEnum):
    dNoSummary = 'dNoSummary'
    dByItems = 'dByItems'
    dByDocuments = 'dByDocuments'

class BoDocWhsAutoIssueMethod(StrEnum):
    whsBinSingleChoiceOnly = 'whsBinSingleChoiceOnly'
    whsBinBinCodeOrder = 'whsBinBinCodeOrder'
    whsBinAltSortCodeOrder = 'whsBinAltSortCodeOrder'
    whsBinQtyDescendingOrder = 'whsBinQtyDescendingOrder'
    whsBinQtyAscendingOrder = 'whsBinQtyAscendingOrder'
    whsBinFIFO = 'whsBinFIFO'
    whsBinLIFO = 'whsBinLIFO'
    whsBinSingleBinPreferred = 'whsBinSingleBinPreferred'

class BoDocWhsUpdateTypes(StrEnum):
    dwh_No = 'dwh_No'
    dwh_OrdersFromVendors = 'dwh_OrdersFromVendors'
    dwh_CustomerOrders = 'dwh_CustomerOrders'
    dwh_Consignment = 'dwh_Consignment'
    dwh_Stock = 'dwh_Stock'

class BoDocumentLinePickStatus(StrEnum):
    dlps_Picked = 'dlps_Picked'
    dlps_NotPicked = 'dlps_NotPicked'
    dlps_ReleasedForPicking = 'dlps_ReleasedForPicking'
    dlps_PartiallyPicked = 'dlps_PartiallyPicked'

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

class BoDocumentTypes(StrEnum):
    dDocument_Items = 'dDocument_Items'
    dDocument_Service = 'dDocument_Service'

class BoDueDateEnum(StrEnum):
    boddDateOfPaymentRun = 'boddDateOfPaymentRun'
    boddDueDateOfInvoice = 'boddDueDateOfInvoice'
    boddPaymentTerms = 'boddPaymentTerms'

class BoDurations(StrEnum):
    du_Seconds = 'du_Seconds'
    du_Minuts = 'du_Minuts'
    du_Hours = 'du_Hours'
    du_Days = 'du_Days'

class BoEquipmentBPType(StrEnum):
    et_Sales = 'et_Sales'
    et_Purchasing = 'et_Purchasing'
    et_SalesAndPurchasing = 'et_SalesAndPurchasing'

class BoExpenseOperationTypeEnum(StrEnum):
    bo_ExpOpType_ProfessionalServices = 'bo_ExpOpType_ProfessionalServices'
    bo_ExpOpType_RentingAssets = 'bo_ExpOpType_RentingAssets'
    bo_ExpOpType_Others = 'bo_ExpOpType_Others'
    bo_ExpOpType_None = 'bo_ExpOpType_None'

class BoExtensionErrorActionEnum(StrEnum):
    eeaStop = 'eeaStop'
    eeaIgnore = 'eeaIgnore'
    eeaPrompt = 'eeaPrompt'

class BoFatherCardTypes(StrEnum):
    cPayments_sum = 'cPayments_sum'
    cDelivery_sum = 'cDelivery_sum'

class BoFieldTypes(StrEnum):
    db_Alpha = 'db_Alpha'
    db_Memo = 'db_Memo'
    db_Numeric = 'db_Numeric'
    db_Date = 'db_Date'
    db_Float = 'db_Float'

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

class BoForecastViewType(StrEnum):
    fvtDaily = 'fvtDaily'
    fvtWeekly = 'fvtWeekly'
    fvtMonthly = 'fvtMonthly'

class BoFormattedSearchActionEnum(StrEnum):
    bofsaNone = 'bofsaNone'
    bofsaValidValues = 'bofsaValidValues'
    bofsaQuery = 'bofsaQuery'

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

class BoGLMethods(StrEnum):
    glm_WH = 'glm_WH'
    glm_ItemClass = 'glm_ItemClass'
    glm_ItemLevel = 'glm_ItemLevel'

class BoGSTRegnTypeEnum(StrEnum):
    invalid = 'invalid'
    gstRegularTDSISD = 'gstRegularTDSISD'
    gstCasualTaxablePerson = 'gstCasualTaxablePerson'
    gstCompositionLevy = 'gstCompositionLevy'
    gstGoverDepartPSU = 'gstGoverDepartPSU'
    gstNonResidentTaxablePerson = 'gstNonResidentTaxablePerson'
    gstUNAgencyEmbassy = 'gstUNAgencyEmbassy'

class BoGenderTypes(StrEnum):
    gt_Female = 'gt_Female'
    gt_Male = 'gt_Male'
    gt_Undefined = 'gt_Undefined'
    gt_Masked = 'gt_Masked'
    gt_Invalid = 'gt_Invalid'

class BoGridTypeEnum(StrEnum):
    gtCombination = 'gtCombination'
    gtContinuousLine = 'gtContinuousLine'
    gtBrokenLine = 'gtBrokenLine'
    gtDots = 'gtDots'

class BoHorizontalAlignmentEnum(StrEnum):
    rlhjRight = 'rlhjRight'
    rlhjLeft = 'rlhjLeft'
    rlhjCentralized = 'rlhjCentralized'
    rlhjLanguageDependent = 'rlhjLanguageDependent'

class BoInterimDocTypes(StrEnum):
    boidt_None = 'boidt_None'
    boidt_ExchangeRate = 'boidt_ExchangeRate'
    boidt_CashDiscount = 'boidt_CashDiscount'

class BoInventorySystem(StrEnum):
    bis_MovingAverage = 'bis_MovingAverage'
    bis_Standard = 'bis_Standard'
    bis_FIFO = 'bis_FIFO'
    bis_SNB = 'bis_SNB'

class BoIssueMethod(StrEnum):
    im_Backflush = 'im_Backflush'
    im_Manual = 'im_Manual'

class BoItemTreeTypes(StrEnum):
    iNotATree = 'iNotATree'
    iAssemblyTree = 'iAssemblyTree'
    iSalesTree = 'iSalesTree'
    iProductionTree = 'iProductionTree'
    iTemplateTree = 'iTemplateTree'
    iIngredient = 'iIngredient'

class BoLineBreakEnum(StrEnum):
    rlsAllowOverflow = 'rlsAllowOverflow'
    rlsAdjustToCell = 'rlsAdjustToCell'
    rlsDivideIntoRows = 'rlsDivideIntoRows'

class BoMRPComponentWarehouse(StrEnum):
    bomcw_BOM = 'bomcw_BOM'
    bomcw_Parent = 'bomcw_Parent'

class BoMYFTypeEnum(StrEnum):
    myft_WholesaleSales = 'myft_WholesaleSales'
    myft_RetailSales = 'myft_RetailSales'
    myft_WholesalePurchases = 'myft_WholesalePurchases'
    myft_OtherExpenseTransactions = 'myft_OtherExpenseTransactions'

class BoManageMethod(StrEnum):
    bomm_OnEveryTransaction = 'bomm_OnEveryTransaction'
    bomm_OnReleaseOnly = 'bomm_OnReleaseOnly'

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

class BoMeritalStatuses(StrEnum):
    mts_Single = 'mts_Single'
    mts_Married = 'mts_Married'
    mts_Divorced = 'mts_Divorced'
    mts_Widowed = 'mts_Widowed'
    mts_NotSpecified = 'mts_NotSpecified'

class BoMoneyPrecisionTypes(StrEnum):
    mpt_Sum = 'mpt_Sum'
    mpt_Price = 'mpt_Price'
    mpt_Rate = 'mpt_Rate'
    mpt_Quantity = 'mpt_Quantity'
    mpt_Percent = 'mpt_Percent'
    mpt_Measure = 'mpt_Measure'
    mpt_Tax = 'mpt_Tax'

class BoMsgPriorities(StrEnum):
    pr_Low = 'pr_Low'
    pr_Normal = 'pr_Normal'
    pr_High = 'pr_High'

class BoMsgRcpTypes(StrEnum):
    rt_RandomUser = 'rt_RandomUser'
    rt_ContactPerson = 'rt_ContactPerson'
    rt_InternalUser = 'rt_InternalUser'

class BoORCTPaymentTypeEnum(StrEnum):
    bopt_None = 'bopt_None'
    bopt_Electronic = 'bopt_Electronic'
    bopt_Post = 'bopt_Post'
    bopt_Telegraph = 'bopt_Telegraph'
    bopt_Express = 'bopt_Express'

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

class BoOpexStatus(StrEnum):
    bos_Open = 'bos_Open'
    bos_Close = 'bos_Close'

class BoOrientationEnum(StrEnum):
    ortVertical = 'ortVertical'
    ortHorizontal = 'ortHorizontal'

class BoPayTermDueTypes(StrEnum):
    pdt_MonthEnd = 'pdt_MonthEnd'
    pdt_HalfMonth = 'pdt_HalfMonth'
    pdt_MonthStart = 'pdt_MonthStart'
    pdt_None = 'pdt_None'

class BoPaymentMeansEnum(StrEnum):
    bopmCheck = 'bopmCheck'
    bopmBankTransfer = 'bopmBankTransfer'
    bopmBillOfExchange = 'bopmBillOfExchange'

class BoPaymentPriorities(StrEnum):
    bopp_Priority_1 = 'bopp_Priority_1'
    bopp_Priority_2 = 'bopp_Priority_2'
    bopp_Priority_3 = 'bopp_Priority_3'
    bopp_Priority_4 = 'bopp_Priority_4'
    bopp_Priority_5 = 'bopp_Priority_5'
    bopp_Priority_6 = 'bopp_Priority_6'

class BoPaymentTypeEnum(StrEnum):
    boptIncoming = 'boptIncoming'
    boptOutgoing = 'boptOutgoing'

class BoPaymentsObjectType(StrEnum):
    bopot_IncomingPayments = 'bopot_IncomingPayments'
    bopot_OutgoingPayments = 'bopot_OutgoingPayments'

class BoPermission(StrEnum):
    boper_Full = 'boper_Full'
    boper_ReadOnly = 'boper_ReadOnly'
    boper_None = 'boper_None'
    boper_Various = 'boper_Various'
    boper_Undefined = 'boper_Undefined'

class BoPickStatus(StrEnum):
    ps_Released = 'ps_Released'
    ps_Picked = 'ps_Picked'
    ps_PartiallyPicked = 'ps_PartiallyPicked'
    ps_PartiallyDelivered = 'ps_PartiallyDelivered'
    ps_Closed = 'ps_Closed'

class BoPictureSizeEnum(StrEnum):
    rlpsOriginalSize = 'rlpsOriginalSize'
    rlpsFitFieldSizeNonProportionally = 'rlpsFitFieldSizeNonProportionally'
    rlpsFitFieldSizeProportionally = 'rlpsFitFieldSizeProportionally'
    rlpsFitFieldHeight = 'rlpsFitFieldHeight'
    rlpsFitFieldWidth = 'rlpsFitFieldWidth'

class BoPlanningSystem(StrEnum):
    bop_MRP = 'bop_MRP'
    bop_None = 'bop_None'

class BoPriceListGroupNum(StrEnum):
    boplgn_Group1 = 'boplgn_Group1'
    boplgn_Group2 = 'boplgn_Group2'
    boplgn_Group3 = 'boplgn_Group3'
    boplgn_Group4 = 'boplgn_Group4'

class BoPrintReceiptEnum(StrEnum):
    boprcAlways = 'boprcAlways'
    boprcNo = 'boprcNo'
    boprcOnlyWhenAdding = 'boprcOnlyWhenAdding'

class BoProcurementMethod(StrEnum):
    bom_Buy = 'bom_Buy'
    bom_Make = 'bom_Make'

class BoProductSources(StrEnum):
    bps_PurchasedFromDomVendor = 'bps_PurchasedFromDomVendor'
    bps_ImportedByCompany = 'bps_ImportedByCompany'
    bps_ImportedGoodsPurchasedFromDomVendor = 'bps_ImportedGoodsPurchasedFromDomVendor'
    bps_ProducedByCompany = 'bps_ProducedByCompany'

class BoProductionOrderOriginEnum(StrEnum):
    bopooManual = 'bopooManual'
    bopooMRP = 'bopooMRP'
    bopooSalesOrder = 'bopooSalesOrder'
    bopooProductionOrder = 'bopooProductionOrder'

class BoProductionOrderStatusEnum(StrEnum):
    boposPlanned = 'boposPlanned'
    boposReleased = 'boposReleased'
    boposClosed = 'boposClosed'
    boposCancelled = 'boposCancelled'

class BoProductionOrderTypeEnum(StrEnum):
    bopotStandard = 'bopotStandard'
    bopotSpecial = 'bopotSpecial'
    bopotDisassembly = 'bopotDisassembly'

class BoQueryTypeEnum(StrEnum):
    qtRegular = 'qtRegular'
    qtWizard = 'qtWizard'

class BoRcptCredTypes(StrEnum):
    cr_Regular = 'cr_Regular'
    cr_Telephone = 'cr_Telephone'
    cr_InternetTransaction = 'cr_InternetTransaction'

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

class BoRcptTypes(StrEnum):
    rCustomer = 'rCustomer'
    rAccount = 'rAccount'
    rSupplier = 'rSupplier'

class BoRemindUnits(StrEnum):
    reu_Days = 'reu_Days'
    reu_Weeks = 'reu_Weeks'
    reu_Month = 'reu_Month'

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

class BoResolutionUnits(StrEnum):
    rsu_Days = 'rsu_Days'
    rsu_Hours = 'rsu_Hours'

class BoResponseUnit(StrEnum):
    boru_Day = 'boru_Day'
    boru_Hour = 'boru_Hour'

class BoRoleInTeam(StrEnum):
    borit_Leader = 'borit_Leader'
    borit_Member = 'borit_Member'

class BoRoundingMethod(StrEnum):
    borm_FixedEnding = 'borm_FixedEnding'
    borm_FixedInterval = 'borm_FixedInterval'
    borm_NoRounding = 'borm_NoRounding'
    borm_RoundToFullAmount = 'borm_RoundToFullAmount'
    borm_RoundToFullDecAmount = 'borm_RoundToFullDecAmount'
    borm_RoundToFullTensAmount = 'borm_RoundToFullTensAmount'

class BoRoundingRule(StrEnum):
    borrRoundDown = 'borrRoundDown'
    borrRoundOff = 'borrRoundOff'
    borrRoundUp = 'borrRoundUp'

class BoSalaryCostUnits(StrEnum):
    scu_Hour = 'scu_Hour'
    scu_Day = 'scu_Day'
    scu_Week = 'scu_Week'
    scu_Month = 'scu_Month'
    scu_Year = 'scu_Year'
    scu_Semimonthly = 'scu_Semimonthly'
    scu_Biweekly = 'scu_Biweekly'

class BoSerialNumberStatus(StrEnum):
    sns_Active = 'sns_Active'
    sns_Returned = 'sns_Returned'
    sns_Terminated = 'sns_Terminated'
    sns_Loaned = 'sns_Loaned'
    sns_InLab = 'sns_InLab'

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

class BoSeriesTypeEnum(StrEnum):
    stDocument = 'stDocument'
    stBusinessPartner = 'stBusinessPartner'
    stItem = 'stItem'
    stResource = 'stResource'

class BoServicePaymentMethods(StrEnum):
    spmAccreditedToBankAccount = 'spmAccreditedToBankAccount'
    spmBankTransfer = 'spmBankTransfer'
    spmOther = 'spmOther'

class BoServiceSupplyMethods(StrEnum):
    ssmImmediate = 'ssmImmediate'
    ssmToMoreResumptions = 'ssmToMoreResumptions'

class BoServiceTypes(StrEnum):
    bst_Regular = 'bst_Regular'
    bst_Warranty = 'bst_Warranty'

class BoSoClosedInTypes(StrEnum):
    sos_Months = 'sos_Months'
    sos_Weeks = 'sos_Weeks'
    sos_Days = 'sos_Days'

class BoSoOsStatus(StrEnum):
    sos_Open = 'sos_Open'
    sos_Missed = 'sos_Missed'
    sos_Sold = 'sos_Sold'

class BoSoStatus(StrEnum):
    so_Open = 'so_Open'
    so_Closed = 'so_Closed'

class BoSortTypeEnum(StrEnum):
    rlstAlpha = 'rlstAlpha'
    rlstNumeric = 'rlstNumeric'
    rlstMoney = 'rlstMoney'
    rlstDate = 'rlstDate'

class BoStatus(StrEnum):
    bost_Open = 'bost_Open'
    bost_Close = 'bost_Close'
    bost_Paid = 'bost_Paid'
    bost_Delivered = 'bost_Delivered'

class BoStckTrnDir(StrEnum):
    bos_TransferToTechnician = 'bos_TransferToTechnician'
    bos_TransferFromTechnician = 'bos_TransferFromTechnician'

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

class BoSvcCallPriorities(StrEnum):
    scp_Low = 'scp_Low'
    scp_Medium = 'scp_Medium'
    scp_High = 'scp_High'

class BoSvcContractStatus(StrEnum):
    scs_Approved = 'scs_Approved'
    scs_Frozen = 'scs_Frozen'
    scs_Draft = 'scs_Draft'
    scs_Terminated = 'scs_Terminated'

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

class BoSvcExpPartTypes(StrEnum):
    sep_Inventory = 'sep_Inventory'
    sep_NonInventory = 'sep_NonInventory'

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

class BoTCDDocumentTypeEnum(StrEnum):
    tcddtItem = 'tcddtItem'
    tcddtService = 'tcddtService'
    tcddtItemAndService = 'tcddtItemAndService'

class BoTaxInvoiceTypes(StrEnum):
    botit_AlterationCorrectionInvoice = 'botit_AlterationCorrectionInvoice'
    botit_AlterationInvoice = 'botit_AlterationInvoice'
    botit_CorrectionInvoice = 'botit_CorrectionInvoice'
    botit_Invoice = 'botit_Invoice'
    botit_JournalEntry = 'botit_JournalEntry'
    botit_Payment = 'botit_Payment'

class BoTaxOnInstallmentsTypeEnum(StrEnum):
    toiProportionally = 'toiProportionally'
    toiTaxInFirst = 'toiTaxInFirst'
    toiTaxInFirstOnly = 'toiTaxInFirstOnly'

class BoTaxPostAccEnum(StrEnum):
    tpa_Default = 'tpa_Default'
    tpa_SalesTaxAccount = 'tpa_SalesTaxAccount'
    tpa_PurchaseTaxAccount = 'tpa_PurchaseTaxAccount'

class BoTaxPostingAccountTypeEnum(StrEnum):
    tpatEmpty = 'tpatEmpty'
    tpatSalesTaxAccount = 'tpatSalesTaxAccount'
    tpatPurchasingTaxAccount = 'tpatPurchasingTaxAccount'

class BoTaxRoundingRuleTypes(StrEnum):
    trr_RoundDown = 'trr_RoundDown'
    trr_RoundUp = 'trr_RoundUp'
    trr_RoundOff = 'trr_RoundOff'
    trr_CompanyDefault = 'trr_CompanyDefault'

class BoTaxTypes(StrEnum):
    tt_Yes = 'tt_Yes'
    tt_No = 'tt_No'
    tt_UseTax = 'tt_UseTax'
    tt_OffsetTax = 'tt_OffsetTax'

class BoTimeTemplate(StrEnum):
    tt_24H = 'tt_24H'
    tt_12H = 'tt_12H'

class BoTransactionTypeEnum(StrEnum):
    botrntComplete = 'botrntComplete'
    botrntReject = 'botrntReject'

class BoUDOObjType(StrEnum):
    boud_Document = 'boud_Document'
    boud_MasterData = 'boud_MasterData'

class BoUPTOptions(StrEnum):
    bou_FullNone = 'bou_FullNone'
    bou_FullReadNone = 'bou_FullReadNone'

class BoUTBTableType(StrEnum):
    bott_Document = 'bott_Document'
    bott_DocumentLines = 'bott_DocumentLines'
    bott_MasterData = 'bott_MasterData'
    bott_MasterDataLines = 'bott_MasterDataLines'
    bott_NoObject = 'bott_NoObject'
    bott_NoObjectAutoIncrement = 'bott_NoObjectAutoIncrement'

class BoUniqueSerialNumber(StrEnum):
    usn_None = 'usn_None'
    usn_MfrSerialNumber = 'usn_MfrSerialNumber'
    usn_SerialNumber = 'usn_SerialNumber'
    usn_LotNumber = 'usn_LotNumber'

class BoUpdateAllocationEnum(StrEnum):
    bouaManual = 'bouaManual'
    bouaCalculated = 'bouaCalculated'
    bouaRunCalculation = 'bouaRunCalculation'

class BoUserGroup(StrEnum):
    ug_Regular = 'ug_Regular'
    ug_Deleted = 'ug_Deleted'

class BoVatCategoryEnum(StrEnum):
    bovcInputTax = 'bovcInputTax'
    bovcOutputTax = 'bovcOutputTax'

class BoVatStatus(StrEnum):
    vExempted = 'vExempted'
    vLiable = 'vLiable'
    vEC = 'vEC'

class BoVerticalAlignmentEnum(StrEnum):
    rlvaTop = 'rlvaTop'
    rlvaBottom = 'rlvaBottom'
    rlvaCentralized = 'rlvaCentralized'

class BoWeekEnum(StrEnum):
    Sunday = 'Sunday'
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'

class BoWeekNoRuleEnum(StrEnum):
    fromJanFirst = 'fromJanFirst'
    fromFirstFourDayWeek = 'fromFirstFourDayWeek'
    fromFirstFullWeek = 'fromFirstFullWeek'

class BoWorkOrderStat(StrEnum):
    wk_ProductComplete = 'wk_ProductComplete'
    wk_WorkInstruction = 'wk_WorkInstruction'
    wk_WorkOrder = 'wk_WorkOrder'

class BoYesNoEnum(StrEnum):
    tNO = 'tNO'
    tYES = 'tYES'

class BoYesNoNoneEnum(StrEnum):
    boNO = 'boNO'
    boYES = 'boYES'
    boNONE = 'boNONE'

class BrazilMultiIndexerTypes(StrEnum):
    bmitInvalid = 'bmitInvalid'
    bmitIncomeNature = 'bmitIncomeNature'

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

class CalculateInterestMethodEnum(StrEnum):
    cimOnRemainingAmount = 'cimOnRemainingAmount'
    cimOnOriginalSum = 'cimOnOriginalSum'

class CalculationBaseEnum(StrEnum):
    cbYearly = 'cbYearly'
    cbMonthly = 'cbMonthly'

class CallMessageStatusEnum(StrEnum):
    cmsUnread = 'cmsUnread'
    cmsRead = 'cmsRead'

class CallMessageTypeEnum(StrEnum):
    cmtInformation = 'cmtInformation'
    cmtWarning = 'cmtWarning'
    cmtError = 'cmtError'

class CampaignAssignToEnum(StrEnum):
    catUser = 'catUser'
    catEmployee = 'catEmployee'

class CampaignBPStatusEnum(StrEnum):
    cbpsActive = 'cbpsActive'
    cbpsInactive = 'cbpsInactive'

class CampaignItemTypeEnum(StrEnum):
    citItems = 'citItems'
    citLabel = 'citLabel'
    citTravel = 'citTravel'

class CampaignStatusEnum(StrEnum):
    csOpen = 'csOpen'
    csFinished = 'csFinished'
    csCanceled = 'csCanceled'

class CampaignTypeEnum(StrEnum):
    ctEmail = 'ctEmail'
    ctMail = 'ctMail'
    ctFax = 'ctFax'
    ctPhoneCall = 'ctPhoneCall'
    ctMeeting = 'ctMeeting'
    ctSMS = 'ctSMS'
    ctWeb = 'ctWeb'
    ctOthers = 'ctOthers'

class CancelStatusEnum(StrEnum):
    csYes = 'csYes'
    csNo = 'csNo'
    csCancellation = 'csCancellation'

class CardOrAccountEnum(StrEnum):
    coaCard = 'coaCard'
    coaAccount = 'coaAccount'

class ClosingOptionEnum(StrEnum):
    coByCurrentSystemDate = 'coByCurrentSystemDate'
    coByOriginalDocumentDate = 'coByOriginalDocumentDate'
    coBySpecifiedDate = 'coBySpecifiedDate'

class CommissionTradeTypeEnum(StrEnum):
    ct_Empty = 'ct_Empty'
    ct_SalesAgent = 'ct_SalesAgent'
    ct_PurchaseAgent = 'ct_PurchaseAgent'
    ct_Consignor = 'ct_Consignor'

class ContractSequenceEnum(StrEnum):
    cs_Monthly = 'cs_Monthly'
    cs_Quarterly = 'cs_Quarterly'
    cs_SemiAnnually = 'cs_SemiAnnually'
    cs_Yearly = 'cs_Yearly'

class CounterTypeEnum(StrEnum):
    ctUser = 'ctUser'
    ctEmployee = 'ctEmployee'

class CountingDocumentStatusEnum(StrEnum):
    cdsOpen = 'cdsOpen'
    cdsClosed = 'cdsClosed'

class CountingLineStatusEnum(StrEnum):
    clsOpen = 'clsOpen'
    clsClosed = 'clsClosed'

class CountingTypeEnum(StrEnum):
    ctSingleCounter = 'ctSingleCounter'
    ctMultipleCounters = 'ctMultipleCounters'

class CreateMethodEnum(StrEnum):
    cmManual = 'cmManual'
    cmAutomatic = 'cmAutomatic'

class CreditOrDebitEnum(StrEnum):
    codCredit = 'codCredit'
    codDebit = 'codDebit'

class CurrenciesDecimalsEnum(StrEnum):
    cd1Digit = 'cd1Digit'
    cd2Digits = 'cd2Digits'
    cd3Digits = 'cd3Digits'
    cd4Digits = 'cd4Digits'
    cd5Digits = 'cd5Digits'
    cd6Digits = 'cd6Digits'
    cdDefault = 'cdDefault'
    cdWithoutDecimals = 'cdWithoutDecimals'

class CycleCountDeterminationCycleByEnum(StrEnum):
    ccdcbItemGroup = 'ccdcbItemGroup'
    ccdcbWarehouseSublevel1 = 'ccdcbWarehouseSublevel1'
    ccdcbWarehouseSublevel2 = 'ccdcbWarehouseSublevel2'
    ccdcbWarehouseSublevel3 = 'ccdcbWarehouseSublevel3'
    ccdcbWarehouseSublevel4 = 'ccdcbWarehouseSublevel4'

class DataPrivacyProtectionEnum(StrEnum):
    dpp_None = 'dpp_None'
    dpp_Erased = 'dpp_Erased'
    dpp_Blocked = 'dpp_Blocked'
    dpp_Unblocked = 'dpp_Unblocked'

class DataSensitiveStatusEnum(StrEnum):
    dss_FieldNotSentive = 'dss_FieldNotSentive'
    dss_DataSubjectNotNaturalPerson = 'dss_DataSubjectNotNaturalPerson'
    dss_DataSubjectIsBlockedOrErased = 'dss_DataSubjectIsBlockedOrErased'
    dss_DataIsSensitive = 'dss_DataIsSensitive'
    dss_Error = 'dss_Error'
    dss_TransactionIsErased = 'dss_TransactionIsErased'

class DepreciationCalculationBaseEnum(StrEnum):
    dcbAcquisitionValue = 'dcbAcquisitionValue'
    dcbNetBookValue = 'dcbNetBookValue'

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

class DepreciationRoundingMethodEnum(StrEnum):
    drmTruncate = 'drmTruncate'
    drmRoundUp = 'drmRoundUp'
    drmRoundDown = 'drmRoundDown'

class DirectDebitTypeEnum(StrEnum):
    ddtCORE = 'ddtCORE'
    ddtB2B = 'ddtB2B'
    ddtCOR1 = 'ddtCOR1'

class DiscountGroupBaseObjectEnum(StrEnum):
    dgboNone = 'dgboNone'
    dgboItemGroups = 'dgboItemGroups'
    dgboItemProperties = 'dgboItemProperties'
    dgboManufacturer = 'dgboManufacturer'
    dgboItems = 'dgboItems'

class DiscountGroupDiscountTypeEnum(StrEnum):
    dgdt_Fixed = 'dgdt_Fixed'
    dgdt_Variable = 'dgdt_Variable'

class DiscountGroupRelationsEnum(StrEnum):
    dgrLowestDiscount = 'dgrLowestDiscount'
    dgrHighestDiscount = 'dgrHighestDiscount'
    dgrAverageDiscount = 'dgrAverageDiscount'
    dgrDiscountTotals = 'dgrDiscountTotals'
    dgrMultipliedDiscount = 'dgrMultipliedDiscount'

class DiscountGroupTypeEnum(StrEnum):
    dgt_AllBPs = 'dgt_AllBPs'
    dgt_CustomerGroup = 'dgt_CustomerGroup'
    dgt_VendorGroup = 'dgt_VendorGroup'
    dgt_SpecificBP = 'dgt_SpecificBP'

class DisplayBatchQtyUoMByEnum(StrEnum):
    dispBatchQtyByDocRowUoM = 'dispBatchQtyByDocRowUoM'
    dispBatchQtyByInventoryUoM = 'dispBatchQtyByInventoryUoM'

class DocumentAuthorizationStatusEnum(StrEnum):
    dasWithout = 'dasWithout'
    dasPending = 'dasPending'
    dasApproved = 'dasApproved'
    dasRejected = 'dasRejected'
    dasGenerated = 'dasGenerated'
    dasGeneratedbyAuthorizer = 'dasGeneratedbyAuthorizer'
    dasCancelled = 'dasCancelled'

class DocumentDeliveryTypeEnum(StrEnum):
    ddtNoneSeleted = 'ddtNoneSeleted'
    ddtCreateOnlineDocument = 'ddtCreateOnlineDocument'
    ddtPostToAribaNetwork = 'ddtPostToAribaNetwork'

class DocumentObjectTypeEnum(StrEnum):
    dc_ArInvoice = 'dc_ArInvoice'
    dc_Delivery = 'dc_Delivery'
    dc_GoodsReturn = 'dc_GoodsReturn'
    dc_InventoryTransfer = 'dc_InventoryTransfer'

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

class DocumentRemarksIncludeTypeEnum(StrEnum):
    driBaseDocumentNumber = 'driBaseDocumentNumber'
    driBPReferenceNumber = 'driBPReferenceNumber'
    driManualRemarksOnly = 'driManualRemarksOnly'

class DomesticBankAccountValidationEnum(StrEnum):
    dbavNone = 'dbavNone'
    dbavBelgium = 'dbavBelgium'
    dbavSpain = 'dbavSpain'
    dbavFrance = 'dbavFrance'
    dbavItaly = 'dbavItaly'
    dbavNetherlands = 'dbavNetherlands'
    dbavPortugal = 'dbavPortugal'

class DownPaymentTypeEnum(StrEnum):
    dptRequest = 'dptRequest'
    dptInvoice = 'dptInvoice'

class DrawingMethodEnum(StrEnum):
    dmAll = 'dmAll'
    dmNone = 'dmNone'
    dmQuantity = 'dmQuantity'
    dmTotal = 'dmTotal'

class DueDateTypesEnum(StrEnum):
    ddtAfterTimePeriod = 'ddtAfterTimePeriod'
    ddtByDates = 'ddtByDates'

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

class ECDPostingTypeEnum(StrEnum):
    ecdNormal = 'ecdNormal'
    ecdStatement = 'ecdStatement'

class EDocGenerationTypeEnum(StrEnum):
    edocGenerate = 'edocGenerate'
    edocGenerateLater = 'edocGenerateLater'
    edocNotRelevant = 'edocNotRelevant'

class EDocStatusEnum(StrEnum):
    edoc_New = 'edoc_New'
    edoc_Pending = 'edoc_Pending'
    edoc_Sent = 'edoc_Sent'
    edoc_Error = 'edoc_Error'
    edoc_Ok = 'edoc_Ok'

class EDocTypeEnum(StrEnum):
    edocFE = 'edocFE'
    edocFCE = 'edocFCE'

class EWBSupplyTypeEnum(StrEnum):
    ewb_st_Inward = 'ewb_st_Inward'
    ewb_st_Outward = 'ewb_st_Outward'

class EWBTransactionTypeEnum(StrEnum):
    ewb_tt_Regular = 'ewb_tt_Regular'
    ewb_tt_BillToShipTo = 'ewb_tt_BillToShipTo'
    ewb_tt_BillFromDispathFrom = 'ewb_tt_BillFromDispathFrom'
    ewb_tt_CombinationOfBillAndShip = 'ewb_tt_CombinationOfBillAndShip'

class EffectivePriceEnum(StrEnum):
    epDefaultPriority = 'epDefaultPriority'
    epLowestPrice = 'epLowestPrice'
    epHighestPrice = 'epHighestPrice'

class ElecCommStatusEnum(StrEnum):
    ecsApproved = 'ecsApproved'
    ecsPendingApproval = 'ecsPendingApproval'
    ecsRejected = 'ecsRejected'

class ElectronicDocGenTypeEnum(StrEnum):
    edgt_NotRelevant = 'edgt_NotRelevant'
    edgt_Generate = 'edgt_Generate'
    edgt_GenerateLater = 'edgt_GenerateLater'

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

class ElectronicDocumentAuthorityProcessEnum(StrEnum):
    edapNone = 'edapNone'
    edapApproval = 'edapApproval'
    edapRejection = 'edapRejection'

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

class ElectronicDocumentEntryPeriodTypeEnum(StrEnum):
    edeptIgnore = 'edeptIgnore'
    edeptYear = 'edeptYear'
    edeptQuarter = 'edeptQuarter'
    edeptMonth = 'edeptMonth'
    edeptDateRange = 'edeptDateRange'

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

class EmployeeExemptionUnitEnum(StrEnum):
    eeu_None = 'eeu_None'
    eeu_Yearly = 'eeu_Yearly'
    eeu_Monthly = 'eeu_Monthly'
    eeu_Weekly = 'eeu_Weekly'
    eeu_Daily = 'eeu_Daily'

class EmployeePaymentMethodEnum(StrEnum):
    epm_None = 'epm_None'
    epm_BankTransfer = 'epm_BankTransfer'

class EmployeeTransferProcessingStatusEnum(StrEnum):
    etps_New = 'etps_New'
    etps_Sent = 'etps_Sent'
    etps_Accepted = 'etps_Accepted'
    etps_Error = 'etps_Error'

class EmployeeTransferStatusEnum(StrEnum):
    ets_New = 'ets_New'
    ets_Processing = 'ets_Processing'
    ets_Sent = 'ets_Sent'
    ets_Received = 'ets_Received'
    ets_Accepted = 'ets_Accepted'
    ets_Error = 'ets_Error'

class EndTypeEnum(StrEnum):
    etNoEndDate = 'etNoEndDate'
    etByCounter = 'etByCounter'
    etByDate = 'etByDate'

class ExchangeRateSelectEnum(StrEnum):
    ierFromInovice = 'ierFromInovice'
    ierCurrentRate = 'ierCurrentRate'

class ExemptionMaxAmountValidationTypeEnum(StrEnum):
    emaIndividual = 'emaIndividual'
    emaAccumulated = 'emaAccumulated'

class ExternalCallStatusEnum(StrEnum):
    ecsNew = 'ecsNew'
    ecsInProcess = 'ecsInProcess'
    ecsCompleted = 'ecsCompleted'
    ecsConfirmed = 'ecsConfirmed'
    ecsFailed = 'ecsFailed'

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

class FormattedSearchByFieldEnum(StrEnum):
    fsbfWhenExitingAlteredColumn = 'fsbfWhenExitingAlteredColumn'
    fsbfWhenFieldChanges = 'fsbfWhenFieldChanges'
    fsbfWhenColumnValueChanges = 'fsbfWhenColumnValueChanges'

class FreightTypeEnum(StrEnum):
    ftShipping = 'ftShipping'
    ftInsurance = 'ftInsurance'
    ftOther = 'ftOther'
    ftSpecial = 'ftSpecial'

class FreightTypeForBolloEnum(StrEnum):
    ftStandard = 'ftStandard'
    ftBollo = 'ftBollo'

class GSTTaxCategoryEnum(StrEnum):
    gtc_Regular = 'gtc_Regular'
    gtc_NilRated = 'gtc_NilRated'
    gtc_Exempt = 'gtc_Exempt'

class GSTTransactionTypeEnum(StrEnum):
    gsttrantyp_BillOfSupply = 'gsttrantyp_BillOfSupply'
    gsttrantyp_GSTTaxInvoice = 'gsttrantyp_GSTTaxInvoice'
    gsttrantyp_GSTDebitMemo = 'gsttrantyp_GSTDebitMemo'

class GTSResponseToExceedingEnum(StrEnum):
    Block = 'Block'
    Split = 'Split'

class GeneratedAssetStatusEnum(StrEnum):
    gasOpen = 'gasOpen'
    gasClosed = 'gasClosed'

class GetGLAccountByEnum(StrEnum):
    gglab_General = 'gglab_General'
    gglab_Warehouse = 'gglab_Warehouse'
    gglab_ItemGroup = 'gglab_ItemGroup'

class GovPayCodePeriodicityEnum(StrEnum):
    gpcpMonth = 'gpcpMonth'
    gpcpQuarter = 'gpcpQuarter'
    gpcpHalfMonth = 'gpcpHalfMonth'
    gpcpTenDays = 'gpcpTenDays'

class GovPayCodeSPEDCategoryEnum(StrEnum):
    gpcscICMS = 'gpcscICMS'
    gpcscICMSST = 'gpcscICMSST'
    gpcscIPI = 'gpcscIPI'
    gpcscISS = 'gpcscISS'
    gpcscPIS = 'gpcscPIS'
    gpcscCOFINS = 'gpcscCOFINS'
    gpcsPISST = 'gpcsPISST'
    gpcsCONFINSST = 'gpcsCONFINSST'

class GroupingMethodEnum(StrEnum):
    gmPerInvoice = 'gmPerInvoice'
    gmPerDunningLevel = 'gmPerDunningLevel'
    gmPerBP = 'gmPerBP'

class IdentificationCodeTypeEnum(StrEnum):
    idctOrder = 'idctOrder'
    idctDelivery = 'idctDelivery'
    idctInvoice = 'idctInvoice'
    idctCreditNote = 'idctCreditNote'
    idctStandardItemTypeIdentification = 'idctStandardItemTypeIdentification'
    idctItemCommodityClassification = 'idctItemCommodityClassification'

class ImportFieldTypeEnum(StrEnum):
    iftInvalid = 'iftInvalid'
    iftFederalTaxID = 'iftFederalTaxID'
    iftAdditionalID = 'iftAdditionalID'
    iftUnifiedFederalTaxID = 'iftUnifiedFederalTaxID'
    iftCNPJ = 'iftCNPJ'
    iftAliasName = 'iftAliasName'
    iftIBAN = 'iftIBAN'
    iftBPName = 'iftBPName'

class ImportOrExportTypeEnum(StrEnum):
    et_IpmortsOrExports = 'et_IpmortsOrExports'
    et_SEZ_Developer = 'et_SEZ_Developer'
    et_SEZ_Unit = 'et_SEZ_Unit'
    et_Deemed_ImportsOrExports = 'et_Deemed_ImportsOrExports'

class InstallmentPaymentsPossiblityEnum(StrEnum):
    ippCr = 'ippCr'
    ippNo = 'ippNo'
    ippRd = 'ippRd'
    ippYes = 'ippYes'

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

class IntrastatConfigurationTriangDealEnum(StrEnum):
    enNone = 'enNone'
    enType11 = 'enType11'
    enType21 = 'enType21'
    enType31 = 'enType31'

class InvBaseDocTypeEnum(StrEnum):
    Default = 'Default'
    Empty = 'Empty'
    PurchaseDeliveryNotes = 'PurchaseDeliveryNotes'
    InventoryGeneralEntry = 'InventoryGeneralEntry'
    WarehouseTransfers = 'WarehouseTransfers'
    InventoryTransferRequest = 'InventoryTransferRequest'

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

class InventoryCycleTypeEnum(StrEnum):
    ictCylce = 'ictCylce'
    ictMRP = 'ictMRP'

class InventoryOpeningBalancePriceSourceEnum(StrEnum):
    iobpsByPriceList = 'iobpsByPriceList'
    iobpsLastEvaluatedPrice = 'iobpsLastEvaluatedPrice'
    iobpsItemCost = 'iobpsItemCost'

class InventoryPostingCopyOptionEnum(StrEnum):
    ipcoNoCountersDiff = 'ipcoNoCountersDiff'
    ipcoIndividual1CountedQuantity = 'ipcoIndividual1CountedQuantity'
    ipcoIndividual2CountedQuantity = 'ipcoIndividual2CountedQuantity'
    ipcoIndividual3CountedQuantity = 'ipcoIndividual3CountedQuantity'
    ipcoIndividual4CountedQuantity = 'ipcoIndividual4CountedQuantity'
    ipcoIndividual5CountedQuantity = 'ipcoIndividual5CountedQuantity'
    ipcoTeamCountedQuantity = 'ipcoTeamCountedQuantity'

class InventoryPostingPriceSourceEnum(StrEnum):
    ippsByPriceList = 'ippsByPriceList'
    ippsLastEvaluatedPrice = 'ippsLastEvaluatedPrice'
    ippsItemCost = 'ippsItemCost'

class IssuePrimarilyByEnum(StrEnum):
    ipbSerialAndBatchNumbers = 'ipbSerialAndBatchNumbers'
    ipbBinLocations = 'ipbBinLocations'

class ItemClassEnum(StrEnum):
    itcService = 'itcService'
    itcMaterial = 'itcMaterial'

class ItemTypeEnum(StrEnum):
    itItems = 'itItems'
    itLabor = 'itLabor'
    itTravel = 'itTravel'
    itFixedAssets = 'itFixedAssets'

class ItemUoMTypeEnum(StrEnum):
    iutPurchasing = 'iutPurchasing'
    iutSales = 'iutSales'
    iutInventory = 'iutInventory'

class KPITypeEnum(StrEnum):
    asSingle = 'asSingle'
    asQuarterly = 'asQuarterly'
    asMonthly = 'asMonthly'
    asMultiple = 'asMultiple'

class LCCostTypeEnum(StrEnum):
    asFixedCosts = 'asFixedCosts'
    asVariableCosts = 'asVariableCosts'
    asLegalCosts = 'asLegalCosts'

class LandedCostAllocationByEnum(StrEnum):
    asCashValueBeforeCustoms = 'asCashValueBeforeCustoms'
    asCashValueAfterCustoms = 'asCashValueAfterCustoms'
    asQuantity = 'asQuantity'
    asWeight = 'asWeight'
    asVolume = 'asVolume'
    asEqual = 'asEqual'
    asLegalCost = 'asLegalCost'

class LandedCostBaseDocumentTypeEnum(StrEnum):
    asDefault = 'asDefault'
    asEmpty = 'asEmpty'
    asGoodsReceiptPO = 'asGoodsReceiptPO'
    asLandedCosts = 'asLandedCosts'
    asPurchaseInvoice = 'asPurchaseInvoice'

class LandedCostCostCategoryEnum(StrEnum):
    lccc_CustomsVAT = 'lccc_CustomsVAT'
    lccc_ExciseCost = 'lccc_ExciseCost'
    lccc_CustomsDuty = 'lccc_CustomsDuty'

class LandedCostDocStatusEnum(StrEnum):
    lcOpen = 'lcOpen'
    lcClosed = 'lcClosed'

class LegalDataLineTypeEnum(StrEnum):
    ldlt_DocumentTotal = 'ldlt_DocumentTotal'
    ldlt_TaxPerLine = 'ldlt_TaxPerLine'
    ldlt_TotalTax = 'ldlt_TotalTax'

class LicenseTypeEnum(StrEnum):
    lkIdirect = 'lkIdirect'
    lkSOAIndirect = 'lkSOAIndirect'
    lkSOA = 'lkSOA'
    lkB1iIndirect = 'lkB1iIndirect'
    lkB1i = 'lkB1i'

class LicenseUpdateTypeEnum(StrEnum):
    ultAssign = 'ultAssign'
    ultRemove = 'ultRemove'

class LineStatusTypeEnum(StrEnum):
    lst_Open = 'lst_Open'
    lst_Closed = 'lst_Closed'

class LineTypeEnum(StrEnum):
    ltDocument = 'ltDocument'
    ltRounding = 'ltRounding'
    ltVat = 'ltVat'

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

class LinkedDocTypeEnum(StrEnum):
    ldtEmptyLink = 'ldtEmptyLink'
    ldtSalesOpportunitiesLink = 'ldtSalesOpportunitiesLink'
    ldtSalesQuotationsLink = 'ldtSalesQuotationsLink'
    ldtSalesOrdersLink = 'ldtSalesOrdersLink'
    ldtDeliveriesLink = 'ldtDeliveriesLink'
    ldtARInvoicesLink = 'ldtARInvoicesLink'

class LogonMethodEnum(StrEnum):
    lmBOneIntegrationFramework = 'lmBOneIntegrationFramework'
    lmStandardLogon = 'lmStandardLogon'
    lmNoControl = 'lmNoControl'

class MobileAddonSettingTypeEnum(StrEnum):
    mastModule = 'mastModule'
    mastHome = 'mastHome'

class MobileAppReportChoiceEnum(StrEnum):
    marSystemReport = 'marSystemReport'
    marCustomizedReport = 'marCustomizedReport'

class MultipleCounterRoleEnum(StrEnum):
    mcrTeamCounter = 'mcrTeamCounter'
    mcrIndividualCounter = 'mcrIndividualCounter'

class OperationCode347Enum(StrEnum):
    ocGoodsOrServiciesAcquisitions = 'ocGoodsOrServiciesAcquisitions'
    ocPublicEntitiesAcquisitions = 'ocPublicEntitiesAcquisitions'
    ocTravelAgenciesPurchases = 'ocTravelAgenciesPurchases'
    ocSalesOrServicesRevenues = 'ocSalesOrServicesRevenues'
    ocPublicSubsidies = 'ocPublicSubsidies'
    ocTravelAgenciesSales = 'ocTravelAgenciesSales'

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

class OpportunityTypeEnum(StrEnum):
    boOpSales = 'boOpSales'
    boOpPurchasing = 'boOpPurchasing'

class PMCategorizeTypeEnum(StrEnum):
    pm_cat_Ignore = 'pm_cat_Ignore'
    pm_cat_OpenAmountAP = 'pm_cat_OpenAmountAP'
    pm_cat_OpenAmountAR = 'pm_cat_OpenAmountAR'
    pm_cat_InvoicedAP = 'pm_cat_InvoicedAP'
    pm_cat_InvoicedAR = 'pm_cat_InvoicedAR'

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

class PMOperationTypeEnum(StrEnum):
    pm_op_Ignore = 'pm_op_Ignore'
    pm_op_Add = 'pm_op_Add'
    pm_op_Subtract = 'pm_op_Subtract'

class PaymentInvoiceTypeEnum(StrEnum):
    itARInvoice = 'itARInvoice'
    itARDownPaymentInvoice = 'itARDownPaymentInvoice'

class PaymentMeansTypeEnum(StrEnum):
    pmtNotAssigned = 'pmtNotAssigned'
    pmtChecks = 'pmtChecks'
    pmtBankTransfer = 'pmtBankTransfer'
    pmtCash = 'pmtCash'
    pmtCreditCard = 'pmtCreditCard'

class PaymentRunExportRowTypeEnum(StrEnum):
    prtGeneral = 'prtGeneral'
    prtPayOnAccount = 'prtPayOnAccount'
    prtPayToAccount = 'prtPayToAccount'

class PaymentsAuthorizationStatusEnum(StrEnum):
    pasWithout = 'pasWithout'
    pasPending = 'pasPending'
    pasApproved = 'pasApproved'
    pasRejected = 'pasRejected'
    pasGenerated = 'pasGenerated'
    pasGeneratedbyAuthorizer = 'pasGeneratedbyAuthorizer'
    pasCancelled = 'pasCancelled'

class PeriodStatusEnum(StrEnum):
    ltUnlocked = 'ltUnlocked'
    ltUnlockedExceptSales = 'ltUnlockedExceptSales'
    ltPeriodClosing = 'ltPeriodClosing'
    ltLocked = 'ltLocked'

class PostingMethodEnum(StrEnum):
    pmGLAccountBankAccount = 'pmGLAccountBankAccount'
    pmBussinessPartnerBankAccount = 'pmBussinessPartnerBankAccount'
    pmInterimAccountBankAccount = 'pmInterimAccountBankAccount'
    pmExternalReconciliation = 'pmExternalReconciliation'
    pmIgnore = 'pmIgnore'

class PostingOfDepreciationEnum(StrEnum):
    podDirectPosting = 'podDirectPosting'
    podIndirectPosting = 'podIndirectPosting'

class PriceModeDocumentEnum(StrEnum):
    pmdNet = 'pmdNet'
    pmdGross = 'pmdGross'
    pmdNetAndGross = 'pmdNetAndGross'

class PriceModeEnum(StrEnum):
    pmNet = 'pmNet'
    pmGross = 'pmGross'

class PriceProceedMethodEnum(StrEnum):
    ppmRemove = 'ppmRemove'
    ppmUpdate = 'ppmUpdate'
    ppmKeepCorresponding = 'ppmKeepCorresponding'
    ppmKeepAll = 'ppmKeepAll'

class PrintOnEnum(StrEnum):
    poBlankPaper = 'poBlankPaper'
    poDefault = 'poDefault'
    poOverflowBlankPaper = 'poOverflowBlankPaper'
    poOverflowCheckStock = 'poOverflowCheckStock'

class PrintStatusEnum(StrEnum):
    psNo = 'psNo'
    psYes = 'psYes'
    psAmended = 'psAmended'

class ProductionItemType(StrEnum):
    pit_Item = 'pit_Item'
    pit_Resource = 'pit_Resource'
    pit_Text = 'pit_Text'

class ProjectStatusTypeEnum(StrEnum):
    pst_Started = 'pst_Started'
    pst_Paused = 'pst_Paused'
    pst_Stopped = 'pst_Stopped'
    pst_Finished = 'pst_Finished'
    pst_Canceled = 'pst_Canceled'

class ProjectTypeEnum(StrEnum):
    pt_External = 'pt_External'
    pt_Internal = 'pt_Internal'

class RclRecurringExecutionHandlingEnum(StrEnum):
    rehStopOnError = 'rehStopOnError'
    rehSkipTransaction = 'rehSkipTransaction'

class RclRecurringTransactionStatusEnum(StrEnum):
    rtsNotExecuted = 'rtsNotExecuted'
    rtsExecuted = 'rtsExecuted'
    rtsRemoved = 'rtsRemoved'

class ReceivingBinLocationsMethodEnum(StrEnum):
    rblmBinLocationCodeOrder = 'rblmBinLocationCodeOrder'
    rblmAlternativeSortCodeOrder = 'rblmAlternativeSortCodeOrder'

class ReceivingUpToMethodEnum(StrEnum):
    rutmBothMaxQtyAndWeight = 'rutmBothMaxQtyAndWeight'
    rutmMaximumQty = 'rutmMaximumQty'
    rutmMaximumWeight = 'rutmMaximumWeight'

class RecipientTypeEnum(StrEnum):
    rtUser = 'rtUser'
    rtEmployee = 'rtEmployee'

class ReconSelectDateTypeEnum(StrEnum):
    rsdtPostDate = 'rsdtPostDate'
    rsdtDueDate = 'rsdtDueDate'
    rsdtDocDate = 'rsdtDocDate'

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

class ReconciliationAccountTypeEnum(StrEnum):
    rat_GLAccount = 'rat_GLAccount'
    rat_BusinessPartner = 'rat_BusinessPartner'

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

class RecurrencePatternEnum(StrEnum):
    rpNone = 'rpNone'
    rpDaily = 'rpDaily'
    rpWeekly = 'rpWeekly'
    rpMonthly = 'rpMonthly'
    rpAnnually = 'rpAnnually'

class RecurrenceSequenceEnum(StrEnum):
    rsFirst = 'rsFirst'
    rsSecond = 'rsSecond'
    rsThird = 'rsThird'
    rsFourth = 'rsFourth'
    rsLast = 'rsLast'

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

class RelatedDocumentTypeEnum(StrEnum):
    rdt_Payment = 'rdt_Payment'
    rdt_Reconciliation = 'rdt_Reconciliation'

class RepeatOptionEnum(StrEnum):
    roByDate = 'roByDate'
    roByWeekDay = 'roByWeekDay'

class Report349CodeListEnum(StrEnum):
    r349cA = 'r349cA'
    r349cE = 'r349cE'
    r349cEmpty = 'r349cEmpty'
    r349cH = 'r349cH'
    r349cI = 'r349cI'
    r349cM = 'r349cM'
    r349cS = 'r349cS'
    r349cT = 'r349cT'

class ReportLayoutCategoryEnum(StrEnum):
    rlcPLD = 'rlcPLD'
    rlcCrystal = 'rlcCrystal'
    rlcLegalList = 'rlcLegalList'
    rlcUserDefinedType = 'rlcUserDefinedType'

class ResidenceNumberTypeEnum(StrEnum):
    rntSpanishFiscalID = 'rntSpanishFiscalID'
    rntVATRegistrationNumber = 'rntVATRegistrationNumber'
    rntPassport = 'rntPassport'
    rntFiscalIDIssuedbytheResidenceCountry = 'rntFiscalIDIssuedbytheResidenceCountry'
    rntCertificateofFiscalResidence = 'rntCertificateofFiscalResidence'
    rntOtherDocument = 'rntOtherDocument'

class ResourceAllocationEnum(StrEnum):
    raOnStartDate = 'raOnStartDate'
    raOnEndDate = 'raOnEndDate'
    raStartDateForwards = 'raStartDateForwards'
    raEndDateBackwards = 'raEndDateBackwards'

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

class ResourceCapacityBaseTypeEnum(StrEnum):
    rcbtNone = 'rcbtNone'
    rcbtProductionOrder = 'rcbtProductionOrder'

class ResourceCapacityMemoSourceEnum(StrEnum):
    rcmsUnknown = 'rcmsUnknown'
    rcmsResourceCapacityForm = 'rcmsResourceCapacityForm'
    rcmsSetDailyInternalCapacitiesForm = 'rcmsSetDailyInternalCapacitiesForm'

class ResourceCapacityOwningTypeEnum(StrEnum):
    rcotNone = 'rcotNone'
    rcotProductionOrder = 'rcotProductionOrder'
    rcotIssueForProduction = 'rcotIssueForProduction'
    rcotReceiptFromProduction = 'rcotReceiptFromProduction'

class ResourceCapacityRevertedTypeEnum(StrEnum):
    rcrtNone = 'rcrtNone'
    rcrtIssueForProduction = 'rcrtIssueForProduction'

class ResourceCapacitySourceTypeEnum(StrEnum):
    rcstNone = 'rcstNone'
    rcstProductionOrder = 'rcstProductionOrder'
    rcstIssueForProduction = 'rcstIssueForProduction'
    rcstReceiptFromProduction = 'rcstReceiptFromProduction'

class ResourceCapacityTypeEnum(StrEnum):
    rctInternal = 'rctInternal'
    rctOrdered = 'rctOrdered'
    rctCommitted = 'rctCommitted'
    rctConsumed = 'rctConsumed'

class ResourceDailyCapacityWeekdayEnum(StrEnum):
    rdcwFirst = 'rdcwFirst'
    rdcwSecond = 'rdcwSecond'
    rdcwThird = 'rdcwThird'
    rdcwFourth = 'rdcwFourth'
    rdcwFifth = 'rdcwFifth'
    rdcwSixth = 'rdcwSixth'
    rdcwSeventh = 'rdcwSeventh'

class ResourceIssueMethodEnum(StrEnum):
    rimBackflush = 'rimBackflush'
    rimManual = 'rimManual'

class ResourceTypeEnum(StrEnum):
    rtMachine = 'rtMachine'
    rtLabor = 'rtLabor'
    rtOther = 'rtOther'

class RetirementMethodEnum(StrEnum):
    rmGross = 'rmGross'
    rmNet = 'rmNet'

class RetirementPeriodControlEnum(StrEnum):
    rpcProRataTemporis = 'rpcProRataTemporis'
    rpcHalfYearConvention = 'rpcHalfYearConvention'
    rpcOnlyAfterEndOfUsefulLife = 'rpcOnlyAfterEndOfUsefulLife'

class RetirementProRataTypeEnum(StrEnum):
    rprtExactlyDailyBase = 'rprtExactlyDailyBase'
    rprtLastDayOfPriorPeriod = 'rprtLastDayOfPriorPeriod'
    rprtLastDayOfCurrentPeriod = 'rprtLastDayOfCurrentPeriod'

class ReturnTypeEnum(StrEnum):
    rt26Q = 'rt26Q'
    rt27Q = 'rt27Q'
    rt27EQ = 'rt27EQ'

class RiskLevelTypeEnum(StrEnum):
    rlt_Low = 'rlt_Low'
    rlt_Medium = 'rlt_Medium'
    rlt_High = 'rlt_High'

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

class RoundingSysEnum(StrEnum):
    rsNoRounding = 'rsNoRounding'
    rsRoundToFiveHundredth = 'rsRoundToFiveHundredth'
    rsRoundToOne = 'rsRoundToOne'
    rsRoundToTen = 'rsRoundToTen'
    rsRoundToTenHundredth = 'rsRoundToTenHundredth'

class RoundingTypeEnum(StrEnum):
    rt_TruncatedAU = 'rt_TruncatedAU'
    rt_CommercialValues = 'rt_CommercialValues'
    rt_NoRounding = 'rt_NoRounding'

class SAFTProductTypeEnum(StrEnum):
    saftpt_Products = 'saftpt_Products'
    saftpt_Services = 'saftpt_Services'
    saftpt_Other = 'saftpt_Other'
    saftpt_Taxes = 'saftpt_Taxes'
    saftpt_NonSystem = 'saftpt_NonSystem'

class SAFTTaxCodeEnum(StrEnum):
    safttc_ReducedTax = 'safttc_ReducedTax'
    safttc_MiddleTax = 'safttc_MiddleTax'
    safttc_NormalTax = 'safttc_NormalTax'
    safttc_Exempt = 'safttc_Exempt'
    safttt_Others = 'safttt_Others'
    safttc_NonSystem = 'safttc_NonSystem'

class SAFTTransactionTypeEnum(StrEnum):
    safttt_Default = 'safttt_Default'
    safttt_Normal = 'safttt_Normal'
    safttt_AdjustmentsofTheTaxPeriod = 'safttt_AdjustmentsofTheTaxPeriod'
    safttt_MeasurementofResults = 'safttt_MeasurementofResults'
    safttt_Adjustment = 'safttt_Adjustment'
    safttt_DoNotExport = 'safttt_DoNotExport'
    safttt_NonSystem = 'safttt_NonSystem'

class SEPASequenceTypeEnum(StrEnum):
    sstOOFF = 'sstOOFF'
    sstFRST = 'sstFRST'
    sstRCUR = 'sstRCUR'
    sstFNAL = 'sstFNAL'

class SOIExcisableTypeEnum(StrEnum):
    se_Excisable = 'se_Excisable'
    se_Exemption = 'se_Exemption'
    se_PaidToOther = 'se_PaidToOther'
    se_NotExcisable = 'se_NotExcisable'

class SPEDContabilAccountPurposeCode(StrEnum):
    spedContasDeAtivo = 'spedContasDeAtivo'
    spedContasDePassivo = 'spedContasDePassivo'
    spedPatrimonioLiquido = 'spedPatrimonioLiquido'
    spedContasDeResultado = 'spedContasDeResultado'
    spedContasDeCompensacao = 'spedContasDeCompensacao'
    spedOutras = 'spedOutras'

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

class ServiceTypeEnum(StrEnum):
    srvcSales = 'srvcSales'
    srvcPurchasing = 'srvcPurchasing'

class Services(StrEnum):
    MessagesService = 'MessagesService'
    CompanyService = 'CompanyService'
    SeriesService = 'SeriesService'
    ReportLayoutsService = 'ReportLayoutsService'
    FormPreferencesService = 'FormPreferencesService'
    AccountsService = 'AccountsService'
    BusinessPartnersService = 'BusinessPartnersService'

class ShaamGroupEnum(StrEnum):
    sgServicesAndAsset = 'sgServicesAndAsset'
    sgAgriculturalProducts = 'sgAgriculturalProducts'
    sgInsuranceCommissions = 'sgInsuranceCommissions'
    sgWHTaxInstructions = 'sgWHTaxInstructions'
    sgInterestExchangeRateDiffs = 'sgInterestExchangeRateDiffs'
    sgRentalFees = 'sgRentalFees'

class SingleUserConnectionActionEnum(StrEnum):
    sucaWarning = 'sucaWarning'
    sucaBlock = 'sucaBlock'

class SortOrderEnum(StrEnum):
    soAscending = 'soAscending'
    soDescending = 'soDescending'

class SourceCurrencyEnum(StrEnum):
    sc_PrimaryCurrency = 'sc_PrimaryCurrency'
    sc_AdditionalCurrency1 = 'sc_AdditionalCurrency1'
    sc_AdditionalCurrency2 = 'sc_AdditionalCurrency2'

class SpecialDepreciationCalculationMethodEnum(StrEnum):
    spcmAdditional = 'spcmAdditional'
    spcmAlternative = 'spcmAlternative'

class SpecialDepreciationMaximumFlagEnum(StrEnum):
    spmfPercentage = 'spmfPercentage'
    spmfAmount = 'spmfAmount'

class SpecialProductTypeEnum(StrEnum):
    sptMT = 'sptMT'
    sptIO = 'sptIO'

class StageDepTypeEnum(StrEnum):
    sdt_Project = 'sdt_Project'
    sdt_Subproject = 'sdt_Subproject'

class StockTransferAuthorizationStatusEnum(StrEnum):
    sasWithout = 'sasWithout'
    sasPending = 'sasPending'
    sasApproved = 'sasApproved'
    sasRejected = 'sasRejected'
    sasGenerated = 'sasGenerated'
    sasGeneratedbyAuthorizer = 'sasGeneratedbyAuthorizer'
    sasCancelled = 'sasCancelled'

class StraightLineCalculationMethodEnum(StrEnum):
    slcmAuquisitionValueDividedByTotalUsefulLife = 'slcmAuquisitionValueDividedByTotalUsefulLife'
    slcmPercentageOfAcquisitionValue = 'slcmPercentageOfAcquisitionValue'
    slcmNetBookValueDividedByRemainingLife = 'slcmNetBookValueDividedByRemainingLife'

class StraightLinePeriodControlDepreciationPeriodsEnum(StrEnum):
    slpcdpStandard = 'slpcdpStandard'
    slpcdpIndividual = 'slpcdpIndividual'
    slpcdpIndividualUsage = 'slpcdpIndividualUsage'

class SubprojectStatusTypeEnum(StrEnum):
    sst_Open = 'sst_Open'
    sst_Closed = 'sst_Closed'

class SubsequentAcquisitionPeriodControlEnum(StrEnum):
    sapcProRataTemporis = 'sapcProRataTemporis'
    sapcHalfYearConvention = 'sapcHalfYearConvention'
    sapcFullYear = 'sapcFullYear'

class SubsequentAcquisitionProRataTypeEnum(StrEnum):
    saprtExactlyDailyBase = 'saprtExactlyDailyBase'
    saprtFirstDayOfCurrentPeriod = 'saprtFirstDayOfCurrentPeriod'
    saprtFirstDayOfNextPeriod = 'saprtFirstDayOfNextPeriod'

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

class TCSAccumulationBaseEnum(StrEnum):
    tcsAccumulationOnInvoice = 'tcsAccumulationOnInvoice'
    tcsAccumulationOnPayment = 'tcsAccumulationOnPayment'

class TargetGroupTypeEnum(StrEnum):
    tgtCustomer = 'tgtCustomer'
    tgtVendor = 'tgtVendor'

class TargetGroupsDetailStatusEnum(StrEnum):
    tdsActive = 'tdsActive'
    tdsInactive = 'tdsInactive'

class TaxCalcSysEnum(StrEnum):
    PreconfiguredFormulaWithJurisdictionSupport = 'PreconfiguredFormulaWithJurisdictionSupport'
    UserDefinedFormula = 'UserDefinedFormula'
    PreconfiguredFormula = 'PreconfiguredFormula'

class TaxCodeDeterminationTCDByUsageTypeEnum(StrEnum):
    tcdbutDefaultSales = 'tcdbutDefaultSales'
    tcdbutDefaultPurchase = 'tcdbutDefaultPurchase'
    tcdbutLine = 'tcdbutLine'

class TaxCodeDeterminationTCDDefaultWTTypeEnum(StrEnum):
    tcddwttDefaultSales = 'tcddwttDefaultSales'
    tcddwttDefaultPurchase = 'tcddwttDefaultPurchase'
    tcddwttLine = 'tcddwttLine'

class TaxCodeDeterminationTCDTypeEnum(StrEnum):
    tcdtMaterialItem = 'tcdtMaterialItem'
    tcdtServiceItem = 'tcdtServiceItem'
    tcdtServiceDocument = 'tcdtServiceDocument'
    tcdtWithholdingTax = 'tcdtWithholdingTax'

class TaxInvoiceReportLineTypeEnum(StrEnum):
    LineOfBusinessPlace = 'LineOfBusinessPlace'
    LineOfBusinessPartner = 'LineOfBusinessPartner'
    LineOfDocument = 'LineOfDocument'
    LineOfItem = 'LineOfItem'

class TaxInvoiceReportNTSApprovedEnum(StrEnum):
    NotApproved = 'NotApproved'
    Approved = 'Approved'

class TaxRateDeterminationEnum(StrEnum):
    trd_PostingDate = 'trd_PostingDate'
    trd_DocumentDate = 'trd_DocumentDate'

class TaxReportFilterApArDocumentType(StrEnum):
    trfadt_APDocuments = 'trfadt_APDocuments'
    trfadt_ARDocuments = 'trfadt_ARDocuments'

class TaxReportFilterDeclarationType(StrEnum):
    trfdt_Original = 'trfdt_Original'
    trfdt_Substitute = 'trfdt_Substitute'
    trfdt_Complementary = 'trfdt_Complementary'

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

class TaxReportFilterPeriod(StrEnum):
    trfP_Quarter = 'trfP_Quarter'
    trfP_Year = 'trfP_Year'
    trfP_Month = 'trfP_Month'
    trfP_NULL = 'trfP_NULL'

class TaxReportFilterQuarterOrDates(StrEnum):
    trfqd_Interval = 'trfqd_Interval'
    trfqd_Date = 'trfqd_Date'

class TaxReportFilterReportLayoutType(StrEnum):
    trfrlt_RegisterBookLayout = 'trfrlt_RegisterBookLayout'
    trfrlt_DeclarationLayout = 'trfrlt_DeclarationLayout'

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

class TaxTypeBlackListEnum(StrEnum):
    ttblExcluded = 'ttblExcluded'
    ttblExempt = 'ttblExempt'
    ttblNonSubject = 'ttblNonSubject'
    ttblNotTaxable = 'ttblNotTaxable'
    ttblTaxable = 'ttblTaxable'

class TdsTypeEnum(StrEnum):
    wtETds = 'wtETds'
    wtGstTds = 'wtGstTds'
    wtGstTcs = 'wtGstTcs'
    wtTcs = 'wtTcs'

class ThreatLevelEnum(StrEnum):
    tlLow = 'tlLow'
    tlMedium = 'tlMedium'
    tlHigh = 'tlHigh'

class TimeSheetTypeEnum(StrEnum):
    tsh_Employee = 'tsh_Employee'
    tsh_User = 'tsh_User'
    tsh_Other = 'tsh_Other'

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

class TransferSourcePeriodControlEnum(StrEnum):
    tspcProRataTemporis = 'tspcProRataTemporis'

class TransferSourceProRataTypeEnum(StrEnum):
    tsprtExactlyDailyBase = 'tsprtExactlyDailyBase'
    tsprtLastDayOfPriorPeriod = 'tsprtLastDayOfPriorPeriod'
    tsprtLastDayofCurrentPeriod = 'tsprtLastDayofCurrentPeriod'

class TransferTargetPeriodControlEnum(StrEnum):
    ttpcProRataTemporis = 'ttpcProRataTemporis'

class TransferTargetProRataTypeEnum(StrEnum):
    ttprtExactlyDailyBase = 'ttprtExactlyDailyBase'
    ttprtFirstDayOfCurrentPeriod = 'ttprtFirstDayOfCurrentPeriod'
    ttprtFirstDayOfNextPeriod = 'ttprtFirstDayOfNextPeriod'

class TranslationCategoryEnum(StrEnum):
    asCRReport = 'asCRReport'
    asMenuItem = 'asMenuItem'
    asEFMItem = 'asEFMItem'

class TypeOfAdvancedRulesEnum(StrEnum):
    toarGeneral = 'toarGeneral'
    toarWarehouse = 'toarWarehouse'
    toarItemGroup = 'toarItemGroup'

class TypeOfOperationEnum(StrEnum):
    tooProfessionalServices = 'tooProfessionalServices'
    tooRentingAssets = 'tooRentingAssets'
    tooOthers = 'tooOthers'

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

class UserGroupCategoryEnum(StrEnum):
    gc_Authorization = 'gc_Authorization'
    gc_Formsetting = 'gc_Formsetting'
    gc_Alert = 'gc_Alert'
    gc_UITmplate = 'gc_UITmplate'
    gc_All = 'gc_All'

class UserMenuItemTypeEnum(StrEnum):
    umitForm = 'umitForm'
    umitQuery = 'umitQuery'
    umitFolder = 'umitFolder'
    umitReport = 'umitReport'
    umitLink = 'umitLink'

class UserQueryTypeEnum(StrEnum):
    uqtRegular = 'uqtRegular'
    uqtWizard = 'uqtWizard'
    uqtGenerator = 'uqtGenerator'
    uqtStoredProcedure = 'uqtStoredProcedure'

class VMCommunicationStatusEnum(StrEnum):
    vmcs_Pending = 'vmcs_Pending'
    vmcs_Error = 'vmcs_Error'
    vmcs_Successful = 'vmcs_Successful'
    vmcs_New = 'vmcs_New'
    vmcs_Rejected = 'vmcs_Rejected'

class VMCommunicationTypeEnum(StrEnum):
    vmct_MasterData = 'vmct_MasterData'
    vmct_Transaction = 'vmct_Transaction'

class VatGroupsTaxRegionEnum(StrEnum):
    vgtrPT = 'vgtrPT'
    vgtrPT_AC = 'vgtrPT_AC'
    vgtrPT_MA = 'vgtrPT_MA'

class ViewStyleTypeEnum(StrEnum):
    vstPage = 'vstPage'
    vstFullScreen = 'vstFullScreen'
    vstLandscape = 'vstLandscape'

class WTDDetailType(StrEnum):
    Allowed = 'Allowed'
    SpecialRate = 'SpecialRate'
    Exemption = 'Exemption'

class WithholdingTaxCodeBaseTypeEnum(StrEnum):
    wtcbt_Gross = 'wtcbt_Gross'
    wtcbt_Net = 'wtcbt_Net'
    wtcbt_VAT = 'wtcbt_VAT'
    wtcbt_Gross_VAT = 'wtcbt_Gross_VAT'
    wtcbt_UoM = 'wtcbt_UoM'

class WithholdingTaxCodeCategoryEnum(StrEnum):
    wtcc_Invoice = 'wtcc_Invoice'
    wtcc_Payment = 'wtcc_Payment'

class WithholdingTypeEnum(StrEnum):
    wt_VatWithholding = 'wt_VatWithholding'
    wt_IncomeTaxWithholding = 'wt_IncomeTaxWithholding'
