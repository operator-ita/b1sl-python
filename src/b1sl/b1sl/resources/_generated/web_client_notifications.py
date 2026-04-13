from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WebClientNotificationsService(GenericResource["WebClientNotification"]):
    """This entity enables you to manipulate 'WebClientNotifications'."""
    endpoint = "WebClientNotifications"
    
    def __init__(self, adapter):
        from ...models._generated._types import WebClientNotification
        self.model = WebClientNotification
        super().__init__(adapter)
