# Release 0.1.14

## Status
IN DEVELOPMENT

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

## Release Date
TBD

## PyPI Package
TBD
