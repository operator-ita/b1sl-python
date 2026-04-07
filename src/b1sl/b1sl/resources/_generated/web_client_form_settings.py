from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class WebClientFormSettingsService(GenericResource["WebClientFormSetting"]):
    """This entity enables you to manipulate 'WebClientFormSettings'."""
    endpoint = "WebClientFormSettings"

    def __init__(self, adapter):
        from ...models._generated._types import WebClientFormSetting
        self.model = WebClientFormSetting
        super().__init__(adapter)
