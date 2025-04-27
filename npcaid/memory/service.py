import json
from typing import Dict, List, Optional
from datetime import datetime
from ..context.blocks import ContextBlock
from ..dialogue.manager import CurrentDialogue


class MemoryService:
    """Stores and retrieves NPC memories (context blocks and past dialogues)."""

    def __init__(self, storage_path: str = "npc_memory.json"):
        self.storage_path = storage_path
        self.past_dialogues: Dict[str, List[CurrentDialogue]] = {}

    def save_dialogue(self, dialogue: CurrentDialogue) -> None:
        """Store a completed dialogue."""
        if not dialogue.npc_id in self.past_dialogues:
            self.past_dialogues[dialogue.npc_id] = []
        self.past_dialogues[dialogue.npc_id].append(dialogue)
        self._save_to_disk()

    def get_past_dialogues(self, npc_id: str, limit: Optional[int] = None) -> List[CurrentDialogue]:
        """Retrieve past dialogues for an NPC, most recent first."""
        dialogues = self.past_dialogues.get(npc_id, [])
        dialogues.sort(key=lambda d: d.started_at, reverse=True)
        if limit is not None:
            dialogues = dialogues[:limit]
        return dialogues

    def _save_to_disk(self) -> None:
        """Save all data to disk."""
        data = {
            'past_dialogues': {
                npc_id: [dialogue.to_dict() for dialogue in dialogues]
                for npc_id, dialogues in self.past_dialogues.items()
            }
        }
        with open(self.storage_path, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_disk(self) -> None:
        """Load data from disk."""
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)

            self.past_dialogues = {
                npc_id: [CurrentDialogue.from_dict(dialogue) for dialogue in dialogues]
                for npc_id, dialogues in data.get('past_dialogues', {}).items()
            }
        except FileNotFoundError:
            # First run, no data to load
            pass