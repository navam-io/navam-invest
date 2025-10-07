# Release 0.1.13

## Status
Published: October 6, 2025

## Features

### Quill - Equity Research Agent

Added specialized Quill agent for institutional-quality equity research and investment thesis building.

**Implementation Details**:
- **New file**: `src/navam_invest/agents/quill.py` (129 lines)
- **Modified**: `src/navam_invest/tui/app.py` for TUI integration
- **Agent focus**: Bottom-up fundamental analysis, DCF valuation, thesis development
- **System prompt**: Institutional research framework with 6-step analysis methodology
  1. Business Quality (moats, market position, unit economics)
  2. Financial Health (profitability, balance sheet, cash flow)
  3. Growth Trajectory (revenue growth, margin expansion)
  4. Valuation (P/E, P/S, EV/EBITDA vs peers/history)
  5. Catalysts (near-term and long-term value drivers)
  6. Risks (downside scenarios and red flags)

**Tools Available** (20+ tools across 4 categories):
- Market data (current price, overview)
- Fundamentals (financial statements, ratios, 5-year historical data via Tiingo)
- SEC filings (10-K, 10-Q, insider trades, institutional holdings)
- Company news (thesis validation)

**TUI Integration**:
- `/quill` command to switch to Quill agent
- 8 example prompts covering common equity research queries
- Streaming output showing tool calls and analysis progress
- Agent name displayed as "Quill (Equity Research)"

**Testing**:
- Agent creation: ✅ Passed
- Full test suite: ✅ 48/48 tests passed (41% coverage)
- Manual TUI verification: ✅ Compiles and runs

**Output Format**:
- Clear investment recommendations (Strong Buy/Buy/Hold/Sell/Strong Sell)
- Fair value range with DCF/comp-based valuation
- 2-3 key catalysts and 2-3 key risks
- Financial metrics with trend analysis
- Data-backed references from filings and fundamentals

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.13/
