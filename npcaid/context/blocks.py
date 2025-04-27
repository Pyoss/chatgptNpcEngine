from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any


class IContextBlock(ABC):
    """Interface for context blocks with required methods."""

    @abstractmethod
    def generate_block_content(self) -> Dict[str, Any]:
        """Generate the content dictionary for this block."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize the block to a dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'IContextBlock':
        """Deserialize from a dictionary."""
        pass


class ContextBlock(IContextBlock):
    """Base implementation of a context block."""

    def __init__(self, block_type: str, priority: int = 1):
        self.block_type = block_type
        self.priority = priority
        self.created_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Default serialization implementation."""
        return {
            'type': self.block_type,
            'content': self.generate_block_content(),
            'priority': self.priority,
            'created_at': self.created_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextBlock':
        """Default deserialization implementation."""
        # This will be overridden by specific block types
        raise NotImplementedError("Subclasses should implement their own from_dict")