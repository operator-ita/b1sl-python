from __future__ import annotations
from typing import TYPE_CHECKING, Any
from b1sl.b1sl.resources.base import GenericResource

if TYPE_CHECKING:
    from ...models._generated._types import *

class UsersService(GenericResource["User"]):
    """This entity enables you to manipulate 'Users'. It represents the users table of the SAP Business One application. The users table includes the users list, login details, and authorizations."""
    endpoint = "Users"
    
    def __init__(self, adapter):
        from ...models._generated._types import User
        self.model = User
        super().__init__(adapter)
