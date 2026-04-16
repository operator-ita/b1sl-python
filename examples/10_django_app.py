"""
examples/django_integration.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Demonstrates how to use the SDK within a Django project.

The SDK provides a built-in adapter that automatically pulls credentials 
from `django.conf.settings`. This is perfect for legacy migrations or 
shared-pool synchronous tasks.

Requirements:
    - django (pip install django)
    - Settings prefixed with B1SL_ in your settings.py
"""

import sys
from pathlib import Path

# --- Path hack to run from the repo root ---
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

# --- 1. MOCKING DJANGO SETTINGS (For demonstration purposes) ---
# In a real project, this would be your settings.py
class MockSettings:
    B1SL_BASE_URL = "https://host:50000/b1s/v2"
    B1SL_USERNAME = "manager"
    B1SL_PASSWORD = "password"
    B1SL_COMPANY_DB = "SBO_DEMO"
    B1SL_ENV = "dev"

# Injecting into sys.modules so 'import django' doesn't fail
from unittest.mock import MagicMock

sys.modules['django'] = MagicMock()
sys.modules['django.conf'] = MagicMock()
from django.conf import settings

settings.B1SL_BASE_URL = MockSettings.B1SL_BASE_URL
settings.B1SL_USERNAME = MockSettings.B1SL_USERNAME
settings.B1SL_PASSWORD = MockSettings.B1SL_PASSWORD
settings.B1SL_COMPANY_DB = MockSettings.B1SL_COMPANY_DB
settings.B1SL_ENV = MockSettings.B1SL_ENV

# --- 2. USING THE ADAPTER ---
from b1sl.b1sl.adapter import get_rest_adapter
from b1sl.b1sl.client import B1Client
from b1sl.b1sl.config import B1Config


def django_view_example():
    """
    Example of how you would use it in a Django View.
    """
    print("--- Django Integration Example ---")

    # Method A: Use the legacy shared adapter (Singleton-like)
    # Useful for porting old scripts quickly.
    adapter = get_rest_adapter()
    print(f"Shared Adapter initialized for: {adapter.url}")

    # Method B: Use the B1Client with Django Config (Recommended)
    # This is the modern, type-safe approach.
    config = B1Config.from_django_settings()
    client = B1Client(config)

    print(f"B1Client connected to {client._adapter.url}")
    print("Successfully loaded settings from django.conf.settings!")

if __name__ == "__main__":
    django_view_example()
