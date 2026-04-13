from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ReportLayoutsService(GenericResource[Any]):
    endpoint = "ReportLayoutsService"
    
    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def add_report_layout(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_AddReportLayout
        Invoke the method 'AddReportLayout' on this service by specifying the payload 'ReportLayout' in the JSON format.

        Example:
        ```json
        {
            "ReportLayout": {
                "LayoutCode": "POR10007",
                "Name": "layout 123",
                "TypeCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_AddReportLayout", data=payload)

    def add_report_layout_to_menu(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_AddReportLayoutToMenu
        Invoke the method 'AddReportLayoutToMenu' on this service by specifying the payload 'ReportLayout,ReportInputParams' in the JSON format.

        Example:
        ```json
        {
            "ReportInputParams": {
                "ReportLayoutMenuID": 1
            },
            "ReportLayout": {
                "AllignFooterToBottom": "tNO",
                "Author": null,
                "B1Version": null,
                "BottomMargin": 10,
                "CRVersion": null,
                "Category": "rlcPLD",
                "ChangeFontSizeForEMail": -1,
                "ChangeFontSizeInPreview": -1,
                "ConvertFontForEMail": "tNO",
                "ConvertFontInPrintPreview": "tNO",
                "EMailFont": "Arial",
                "Editable": "tYES",
                "ExtensionErrorAction": "eeaStop",
                "ExtensionName": null,
                "FollowUpReport": null,
                "ForeignLanguageReport": "tNO",
                "GridSize": 10,
                "GridType": "gtCombination",
                "Height": 842,
                "ImpExpObjCode": 0,
                "LayoutCode": "POR10005",
                "LeaderReport": null,
                "LeftMargin": 10,
                "Localization": null,
                "Name": "layout 125",
                "NumberOfCopies": 1,
                "Orientation": "ortVertical",
                "PaperSize": "A4",
                "Picture": null,
                "PreviewPrintingFont": "Arial",
                "Printer": null,
                "PrinterFirstPage": null,
                "Query": null,
                "QueryType": "qtRegular",
                "Remarks": null,
                "RepetitiveAreasNumber": 0,
                "ReportLayoutItems": [],
                "ReportLayout_TranslationLines": [],
                "RightMargin": 30,
                "ShowGrid": "tYES",
                "SnapToGrid": "tYES",
                "Sortable": "tYES",
                "TopMargin": 10,
                "TypeCode": "POR1",
                "TypeDetail": null,
                "UseFirstPrinter": "tNO",
                "Width": 595,
                "language": 31
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_AddReportLayoutToMenu", data=payload)

    def delete_report_layout(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_DeleteReportLayout
        Invoke the method 'DeleteReportLayout' on this service by specifying the payload 'ReportLayoutParams' in the JSON format.

        Example:
        ```json
        {
            "ReportLayoutParams": {
                "LayoutCode": "POR10007"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_DeleteReportLayout", data=payload)

    def delete_report_layout_and_menu(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_DeleteReportLayoutAndMenu
        Invoke the method 'DeleteReportLayoutAndMenu' on this service by specifying the payload 'ReportLayoutParams' in the JSON format.

        Example:
        ```json
        {
            "ReportLayoutParams": {
                "LayoutCode": "POR10007"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_DeleteReportLayoutAndMenu", data=payload)

    def get_default_report(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_GetDefaultReport
        Invoke the method 'GetDefaultReport' on this service by specifying the payload 'ReportParams' in the JSON format.

        Example:
        ```json
        {
            "ReportParams": {
                "ReportCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_GetDefaultReport", data=payload)

    def get_default_report_layout(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_GetDefaultReportLayout
        Invoke the method 'GetDefaultReportLayout' on this service by specifying the payload 'ReportParams' in the JSON format.

        Example:
        ```json
        {
            "ReportParams": {
                "ReportCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_GetDefaultReportLayout", data=payload)

    def get_report_layout(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_GetReportLayout
        Invoke the method 'GetReportLayout' on this service by specifying the payload 'ReportLayoutParams' in the JSON format.

        Example:
        ```json
        {
            "ReportLayoutParams": {
                "LayoutCode": "POR10007"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_GetReportLayout", data=payload)

    def get_report_layout_list(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_GetReportLayoutList
        Invoke the method 'GetReportLayoutList' on this service by specifying the payload 'ReportParams' in the JSON format.

        Example:
        ```json
        {
            "ReportParams": {
                "ReportCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_GetReportLayoutList", data=payload)

    def set_default_report(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_SetDefaultReport
        Invoke the method 'SetDefaultReport' on this service by specifying the payload 'DefaultReportParams' in the JSON format.

        Example:
        ```json
        {
            "DefaultReportParams": {
                "LayoutCode": "POR10007",
                "ReportCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_SetDefaultReport", data=payload)

    def update_language_report(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_UpdateLanguageReport
        Invoke the method 'UpdateLanguageReport' on this service by specifying the payload 'ReportLayout' in the JSON format.

        Example:
        ```json
        {
            "ReportLayout": {
                "LayoutCode": "POR10007",
                "language": 35
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_UpdateLanguageReport", data=payload)

    def update_printer_settings(self, payload: dict | None = None) -> Any:
        """POST ReportLayoutsService_UpdatePrinterSettings
        Invoke the method 'UpdatePrinterSettings' on this service by specifying the payload 'ReportLayout' in the JSON format.

        Example:
        ```json
        {
            "ReportLayout": {
                "LayoutCode": "POR10007",
                "Name": "aaaaaa",
                "Printer": "Fax",
                "TypeCode": "POR1"
            }
        }
        ```
        """
        return self._adapter.post(f"ReportLayoutsService_UpdatePrinterSettings", data=payload)
