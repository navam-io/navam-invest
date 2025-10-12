# Release 0.1.36

## Status
IN DEVELOPMENT

## Features

### 🚧 Planned Features

**Prompt Routing & Orchestration** - Automatic agent selection based on user intent
- **Router Agent**: LangGraph-based routing agent that analyzes user prompts
- **Intent Classification**: Understands query type (fundamental analysis, risk assessment, tax optimization, etc.)
- **Automatic Agent Selection**: Routes to appropriate specialist agent(s) without manual /command switching
- **Multi-Agent Coordination**: Orchestrates multiple agents when needed (e.g., combining Quill + Macro Lens)
- **Seamless UX**: Users simply ask their question; system handles agent routing automatically
- **Fallback Handling**: Default to general-purpose agent for ambiguous queries
- **Context Preservation**: Maintains conversation context across agent switches

**Implementation Approach**:
- Create `src/navam_invest/agents/router.py` with routing logic
- Use LangChain's routing capabilities with custom routing prompt
- Update TUI to use router as default entry point
- Preserve `/command` syntax for manual agent selection (power users)
- Add routing transparency (show which agent is being used)

**Enhanced Multi-Agent Workflows**
- Extend `/analyze` workflow with additional agents (News Sentry, Risk Shield, Tax Scout)
- Parallel agent execution for faster analysis
- Conditional branching based on agent findings
- Agent communication patterns and state sharing
- Cross-agent data passing and synthesis

**API Caching Layer**
- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation strategies
- Configurable TTL per data source
- Cache statistics and monitoring
- Hit/miss ratio tracking
- Selective cache warming

---

## Technical Improvements

- [ ] Implement router agent with intent classification
- [ ] Refactor TUI to use router as default entry point
- [ ] Add routing transparency (show active agent in status bar)
- [ ] Document routing architecture and customization
- [ ] Refactor agent initialization patterns (reduce code duplication)
- [ ] Add type hints to all tool functions
- [ ] Improve test coverage for TUI components
- [ ] Performance optimization for multi-agent workflows

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
