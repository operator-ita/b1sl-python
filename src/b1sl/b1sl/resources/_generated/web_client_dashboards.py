from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WebClientDashboardsService(GenericResource["WebClientDashboard"]):
    """This entity enables you to manipulate 'WebClientDashboards'."""
    endpoint = "WebClientDashboards"
    
    def __init__(self, adapter):
        from ...models._generated._types import WebClientDashboard
        self.model = WebClientDashboard
        super().__init__(adapter)
