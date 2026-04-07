import logging
import os
import warnings
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from b1sl.b1sl import AsyncB1Client, B1Client, B1Environment
from b1sl.b1sl.testing import B1TestHelper

# Suppress Pydantic warnings for examples
try:
    from pydantic import ArbitraryTypeWarning
    warnings.filterwarnings("ignore", category=ArbitraryTypeWarning)
except ImportError:
    warnings.filterwarnings("ignore", module="pydantic")

# Configure logging
logging.basicConfig(level=logging.ERROR)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Check if .env exists to warn the user
    if os.path.exists(".env"):
        print("⚠️  Warning: .env file found but 'python-dotenv' is not installed.")
        print("   Using fallback configurations from 'configs/' directory.")
    pass

class ExampleRunner:
    """Helper class to standardize SAP B1 examples."""

    def __init__(self, name: str, **client_kwargs):
        self.name = name
        self.env = B1Environment.load()
        self.test_data = B1TestHelper(self.env.test_data)
        self.client = B1Client(config=self.env.config, version="v2", **client_kwargs)
        print(f"✅ Environment: [{self.env.name}] | Example: [{name}]")

    def header(self, title: str):
        print(f"\n{'='*60}")
        print(f"  {title.upper()}")
        print(f"{'='*60}")

    def info(self, msg: str):
        print(f"🔍 {msg}")

    def success(self, msg: str):
        print(f"✨ {msg}")

    def result(self, label: str, value: any):
        print(f"  → {label:<25} : {value}")

    def error(self, msg: str, exception: Exception = None):
        print(f"\n❌ ERROR: {msg}")
        if exception:
            print(f"   Detail: {exception}")

@contextmanager
def use_sap_b1(example_name: str, **client_kwargs) -> Generator[ExampleRunner, None, None]:
    """Context manager for SAP B1 examples."""
    runner = ExampleRunner(example_name, **client_kwargs)
    try:
        yield runner
    except Exception as e:
        runner.error("Execution failed", e)
    finally:
        pass

class AsyncExampleRunner(ExampleRunner):
    """Asynchronous version of ExampleRunner."""

    def __init__(self, name: str, **client_kwargs):
        self.name = name
        self.env = B1Environment.load()
        self.test_data = B1TestHelper(self.env.test_data)
        self.client = AsyncB1Client(config=self.env.config, version="v2", **client_kwargs)
        print(f"✅ Environment: [{self.env.name}] | Example: [{name}] (Async)")

@asynccontextmanager
async def use_async_sap_b1(example_name: str, **client_kwargs) -> AsyncGenerator[AsyncExampleRunner, None]:
    """Asynchronous context manager for SAP B1 examples."""
    runner = AsyncExampleRunner(example_name, **client_kwargs)
    try:
        async with runner.client as b1:
            yield runner
    except Exception as e:
        runner.error("Execution failed", e)
    finally:
        pass


def build_async_client():
    """Helper to return a B1Config from default environment."""
    from b1sl.b1sl import B1Environment

    env = B1Environment.load()
    return env.config
