from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Type

if TYPE_CHECKING:
    from b1sl.b1sl.models.base import B1Model

@dataclass
class BatchResult:
    """Individual result of an operation within a batch."""
    status: int
    data: Any = None
    error: str | None = None
    model_type: Type[B1Model] | None = None
    index: int = 0  # Original position in the batch

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

    @property
    def entity(self) -> Any:
        """Returns the parsed data as a Pydantic model if available."""
        if self.ok and self.model_type and isinstance(self.data, (dict, list)):
            if isinstance(self.data, list):
                return [self.model_type.model_validate(item) for item in self.data]
            # Special case: SAP sometimes returns the object in a 'value' node or directly
            val = self.data.get("value", self.data) if isinstance(self.data, dict) else self.data
            if isinstance(val, list):
                return [self.model_type.model_validate(item) for item in val]
            return self.model_type.model_validate(val)
        return self.data

class BatchResults:
    """Intelligent container for the results of a complete batch."""
    def __init__(self, results: list[BatchResult]):
        self.results = results

    @property
    def all_ok(self) -> bool:
        return all(r.ok for r in self.results)

    @property
    def failed(self) -> list[BatchResult]:
        """Returns only the failed operations, preserving their original index."""
        return [r for r in self.results if not r.ok]

    def __len__(self):
        return len(self.results)

    def __getitem__(self, idx: int) -> BatchResult:
        return self.results[idx]

    def __iter__(self):
        return iter(self.results)
