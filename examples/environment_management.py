"""
Example: Unified Environment & Configuration Management.

This example demonstrates how to use the single canonical B1SL_ENV variable
to control both configuration loading and structured logging across the SDK.
"""

import sys
from pathlib import Path

# Add project roots to sys.path for standalone script execution
sys.path.append(str(Path(__file__).parent.parent / "src"))

import os

from b1sl.b1sl import B1Client, B1Env, B1Environment
from b1sl.b1sl.logging_utils import setup_logging


def run_example():
    # 1. Loading the environment.
    # The B1Environment class automatically reads B1SL_ENV.
    # If B1SL_ENV is not set, it defaults to B1Env.DEV.
    env = B1Environment.load()

    # 2. Strong-typed Environment Access.
    # config.environment is now a B1Env enum (not just a string).
    current_env = env.config.environment
    print(f"✅ Current SDK Environment: [{current_env.value}]")

    if current_env == B1Env.PROD:
        print("🚀 Production mode detected! Using structured JSON logging.")
    elif current_env == B1Env.TEST:
        print("🧪 Test mode detected! Logs will be human-readable.")
    else:
        print("🛠️ Development mode detected! Logs will be human-readable.")

    # 3. Explicit logging setup.
    # Pass the environment from the config to the logger setup.
    # This ensures that your logs match your loaded environment.
    logger = setup_logging(env=current_env)

    # 4. Dry Run Detection.
    if env.config.dry_run:
         logger.warning("🛡️ DRY RUN mode is enabled via B1SL_DRY_RUN=1")

    # Let's see some logs!
    logger.info(f"Initialized SDK with URL: {env.config.base_url}")
    logger.debug("Testing debug output (only visible if level is set to DEBUG)")

    # 4. Starting the Client.
    # The client now has the environment context inside the config.
    client = B1Client(config=env.config)

    print("\n✅ Setup complete! The SDK is now configured with unified environment management.")
    print("👉 To switch modes, set: export B1SL_ENV=prod")

if __name__ == "__main__":
    # Ensure some defaults for the example if not present
    if "B1SL_BASE_URL" not in os.environ:
        os.environ["B1SL_BASE_URL"] = "https://localhost:50000/b1s/v2"
    if "B1SL_USERNAME" not in os.environ:
        os.environ["B1SL_USERNAME"] = "manager"
    if "B1SL_PASSWORD" not in os.environ:
        os.environ["B1SL_PASSWORD"] = "sap"
    if "B1SL_COMPANY_DB" not in os.environ:
        os.environ["B1SL_COMPANY_DB"] = "SBODemoMX"

    run_example()
