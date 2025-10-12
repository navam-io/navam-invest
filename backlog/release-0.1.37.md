# Release 0.1.37

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

**Extended `/analyze` Workflow** - Comprehensive 5-Agent Investment Analysis

The `/analyze` workflow has been extended from 2 agents to 5 agents, providing comprehensive investment analysis that integrates fundamental, event, macro, risk, and tax perspectives.

**Workflow Sequence**:
1. **Quill (Equity Research)** - Bottom-up fundamental analysis with valuation and investment thesis
2. **News Sentry (Event Monitor)** - Material events, insider trading, recent news that could impact the thesis
3. **Macro Lens (Market Strategist)** - Top-down macro validation and timing assessment
4. **Risk Shield (Risk Manager)** - Portfolio fit, concentration risk, volatility analysis
5. **Tax Scout (Tax Advisor)** - Tax implications, wash-sale checks, timing optimization
6. **Synthesis** - Combined recommendation integrating all five perspectives

**Key Features**:
- Sequential execution with state accumulation (each agent sees prior analyses)
- Context-aware system prompts that reference previous agent outputs
- Tool execution loops for each agent with proper routing
- Comprehensive final recommendation synthesizing all perspectives
- LangGraph StateGraph implementation with proper state management

**Implementation Details**:
- Extended `InvestmentAnalysisState` TypedDict with 3 new fields: `news_events`, `risk_assessment`, `tax_implications`
- Added 3 new agent node functions with specialized system prompts
- Added 3 new tool nodes for News Sentry, Risk Shield, and Tax Scout
- Added conditional edge functions for tool routing
- Updated synthesis function to incorporate all 5 agent analyses
- Modified workflow graph with sequential edges connecting all agents

**Files Modified**:
- `src/navam_invest/workflows/investment_analysis.py` - Complete 5-agent workflow (435 lines)
- `docs/faq.md` - Updated workflow documentation to reflect 5-agent sequence

### 🚧 In Progress Features

**`/discover` Workflow - Systematic Idea Discovery** (IN PROGRESS)

A 3-agent workflow for systematic investment idea generation and validation.

**Workflow Sequence**:
1. **Screen Forge (Equity Screener)** - Systematic screening with factor-based filters
2. **Quill (Equity Research)** - Deep fundamental analysis on top 3-5 candidates
3. **Risk Shield (Risk Manager)** - Portfolio fit assessment and position sizing
4. **Synthesis** - Final ranked recommendations with action steps

**Implementation Status**:
- ✅ Core workflow implementation (`src/navam_invest/workflows/idea_discovery.py` - 435 lines)
- ✅ Workflow export in `__init__.py`
- ✅ FAQ documentation updated
- ⏳ TUI integration pending (needs `/discover` command handler + workflow initialization)

**Key Features**:
- Sequential execution with state accumulation (each agent sees prior analyses)
- Screen Forge identifies 10-15 candidates with factor-based scoring
- Quill performs deep analysis on top 3-5 picks
- Risk Shield provides portfolio fit assessment and position sizing recommendations
- Final synthesis ranks candidates and provides actionable next steps

**Files Modified**:
- `src/navam_invest/workflows/idea_discovery.py` - NEW (435 lines)
- `src/navam_invest/workflows/__init__.py` - Export new workflow
- `docs/faq.md` - Documented new workflow

### 🚧 Planned Features

**Enhanced Multi-Agent Workflows** - Extended agent coordination and new workflow patterns

Building on the router foundation from v0.1.36, this release continues to extend multi-agent collaboration patterns and introduces new systematic workflows for common investment tasks.

**New Workflow: `/discover`** - Systematic Idea Generation:
- Screen Forge identifies candidates matching investment criteria
- Quill performs deep fundamental analysis on shortlist
- Risk Shield assesses portfolio fit and concentration
- Atlas provides strategic allocation recommendations
- Notionist catalogs research and investment theses

**New Workflow: `/optimize-tax`** - Tax-Loss Harvesting:
- Tax Scout identifies tax-loss harvesting opportunities
- Hedge Smith suggests replacement positions to maintain exposure
- Rebalance Bot executes tax-efficient rebalancing
- Complete tax optimization pipeline with wash-sale compliance

**New Workflow: `/protect`** - Portfolio Hedging:
- Risk Shield analyzes portfolio exposures and vulnerabilities
- Hedge Smith designs protective options strategies
- Atlas evaluates hedging cost vs portfolio protection
- Complete hedging workflow with multiple strategy options

**Workflow Orchestration Improvements**:
- Better parallel execution coordination
- Progress tracking for multi-step workflows
- Workflow result synthesis across agents
- Error recovery and partial completion handling

---

## Technical Improvements

**Workflow Engine** (Planned):
- [ ] Create workflow orchestration layer for complex multi-agent sequences
- [ ] Implement workflow state management and checkpointing
- [ ] Add workflow progress visualization in TUI
- [ ] Build workflow templates for common investment tasks

**Extended `/analyze` Workflow**: ✅ COMPLETED
- [x] Integrate News Sentry for material event detection
- [x] Integrate Risk Shield for portfolio risk assessment
- [x] Integrate Tax Scout for tax implications analysis
- [x] Add workflow result synthesis across all agents
- [x] Implement sequential execution with state accumulation pattern
- [x] Create context-aware system prompts for each agent
- [x] Add tool execution loops and conditional routing

**New Workflows**:
- [x] Implement `/discover` systematic idea generation workflow (PARTIAL - core implementation done, TUI integration pending)
- [ ] Implement `/optimize-tax` tax-loss harvesting workflow
- [ ] Implement `/protect` portfolio hedging workflow
- [x] Add workflow documentation for `/discover` in FAQ

**Documentation Updates** (Planned):
- [ ] Update `docs/user-guide/multi-agent-workflows.md` - New workflows
- [ ] Update `docs/user-guide/getting-started.md` - Workflow examples
- [ ] Create `docs/architecture/workflows.md` - Workflow design patterns
- [ ] Update `README.md` - New workflow capabilities

---

## Breaking Changes

None planned for this release.

---

## Release Date
TBD

## PyPI Package
TBD
