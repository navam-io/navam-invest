# Active Backlog

## 🚀 PIVOT: Prompt Routing & Orchestration (v0.1.36)

### Vision
Transform Navam Invest from **manual agent switching** (`/command` syntax) to **automatic intent-based routing**. Users simply ask their question naturally, and the system intelligently routes to the appropriate specialist agent(s).

### Current State Analysis

**Architecture:**
- 10 specialized AI agents (Quill, Screen Forge, Macro Lens, Earnings Whisperer, News Sentry, Risk Shield, Tax Scout, Hedge Smith, Portfolio, Research)
- Manual agent activation via `/command` syntax (e.g., `/quill`, `/hedge`, `/risk`)
- TUI stores `current_agent` state and switches context explicitly
- Each agent: LangGraph StateGraph with custom system prompts and specialized tool sets

**User Experience Pain Points:**
1. Users must know which agent to activate for their question
2. Requires understanding of agent capabilities and specializations
3. Multi-faceted questions require manual switching between agents
4. No automatic coordination when multiple agents could contribute

**Example Current UX:**
```
User: "Should I invest in AAPL?"
→ User must decide: /quill for fundamentals? /macro for timing? /risk for exposure?
→ User manually switches: /quill
User: "Analyze AAPL fundamentals"
User: (switches) /macro
User: "Is now a good time to invest?"
```

### Target State Vision

**Ideal User Experience:**
```
User: "Should I invest in AAPL?"
→ Router Agent analyzes intent → Coordinates Quill + Macro Lens + Risk Shield
→ System: "I'll analyze AAPL from multiple angles..."
→ [Parallel execution: Fundamental analysis + Macro timing + Risk assessment]
→ System: "Based on comprehensive analysis across fundamental, macro, and risk dimensions..."
```

**Key Benefits:**
- ✅ Zero learning curve - just ask questions naturally
- ✅ Automatic multi-agent coordination for complex queries
- ✅ Optimal agent selection based on intent classification
- ✅ Preserve `/command` syntax for power users who want manual control
- ✅ Transparent routing (show which agents are being used)

### LangGraph Architecture Patterns (Research Findings)

From `refer/langgraph/guides/multi-agent.md` and `refer/langgraph/concepts/agentic-concepts.md`:

**Best Architecture for Navam Invest: Tool-Calling Supervisor**

Why this pattern fits:
1. **Clear delegation**: Supervisor LLM decides which specialist agents to invoke
2. **Natural composition**: Each agent exposed as a tool with clear description
3. **Parallel execution**: Can call multiple agents simultaneously when needed
4. **Transparent reasoning**: Supervisor explains which agents it's using and why
5. **Fallback handling**: Supervisor can route to general Portfolio agent for ambiguous queries

**Implementation Pattern:**
```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent

# Define agents as tools
@tool
def quill_agent_tool(query: str) -> str:
    """Deep fundamental equity analysis with investment thesis.

    Use this for: Company valuation, DCF analysis, financial statement analysis,
    investment recommendations, fair value estimates.

    Args:
        query: Investment analysis question about a specific stock
    """
    result = quill_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

@tool
def risk_shield_tool(query: str) -> str:
    """Portfolio risk analysis and exposure monitoring.

    Use this for: Portfolio risk assessment, concentration analysis, VAR calculations,
    drawdown analysis, position size checks.

    Args:
        query: Risk management or portfolio analysis question
    """
    result = risk_shield_agent.invoke({"messages": [{"role": "user", "content": query}]})
    return result["messages"][-1].content

# Supervisor with agent tools
router_supervisor = create_react_agent(
    model=supervisor_llm,
    tools=[
        quill_agent_tool,
        macro_lens_tool,
        screen_forge_tool,
        earnings_whisperer_tool,
        news_sentry_tool,
        risk_shield_tool,
        tax_scout_tool,
        hedge_smith_tool,
        portfolio_tool,  # Fallback general-purpose agent
    ],
    name="InvestmentSupervisor"
)
```

**Supervisor System Prompt:**
```
You are an Investment Advisory Supervisor coordinating a team of 10 specialized AI agents.

Your role:
1. Understand the user's investment question and intent
2. Classify the query type (fundamental analysis, risk assessment, tax planning, etc.)
3. Select the appropriate specialist agent(s) to handle the query
4. Coordinate multi-agent responses when questions span multiple domains
5. Synthesize results from multiple agents into coherent recommendations

Available Specialist Agents:
- Quill: Fundamental equity analysis, investment thesis, valuation (DCF, comps)
- Screen Forge: Equity screening, factor-based stock discovery, shortlist generation
- Macro Lens: Top-down market analysis, sector allocation, regime assessment
- Earnings Whisperer: Earnings analysis, surprises, post-earnings drift opportunities
- News Sentry: Material event monitoring, insider trading alerts, news filtering
- Risk Shield: Portfolio risk analysis, VAR, drawdown, concentration monitoring
- Tax Scout: Tax-loss harvesting, wash-sale compliance, year-end tax planning
- Hedge Smith: Options strategies, protective collars, covered calls, put protection
- Portfolio: General portfolio questions (fallback for ambiguous queries)
- Research: Macroeconomic indicators, FRED data (fallback for macro queries)

Intent Classification Examples:
- "Should I buy AAPL?" → Quill (fundamentals) + Macro Lens (timing) + Risk Shield (exposure)
- "Find undervalued growth stocks" → Screen Forge
- "Tax-loss harvest opportunities" → Tax Scout
- "Protect my NVDA position" → Hedge Smith
- "Is recession risk high?" → Macro Lens
- "TSLA earnings analysis" → Earnings Whisperer
- "Material events for META" → News Sentry
- "Portfolio risk assessment" → Risk Shield

Coordination Strategies:
- Single-agent queries: Route directly to specialist
- Multi-faceted queries: Coordinate 2-3 relevant agents in parallel
- Ambiguous queries: Route to Portfolio (general) or ask clarifying questions
- Complex workflows: Sequence agents (e.g., Screen Forge → Quill → Risk Shield)

Always explain which agent(s) you're using and why, to maintain transparency.
```

### Implementation Plan

#### Phase 1: Router Agent Foundation (v0.1.36 - Week 1)

**Files to Create:**
- [x] `src/navam_invest/agents/router.py` - Router supervisor agent implementation (479 lines) ✅ COMPLETED
- [x] `tests/test_router.py` - Comprehensive router testing (16 tests, all passing) ✅ COMPLETED

**Files to Modify:**
- [x] `src/navam_invest/tui/app.py` - Integrate router as default entry point ✅ COMPLETED (Phase 1b)
- [x] `src/navam_invest/agents/router.py` - Enable progressive disclosure of sub-agent tool calls ✅ COMPLETED (Phase 1c)
- [ ] `src/navam_invest/tools/__init__.py` - Add agent tool wrappers if needed

**Implementation Steps:**

1. **Create Router Agent** (`router.py`)
   - Implement tool wrappers for each specialist agent
   - Create supervisor LLM with routing system prompt
   - Build intent classification logic
   - Add fallback handling for ambiguous queries
   - Implement multi-agent coordination patterns

2. **Test Router** (`test_router.py`)
   - Test single-agent routing (10 test cases, one per agent)
   - Test multi-agent coordination (5 test cases)
   - Test ambiguous query fallback (3 test cases)
   - Test intent classification accuracy (20 test cases)
   - Test error handling (agent failures, timeouts)

3. **TUI Integration** (`app.py`) ✅ COMPLETED
   - ✅ Add router agent initialization in `on_mount()`
   - ✅ Modify `on_input_submitted()` to route through router by default
   - ✅ Preserve `/command` syntax for manual agent selection
   - ✅ Add routing transparency in status bar (show active agent)
   - ✅ Implement `/router on|off` command for toggle
   - ✅ Manual agent commands disable router mode automatically
   - ✅ Update welcome message to emphasize automatic routing
   - ✅ Update `/help` command with router control section

4. **Status Bar Enhancement** ✅ COMPLETED
   - ✅ "Router: Active | Ready" when router_mode=True
   - ✅ "Manual: [Agent] | Ready" when router_mode=False
   - ✅ Shows routing intent during processing with "🔀 Router analyzing..."

5. **Progressive Disclosure Enhancement** (`router.py`, `app.py`) ✅ COMPLETED (Phase 1c)
   - ✅ Created `_stream_agent_with_tool_log()` helper function
   - ✅ Refactored all 10 router tools to stream sub-agent execution
   - ✅ Collect tool call information during streaming
   - ✅ Return formatted strings with `[TOOL CALLS]` + `[ANALYSIS]` sections
   - ✅ TUI parses ToolMessage content to extract and display sub-agent tool calls
   - ✅ Display tool names and arguments with proper indentation (6 spaces)
   - ✅ Users now see full transparency: router tools → sub-agent tools → results

6. **True Progressive Streaming** (`router.py`, `app.py`) ✅ COMPLETED (Phase 1d)
   - ✅ Implemented AsyncIO queue-based streaming architecture
   - ✅ Router pushes tool call events to queue as they occur (non-blocking)
   - ✅ TUI background consumer displays events in real-time
   - ✅ Proper task lifecycle management (start/stop with query)
   - ✅ Tool calls now stream progressively, not in batches
   - ✅ Works correctly with parallel multi-agent execution
   - ✅ Graceful error handling and task cancellation

**Example TUI Flow:**
```
User: "Should I invest in TSLA?"
Status: Router: Active | Processing
Chat: [Router] Analyzing your question... routing to Quill (fundamentals) + Macro Lens (timing)
Status: Router: → Quill + Macro Lens | Processing
Chat: [Quill] Analyzing TSLA fundamentals...
      [Macro Lens] Assessing market timing...
      [Router] Synthesizing recommendation...
```

**Backward Compatibility:**
- All existing `/command` syntax continues to work
- Manual agent switching bypasses router
- Power users can use `/quill`, `/hedge`, etc. directly
- Router only active when no manual agent selected

#### Phase 2: Enhanced Multi-Agent Workflows (v0.1.37)

**Extend Existing `/analyze` Workflow:**
- Add News Sentry (material events, insider trading)
- Add Risk Shield (portfolio fit, concentration risk)
- Add Tax Scout (tax implications if selling/buying)

**New Workflows:**
- `/discover` - Systematic idea generation (Screen Forge → Quill → Risk Shield)
- `/optimize-tax` - Tax-loss harvesting workflow (Tax Scout → Hedge Smith for replacement positions)
- `/protect` - Portfolio hedging workflow (Risk Shield → Hedge Smith for protection strategies)

#### Phase 3: API Caching Layer (v0.1.38)

- DuckDB-based caching to reduce API calls
- Intelligent cache invalidation
- Cache warming for common queries

### Technical Implementation Notes

**Router Agent Tool Pattern:**
```python
from langchain_core.tools import tool

@tool
async def route_to_quill(query: str) -> str:
    """Route to Quill for fundamental equity analysis.

    Use when: User asks about company valuation, investment thesis, financial analysis,
    fair value estimates, DCF models, or investment recommendations.

    Args:
        query: The user's investment analysis question
    """
    try:
        result = await quill_agent.ainvoke({"messages": [HumanMessage(content=query)]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: Quill agent failed - {str(e)}"

@tool
async def route_to_risk_shield(query: str) -> str:
    """Route to Risk Shield for portfolio risk analysis.

    Use when: User asks about portfolio risk, concentration, VAR, drawdown,
    position sizing, or risk mitigation strategies.

    Args:
        query: The user's risk management question
    """
    try:
        result = await risk_shield_agent.ainvoke({"messages": [HumanMessage(content=query)]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Error: Risk Shield agent failed - {str(e)}"

# ... similar for all 10 agents
```

**Supervisor Agent Creation:**
```python
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

async def create_router_agent() -> StateGraph:
    """Create router supervisor agent for intent-based routing."""
    settings = get_settings()

    # Use a powerful model for routing decisions
    supervisor_llm = ChatAnthropic(
        model=settings.anthropic_model,
        api_key=settings.anthropic_api_key,
        temperature=0.1,  # Lower temperature for consistent routing
        max_tokens=8192,
    )

    # Create all agent tools
    agent_tools = [
        route_to_quill,
        route_to_screen_forge,
        route_to_macro_lens,
        route_to_earnings_whisperer,
        route_to_news_sentry,
        route_to_risk_shield,
        route_to_tax_scout,
        route_to_hedge_smith,
        route_to_portfolio,  # Fallback
        route_to_research,   # Fallback
    ]

    # Create supervisor with routing prompt
    router = create_react_agent(
        model=supervisor_llm,
        tools=agent_tools,
        state_schema=RouterState,
    )

    return router
```

### Success Metrics

**User Experience:**
- ✅ Zero-friction prompting (no need to know which agent to use)
- ✅ Automatic multi-agent coordination for complex queries
- ✅ Transparent routing (users understand which agents are being used)
- ✅ Backward compatible (all `/command` syntax preserved)

**Technical:**
- ✅ 95%+ intent classification accuracy (validated via test suite)
- ✅ <2 second routing overhead (agent selection time)
- ✅ Graceful fallback handling (ambiguous queries → Portfolio agent)
- ✅ Error recovery (agent failures don't break entire flow)

**Testing Coverage:**
- ✅ 20+ intent classification test cases
- ✅ 10+ single-agent routing tests
- ✅ 5+ multi-agent coordination tests
- ✅ 5+ error handling tests

### Release Strategy

**v0.1.36: Router Foundation**
- Router agent implementation
- TUI integration with router as default
- Preserve manual agent switching
- Documentation updates

**v0.1.37: Enhanced Workflows**
- Extended `/analyze` with more agents
- New workflows (`/discover`, `/optimize-tax`, `/protect`)

**v0.1.38: Performance Optimization**
- API caching layer (DuckDB)
- Cache warming
- Performance monitoring

### Documentation Updates

**User-facing:**
- [x] Update `docs/user-guide/getting-started.md` - New UX flow ✅ COMPLETED
- [ ] Update `docs/user-guide/agents.md` - Router agent description (deferred - not user-facing)
- [x] Update `docs/faq.md` - Add router FAQs ✅ COMPLETED
- [x] Update `README.md` - New UX examples ✅ COMPLETED

**Developer:**
- [ ] Update `CLAUDE.md` - Router architecture patterns (deferred to Phase 2)
- [ ] Create `docs/architecture/routing.md` - Router design doc (deferred to Phase 2)
- [ ] Update `docs/architecture/agents-tools-mapping.md` - Add router (deferred to Phase 2)

---

## Completed Features (To Be Moved to Release Files)

All completed features below should be moved to their respective release files during the pivot:

### Completed in v0.1.27
- [x] **Earnings Whisperer Agent** - Earnings analysis and post-earnings drift opportunities
  - Leverages Yahoo Finance earnings tools (`get_earnings_history`, `get_earnings_calendar`)
  - Tracks earnings surprises and analyst estimate revisions
  - Identifies post-earnings drift patterns
  - TUI command: `/earnings`

### Completed in v0.1.28
- [x] **`/api` Command - Self-Service API Status Checker**
  - Interactive API connectivity testing in chat interface
  - Real-time validation of all 10 data providers
  - Rich table formatting with color-coded status
  - Troubleshooting tips and error diagnosis
  - Documentation clarifying NewsAPI.org vs NewsAPI.ai

### Completed in v0.1.32
- [x] **News Sentry Agent** - Real-time event detection and material event monitoring
  - Leverages SEC 8-K filings (`get_latest_8k`), Form 4 insider trades (`get_insider_transactions`)
  - Filters market-moving news and SEC filings with event prioritization (CRITICAL/HIGH/MEDIUM/LOW)
  - Material event categorization (earnings, M&A, management changes, bankruptcy)
  - Breaking news with sentiment analysis and insider trading alerts
  - Analyst rating change tracking with actionability scoring (1-10 scale)
  - TUI command: `/news`

### Completed in v0.1.33
- [x] **Risk Shield Manager** - Portfolio risk management and exposure monitoring
  - Drawdown analysis and limit breach detection
  - VAR calculations and scenario testing
  - Risk mitigation strategies
  - TUI command: `/risk`

### Completed in v0.1.34
- [x] **Tax Scout** - Tax optimization and loss harvesting
  - Tax-loss harvesting opportunities
  - Wash-sale rule compliance
  - Year-end tax planning
  - TUI command: `/tax`

### Completed in v0.1.35
- [x] **Hedge Smith** - Options strategies for portfolio protection
  - Leverages Yahoo Finance options chain (`get_options_chain`)
  - Protective collar strategies (simultaneous put + call for downside protection)
  - Covered call yield enhancement (generate income on existing holdings)
  - Put protection analysis (portfolio insurance)
  - Strike selection and expiration optimization
  - Options Greeks analysis (delta, gamma, theta, vega, IV)
  - TUI command: `/hedge`

---

## Future Enhancements (Post-Pivot)

### Multi-Agent Workflows
- [ ] **Workflow 2**: Systematic Idea Generation (Screen Forge → Quill → Atlas → Notionist)
  - Weekly pipeline of investment ideas
  - Automated screening, research, allocation, and cataloging

- [ ] **Workflow 3**: Extended Investment Analysis (Quill → Macro Lens → Atlas)
  - Add Atlas to existing /analyze workflow
  - Complete bottom-up → top-down → allocation pipeline

- [ ] **Workflow 4**: Tax-Efficient Rebalancing
  - Automated tax-loss harvesting workflow
  - Integration with rebalancing logic

### Infrastructure Enhancements
- [ ] **Enhanced TUI Features**
  - Agent selection menu
  - Active agent in header/status bar (✅ Implemented in router)
  - Workflow progress visualization

- [ ] **State Persistence**
  - PostgreSQL checkpointer for LangGraph workflows
  - Multi-session conversation continuity
  - Portfolio state tracking
