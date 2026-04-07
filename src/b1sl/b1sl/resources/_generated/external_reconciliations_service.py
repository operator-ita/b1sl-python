from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ExternalReconciliationsService(GenericResource[Any]):
    endpoint = "ExternalReconciliationsService"

    def __init__(self, adapter):
        self.model = None
        super().__init__(adapter)

    # --- Actions ---

    def cancel_reconciliation(self, payload: dict | None = None) -> Any:
        """POST ExternalReconciliationsService_CancelReconciliation
        Invoke the method 'CancelReconciliation' on this service by specifying the payload 'ExternalReconciliationParams' in the JSON format.

        Example:
        ```json
        {
            "ExternalReconciliationParams": {
                "AccountCode": "_SYS00000000001",
                "ReconciliationNo": 1
            }
        }
        ```
        """
        return self._adapter.post("ExternalReconciliationsService_CancelReconciliation", data=payload)

    def get_reconciliation(self, payload: dict | None = None) -> Any:
        """POST ExternalReconciliationsService_GetReconciliation
        Invoke the method 'GetReconciliation' on this service by specifying the payload 'ExternalReconciliationParams' in the JSON format. It retrieves an external reconciliation.

        Example:
        ```json
        {
            "ExternalReconciliationParams": {
                "AccountCode": "_SYS00000000001",
                "ReconciliationNo": 1
            }
        }
        ```
        """
        return self._adapter.post("ExternalReconciliationsService_GetReconciliation", data=payload)

    def get_reconciliation_list(self, payload: dict | None = None) -> Any:
        """POST ExternalReconciliationsService_GetReconciliationList
        Invoke the method 'GetReconciliationList' on this service by specifying the payload 'ExternalReconciliationFilterParams' in the JSON format.
					It returns the 'ExternalReconciliationsParamsCollection' data collection that identifies all eternal reconciliations with the optional filter payload.

        Example:
        ```json
        {
            "ExternalReconciliationFilterParams": {
                "AccountCodeFrom": "_SYS00000000001",
                "AccountCodeTo": "_SYS00000000002",
                "ReconciliationAccountType": "rat_GLAccount",
                "ReconciliationDateFrom": "2016-05-03",
                "ReconciliationDateTo": "2016-12-03",
                "ReconciliationNoFrom": 1,
                "ReconciliationNoTo": 2
            }
        }
        ```
        """
        return self._adapter.post("ExternalReconciliationsService_GetReconciliationList", data=payload)

    def reconcile(self, payload: dict | None = None) -> Any:
        """POST ExternalReconciliationsService_Reconcile
        Invoke the method 'Reconcile' on this service by specifying the payload 'ExternalReconciliation' in the JSON format.

        Example:
        ```json
        {
            "ExternalReconciliation": {
                "ReconciliationAccountType": "rat_BusinessPartner",
                "ReconciliationBankStatementLines": [
                    {
                        "BankStatementAccountCode": "C1",
                        "Sequence": 1
                    },
                    {
                        "BankStatementAccountCode": "C1",
                        "Sequence": 2
                    }
                ],
                "ReconciliationJournalEntryLines": [
                    {
                        "LineNumber": 1,
                        "TransactionNumber": 1
                    },
                    {
                        "LineNumber": 2,
                        "TransactionNumber": 2
                    }
                ]
            }
        }
        ```
        """
        return self._adapter.post("ExternalReconciliationsService_Reconcile", data=payload)
