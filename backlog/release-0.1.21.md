# Release 0.1.21

## Status
IN DEVELOPMENT

## Bug Fixes

### Critical Fix: Anthropic API Tool-Use/Tool-Result Pairing

**Problem**: All agents were experiencing Anthropic API error 400: "tool_use blocks must have corresponding tool_result block in the next message"

**Root Cause**: ChatAnthropic expects system prompts via `.bind(system=...)` parameter, NOT as SystemMessage objects in the messages array. Previous implementations (v0.1.18-v0.1.20) were incorrectly prepending SystemMessage to the messages list, which broke the tool_use/tool_result message pairing required by Anthropic's API.

**Failed Approaches**:
- v0.1.18: Fixed import location but kept SystemMessage in messages
- v0.1.19: Changed HumanMessage to SystemMessage (still in messages array)
- v0.1.20: Only prepended SystemMessage on first call (still broke pairing on subsequent calls)

**Correct Solution** (v0.1.21):
```python
# BEFORE (BROKEN):
system_msg = SystemMessage(content="You are...")
messages = state["messages"]
if not messages or messages[0].type != "system":
    messages = [system_msg] + messages
response = await llm_with_tools.ainvoke(messages)

# AFTER (FIXED):
system_prompt = "You are..."
llm_with_tools = llm.bind_tools(tools).bind(system=system_prompt)
response = await llm_with_tools.ainvoke(state["messages"])
```

**Files Fixed**:
- `src/navam_invest/agents/atlas.py`
- `src/navam_invest/agents/portfolio.py`
- `src/navam_invest/agents/research.py`
- `src/navam_invest/agents/quill.py`
- `src/navam_invest/agents/screen_forge.py`
- `src/navam_invest/agents/macro_lens.py`

**Technical Details**:
- System prompts are now bound to the LLM instance, not included in conversation messages
- Messages array contains only user/assistant/tool messages for proper API pairing
- This aligns with LangChain Anthropic integration best practices

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.21/
