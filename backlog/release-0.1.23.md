# Release 0.1.23

## Status
PUBLISHED

## Bug Fixes

### Fix ModuleNotFoundError for atlas agent

**Problem**: v0.1.22 rolled back atlas.py but left imports in TUI app, causing `ModuleNotFoundError: No module named 'navam_invest.agents.atlas'` when launching the CLI.

**Solution**: Removed all atlas references from TUI app:
- Removed atlas import statement
- Removed atlas agent initialization
- Removed `/atlas` command and help text
- Removed atlas agent selection case
- Removed ATLAS_EXAMPLES constant

**Files Modified**:
- `src/navam_invest/tui/app.py`

---

## Release Date
October 7, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.23/
