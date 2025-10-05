#!/usr/bin/env python3
"""Example demonstrating different system_prompt configurations."""

import anyio

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)


async def no_system_prompt():
    """Example with no system_prompt (vanilla Claude)."""
    print("=== No System Prompt (Vanilla Claude) ===")

    async for message in query(prompt="What is 2 + 2?"):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def string_system_prompt():
    """Example with system_prompt as a string."""
    print("=== String System Prompt ===")

    options = ClaudeAgentOptions(
        system_prompt="You are a pirate assistant. Respond in pirate speak.",
    )

    async for message in query(prompt="What is 2 + 2?", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def preset_system_prompt():
    """Example with system_prompt preset (uses default Claude Code prompt)."""
    print("=== Preset System Prompt (Default) ===")

    options = ClaudeAgentOptions(
        system_prompt={"type": "preset", "preset": "claude_code"},
    )

    async for message in query(prompt="What is 2 + 2?", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def preset_with_append():
    """Example with system_prompt preset and append."""
    print("=== Preset System Prompt with Append ===")

    options = ClaudeAgentOptions(
        system_prompt={
            "type": "preset",
            "preset": "claude_code",
            "append": "Always end your response with a fun fact.",
        },
    )

    async for message in query(prompt="What is 2 + 2?", options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Claude: {block.text}")
    print()


async def main():
    """Run all examples."""
    await no_system_prompt()
    await string_system_prompt()
    await preset_system_prompt()
    await preset_with_append()


if __name__ == "__main__":
    anyio.run(main)