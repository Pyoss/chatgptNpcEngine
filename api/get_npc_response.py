import requests  # Required for DeepSeek API calls
from typing import Optional, Dict, Any

from npc_controller.npc import NPC


def get_npc_response(
        npc: NPC,
        player_input: str,
        player_name: str = "Player",
        initial_prompt: Optional[str] = None,
        max_context_blocks: Optional[int] = None,
        model: str = "deepseek-chat",  # DeepSeek model name
        temperature: float = 0.7,
        max_tokens: int = 150,
        api_key: Optional[str] = None,  # Your DeepSeek API key
        api_base_url: str = "https://api.deepseek.com/v1"  # DeepSeek API endpoint
) -> str:
    """
    Get an NPC's response using context and dialogue history with DeepSeek API.

    Args:
        npc: NPC,
        player_input: The player's input text
        player_name: Name of the player character
        initial_prompt: Optional initial prompt for new dialogues
        max_context_blocks: Max context blocks to include (None for all)
        model: DeepSeek model name (default: "deepseek-chat")
        temperature: Creativity parameter (0-1)
        max_tokens: Maximum length of response
        api_key: Your DeepSeek API key (required)
        api_base_url: DeepSeek API base URL

    Returns:
        The NPC's generated response
    """
    if not api_key:
        raise ValueError("DeepSeek API key is required!")

    # Get or create the current dialogue
    current_dialogue = npc.dialogue
    if not current_dialogue:
        initial_prompt = initial_prompt or f"{npc.id} engages in conversation with {player_name}"
        current_dialogue = npc.open_dialogue(initial_prompt)

    # Add the player's input to the dialogue
    current_dialogue.add_to_dialogue(player_name, player_input)



    # Prepare the AI prompt (DeepSeek API expects a 'messages' list)
    messages = [
        {
            "role": "system",
            "content": f"""You are roleplaying as {npc.name}. Stay in character based on the following context:

            NPC Context:
            {npc.context}

            Current Conversation:
            {npc.dialogue.get_full_transcript()}

            Instructions:
            - Respond naturally as {npc.name} would.
            - Keep responses under {max_tokens} tokens.
            - Do not break character or mention AI."""
        },
        {
            "role": "user",
            "content": player_input
        }
    ]

    # Call the DeepSeek API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(
            f"{api_base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()  # Raise error if API call fails
        npc_response = response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        npc_response = f"(Sorry, I can't respond right now: {str(e)})"

    # Add the NPC's response to the dialogue
    npc.dialogue.add_to_dialogue(npc.name, npc_response)

    return npc_response