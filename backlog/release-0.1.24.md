# Release 0.1.24

## Status
PUBLISHED

## Bug Fixes

### Fix add_messages import in investment_analysis workflow

**Problem**: v0.1.22 rollback restored broken import causing:
`ImportError: cannot import name 'add_messages' from 'langchain_core.messages'`

**Root Cause**: The rollback to v0.1.16 restored the incorrect import location. `add_messages` is part of LangGraph, not LangChain Core.

**Solution**:
- Changed import from `langchain_core.messages` to `langgraph.graph`
- This is the same fix that was attempted in v0.1.18 but was rolled back

**Files Modified**:
- `src/navam_invest/workflows/investment_analysis.py`

**Correct Import**:
```python
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph, add_messages
```

---

## Release Date
October 7, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.24/
