from __future__ import annotations

from typing import Any


class B1TestHelper:
    """
    Test helper for SAP B1 environments.
    Groups test_data logic away from the core runtime SDK.
    """
    def __init__(self, test_data: dict[str, Any]):
        self.test_data = test_data

    def get_test_item(self, profile: str = "simple") -> str:
        """Retrieves a test item code from the environment test data."""
        return self.test_data.get("items", {}).get(profile, "")

    def get_test_customer(self, profile: str = "retail") -> str:
        """Retrieves a test customer code from the environment test data."""
        return self.test_data.get("customers", {}).get(profile, "")

    def get_test_bp(self, profile: str = "simple") -> str:
        """Retrieves a test Business Partner code from the environment test data."""
        return self.test_data.get("business_partners", {}).get(profile, "")
