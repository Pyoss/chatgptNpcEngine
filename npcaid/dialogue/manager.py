from datetime import datetime
from typing import Dict, List, Optional
from .lines import DialogueLine


class CurrentDialogue:
    """Manages an ongoing dialogue session with an NPC."""

    def __init__(self, npc_id: str, initial_prompt: str = ""):
        self.npc_id = npc_id
        self.lines: List[DialogueLine] = []
        self.initial_prompt = initial_prompt
        self.started_at = datetime.now()
        self.ended_at: Optional[datetime] = None

    def add_line(self, speaker: str, text: str) -> None:
        """Add a new line to the dialogue."""
        self.lines.append(DialogueLine(speaker, text))

    def end_dialogue(self) -> None:
        """Mark the dialogue as completed."""
        self.ended_at = datetime.now()

    def is_active(self) -> bool:
        """Check if the dialogue is still active."""
        return self.ended_at is None

    def get_full_transcript(self) -> str:
        """Get the full dialogue transcript as text."""
        lines = [f"{line.speaker}: {line.text}" for line in self.lines]
        return "\n".join(lines)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'npc_id': self.npc_id,
            'initial_prompt': self.initial_prompt,
            'lines': [line.to_dict() for line in self.lines],
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'CurrentDialogue':
        """Create from dictionary."""
        dialogue = cls(
            npc_id=data['npc_id'],
            initial_prompt=data['initial_prompt']
        )
        dialogue.lines = [DialogueLine.from_dict(line) for line in data['lines']]
        dialogue.started_at = datetime.fromisoformat(data['started_at'])
        if data['ended_at']:
            dialogue.ended_at = datetime.fromisoformat(data['ended_at'])
        return dialogue

    def add_to_dialogue(self, name, line):
        self.add_line(name, line)