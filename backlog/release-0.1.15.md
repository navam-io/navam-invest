# Release 0.1.15

## Status
IN DEVELOPMENT

## Features

### Macro Lens - Market Strategist Agent

Added specialized Macro Lens agent for top-down macroeconomic analysis and regime identification.

**Implementation Details**:
- **New file**: `src/navam_invest/agents/macro_lens.py` (182 lines)
- **Modified**: `src/navam_invest/tui/app.py` for TUI integration
- **Modified**: `src/navam_invest/tools/__init__.py` for agent tool mappings
- **Agent focus**: Top-down macro analysis, regime identification, sector/factor guidance
- **System prompt**: Comprehensive macro regime framework with economic cycle phases

**Macro Regime Framework** (4 phases):
1. **Early Expansion** (Recovery): Rising GDP, falling unemployment → Financials, Industrials, Value
2. **Mid Expansion** (Growth): Strong GDP, stable inflation → Technology, Growth, Momentum
3. **Late Expansion** (Peak): Slowing GDP, rising inflation → Energy, Materials, Quality
4. **Contraction** (Recession): Negative GDP, falling inflation → Utilities, Staples, Defensive

**Tools Available** (10 tools across 4 categories):
- **Macro data**: FRED economic indicators (GDP, CPI, unemployment, PMI)
- **Treasury data**: Yield curve, rates, spreads, debt/GDP
- **News**: Market news search, financial headlines
- **Files**: Local file reading for analysis

**Key Indicators Framework**:
- Growth: GDP, industrial production, consumer sentiment
- Inflation: CPI, PCE, core inflation metrics
- Employment: Unemployment rate, payrolls, initial claims
- Interest Rates: Fed funds rate, 10Y treasury, yield curve
- Leading Indicators: PMI, consumer confidence, yield curve shape

**Yield Curve Signals**:
- Normal curve (10Y-2Y > 0): Healthy expansion
- Flat curve (10Y-2Y ≈ 0): Late cycle concerns
- Inverted curve (10Y-2Y < 0): Recession warning (12-18 month lead)
- Steepening: Recovery expectations or inflation concerns

**TUI Integration**:
- `/macro` command to switch to Macro Lens agent
- 8 example prompts covering regime analysis, sector guidance, risk assessment
- Streaming output showing tool calls and macro analysis progress
- Agent name displayed as "Macro Lens (Market Strategist)"

**Testing**:
- Agent creation: ✅ Passed
- Full test suite: ✅ 48/48 tests passed (38% coverage)
- TUI integration: ✅ Compiles and runs

**Output Format**:
The agent provides structured macro analysis including:
1. Current regime assessment (cycle phase identification)
2. Sector allocation guidance (overweight/underweight with rationale)
3. Factor recommendations (value/growth, size, quality, momentum)
4. Key risks to monitor (top 3-5 macro scenarios)
5. Data sources & recency notes (transparency on data freshness)

**Analysis Capabilities**:
- **Regime identification**: Determine economic cycle phase using multiple indicators
- **Sector guidance**: Recommend sector tilts based on macro conditions
- **Factor allocation**: Suggest factor exposures aligned with regime
- **Risk assessment**: Identify top macro risks and leading indicators to track
- **Yield curve analysis**: Interpret curve shape for recession signals
- **Forward-looking**: Provide 3-6 month horizon guidance

**Tool Mapping Enhancement**:
Updated `get_tools_for_agent()` to include Macro Lens mapping:
- Macro Lens: 10 tools (macro indicators, treasury data, news, files)
- Quill: 16 tools (equity research)
- Screen Forge: 9 tools (screening)
- Portfolio: 24 tools (legacy generalist)
- Research: 10 tools (legacy macro - will be phased out)

**Strategic Position**:
This agent completes the specialized agent suite from Phase 2A, providing:
- Foundation for future multi-agent workflows (Quill → Macro Lens → Atlas)
- Enhanced macro analysis beyond legacy Research agent
- Regime-based investment guidance for portfolio positioning
- Bridge to Phase 2B multi-agent orchestration

---

## Release Date
TBD

## PyPI Package
TBD
