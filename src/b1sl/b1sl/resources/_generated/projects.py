from __future__ import annotations

from typing import TYPE_CHECKING, Any

from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class ProjectsService(GenericResource["Project"]):
    """This entity enables you to manipulate 'Projects'."""
    endpoint = "Projects"

    def __init__(self, adapter):
        from ...models._generated._types import Project
        self.model = Project
        super().__init__(adapter)
