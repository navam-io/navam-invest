# Release 0.1.14

## Status
Published: October 6, 2025

## Features

### Screen Forge - Equity Screening Agent

Added specialized Screen Forge agent for systematic stock screening and investment idea generation.

**Implementation Details**:
- **New file**: `src/navam_invest/agents/screen_forge.py` (132 lines)
- **Modified**: `src/navam_invest/tui/app.py` for TUI integration
- **Agent focus**: Multi-factor stock screening, watchlist generation, candidate identification
- **System prompt**: Systematic screening framework with common screen types
  - Value screens (low P/E, P/B, positive earnings)
  - Growth screens (revenue/earnings growth, expanding margins)
  - Quality screens (high ROE, margins, low debt)
  - Dividend screens (yield, payout ratio, payment history)
  - Small-cap screens (market cap range, growth rate)
  - Momentum screens (price trends, analyst sentiment)

**Tools Available** (15+ tools across 3 categories):
- Market data (price, overview, volume for liquidity checks)
- Fundamentals (screening tool, financial ratios, fundamentals for validation)
- Sentiment data (Finnhub analyst recommendations, insider activity, social sentiment)

**TUI Integration**:
- `/screen` command to switch to Screen Forge agent
- 8 example prompts covering common screening scenarios
- Streaming output showing tool calls and screening progress
- Agent name displayed as "Screen Forge (Equity Screening)"

**Testing**:
- Agent creation: ✅ Passed
- Full test suite: ✅ 48/48 tests passed (40% coverage)
- TUI integration: ✅ Compiles and runs

**Output Format**:
- 5-15 ranked candidates with key metrics (P/E, growth rates, margins, market cap)
- Standout metrics highlighted for each candidate (why it passed the screen)
- Multi-factor scoring for prioritization
- Next step suggestions (e.g., "Deep dive with Quill on top 3-5 picks")
- Transparent screening methodology and limitation notes

**Screening Capabilities**:
- **Factor-based screening**: Value, growth, quality, momentum
- **Quantitative filters**: Market cap thresholds, liquidity requirements
- **Qualitative overlays**: Sector themes, macro alignment, sentiment validation
- **Ranking system**: Multi-factor scoring to prioritize candidates
- **Integration ready**: Works seamlessly with Quill agent for deep-dive analysis

---

### Tools Registry Enhancement - Agent-Specific Tool Mappings

Enhanced tools registry with agent-specific tool mapping functionality to support specialized agents.

**Implementation Details**:
- **Modified**: `src/navam_invest/tools/__init__.py`
- **New function**: `get_tools_for_agent(agent_name: str) -> List[BaseTool]`
- **Purpose**: Map specialized agents to their optimal tool sets based on agent refactoring plan

**Agent Tool Mappings**:

1. **Quill (Equity Research)** - 16 tools:
   - Market data: price, overview
   - Fundamentals: financials, ratios, insider trades, historical data (5yr via Tiingo)
   - SEC filings: 10-K, 10-Q, company filings, institutional holdings
   - News: company-specific news for thesis validation

2. **Screen Forge (Equity Screening)** - 9 tools:
   - Market data: price, overview for validation
   - Screening: stock screener, fundamentals, financial ratios
   - Sentiment: Finnhub sentiment, social sentiment, insider sentiment, recommendations

3. **Portfolio (Legacy Generalist)** - 24 tools:
   - Comprehensive tool set across all categories
   - Backward compatibility maintained

4. **Research (Legacy Macro)** - 10 tools:
   - Macro indicators: FRED economic data
   - Treasury data: yield curve, rates, spreads
   - Macro news and file reading

**Benefits**:
- **Focused agents**: Each specialized agent has curated tools for their domain
- **Reduced tool sprawl**: Quill excludes screening tools, Screen Forge excludes SEC filings
- **Clear separation**: Tool sets reflect agent specialization (bottom-up vs systematic screening)
- **Future-ready**: Foundation for multi-agent workflows where agents share tool results
- **Maintainability**: Centralized mapping makes it easy to adjust agent capabilities

**Testing**:
- Quill agent: ✅ 16 tools mapped correctly
- Screen Forge agent: ✅ 9 tools mapped correctly
- Portfolio agent: ✅ 24 tools (backward compatible)
- Research agent: ✅ 10 tools
- Full test suite: ✅ 48/48 tests PASSED

**Phase 2A Status**: ✅ COMPLETE (All specialized agent tasks finished)

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.14/
