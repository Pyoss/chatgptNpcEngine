from ..blocks import ContextBlock
from typing import Dict, Any


class BaseBlockType(ContextBlock):
    """Base class for all specific block types with common functionality."""

    def __init__(self, block_type: str, priority: int = 1):
        super().__init__(block_type, priority)

    def generate_block_content(self) -> Dict[str, Any]:
        """Base implementation that specific blocks should override."""
        return {}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseBlockType':
        """Base deserialization that specific blocks can extend."""
        return cls(
            block_type=data['type'],
            priority=data.get('priority', 1)
        )

    def __str__(self):
        return self.to_dict()