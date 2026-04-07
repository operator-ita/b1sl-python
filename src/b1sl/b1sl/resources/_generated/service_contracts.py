from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ServiceContractsService(GenericResource["ServiceContract"]):
    """This entity enables you to manipulate 'ServiceContracts'. It represents the service contracts table in the Service module of the SAP Business One application. This object enables you to do the following: Add a service contract; retrieve a service contract by its key; update a service contract; remove a service contract."""
    endpoint = "ServiceContracts"

    def __init__(self, adapter):
        from ...models._generated._types import ServiceContract
        self.model = ServiceContract
        super().__init__(adapter)
