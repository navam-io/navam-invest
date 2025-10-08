# Release 0.1.27

## Status
✅ **PUBLISHED** - October 07, 2025

## Features

### Earnings Whisperer Agent - Earnings Analysis Specialist

Added specialized Earnings Whisperer agent for earnings surprise analysis, post-earnings drift identification, and earnings momentum tracking.

**Implementation Details**:
- **New file**: `src/navam_invest/agents/earnings_whisperer.py` (154 lines)
- **Modified**: `src/navam_invest/tui/app.py` for TUI integration
- **Modified**: `src/navam_invest/tools/__init__.py` for agent tool mapping
- **Agent focus**: Earnings surprise analysis, post-earnings drift, analyst estimate tracking
- **System prompt**: Comprehensive earnings analysis framework with 5-step methodology
  1. **Earnings History Analysis**: Beat/miss patterns, consistency, quality assessment
  2. **Post-Earnings Drift Detection**: Price momentum patterns, underreaction identification
  3. **Analyst Response Tracking**: Recommendation changes, estimate revisions
  4. **Upcoming Earnings Calendar**: Next earnings date, probability assessment
  5. **News & Catalyst Integration**: 8-K filings, guidance changes, red flags

**Tools Available** (14 tools across 5 categories):
- **Earnings data** (2): Historical earnings with surprises, upcoming earnings calendar (Yahoo Finance)
- **Market data** (3): Real-time quotes, historical prices, current price
- **Analyst coverage** (2): Recommendations, rating changes (Yahoo + Finnhub)
- **SEC filings** (2): 8-K earnings releases, flexible filing search
- **News** (2): Company news for earnings context
- **Fundamentals** (2): Financial statements, ratios for quality checks

**TUI Integration**:
- `/earnings` command to switch to Earnings Whisperer agent
- 8 example prompts covering common earnings analysis queries
- Streaming output showing tool calls and analysis progress
- Agent name displayed as "Earnings Whisperer"

**Testing**:
- Agent creation: ✅ Passed
- Syntax validation: ✅ All files pass (`earnings_whisperer.py`, `app.py`, `tools/__init__.py`)
- Tool mapping: ✅ 14 tools correctly mapped

**Output Format**:
- Earnings verdict: STRONG BEAT MOMENTUM / BEAT / MIXED / MISS / DETERIORATING
- Earnings surprise score (1-10) based on consistency and magnitude
- Post-earnings drift opportunity (YES/NO/UNCERTAIN)
- Key catalysts: Next earnings date, estimate revisions, analyst actions
- Trading recommendation: BUY (drift play) / HOLD / SELL (negative momentum)
- Risk factors: Earnings quality issues, guidance concerns

**Analysis Capabilities**:
- **Historical Surprise Tracking**: Analyze last 4-8 quarters for beat/miss patterns
- **Earnings Momentum**: Identify consistent beaters (3+ consecutive quarters)
- **Post-Earnings Drift**: Detect underreaction opportunities (1-3 days post-earnings)
- **Analyst Tracking**: Monitor estimate revisions and rating changes
- **Earnings Quality**: Flag revenue misses vs EPS beats, non-recurring items
- **Calendar Monitoring**: Identify upcoming earnings with probability of surprise

**Key Patterns Detected**:
- Consistent beaters (3+ quarters beating estimates)
- Accelerating beats (increasing surprise magnitude)
- Post-earnings drift (continuation vs. reversal)
- Estimate revisions (analyst upgrades post-earnings)
- Quality issues (EPS beat but revenue miss)
- Guidance changes (catalyst for re-rating)

---

## Release Date
October 07, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.27/

## Installation

```bash
pip install navam-invest==0.1.27
# or
pip install --upgrade navam-invest
```
