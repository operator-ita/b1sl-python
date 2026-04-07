from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Result(BaseModel):
    status_code: int
    message: str = ""
    data: dict | None = None
    next_link: str | None = None
    next_params: dict | None = None
    metadata: str | None = None

    # Update configuration for Pydantic V2
    model_config = ConfigDict(
        extra="allow"  # Allows extra fields not explicitly defined
    )
