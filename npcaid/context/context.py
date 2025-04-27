from typing import List, Optional
import json
from .blocks import ContextBlock


class Context:
    """Generates and manages context for NPCs by combining various ContextBlocks."""

    def __init__(self):
        self.context_blocks: List[ContextBlock] = []


    def add_block(self, block: ContextBlock) -> None:
        """Add a new context block to the generator."""
        self.context_blocks.append(block)

    def remove_block(self, block_type: str) -> None:
        """Remove all blocks of a specific type."""
        self.context_blocks = [b for b in self.context_blocks if b.block_type != block_type]

    def generate_context(self, max_blocks: Optional[int] = None) -> str:
        """
        Generate a context string by combining relevant blocks.

        Args:
            max_blocks: Maximum number of blocks to include (None for all)
        """
        sorted_blocks = sorted(
            self.context_blocks,
            key=lambda x: (-x.priority, x.created_at),
            reverse=True
        )

        if max_blocks is not None:
            sorted_blocks = sorted_blocks[:max_blocks]

        context_parts = []
        for block in sorted_blocks:
            content = block.generate_block_content()
            context_parts.append(f"{block.block_type.upper()}: {json.dumps(content)}")

        return "\n\n".join(context_parts)

    def get_blocks_by_type(self, block_type: str) -> List[ContextBlock]:
        """Get all context blocks of a specific type."""
        return [b for b in self.context_blocks if b.block_type == block_type]

    def __str__(self) -> str:
        """for debugging purposes"""
        return [block.__str__() for block in self.context_blocks].__str__()

