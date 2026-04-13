from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class MobileAppService(GenericResource[Any]):
    endpoint = "MobileAppService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def get_current_server_date_time(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetCurrentServerDateTime
        Invoke the method 'GetCurrentServerDateTime' on this service.
        """
        return self._adapter.post(f"MobileAppService_GetCurrentServerDateTime", data=payload)

    def get_dpp_change_params(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetDppChangeParams
        Invoke the method 'GetDppChangeParams' on this service by specifying the payload 'DppChangeParams' in the JSON format.

        Example:
        ```json
        {
            "DppChangeParams": {
                "FromDate": "2018-03-30",
                "FromTime": "17:30:00"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetDppChangeParams", data=payload)

    def get_employee_full_names(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetEmployeeFullNames
        Invoke the method 'GetEmployeeFullNames' on this service by specifying the payload 'EmployeeFullNamesParamsCollection' in the JSON format.

        Example:
        ```json
        {
            "EmployeeFullNamesParamsCollection": [
                {
                    "EmployeeFullName": "",
                    "EmployeeID": 2
                },
                {
                    "EmployeeFullName": "",
                    "EmployeeID": 3
                }
            ]
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetEmployeeFullNames", data=payload)

    def get_sales_app_setting(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetSalesAppSetting
        Invoke the method 'GetSalesAppSetting' on this service.

        Example:
        ```json
        {
            "SalesAppSettingParams": {
                "Code": -1,
                "Name": "TEST1"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetSalesAppSetting", data=payload)

    def get_service_app_report(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetServiceAppReport
        Invoke the method 'GetServiceAppReport' on this service by specifying the payload 'ServiceAppReportParams' in the JSON format.

        Example:
        ```json
        {
            "ServiceAppReportParams": {
                "Code": -1,
                "ReportChoice": "S"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetServiceAppReport", data=payload)

    def get_service_app_report_content(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetServiceAppReportContent
        Invoke the method 'GetServiceAppReportContent' on this service by specifying the payload 'ServiceAppReportParams' in the JSON format.

        Example:
        ```json
        {
            "ServiceAppReportParams": {
                "Code": -1,
                "ReportChoice": "marCustomizedReport"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetServiceAppReportContent", data=payload)

    def get_technician_schedulings(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetTechnicianSchedulings
        Invoke the method 'GetTechnicianSchedulings' on this service by specifying the payload 'TechnicianSchedulingsParams' in the JSON format.

        Example:
        ```json
        {
            "TechnicianSchedulingsParams": {
                "EndDate": "2017-12-31",
                "StartDate": "2017-08-10",
                "Technician": "2"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetTechnicianSchedulings", data=payload)

    def get_technician_settings(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetTechnicianSettings
        Invoke the method 'GetTechnicianSettings' on this service by specifying the payload 'TechnicianSettingsParams' in the JSON format.

        Example:
        ```json
        {
            "TechnicianSettingsParams": {}
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetTechnicianSettings", data=payload)

    def get_technician_settings_group(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_GetTechnicianSettingsGroup
        Invoke the method 'GetTechnicianSettingsGroup' on this service.

        Example:
        ```json
        {
            "TechnicianSettingsGroupParams": {
                "Code": -1,
                "Name": "TEST1"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_GetTechnicianSettingsGroup", data=payload)

    def update_sales_app_setting(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_UpdateSalesAppSetting
        Invoke the method 'UpdateSalesAppSetting' on this service by specifying the payload 'SalesAppSetting' in the JSON format.

        Example:
        ```json
        {
            "AdvancedDashBoard": -1,
            "Code": -1,
            "CustomerAdvancedDashBoard": -2,
            "Name": "TESTCODE-1"
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_UpdateSalesAppSetting", data=payload)

    def update_service_app_report(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_UpdateServiceAppReport
        Invoke the method 'UpdateServiceAppReport' on this service by specifying the payload 'ServiceAppReport' in the JSON format.

        Example:
        ```json
        {
            "ServiceAppReport": {
                "Code": -1,
                "ReportChoice": "marCustomizedReport"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_UpdateServiceAppReport", data=payload)

    def update_service_app_report_content(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_UpdateServiceAppReportContent
        Invoke the method 'UpdateServiceAppReportContent' on this service by specifying the payload 'ServiceAppReportParams,ServiceAppReportContent' in the JSON format.

        Example:
        ```json
        {
            "ServiceAppReportContent": {
                "ReportContent": ""
            },
            "ServiceAppReportParams": {
                "Code": -1,
                "ReportChoice": "marCustomizedReport"
            }
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_UpdateServiceAppReportContent", data=payload)

    def update_technician_settings(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_UpdateTechnicianSettings
        Invoke the method 'UpdateTechnicianSettings' on this service by specifying the payload 'TechnicianSettings' in the JSON format.

        Example:
        ```json
        {
            "TechnicianSettings": {}
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_UpdateTechnicianSettings", data=payload)

    def update_technician_settings_group(self, payload: dict | None = None) -> Any:
        """POST MobileAppService_UpdateTechnicianSettingsGroup
        Invoke the method 'UpdateTechnicianSettingsGroup' on this service by specifying the payload 'TechnicianSettingsGroup' in the JSON format.

        Example:
        ```json
        {
            "AdvancedDashBoard": -4,
            "Code": -1,
            "CustomizedGroup": "tNO",
            "EnableActualDuration": "tNO",
            "EnableEditTime": "tNO",
            "EnableFollowup": "tNO",
            "EnableReject": "tNO",
            "EnableResign": "tNO",
            "EnableSignature": "tNO",
            "EnableStarRating": "tNO",
            "Name": "TESTCODE-1"
        }
        ```
        """
        return self._adapter.post(f"MobileAppService_UpdateTechnicianSettingsGroup", data=payload)
