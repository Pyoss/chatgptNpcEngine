from .base import BaseBlockType
from typing import Dict, Any, List


class DialogMemoryBlock(BaseBlockType):
    """Block representing memories from past dialogues."""

    def __init__(self, dialogues: List[Dict], priority: int = 3):
        super().__init__("dialog_memory", priority)
        self.dialogues = dialogues

    def generate_block_content(self) -> Dict[str, Any]:
        """Generate dialogue memory content."""
        summary = f"Memories of {len(self.dialogues)} past conversations"
        key_points = []

        for dialog in self.dialogues:
            key_points.append({
                'with': dialog.get('with', 'unknown'),
                'points': dialog.get('key_points', [])
            })

        return {
            "summary": summary,
            "key_points": key_points
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogMemoryBlock':
        """Create from serialized data."""
        content = data['content']
        return cls(
            dialogues=content['key_points'],
            priority=data.get('priority', 3)
        )