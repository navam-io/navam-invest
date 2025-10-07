# Agent Refactoring & Expansion Plan

## Executive Summary

Based on analysis of `refer/specs/agents-tools.md` and `refer/specs/multi-agents.md`, this document provides recommendations for:
1. Refactoring current generalist agents (Portfolio, Research)
2. Building next set of specialized agents
3. Implementing multi-agent workflows

## Current State Assessment

### Existing Agents
- **Portfolio Agent** (Generalist): 6 tool categories, 27+ tools
  - Market data, fundamentals, sentiment, SEC filings, news, local files
  - **Issue**: Too broad, lacks specialized expertise

- **Research Agent** (Generalist): 4 tool categories, 10+ tools
  - Macro indicators, treasury data, news, local files
  - **Issue**: Missing deep macro analysis capabilities

### Key Findings
1. **Tool Sprawl**: Portfolio agent has access to too many tools (27+), diluting focus
2. **Missing Specialization**: No deep equity research, screening, or risk management capabilities
3. **No Multi-Agent Workflows**: Agents work in isolation, no collaboration patterns
4. **Overlapping Responsibilities**: Both agents access news tools, creating redundancy

## Recommendation 1: Refactor Current Agents

### Portfolio Agent → "Atlas" (Investment Strategist)
**New Focus**: Strategic asset allocation and portfolio construction

**Reduced Tool Set**:
- Remove: Individual stock analysis tools (fundamentals, ratios, filings)
- Remove: Screening tools
- Keep: Portfolio optimization (future), local file reading, macro indicators for allocation decisions
- Add: Strategic allocation algorithms, risk/return modeling

**Rationale**: Portfolio "strategy" is distinct from stock "research". Atlas should focus on top-down allocation, not bottom-up stock picking.

### Research Agent → "Macro Lens" (Market Strategist)
**Enhanced Focus**: Top-down macro analysis, regime identification, sector/factor guidance

**Enhanced Tool Set**:
- Keep: All macro tools (FRED, Treasury)
- Keep: News tools for macro sentiment
- Add: Sector performance tracking
- Add: Factor regime identification
- Remove: Company-specific news (delegate to specialists)

**Rationale**: Sharpen focus on macro regime analysis to guide overall investment strategy.

## Recommendation 2: Priority Specialized Agents (Phase 2)

### 1. Quill (Equity Research Analyst) - **HIGHEST PRIORITY**
**Purpose**: Deep fundamental analysis, thesis building, valuation

**Tools Required** (All Available):
- ✅ `get_company_fundamentals` (FMP)
- ✅ `get_financial_ratios` (FMP)
- ✅ `get_latest_10k`, `get_latest_10q` (SEC)
- ✅ `get_historical_fundamentals` (Tiingo)
- ✅ `get_company_news` (NewsAPI)
- ✅ `get_insider_trades` (FMP)
- ✅ `get_stock_price` (Alpha Vantage)

**Implementation Complexity**: LOW (all tools ready)

**Value Add**: Bottom-up stock analysis, DCF modeling, investment theses

---

### 2. Screen Forge (Equity Screener) - **HIGH PRIORITY**
**Purpose**: Systematic idea generation, factor screening, candidate identification

**Tools Required** (All Available):
- ✅ `screen_stocks` (FMP)
- ✅ `get_financial_ratios` (FMP)
- ✅ `get_company_fundamentals` (FMP)
- ⚠️ Future: Enhanced factor screening (quality, momentum scores)

**Implementation Complexity**: LOW (core tools ready)

**Value Add**: Weekly watchlist generation, systematic opportunity identification

---

### 3. News Sentry (Event Detection Analyst) - **MEDIUM PRIORITY**
**Purpose**: Real-time signal filtering, material event detection

**Tools Required** (Mostly Available):
- ✅ `search_market_news` (NewsAPI)
- ✅ `get_company_news` (NewsAPI)
- ✅ `get_company_filings` (SEC - for 8-Ks)
- ❌ Missing: Real-time volume/price alerts
- ❌ Missing: Marketaux API (alternative news source)

**Implementation Complexity**: MEDIUM (need additional data sources)

**Value Add**: Timely alerts on material events, risk signal detection

---

## Recommendation 3: Multi-Agent Workflow Implementation

### Workflow 1: Comprehensive Investment Analysis (Phase 2)
**Sequence**: Quill → Macro Lens → Atlas → User

**Use Case**: "Should I invest in AAPL?"

1. **Quill** analyzes AAPL fundamentals → Investment thesis
2. **Macro Lens** validates against macro regime → Timing assessment
3. **Atlas** determines portfolio fit → Position size recommendation

**Implementation**:
- Pattern: Custom sequential workflow
- State: Shared `InvestmentState` with research_findings, macro_assessment, allocation_decision
- Priority: HIGH (delivers core value proposition)

---

### Workflow 2: Systematic Idea Generation (Phase 2-3)
**Sequence**: Screen Forge → Quill → Atlas → Notionist

**Use Case**: Weekly pipeline of new investment ideas

1. **Screen Forge** runs quality/momentum screens → Top 10 candidates
2. **Quill** analyzes top picks → Investment theses
3. **Atlas** assesses portfolio fit → Watchlist with entry triggers
4. **Notionist** catalogs research → Searchable vault

**Implementation**:
- Pattern: Sequential batch processing
- Schedule: Weekly (Sunday evening)
- Priority: MEDIUM (scalability benefit)

---

## Recommendation 4: Implementation Roadmap

### Phase 2A (v0.1.13-0.1.14) - Specialized Agents
**Timeframe**: 2-3 releases

- [ ] Build Quill (Equity Research) agent
- [ ] Build Screen Forge agent
- [ ] Keep Portfolio/Research agents for backward compatibility
- [ ] Add agent selection in TUI: `/quill`, `/screen`, `/portfolio`, `/research`

**Deliverable**: 4 agents (2 new specialized, 2 legacy generalist)

---

### Phase 2B (v0.1.15) - First Multi-Agent Workflow
**Timeframe**: 1 release

- [ ] Implement Workflow 1: Comprehensive Investment Analysis (Quill → Macro Lens → Atlas)
- [ ] Refactor Portfolio → Atlas (if needed)
- [ ] Refactor Research → Macro Lens (if needed)
- [ ] Add workflow command: `/analyze <SYMBOL>`

**Deliverable**: Working multi-agent analysis pipeline

---

### Phase 3 (v0.2.x) - Advanced Workflows & Portfolio Management
**Timeframe**: 3-5 releases

- [ ] Build Rebalance Bot, Tax Scout, Risk Shield
- [ ] Implement Workflow 2: Tax-efficient rebalancing
- [ ] Implement Workflow 5: Systematic idea generation
- [ ] Add Notionist for knowledge management

**Deliverable**: Full portfolio management suite

---

## Decision Points & Open Questions

### 1. Agent Refactoring Strategy
**Option A**: Keep Portfolio/Research, add new specialized agents (4+ total)
- ✅ Pros: Backward compatibility, gradual migration
- ❌ Cons: Maintenance overhead, user confusion (which agent to use?)

**Option B**: Replace Portfolio/Research with Atlas/Macro Lens immediately
- ✅ Pros: Cleaner architecture, focused agents
- ❌ Cons: Breaking change for existing users

**Recommendation**: Option A for now (Phase 2A), then deprecate in Phase 3

---

### 2. Multi-Agent Orchestration Pattern
**Option A**: LLM-based supervisor (dynamic routing)
- ✅ Pros: Flexible, handles unexpected queries
- ❌ Cons: Higher token costs, less predictable

**Option B**: Rule-based supervisor (deterministic routing)
- ✅ Pros: Predictable, fast, no LLM costs
- ❌ Cons: Less flexible, requires explicit rules

**Option C**: Hybrid (rules first, LLM fallback)
- ✅ Pros: Best of both worlds
- ❌ Cons: More complex implementation

**Recommendation**: Option C (hybrid) for Workflow 1, Option B (rule-based) for Workflow 2

---

### 3. State Management Complexity
**Question**: Should we use a global `InvestmentState` or agent-specific states?

**Recommendation**:
- Global `InvestmentState` for multi-agent workflows (shared context)
- Agent-specific states for standalone agents (simpler, isolated)

---

## Next Steps

### Immediate Actions
1. **Create Quill agent** (reuse Portfolio tools, add valuation logic)
2. **Create Screen Forge agent** (reuse screening tools, add scoring)
3. **Test standalone agents** before multi-agent integration

### Future Considerations
- **Tool Categorization**: Update `tools/__init__.py` registry to map tools to new specialized agents
- **TUI Enhancement**: Add agent selection menu, show active agent in header
- **Documentation**: Update README with new agent capabilities and use cases

---

## Success Metrics

### Phase 2A (Specialized Agents)
- ✅ 4 working agents (2 new, 2 legacy)
- ✅ Clear tool separation between agents
- ✅ Agent selection via TUI commands

### Phase 2B (Multi-Agent Workflows)
- ✅ Workflow 1 completes end-to-end analysis
- ✅ State correctly shared between agents
- ✅ Final recommendation incorporates all agent inputs

### Phase 3 (Portfolio Management)
- ✅ Tax-efficient rebalancing workflow operational
- ✅ Weekly idea generation pipeline automated
- ✅ Knowledge vault with searchable theses

---

## Conclusion

**Priority 1**: Build Quill and Screen Forge agents (low complexity, high value)
**Priority 2**: Implement Workflow 1 (Comprehensive Investment Analysis)
**Priority 3**: Refactor Portfolio/Research into Atlas/Macro Lens

This phased approach delivers immediate value (specialized agents) while building toward the long-term vision (multi-agent workflows) outlined in the product specs.
