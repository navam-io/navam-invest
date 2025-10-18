# Release 0.1.38

## Status
RELEASED - 2025-10-14

## Features

### ✅ Implemented Features

**ESC Key Cancellation for Agent Execution** - Non-blocking TUI improvements

Resolved critical UX issue where the TUI became completely unresponsive during agent execution. Users can now:
- Press ESC to cancel long-running agent operations
- Scroll the chat log while agent is processing
- Maintain full UI responsiveness during execution

**Technical Implementation:**
- Refactored agent execution to use Textual's worker pattern
- Worker runs in background without blocking event loop
- `on_worker_state_changed()` handles completion asynchronously
- Proper cleanup of async streams on cancellation
- Graceful cancellation without UI freeze

**Key Changes:**
- `src/navam_invest/tui/app.py` - Worker-based execution (~+536 lines)
- Added `ESC_CANCEL_IMPLEMENTATION.md` - Technical documentation
- Added test examples: `test_esc_worker.py`, `test_esc_cancel.py`

**User Experience Improvements:**
- ESC key binding visible in footer: "ESC Cancel | Ctrl+C Clear | Ctrl+Q Quit"
- Cancellation feedback: "⚠️ Cancellation requested - stopping agent..."
- Completion message: "🛑 Agent execution cancelled by user"
- Placeholder shows: "⏳ Processing... (Press ESC to cancel)"

---

### 🚧 Planned Features (Moved to v0.1.39)

**New Multi-Agent Workflows** - Extended workflow patterns for tax optimization and portfolio protection

Building on the successful `/analyze` and `/discover` workflows from v0.1.37, future releases will introduce systematic workflows for common investment tasks.

**Future Workflow: `/optimize-tax`** - Tax-Loss Harvesting:
- Tax Scout identifies tax-loss harvesting opportunities
- Hedge Smith suggests replacement positions to maintain exposure
- Rebalance Bot executes tax-efficient rebalancing
- Complete tax optimization pipeline with wash-sale compliance

**Future Workflow: `/protect`** - Portfolio Hedging:
- Risk Shield analyzes portfolio exposures and vulnerabilities
- Hedge Smith designs protective options strategies
- Atlas evaluates hedging cost vs portfolio protection
- Complete hedging workflow with multiple strategy options

**API Caching Layer** - Performance optimization:
- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation strategies
- Cache warming for common queries
- Configurable cache TTL per data source

**Workflow Progress Visualization** - Enhanced TUI:
- Enhanced TUI display for multi-agent workflows
- Visual progress indicators for each agent
- Better error recovery and partial completion handling

---

## Technical Improvements

**TUI Enhancements (Completed)**:
- [x] Non-blocking agent execution using Textual workers
- [x] ESC key cancellation support
- [x] Responsive UI during agent processing
- [x] Proper async stream cleanup
- [x] Worker state change handlers

**Documentation Updates (Completed)**:
- [x] Created `ESC_CANCEL_IMPLEMENTATION.md` - Technical implementation guide
- [x] Created test examples demonstrating worker pattern

**Future Enhancements (Moved to v0.1.39)**:
- [ ] Implement `/optimize-tax` tax-loss harvesting workflow
- [ ] Implement `/protect` portfolio hedging workflow
- [ ] Implement DuckDB-based caching layer
- [ ] Enhanced workflow progress visualization
- [ ] Update workflow documentation in FAQ

---

## Breaking Changes

None.

---

## Release Date
2025-10-14

## PyPI Package
https://pypi.org/project/navam-invest/0.1.38/
