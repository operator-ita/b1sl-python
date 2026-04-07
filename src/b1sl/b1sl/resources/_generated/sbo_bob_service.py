from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class SBOBobService(GenericResource[Any]):
    endpoint = "SBOBobService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def set_currency_rate(self, payload: dict | None = None) -> Any:
        """POST SBOBobService_SetCurrencyRate
        Invoke the method 'SBOBobService_SetCurrencyRate' on this service by specifying the payload 'RateDate,Currency,Rate' in the JSON format.

        Example:
        ```json
        {
            "Currency": "EUR",
            "Rate": "4.8",
            "RateDate": "20161129"
        }
        ```
        """
        return self._adapter.post(f"SBOBobService_SetCurrencyRate", data=payload)

    def set_system_permission(self, payload: dict | None = None) -> Any:
        """POST SBOBobService_SetSystemPermission
        Invoke the method 'SetSystemPermission' on this service by specifying the payload 'UserCode,PermissionID and Permission' in the JSON format.

        Example:
        ```json
        {
            "Permission": 2,
            "PermissionID": "57",
            "UserCode": "andy"
        }
        ```
        """
        return self._adapter.post(f"SBOBobService_SetSystemPermission", data=payload)

    # --- Functions ---

    def format_money_to_string(self, params: dict | None = None) -> Any:
        """POST SBOBobService_Format_MoneyToString(params)
        Invoke the method 'Format_MoneyToString' on this service by specifying the payload 'InMoney,InPrecision' in the JSON format.
        """
        return self._function(f"SBOBobService_Format_MoneyToString", params)

    def get_currency_rate(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetCurrencyRate(params)
        Invoke the method 'GetCurrencyRate' on this service by specifying the payload 'Currency,Date' in the JSON format.
        """
        return self._function(f"SBOBobService_GetCurrencyRate", params)

    def get_due_date(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetDueDate(params)
        Invoke the method 'GetDueDate' on this service by specifying the payload 'CardCode,RefDate' in the JSON format.
        """
        return self._function(f"SBOBobService_GetDueDate", params)

    def get_index_rate(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetIndexRate(params)
        Invoke the method 'GetIndexRate' on this service by specifying the payload 'Index,Date' in the JSON format.
        """
        return self._function(f"SBOBobService_GetIndexRate", params)

    def get_local_currency(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetLocalCurrency(params)
        Invoke the method 'GetLocalCurrency' on this service.
        """
        return self._function(f"SBOBobService_GetLocalCurrency", params)

    def get_system_currency(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetSystemCurrency(params)
        Invoke the method 'GetSystemCurrency' on this service.
        """
        return self._function(f"SBOBobService_GetSystemCurrency", params)

    def get_system_permission(self, params: dict | None = None) -> Any:
        """POST SBOBobService_GetSystemPermission(params)
        Invoke the method 'GetSystemPermission' on this service by specifying the payload 'UserCode,PermissionID' in the JSON format.
        """
        return self._function(f"SBOBobService_GetSystemPermission", params)
