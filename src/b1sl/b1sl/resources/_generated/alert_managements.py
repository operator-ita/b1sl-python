from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class AlertManagementsService(GenericResource["AlertManagement"]):
    """This entity enables you to manipulate 'AlertManagements'.
			For each alert, you need to define its priority, the users and documents to which the alert applies, and the conditions that trigger the alert. In addition to activating system alerts, you can also add alerts based on user-defined queries."""
    endpoint = "AlertManagements"

    def __init__(self, adapter):
        from ...models._generated._types import AlertManagement
        self.model = AlertManagement
        super().__init__(adapter)
