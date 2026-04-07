from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ChartOfAccountsService(GenericResource["ChartOfAccount"]):
    """This entity enables you to manipulate 'ChartOfAccounts'. It represents the General Ledger (G/L) accounts in the Finance module. The Chart of Accounts is an index of all G/L accounts that are used by one or more companies. For every G/L account there is an account number, an account description, and information that determines the function of the account."""
    endpoint = "ChartOfAccounts"
    
    def __init__(self, adapter):
        from ...models._generated._types import ChartOfAccount
        self.model = ChartOfAccount
        super().__init__(adapter)
