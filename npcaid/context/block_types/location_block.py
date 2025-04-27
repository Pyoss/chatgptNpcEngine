from ..blocks import ContextBlock
from .base import BaseBlockType
from typing import Dict, Any


class LocationBlock(BaseBlockType):
    """Block representing an NPC's location context."""

    def __init__(self, current_location: str, nearby_locations: list, priority: int = 2):
        super().__init__("location", priority)
        self.current_location = current_location
        self.nearby_locations = nearby_locations

    def generate_block_content(self) -> Dict[str, Any]:
        """Generate location-specific content."""
        return {
            "current_location": self.current_location,
            "nearby_locations": self.nearby_locations,
            "description": f"Currently at {self.current_location} with {len(self.nearby_locations)} nearby points of interest"
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LocationBlock':
        """Create from serialized data."""
        content = data['content']
        return cls(
            current_location=content['current_location'],
            nearby_locations=content['nearby_locations'],
            priority=data.get('priority', 2)
        )