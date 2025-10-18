# Multi-Agent Workflows

This document defines multi-agent collaboration patterns for Navam Invest, including agent communication protocols, workflow sequences, and orchestration strategies.

## Multi-Agent Architecture Patterns

### 1. Supervisor Architecture (Primary Pattern)

A central supervisor coordinates specialized worker agents based on task requirements.

**Best For**: Clear delegation, parallel execution, dynamic task routing

**Architecture**:
```
User Query → Supervisor → [Worker Agents] → Supervisor → Response
                ↓
          Route Decision
                ↓
     [Research | Analysis | Risk | Tax | Trade]
```

### 2. Hierarchical Architecture (Team-Based)

Multi-layer supervision where team supervisors manage specialist groups.

**Best For**: Large-scale operations, organizational workflows, complex multi-stage analysis

**Architecture**:
```
Top Supervisor
    ├── Research Team Supervisor
    │   ├── Quill (Equity Research)
    │   ├── Screen Forge (Screening)
    │   └── News Sentry (Signals)
    ├── Portfolio Team Supervisor
    │   ├── Atlas (Strategy)
    │   ├── Quant Smith (Optimizer)
    │   └── Rebalance Bot (Execution)
    └── Risk Team Supervisor
        ├── Risk Shield (Monitoring)
        ├── Tax Scout (Optimization)
        └── Sentinel (Compliance)
```

### 3. Custom Sequential Workflow

Fixed or conditional sequences for specific workflows.

**Best For**: Known processes, iterative refinement, multi-stage analysis

**Architecture**:
```
Start → Agent 1 → Agent 2 → Agent 3 → End
           ↓
    (conditional loop back if needed)
```

---

## State Schema Design

### Global Investment State

Shared across all agents in multi-agent workflows:

```python
from typing import TypedDict, Annotated, Optional
from langchain_core.messages import add_messages

class InvestmentState(TypedDict):
    # Conversation history
    messages: Annotated[list, add_messages]

    # Portfolio data
    portfolio: dict  # Current holdings
    cash_available: float

    # Analysis results
    research_findings: Optional[dict]
    risk_metrics: Optional[dict]
    recommendations: list

    # Workflow control
    active_agent: str
    completed_steps: list
    pending_tasks: list

    # User context
    risk_tolerance: str  # conservative, moderate, aggressive
    investment_goals: list
    time_horizon: str
```

---

## Multi-Agent Workflows

### Workflow 1: Comprehensive Investment Analysis

**Objective**: Full bottom-up and top-down analysis for investment decision

**Collaborating Agents**: Quill → Macro Lens → Risk Shield → Atlas → User

**Sequence**:

1. **Quill (Equity Research)**
   - Input: Stock symbol, company name
   - Process: Fundamental analysis, valuation (DCF, comps), thesis building
   - Output: Investment thesis, fair value range, buy/hold/sell tag
   - Tools: `get_company_fundamentals`, `get_financial_ratios`, `get_latest_10k`, `get_latest_10q`, `get_company_news`

2. **Macro Lens (Market Strategist)**
   - Input: Quill's thesis, current macro context
   - Process: Macro regime analysis, sector/factor alignment check
   - Output: Macro validation, regime fit assessment, timing considerations
   - Tools: `get_key_macro_indicators`, `get_treasury_yield_curve`, `get_economic_indicator`

3. **Risk Shield (Risk Manager)**
   - Input: Investment thesis + portfolio context
   - Process: Exposure analysis, concentration checks, drawdown scenarios
   - Output: Risk metrics, position sizing recommendation, hedging needs
   - Tools: Risk calculation (future), VaR/CVaR (future)

4. **Atlas (Investment Strategist)**
   - Input: All previous analysis + IPS constraints
   - Process: Portfolio fit analysis, allocation decision, strategic alignment
   - Output: Final recommendation with position size and execution plan
   - Tools: Portfolio optimization (future), `read_local_file`

**State Flow**:
```python
{
    "messages": [...conversation...],
    "symbol": "AAPL",
    "quill_thesis": {
        "fair_value": 180,
        "recommendation": "buy",
        "catalysts": [...],
        "risks": [...]
    },
    "macro_assessment": {
        "regime": "late_cycle",
        "sector_favorability": "neutral",
        "timing": "wait_for_pullback"
    },
    "risk_metrics": {
        "position_size": 5.0,  # percent
        "stop_loss": 150,
        "max_portfolio_impact": 0.8  # percent
    },
    "final_decision": {
        "action": "buy",
        "shares": 33,
        "cost_basis_target": 165,
        "rationale": "..."
    }
}
```

---

### Workflow 2: Portfolio Rebalancing with Tax Optimization

**Objective**: Tax-efficient portfolio rebalancing to target allocations

**Collaborating Agents**: Atlas → Rebalance Bot → Tax Scout → Trader Jane

**Sequence**:

1. **Atlas (Investment Strategist)**
   - Input: Current portfolio, target allocations, IPS
   - Process: Calculate drift from targets, determine rebalancing needs
   - Output: Target weights, rebalancing thresholds, drift report
   - Tools: Portfolio optimization (future), `read_local_file`

2. **Rebalance Bot (Rebalancing Specialist)**
   - Input: Target weights, current positions, drift tolerance
   - Process: Calculate required trades, minimize turnover
   - Output: Preliminary trade list with buy/sell amounts
   - Tools: Drift calculation (future), rebalancing optimizer (future)

3. **Tax Scout (Tax Optimization)**
   - Input: Trade list, cost basis lots, realized gains
   - Process: Lot selection, wash-sale checks, TLH opportunities
   - Output: Tax-optimized trade list with specific lots
   - Tools: Tax lot tracking (future), wash-sale detection (future)

4. **Trader Jane (Execution)**
   - Input: Tax-optimized trade list
   - Process: Order slicing, venue selection, execution
   - Output: Filled orders, execution report, TCA
   - Tools: Order routing (future), TCA (future)

**Communication Protocol**:
```python
# Handoff structure
{
    "from_agent": "Rebalance Bot",
    "to_agent": "Tax Scout",
    "handoff_type": "trade_list",
    "data": {
        "trades": [
            {"symbol": "AAPL", "action": "sell", "shares": 50},
            {"symbol": "GOOGL", "action": "buy", "shares": 10}
        ],
        "portfolio_context": {...},
        "constraints": {
            "max_turnover": 0.15,
            "min_trade_size": 1000
        }
    },
    "instructions": "Optimize for tax efficiency while maintaining rebalancing goals"
}
```

---

### Workflow 3: Earnings-Driven Position Adjustment

**Objective**: React to earnings releases with updated analysis and position management

**Collaborating Agents**: Earnings Whisperer → Quill → Risk Shield → Trader Jane

**Sequence**:

1. **Earnings Whisperer (Earnings Analyst)**
   - Input: Earnings calendar, company ticker
   - Process: Digest transcript, analyze surprise, identify post-earnings drift signals
   - Output: Earnings summary, guidance changes, thesis impact assessment
   - Tools: Earnings calendar (future), transcript analysis (future), `get_company_news`

2. **Quill (Equity Research)**
   - Input: Earnings analysis, existing thesis
   - Process: Update valuation, refresh catalysts/risks, revise recommendation
   - Output: Updated investment thesis, revised price target
   - Tools: `get_company_fundamentals`, `get_financial_ratios`

3. **Risk Shield (Risk Manager)**
   - Input: Updated thesis, current position
   - Process: Reassess risk exposure, determine if action needed
   - Output: Hold/reduce/increase recommendation with rationale
   - Tools: Risk metrics (future), scenario analysis (future)

4. **Trader Jane (Execution)** (conditional)
   - Input: Position adjustment decision
   - Process: Execute trade if required
   - Output: Fill confirmation, updated portfolio
   - Tools: Order routing (future)

**Trigger**: Scheduled (earnings calendar) or event-driven (8-K filing, unusual volume)

**State Updates**:
```python
{
    "trigger": "earnings_release",
    "symbol": "TSLA",
    "earnings_analysis": {
        "eps_actual": 2.50,
        "eps_estimate": 2.20,
        "surprise": 0.30,
        "guidance": "raised",
        "sentiment": "positive"
    },
    "thesis_update": {
        "prior_target": 250,
        "new_target": 280,
        "action": "upgrade",
        "confidence": "high"
    },
    "risk_decision": {
        "current_weight": 8.0,  # percent
        "target_weight": 10.0,
        "action": "increase"
    },
    "execution": {
        "trade": "buy 20 shares TSLA",
        "fill_price": 265.50,
        "status": "completed"
    }
}
```

---

### Workflow 4: News-Triggered Risk Response

**Objective**: Rapid response to material news events with risk mitigation

**Collaborating Agents**: News Sentry → Quill → Risk Shield → Hedge Smith (optional)

**Sequence**:

1. **News Sentry (Event Detection)**
   - Input: Real-time news feed, portfolio holdings
   - Process: Filter material events, rank by actionability
   - Output: Ranked alerts with urgency tags
   - Tools: `search_market_news`, `get_company_news`, volume alerts (future)

2. **Quill (Equity Research)** (parallel to Risk Shield)
   - Input: News alert, existing thesis
   - Process: Assess thesis impact, update conviction
   - Output: Thesis validation or revision recommendation
   - Tools: `get_company_fundamentals`, `get_company_filings`

3. **Risk Shield (Risk Manager)** (parallel to Quill)
   - Input: News alert, portfolio exposure
   - Process: Calculate downside exposure, stress test scenarios
   - Output: Risk mitigation recommendations
   - Tools: Risk metrics (future), scenario analysis (future)

4. **Hedge Smith (Options Strategist)** (conditional)
   - Input: Risk mitigation needs
   - Process: Design protective options strategy
   - Output: Hedge playbook with Greeks, costs, roll schedule
   - Tools: Options pricing (future), Greeks calculation (future)

**Real-Time Streaming**: Uses `astream()` for immediate updates

**Alert Priority Levels**:
- **CRITICAL**: Immediate action required (downgrade, fraud allegation, bankruptcy)
- **HIGH**: Review within 1 hour (earnings miss, regulatory action)
- **MEDIUM**: Review within 1 day (analyst rating change, insider sale)
- **LOW**: Background monitoring (routine news, industry trends)

---

### Workflow 5: Systematic Idea Generation Pipeline

**Objective**: Continuous screening and research pipeline for new investment ideas

**Collaborating Agents**: Screen Forge → Quill → Atlas → Notionist

**Sequence**:

1. **Screen Forge (Equity Screener)**
   - Input: Screening criteria (quality, momentum, value factors)
   - Process: Run systematic screens, rank candidates
   - Output: Weekly shortlist with entry criteria and key metrics
   - Tools: `screen_stocks`, `get_financial_ratios`

2. **Quill (Equity Research)** (batch process)
   - Input: Screened candidates (top 5-10)
   - Process: Deep dive analysis on promising names
   - Output: Investment theses for candidates
   - Tools: `get_company_fundamentals`, `get_latest_10k`, `get_company_news`

3. **Atlas (Investment Strategist)**
   - Input: New theses, current portfolio
   - Process: Assess portfolio fit, diversification impact
   - Output: Watchlist with entry triggers and position sizes
   - Tools: Portfolio optimization (future)

4. **Notionist (Knowledge Librarian)**
   - Input: All research artifacts
   - Process: Catalog theses, tag by sector/theme, version control
   - Output: Searchable research vault entry
   - Tools: Document management (future), `read_local_file`, `list_local_files`

**Schedule**: Weekly execution (Sunday evening)

**Output Format**:
```python
{
    "week": "2025-W14",
    "screen_results": {
        "criteria": "quality_growth",
        "candidates": 8,
        "top_picks": ["NVDA", "MSFT", "GOOGL"]
    },
    "research_queue": [
        {
            "symbol": "NVDA",
            "priority": "high",
            "research_status": "thesis_drafted",
            "portfolio_fit": "excellent"
        }
    ],
    "watchlist_updates": [
        {
            "symbol": "NVDA",
            "action": "add_to_watchlist",
            "entry_trigger": "pullback to $800",
            "target_weight": 6.0
        }
    ]
}
```

---

### Workflow 6: Year-End Tax Planning

**Objective**: Comprehensive tax optimization before year-end

**Collaborating Agents**: Tax Scout → Quill → Rebalance Bot → Trader Jane

**Sequence**:

1. **Tax Scout (Tax Optimization)**
   - Input: Portfolio with cost basis, realized gains YTD
   - Process: Identify TLH opportunities, calculate potential tax savings
   - Output: TLH candidate list with replacement tickers
   - Tools: Tax lot tracking (future), wash-sale detection (future)

2. **Quill (Equity Research)** (for replacement validation)
   - Input: Loss harvest candidates and replacement suggestions
   - Process: Ensure replacement maintains thesis intent
   - Output: Validated replacement pairs
   - Tools: `get_company_fundamentals`, `get_financial_ratios`

3. **Rebalance Bot (Execution Planning)**
   - Input: TLH trades, target allocations
   - Process: Integrate TLH with rebalancing needs
   - Output: Combined trade list optimizing both goals
   - Tools: Rebalancing optimizer (future)

4. **Trader Jane (Execution)**
   - Input: Year-end trade list
   - Process: Execute with wash-sale timing awareness
   - Output: Fills with tax lot confirmations
   - Tools: Order routing (future)

**Timing**: Mid-November through December 20

**Constraints**:
- Avoid wash-sale violations (30-day rule)
- Maintain strategy integrity (no style drift)
- Minimize round-trip costs (bid-ask spread)
- Consider short-term vs long-term gains

---

## Communication Protocols

### 1. Shared State (Primary Method)

All agents read and update common state object:

```python
class InvestmentState(TypedDict):
    messages: Annotated[list, add_messages]
    portfolio: dict
    research_findings: dict
    risk_metrics: dict
    recommendations: list
```

**Best For**: Sequential workflows, full context sharing

---

### 2. Tagged Messages

Messages indicate source agent:

```python
def quill_agent(state):
    response = llm.invoke(state["messages"])
    return {
        "messages": [{
            "role": "assistant",
            "content": response.content,
            "name": "Quill",  # Agent identification
            "metadata": {
                "agent_type": "equity_research",
                "confidence": 0.85,
                "timestamp": "2025-10-06T10:30:00Z"
            }
        }]
    }
```

**Best For**: Multi-agent conversations, audit trails

---

### 3. Structured Handoffs

Explicit data contracts between agents:

```python
class AgentHandoff(TypedDict):
    from_agent: str
    to_agent: str
    handoff_type: str  # "research", "trade_list", "risk_assessment"
    data: dict
    context: str
    priority: str  # "low", "medium", "high", "critical"

def create_handoff(from_agent: str, to_agent: str, data: dict) -> AgentHandoff:
    return {
        "from_agent": from_agent,
        "to_agent": to_agent,
        "handoff_type": infer_type(data),
        "data": data,
        "context": generate_context(data),
        "priority": assess_priority(data)
    }
```

**Best For**: Clear responsibilities, validation, error handling

---

### 4. Event-Driven Notifications

Agents subscribe to relevant events:

```python
# Event bus pattern
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, agent: str):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(agent)

    def publish(self, event_type: str, event_data: dict):
        agents = self.subscribers.get(event_type, [])
        for agent in agents:
            notify_agent(agent, event_data)

# Usage
event_bus = EventBus()
event_bus.subscribe("earnings_release", "Earnings Whisperer")
event_bus.subscribe("earnings_release", "Quill")
event_bus.subscribe("material_news", "News Sentry")
event_bus.subscribe("material_news", "Risk Shield")
```

**Best For**: Real-time monitoring, parallel agent activation

---

## Supervisor Implementations

### 1. LLM-Based Supervisor (Dynamic Routing)

Supervisor uses LLM to decide next agent:

```python
def supervisor(state: InvestmentState) -> Command[Literal["quill", "atlas", "risk", "finish"]]:
    system_prompt = """
    You manage: Quill (research), Atlas (strategy), Risk Shield (risk).
    Based on conversation, decide which agent should act next.
    Respond with: Quill, Atlas, Risk Shield, or FINISH.
    """

    response = supervisor_llm.invoke([
        {"role": "system", "content": system_prompt},
        *state["messages"]
    ])

    next_agent = parse_supervisor_decision(response)

    return Command(
        goto=next_agent.lower() if next_agent != "FINISH" else END,
        update={"active_agent": next_agent}
    )
```

**Pros**: Flexible, adaptive, handles unexpected requests
**Cons**: Less predictable, token costs, potential routing errors

---

### 2. Rule-Based Supervisor (Deterministic Routing)

Supervisor uses explicit rules:

```python
def rule_based_supervisor(state: InvestmentState):
    last_message = state["messages"][-1].content.lower()
    completed = state["completed_steps"]

    # Rule-based decision tree
    if "analyze" in last_message and "research" not in completed:
        return Command(goto="quill", update={"completed_steps": completed})

    elif "research" in completed and "strategy" not in completed:
        return Command(goto="atlas", update={"completed_steps": completed})

    elif "strategy" in completed and "risk" not in completed:
        return Command(goto="risk", update={"completed_steps": completed})

    else:
        return Command(goto=END)
```

**Pros**: Predictable, fast, no LLM costs, easier debugging
**Cons**: Less flexible, requires explicit rules for all paths

---

### 3. Hybrid Supervisor (Best of Both)

Combine rules for known patterns, LLM for edge cases:

```python
def hybrid_supervisor(state: InvestmentState):
    # Try rule-based first
    if rule_matches := check_known_patterns(state):
        return Command(goto=rule_matches["next_agent"])

    # Fall back to LLM for complex cases
    return llm_based_routing(state)
```

**Pros**: Efficient, flexible, cost-optimized
**Cons**: More complex implementation

---

## Error Handling & Recovery

### 1. Agent-Level Error Handling

```python
async def safe_agent_invoke(agent, state: InvestmentState):
    try:
        result = await agent.ainvoke(state)
        return result
    except Exception as e:
        error_message = {
            "role": "assistant",
            "content": f"Agent {agent.name} encountered an error: {str(e)}",
            "error": True,
            "name": agent.name
        }
        return {"messages": [error_message]}
```

### 2. Workflow-Level Fallbacks

```python
def supervisor_with_fallback(state: InvestmentState):
    primary_agent = determine_best_agent(state)

    result = safe_agent_invoke(primary_agent, state)

    if result.get("error"):
        # Try fallback agent
        fallback_agent = get_fallback_agent(primary_agent)
        result = safe_agent_invoke(fallback_agent, state)

    return result
```

### 3. Human-in-the-Loop Interrupts

```python
# Interrupt before critical actions
graph = builder.compile(
    checkpointer=checkpointer,
    interrupt_before=["trader_jane"]  # Require approval before trades
)

# User reviews and approves
config = {"configurable": {"thread_id": user_thread}}
state = graph.get_state(config)
# ... user reviews state["pending_trades"]
graph.invoke(None, config)  # Resume after approval
```

---

## Implementation Priority

### Phase 2 (v0.1.11-0.1.15) - Basic Multi-Agent
- **Workflow 5**: Screen Forge → Quill (idea generation pipeline)
- **Pattern**: Custom sequential workflow
- **Agents**: Screen Forge, Quill, Notionist

### Phase 3 (v0.2.x) - Portfolio Management
- **Workflow 2**: Atlas → Rebalance Bot → Tax Scout → Trader Jane
- **Pattern**: Supervisor architecture
- **Agents**: Atlas, Rebalance Bot, Tax Scout, Risk Shield

### Phase 4 (v0.3.x) - Advanced Analysis
- **Workflow 1**: Quill → Macro Lens → Risk Shield → Atlas
- **Pattern**: Supervisor architecture with parallel execution
- **Agents**: Quill, Macro Lens, Risk Shield, Quant Smith

### Phase 5 (v0.4.x+) - Real-Time Monitoring
- **Workflow 3**: Earnings Whisperer → Quill → Risk Shield
- **Workflow 4**: News Sentry → Quill → Risk Shield → Hedge Smith
- **Pattern**: Event-driven with hierarchical supervision
- **Agents**: News Sentry, Earnings Whisperer, Hedge Smith

---

## Testing Multi-Agent Workflows

### Unit Tests (Individual Agents)
```python
@pytest.mark.asyncio
async def test_quill_agent_output():
    state = {"messages": [{"role": "user", "content": "Analyze AAPL"}]}
    result = await quill_agent.ainvoke(state)
    assert "research" in result
    assert result["confidence"] > 0.5
```

### Integration Tests (Workflow Sequences)
```python
@pytest.mark.asyncio
async def test_investment_analysis_workflow():
    initial_state = {
        "messages": [{"role": "user", "content": "Should I buy TSLA?"}],
        "symbol": "TSLA"
    }

    result = await investment_workflow.ainvoke(initial_state)

    assert "quill_thesis" in result
    assert "macro_assessment" in result
    assert "final_decision" in result
```

### End-to-End Tests (Full System)
```python
@pytest.mark.asyncio
async def test_full_supervisor_workflow():
    result = await supervisor_graph.ainvoke({
        "messages": [{"role": "user", "content": "Rebalance my portfolio"}]
    })

    assert result["completed_steps"] == ["atlas", "rebalance", "tax", "trader"]
    assert len(result["executed_trades"]) > 0
```

---

## References

- **LangGraph Multi-Agent Guide**: `refer/langgraph/guides/multi-agent.md`
- **Agent-Tool Mapping**: `refer/specs/agents-tools.md`
- **Agent Definitions**: `refer/specs/agents.md`
- **LangGraph State Management**: `refer/langgraph/guides/persistence.md`
- **Streaming Real-Time Updates**: `refer/langgraph/guides/streaming.md`

---

## Notes

1. All workflows use **checkpointing** for durability and resume capability
2. **Real-time workflows** (news, earnings) use `astream()` for immediate updates
3. **Supervisor patterns** are preferred for flexibility and control
4. **State schemas** are versioned to maintain backward compatibility
5. **Human-in-the-loop** interrupts are used for high-stakes decisions (trades, large rebalances)
