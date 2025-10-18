# Release 0.1.19

## Status
Published to PyPI on October 6, 2025

## Critical Bugfix Release

This release fixes a critical runtime error introduced in v0.1.17 that caused Anthropic API 400 errors during agent tool execution.

### System Message Fix

**Issue**: All 6 agents incorrectly used `HumanMessage` for system prompts instead of `SystemMessage`
- **Impact**: Caused Anthropic API error 400 - `invalid_request_error` related to tool_use IDs
- **Root Cause**: System prompts prepended as HumanMessage created invalid message sequences for tool-calling
- **Severity**: Critical - prevented all agent tool execution

**Fix Applied** (All 6 agents):
- Changed `from langchain_core.messages import HumanMessage` → `SystemMessage`
- Changed `system_msg = HumanMessage(...)` → `system_msg = SystemMessage(...)`

**Files Fixed**:
1. `src/navam_invest/agents/atlas.py`
2. `src/navam_invest/agents/portfolio.py`
3. `src/navam_invest/agents/research.py`
4. `src/navam_invest/agents/quill.py`
5. `src/navam_invest/agents/screen_forge.py`
6. `src/navam_invest/agents/macro_lens.py`

**Testing**: All 48 tests pass, proper message format now used for Anthropic API

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.19/
