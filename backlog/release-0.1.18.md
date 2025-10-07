# Release 0.1.18

## Status
Published to PyPI on October 6, 2025

## Bugfix Release

This is a hotfix release addressing a critical import error in v0.1.17.

### Critical Fix

**Import Error Resolution** (`src/navam_invest/workflows/investment_analysis.py`)
- **Issue**: `add_messages` incorrectly imported from `langchain_core.messages`
- **Fix**: Changed import to `langgraph.graph.add_messages` (consistent with all agent files)
- **Impact**: Resolves `ImportError` that prevented package from running after installation
- **Root Cause**: Inconsistent import statement in workflow file vs agent files

**Changes**:
```python
# Before (incorrect)
from langchain_core.messages import AIMessage, HumanMessage, add_messages

# After (correct)
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph, add_messages
```

**Testing**: All 48 tests pass with the corrected import

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.18/
