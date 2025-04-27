from datetime import datetime
from typing import Dict, Optional


class DialogueLine:
    """Represents a single line in a dialogue exchange."""

    def __init__(self, speaker: str, text: str, timestamp: Optional[datetime] = None):
        self.speaker = speaker
        self.text = text
        self.timestamp = timestamp or datetime.now()

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'speaker': self.speaker,
            'text': self.text,
            'timestamp': self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'DialogueLine':
        """Create from dictionary."""
        return cls(
            speaker=data['speaker'],
            text=data['text'],
            timestamp=datetime.fromisoformat(data['timestamp'])
        )