from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from b1sl.b1sl.config import B1Config
from b1sl.b1sl.environment import B1Env


@dataclass
class B1Environment:
    """
    High-level manager for multi-source environment configuration.

    B1Environment loads not only the connection settings (B1Config) but also
    accompanying test data or business profile dictionaries from JSON files.

    AI Role: Recommended for loading environment context.
    It supports multiple profiles (e.g. dev, qa, prod) and provides helpers
    to retrieve realistic test IDs (Items, BP, etc.) defined in JSON.

    Attributes:
        config (B1Config): Connection parameters.
        test_data (dict): Dictionary of resource-specific test IDs.
        name (str): Environment identifier.
    """

    config: B1Config
    test_data: dict[str, Any] = field(default_factory=dict)
    name: B1Env = B1Env.DEV

    @classmethod
    def load(
        cls,
        env_name: str | None = None,
        configs_dir: str = "configs",
        strict: bool = False,
    ) -> B1Environment:
        """
        Loads a complete environment profile by name.

        The loading order is hierarchical:
        1. Environment Variables (B1SL_*) override everything.
        2. JSON Config file (configs/{env}.json) provides defaults.
        3. If no JSON persists, it defaults to purely environment variables.

        Args:
            env_name (str, optional): Profile name (dev, qa, prod).
                Defaults to B1SL_ENV environment variable, then 'dev'.
            configs_dir (str, optional): Base directory for configuration
                files. Defaults to "configs".
            strict (bool, optional): If True, raises EnvironmentError if
                credentials are missing from environment. Default False.

        Returns:
            B1Environment: A fully populated environment object.
        """
        name = B1Env(env_name or os.getenv("B1SL_ENV", "dev").lower())
        config_path = Path(configs_dir) / f"{name.value}.json"

        # Always start with credentials from OS Environment (.env or system vars)
        # We load in non-strict mode by default to allow loading test_data even without .env
        config = B1Config.from_env(strict=strict)
        config.environment = name
        
        test_data = {}
        if config_path.exists():
            with open(config_path, "r") as f:
                data = json.load(f)
                test_data = data.get("test_data", {})

        return cls(config=config, test_data=test_data, name=name)


