# Release 0.1.36

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

**Prompt Routing & Orchestration** - Automatic agent selection based on user intent

**Vision**: Transform Navam Invest from **manual agent switching** (`/command` syntax) to **automatic intent-based routing**. Users simply ask their question naturally, and the system intelligently routes to the appropriate specialist agent(s).

**Current State → Target State:**

*Current UX (Manual)*:
```
User: "Should I invest in AAPL?"
→ User must decide: /quill for fundamentals? /macro for timing? /risk for exposure?
→ User manually switches: /quill
User: "Analyze AAPL fundamentals"
User: (switches) /macro
User: "Is now a good time to invest?"
```

*Target UX (Automatic)*:
```
User: "Should I invest in AAPL?"
→ Router Agent analyzes intent → Coordinates Quill + Macro Lens + Risk Shield
→ System: "I'll analyze AAPL from multiple angles..."
→ [Parallel execution: Fundamental analysis + Macro timing + Risk assessment]
→ System: "Based on comprehensive analysis across fundamental, macro, and risk dimensions..."
```

**Router Agent Architecture** (Tool-Calling Supervisor Pattern):
- **10 Agent Tools**: Each specialist agent exposed as a tool with clear intent descriptions
- **LLM-Based Routing**: Supervisor LLM classifies user intent and selects appropriate agent(s)
- **Parallel Execution**: Can invoke multiple agents simultaneously for multi-faceted queries
- **Transparent Reasoning**: Supervisor explains which agents it's using and why
- **Fallback Handling**: Routes ambiguous queries to general Portfolio agent

**Intent Classification Examples**:
- "Should I buy AAPL?" → Quill (fundamentals) + Macro Lens (timing) + Risk Shield (exposure)
- "Find undervalued growth stocks" → Screen Forge
- "Tax-loss harvest opportunities" → Tax Scout
- "Protect my NVDA position" → Hedge Smith
- "Is recession risk high?" → Macro Lens
- "TSLA earnings analysis" → Earnings Whisperer
- "Material events for META" → News Sentry
- "Portfolio risk assessment" → Risk Shield

**Implementation Files**:
- `src/navam_invest/agents/router.py` - Router supervisor agent with tool wrappers for all 10 agents
- `tests/test_router.py` - Comprehensive testing (20+ intent classification tests, 10+ single-agent routing, 5+ multi-agent coordination)
- `src/navam_invest/tui/app.py` - Integration with router as default entry point

**Backward Compatibility**:
- All existing `/command` syntax continues to work (e.g., `/quill`, `/hedge`, `/risk`)
- Manual agent switching bypasses router for power users
- Router only active when no manual agent selected

**TUI Enhancements**:
- Status bar transparency: "Router: → Quill + Macro Lens | Processing"
- Display which agents are being invoked during routing
- Show "Routing to: [Agent Name]..." messages
- Preserve manual mode display: "Manual: Quill | Ready"

**Success Metrics**:
- ✅ 95%+ intent classification accuracy
- ✅ <2 second routing overhead
- ✅ Zero-friction prompting (no need to know which agent to use)
- ✅ Transparent routing (users understand which agents are active)

---

## Technical Improvements

**Router Implementation (Phase 1)**: ✅ COMPLETED
- [x] Create `src/navam_invest/agents/router.py` with tool-calling supervisor pattern
- [x] Implement 10 agent tool wrappers (route_to_quill, route_to_risk_shield, etc.)
- [x] Create supervisor LLM with comprehensive routing system prompt
- [x] Add intent classification logic with clear agent selection criteria
- [x] Implement multi-agent coordination patterns for complex queries

**Testing (Phase 1)**: ✅ COMPLETED
- [x] Create `tests/test_router.py` with comprehensive test suite (16 tests, all passing)
- [x] Test agent creation and tool registration (2 tests)
- [x] Test intent classification for all 10 agents (10 tests)
- [x] Test error handling with graceful fallback (1 test)
- [x] Test agent instance caching (2 tests)
- [x] Test router agent structure (1 test)

**TUI Integration (Phase 1)**:
- [ ] Add router agent initialization in `app.py::on_mount()`
- [ ] Modify `on_input_submitted()` to route through router by default
- [ ] Preserve `/command` syntax for manual agent selection
- [ ] Add routing transparency in status bar (show active agent)
- [ ] Display "Routing to: [Agent Name]..." during agent selection
- [ ] Show multi-agent coordination progress

**Documentation Updates**:
- [ ] Update `docs/user-guide/getting-started.md` - New UX flow with router
- [ ] Update `docs/user-guide/agents.md` - Router agent description
- [ ] Update `docs/faq.md` - Add router FAQs (How does routing work? Can I still use /commands?)
- [ ] Update `README.md` - New UX examples showing automatic routing
- [ ] Update `CLAUDE.md` - Router architecture patterns and LangGraph supervisor pattern
- [ ] Create `docs/architecture/routing.md` - Router design doc with intent classification logic

**Future Phases (v0.1.37-0.1.38)**:
- [ ] Extended multi-agent workflows (Phase 2)
- [ ] API caching layer with DuckDB (Phase 3)
- [ ] Performance optimization and monitoring (Phase 3)

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
