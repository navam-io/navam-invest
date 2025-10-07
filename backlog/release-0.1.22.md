# Release 0.1.22

## Status
IN DEVELOPMENT

## Critical Rollback

**Problem**: Releases v0.1.17 through v0.1.21 introduced critical bugs with Anthropic API tool_use/tool_result message pairing. Multiple fix attempts failed to resolve the issue.

**Solution**: Complete rollback to v0.1.16 (last known working version).

**What was rolled back**:
- All agent implementations restored to v0.1.16 state
- Atlas investment strategist agent removed (introduced in v0.1.17)
- Investment analysis workflow restored to v0.1.16
- All agents now use HumanMessage for system prompts (v0.1.16 pattern)

**Failed versions** (DO NOT USE):
- v0.1.17: Added Atlas agent, introduced bug
- v0.1.18: Import fix attempt
- v0.1.19: SystemMessage conversion attempt
- v0.1.20: First-call-only prepending attempt
- v0.1.21: bind(system=...) attempt

**Current agent roster** (v0.1.16 baseline):
- Portfolio Analysis agent
- Research agent
- Quill equity research agent
- Screen Forge screening agent
- Macro Lens strategist agent

**Next steps**:
- Investigate root cause of tool_use/tool_result pairing errors
- Test v0.1.22 thoroughly before adding new features
- Re-implement Atlas agent with proper fix once root cause identified

---

## Release Date
October 7, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.22/
