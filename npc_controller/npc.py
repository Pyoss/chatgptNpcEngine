from npcaid.context.block_types.dialogue_memory_block import DialogMemoryBlock
from npcaid.context.block_types.location_block import LocationBlock
from npcaid.context.context import Context
from npcaid.dialogue.manager import CurrentDialogue


class NPC:

    def __init__(self, npc_id: str):
        self.dialogue = None
        self.id = npc_id
        self.name = NPC.loadName(npc_id)
        self.context = NPC.loadContext(npc_id)

    def load(self):
        self.name = self

    @classmethod
    def loadName(cls, npc_id: str):
        return 'Иван Иванович'

    @classmethod
    def loadContext(cls, npc_id: str):
        context = Context()
        context.add_block(LocationBlock(
            current_location="Tavern",
            nearby_locations=["Market", "Blacksmith", "Town Square"]
        ))
        context.add_block(DialogMemoryBlock(dialogues=[{
        'with': 'Player1',
        'key_points': ['Asked about the king', 'Mentioned the secret rebellion']
    }]))
        context.generate_context()
        return context

    def open_dialogue(self, initial_prompt):
        self.dialogue = CurrentDialogue(self.id, initial_prompt)
        return self.dialogue



