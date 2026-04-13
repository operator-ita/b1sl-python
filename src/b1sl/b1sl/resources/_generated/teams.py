from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class TeamsService(GenericResource["Team"]):
    """This entity enables you to manipulate 'Teams'. It represents the list of teams from which team memberships of an employee can be selected. An employee can be a Member or a Leader of more than one team."""
    endpoint = "Teams"
    
    def __init__(self, adapter):
        from ...models._generated._types import Team
        self.model = Team
        super().__init__(adapter)
