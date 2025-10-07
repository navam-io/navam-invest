# Release 0.1.20

## Status
Published to PyPI on October 6, 2025

## Critical Bugfix Release

This release fixes the root cause of the Anthropic API 400 error - system messages were being prepended on every agent call, breaking tool_use/tool_result message pairing.

### System Message Prepending Fix

**Issue**: System messages prepended on EVERY call to `call_model`, not just the first call
- **Impact**: Anthropic API error 400 - `tool_use` blocks need corresponding `tool_result` in next message
- **Root Cause**: Prepending SystemMessage on every call created invalid message sequences during tool execution
- **Severity**: Critical - prevented all tool-calling workflows from functioning

**Problem Flow**:
1. First call: `[SystemMsg, HumanMsg]` → AI makes tool_call
2. ToolNode adds result: `[HumanMsg, AIMsg(tool_calls), ToolResultMsg]`
3. Second call: Prepend AGAIN → `[SystemMsg, HumanMsg, AIMsg(tool_calls), ToolResultMsg]`
4. Anthropic sees new SystemMsg breaking the tool_call/result pairing

**Fix Applied** (All 6 agents):
```python
# Before (WRONG - prepends every time)
messages = [system_msg] + state["messages"]

# After (CORRECT - only on first call)
messages = state["messages"]
if not messages or messages[0].type != "system":
    messages = [system_msg] + messages
```

**Files Fixed**:
1. `src/navam_invest/agents/atlas.py`
2. `src/navam_invest/agents/portfolio.py`
3. `src/navam_invest/agents/research.py`
4. `src/navam_invest/agents/quill.py`
5. `src/navam_invest/agents/screen_forge.py`
6. `src/navam_invest/agents/macro_lens.py`

**Testing**: All 48 tests pass, tool-calling workflows now function correctly

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.20/
