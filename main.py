from api.get_npc_response import get_npc_response
from npc_controller.npc import NPC
from dotenv import load_dotenv
import os

# Load .env file from the root directory
load_dotenv()  # Looks for .env in the current working directory

# Access variables
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

npc = NPC(1)
response = get_npc_response(
    npc=npc,
    player_input="Can you sharpen my sword?",
    player_name="Warrior",
    api_key=DEEPSEEK_API_KEY,  # Required
    temperature=0.5  # Less randomness for consistent NPC behavior
)

print(f"{npc.id}: {response}")