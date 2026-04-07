from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class CompanyService(GenericResource[Any]):
    endpoint = "CompanyService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def create_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_CreatePeriod
        Invoke the method 'CreatePeriod' on this service by specifying the payload 'PeriodCategory' in the JSON format.
					It returns the 'PeriodCategoryParams' identification key based on the 'PeriodCategory' data structure.
					The 'PeriodCategory' object provides two types of properties:
					1.Properties that access existing Accounts and function as foreign keys to the ChartOfAccounts object.
					2.Properties that define new accounts by using Posting and Sub-Period definitions.

        Example:
        ```json
        {
            "PeriodCategory": {
                "BeginningofFinancialYear": "2010-01-01",
                "NumberOfPeriods": 1,
                "PeriodCategory": "2010",
                "PeriodName": "2010",
                "SubPeriodType": "spt_Year"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_CreatePeriod", data=payload)

    def create_period_with_finance_params(self, payload: dict | None = None) -> Any:
        """POST CompanyService_CreatePeriodWithFinanceParams
        Invoke the method 'CreatePeriodWithFinanceParams' on this service by specifying the payload 'PeriodCategory' in the JSON format.
					It returns a 'PeriodCategoryParams' identification key, extended with finance parameters derived by the 'FinancePeriodParams' identification key (system number, period indicator).
					The PeriodCategory object provides two types of properties:
					1.Properties that access existing Accounts and function as foreign keys to the 'ChartOfAccounts' object.
					2.Properties that define new accounts by using Posting and Sub-Period definitions.
					The 'FinancePeriodParams' specifies the identification key(system number, period indicator ) to which the 'CompanyService' is related.

        Example:
        ```json
        {
            "FinancePeriodParams": {
                "PeriodIndicator": "Default"
            },
            "PeriodCategory": {
                "BeginningofFinancialYear": "2010-01-01",
                "NumberOfPeriods": 1,
                "PeriodCategory": "2010",
                "PeriodName": "2010",
                "SubPeriodType": "spt_Year"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_CreatePeriodWithFinanceParams", data=payload)

    def get_advanced_gl_account(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetAdvancedGLAccount
        Invoke the method 'GetAdvancedGLAccount' on this service by specifying the payload 'AdvancedGLAccountParams' in the JSON format.

        Example:
        ```json
        {
            "AdvancedGLAccountParams": {}
        }
        ```
        """
        return self._adapter.post(f"CompanyService_GetAdvancedGLAccount", data=payload)

    def get_features_status(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetFeaturesStatus
        Invoke the method 'GetFeaturesStatus' on this service.
					It returns the 'FeatureStatusCollection'. A feature status can be either blocked or not.
					This object represents the status of a specified feature in the application, whether it is blocked or not according to the installation type: new 2007 release installation or upgrade installation prior to 2007 release.
        """
        return self._adapter.post(f"CompanyService_GetFeaturesStatus", data=payload)

    def get_finance_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetFinancePeriod
        Invoke the method 'GetFinancePeriod' on this service by specifying the payload 'FinancePeriodParams' in the JSON format.
					It returns a 'FinancePeriod' data structure according to the specified finance period key parameters.
					The object is used to identify and define a new 'FinancePeriod'.

        Example:
        ```json
        {
            "FinancePeriodParams": {}
        }
        ```
        """
        return self._adapter.post(f"CompanyService_GetFinancePeriod", data=payload)

    def get_finance_periods(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetFinancePeriods
        Invoke the method 'GetFinancePeriods' on this service by specifying the payload 'PeriodCategoryParams' in the JSON format.
					It returns the 'FinancePeriods' collection according to the specified period category key parameters.
					The object is used to identify and define a new 'FinancePeriods'.

        Example:
        ```json
        {
            "PeriodCategoryParams": {
                "AbsoluteEntry": 1
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_GetFinancePeriods", data=payload)

    def get_item_price(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetItemPrice
        Invoke the method 'GetItemPrice' on this service by specifying the payload 'ItemPriceParams' in the JSON format.
					It returns a business object that contains the item price for specified business partner and item, based on the amount and transaction date.

        Example:
        ```json
        {
            "ItemPriceParams": {
                "CardCode": "Customer",
                "ItemCode": "Item"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_GetItemPrice", data=payload)

    def get_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_GetPeriod
        Invoke the method 'GetPeriod' on this service by specifying the payload 'PeriodCategoryParams' in the JSON format.
					It returns the 'PeriodCategory' data structure according to the specified period category key parameters.
					The 'PeriodCategory' object provides two types of properties:
					1.Properties that access existing Accounts and function as foreign keys to the ChartOfAccounts object.
					2.Properties that define new accounts by using Posting and Sub-Period definitions.

        Example:
        ```json
        {
            "PeriodCategoryParams": {}
        }
        ```
        """
        return self._adapter.post(f"CompanyService_GetPeriod", data=payload)

    def get_periods(self, payload: dict | None = None) -> Any:
        """GET CompanyService_GetPeriods
        Invoke the method 'GetPeriods' on this service.
					It returns the 'PeriodCategoryParamsCollection', which is a collection of 'PeriodCategoryParams' identification keys.
        """
        return self._adapter.post(f"CompanyService_GetPeriods", data=payload)

    def log_login_action(self, payload: dict | None = None) -> Any:
        """POST CompanyService_LogLoginAction
        Invoke the method 'LogLoginAction' on this service by specifying the payload 'UserAccessLog' and 'SupportUserLoginRecord' in the JSON format.
					1. SupportUserLoginRecord is only used in 'On Premise' mode. For 'On Demand' mode, there is no need to provide 'SupportUserLoginRecord'. For 'On Premise' mode, there is no need to provide 'ReasonID' and 'ReasonDesc'.
                    2. 'SessionID' can be retrieved from DB server.
                    3. Must use DB server time for 'ActionDate' and 'ActionTime'.

        Example:
        ```json
        {
            "SupportUserLoginRecord": {
                "ID": 21,
                "LogDetail": "Log detail",
                "LogReason": "J",
                "RealName": "Real name"
            },
            "UserAccessLog": {
                "Action": "I",
                "ActionBy": "Support",
                "ActionDate": "2021-06-23",
                "ActionTime": 102959,
                "ClientIP": "10.10.10.10",
                "ClientName": "SERVER01A",
                "ProcName": "Web Client.jar",
                "ProcessID": 10592,
                "ReasonDesc": "Reason desc",
                "ReasonID": 51,
                "SessionID": 65,
                "Source": "SBO_Web_Client",
                "UserCode": "Support",
                "UserID": 4,
                "WinSessnID": -1,
                "WinUsrName": "b1admin"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_LogLoginAction", data=payload)

    def log_logoff_action(self, payload: dict | None = None) -> Any:
        """POST CompanyService_LogLogoffAction
        Invoke the method 'LogLogoffAction' on this service by specifying the payload 'UserAccessLog' and 'SupportUserLoginRecord' in the JSON format.
					1. SupportUserLoginRecord is only used in 'On Premise' mode. For 'On Demand' mode, there is no need to provide 'SupportUserLoginRecord'. For 'On Premise' mode, there is no need to provide 'ReasonID' and 'ReasonDesc'.
          			2. 'SessionID' can be retrieved from DB server.
          			3. 'ActionDate' and 'ActionTime' must be the same value as those in LogLoginAction.
          			4. 'ID' of 'SupportUserLoginRecord' comes from LogLoginAction.

        Example:
        ```json
        {
            "SupportUserLoginRecord": {
                "ID": 21,
                "LogDetail": "Log detail",
                "LogReason": "J",
                "RealName": "Real name"
            },
            "UserAccessLog": {
                "Action": "O",
                "ActionBy": "Support",
                "ActionDate": "2021-06-23",
                "ActionTime": 102959,
                "ClientIP": "10.10.10.10",
                "ClientName": "SERVER01A",
                "ProcName": "Web Client.jar",
                "ProcessID": 10592,
                "ReasonDesc": "Reason desc",
                "ReasonID": 51,
                "SessionID": 65,
                "Source": "SBO_Web_Client",
                "UserCode": "Support",
                "UserID": 4,
                "WinSessnID": -1,
                "WinUsrName": "b1admin"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_LogLogoffAction", data=payload)

    def remove_finance_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_RemoveFinancePeriod
        Invoke the method 'RemoveFinancePeriod' on this service by specifying the payload 'FinancePeriodParams' in the JSON format.

        Example:
        ```json
        {
            "FinancePeriods": [
                {
                    "AbsoluteEntry": "1"
                }
            ]
        }
        ```
        """
        return self._adapter.post(f"CompanyService_RemoveFinancePeriod", data=payload)

    def round_decimal(self, payload: dict | None = None) -> Any:
        """POST CompanyService_RoundDecimal
        Invoke the method 'RoundDecimal' on this service by specifying the payload 'DecimalData' in the JSON format.
					It rounds data to a specified number of decimal places or to a whole number if no decimal places are specified.

        Example:
        ```json
        {
            "DecimalData": {
                "Context": "rcPrice",
                "Currency": "$",
                "Value": 12.345
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_RoundDecimal", data=payload)

    def update_admin_info(self, payload: dict | None = None) -> Any:
        """POST CompanyService_UpdateAdminInfo
        Invoke the method 'UpdateAdminInfo' on this service by specifying the payload 'AdminInfo' in the JSON format.

        Example:
        ```json
        {
            "AdminInfo": {
                "CalculateBudget": "tYES",
                "ChangeDefReconAPAccounts": "tYES",
                "ChangeDefReconARAccounts": "tYES",
                "ChartofAccountsTemplate": "C",
                "Code": 1,
                "CompanyName": "USTest",
                "ContinuousStockManagement": "tYES",
                "Country": "US",
                "CreditBalancewithMinusSign": "tYES",
                "DefaultWarehouse": "01",
                "ExtendedAdminInfo": {},
                "LocalCurrency": "$",
                "MultiLanguageSupportEnable": "tYES",
                "RoundingMethod": "tYES",
                "SetItemsWarehouses": "tYES",
                "SplitPO": "tYES",
                "SystemCurrency": "$",
                "UniqueSerialNo": "usn_MfrSerialNumber"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_UpdateAdminInfo", data=payload)

    def update_company_info(self, payload: dict | None = None) -> Any:
        """POST CompanyService_UpdateCompanyInfo
        Invoke the method 'UpdateCompanyInfo' on this service by specifying the payload 'CompanyInfo' in the JSON format. It includes the initial parameters related to the company. The default values of some of the properties vary according to the country localization.

        Example:
        ```json
        {
            "CompanyInfo": {
                "EnableAccountSegmentation": "tYES",
                "EnableExpensesManagement": "tYES",
                "MaxRecordsInChooseFromList": 0,
                "MinimumAmountForAnnualList": 0,
                "MinimumAmountForAppndixOP": 0,
                "MinimumBaseAmountPerDoc": 0,
                "PercentOfTotalAcquisition": 0,
                "Version": "910190"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_UpdateCompanyInfo", data=payload)

    def update_finance_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_UpdateFinancePeriod
        Invoke the method 'UpdateFinancePeriod' on this service by specifying the payload 'FinancePeriod' in the JSON format.

        Example:
        ```json
        {
            "FinancePeriod": {
                "AbsoluteEntry": 6,
                "ActiveforFeed": "tNO",
                "PeriodCode": "2015-06",
                "PeriodName": "2015-06",
                "PostingDateFrom": "2015-06-01",
                "PostingDateTo": "2015-06-30",
                "TaxDateFrom": "2015-01-01",
                "TaxDateTo": "2015-12-31",
                "ValueDateFrom": "2015-01-01",
                "ValueDateTo": "2015-12-31"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_UpdateFinancePeriod", data=payload)

    def update_path_admin(self, payload: dict | None = None) -> Any:
        """POST CompanyService_UpdatePathAdmin
        Invoke the method 'UpdatePathAdmin' on this service by specifying the payload 'PathAdmin' in the JSON format.

        Example:
        ```json
        {
            "PathAdmin": {
                "AttachmentsFolderPath": "/usr/sap/SAPBusinessOne/ServiceLayer/modules",
                "ExtensionsFolderPath": null,
                "PicturesFolderPath": null,
                "PrintId": "USBO",
                "WordTemplateFolderPath": null
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_UpdatePathAdmin", data=payload)

    def update_period(self, payload: dict | None = None) -> Any:
        """POST CompanyService_UpdatePeriod
        Invoke the method 'UpdatePeriod' on this service by specifying the payload 'PeriodCategory' in the JSON format.

        Example:
        ```json
        {
            "PeriodCategory": {
                "AbsoluteEntry": 1,
                "AccountforCashReceipt": "_SYS00000000003",
                "BeginningofFinancialYear": "2015-01-01",
                "NumberOfPeriods": 12,
                "PeriodCategory": "2015",
                "SubPeriodType": "spt_Months"
            }
        }
        ```
        """
        return self._adapter.post(f"CompanyService_UpdatePeriod", data=payload)

    # --- Functions ---

    def get_admin_info(self, params: dict | None = None) -> Any:
        """POST CompanyService_GetAdminInfo(params)
        Invoke the method 'GetAdminInfo' on this service. It Returns the 'AdminInfo' data structure, including administration properties for system initialization and various definitions, such as financials and banking.
        """
        return self._function(f"CompanyService_GetAdminInfo", params)

    def get_company_info(self, params: dict | None = None) -> Any:
        """POST CompanyService_GetCompanyInfo(params)
        Invoke the method 'GetCompanyInfo' on this service. It returns the 'CompanyInfo' data structure, including initial parameters related to the company. The default values of some of the properties vary according to the country localization.
        """
        return self._function(f"CompanyService_GetCompanyInfo", params)

    def get_path_admin(self, params: dict | None = None) -> Any:
        """POST CompanyService_GetPathAdmin(params)
        Invoke the method 'GetPathAdmin' on this service.
        """
        return self._function(f"CompanyService_GetPathAdmin", params)
