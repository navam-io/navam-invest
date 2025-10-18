# Release 0.1.25

## Status
PUBLISHED

## Bug Fixes

### Fix investment_analysis workflow causing Anthropic API 400 errors

**Problem**: The `/analyze` command caused Anthropic API error 400: "tool_use blocks must have corresponding tool_result block in the next message"

**Root Cause**: The workflow had TWO critical bugs:
1. **Message prepending**: Each agent node prepended `HumanMessage` with system prompt to state["messages"], breaking tool_use/tool_result pairing
2. **Missing tool execution**: Agents could call tools via `bind_tools()` but had no ToolNode to execute them, leaving tool calls unresolved

**What was wrong** (lines 98, 135):
```python
system_msg = HumanMessage(content="You are...")
messages = [system_msg] + state["messages"]  # ❌ Breaks pairing!
response = await llm.ainvoke(messages)
```

**Correct solution**:
1. Use `.bind(system=...)` instead of prepending HumanMessage
2. Add ToolNode for each agent (quill_tools, macro_tools)
3. Add conditional edges to route to tools when needed
4. Loop back to agent after tool execution

**Files Modified**:
- `src/navam_invest/workflows/investment_analysis.py`

**New workflow structure**:
```
START → quill → [tool_calls?] → quill_tools → quill (loop) → macro_lens →
[tool_calls?] → macro_tools → macro_lens (loop) → synthesize → END
```

**Why rollback failed**: v0.1.16 already had this bug in the workflow, so rolling back agents didn't help. The workflow was the actual culprit, not Atlas agent.

---

## Release Date
October 7, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.25/
