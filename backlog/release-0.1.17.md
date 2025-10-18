# Release 0.1.17

## Status
Published to PyPI on October 6, 2025

## Features

### Atlas - Investment Strategist Agent

**Overview**: Specialized agent for strategic asset allocation, portfolio construction, and investment policy guidance.

**Key Components**:

1. **Agent Implementation** (`src/navam_invest/agents/atlas.py`)
   - **231 lines** of sophisticated investment strategy logic
   - LangGraph-based ReAct pattern for transparent reasoning
   - 12 specialized tools for allocation analysis

2. **Core Capabilities**:

   - **Strategic Asset Allocation**:
     - Design optimal portfolio allocations across asset classes (stocks, bonds, cash)
     - Risk-adjusted return optimization (Sharpe ratio maximization)
     - Asset class expected returns and risk profiles

   - **Risk Tolerance Frameworks**:
     - **Conservative**: 30/60/10 (stocks/bonds/cash), 6-8% volatility target
     - **Moderate**: 60/35/5, 10-12% volatility target
     - **Aggressive**: 85/10/5, 15-18% volatility target

   - **Investment Policy Statement (IPS) Development**:
     - Investment objectives (growth, income, preservation)
     - Time horizon and liquidity needs assessment
     - Strategic allocation with tactical ranges
     - Rebalancing policy and performance benchmarks

   - **Portfolio Construction Strategies**:
     - Geographic allocation (US, International Developed, Emerging Markets)
     - Sector tilts based on macro regime (early/mid/late expansion, recession)
     - Factor tilts (value/growth, size, quality, momentum)
     - Duration management for bond allocation

   - **Rebalancing Strategies**:
     - Threshold-based (rebalance when drift >5%)
     - Calendar-based (quarterly review, semi-annual rebalancing)
     - Tax-aware optimization
     - Band width customization (±3% tight, ±7% wide)

3. **Tools Registry Integration** (`src/navam_invest/tools/__init__.py`)
   - Added Atlas to `agent_tool_map` with 12 tools:
     - **Macro indicators** (2): `get_economic_indicator`, `get_key_macro_indicators`
     - **Treasury data** (4): Yield curve, rates, spreads, debt-to-GDP
     - **Fundamentals** (2): Company data, financial ratios
     - **Market news** (2): Search, headlines
     - **Files** (2): Local file reading, listing

4. **TUI Integration** (`src/navam_invest/tui/app.py`)
   - **New Command**: `/atlas` - Switch to Atlas investment strategist
   - **Agent Initialization**: Created in `on_mount()` alongside other agents
   - **Example Prompts**: 8 strategic allocation examples
     - "Design a strategic asset allocation for a 35-year-old with moderate risk tolerance"
     - "What's the optimal 60/40 portfolio given the current macro environment?"
     - "Build an investment policy statement for retirement planning"
     - "How should I tactically adjust my allocation in late expansion phase?"
     - "Recommend a rebalancing strategy for my portfolio"
     - "What's the right stock/bond/cash mix for a conservative investor?"
     - "Design a portfolio for maximum Sharpe ratio with 10% volatility target"
     - "Should I increase bond duration given current interest rate environment?"

   - **Updated Commands**:
     - Welcome message includes `/atlas` command
     - `/help` updated with Atlas
     - `/examples` shows Atlas-specific prompts
     - Agent selection logic supports Atlas

5. **Investment Framework**:

   **Asset Allocation Principles**:
   - **Stocks**: 8-10% expected return, 15-20% volatility, best for 10+ year horizons
   - **Bonds**: 3-5% expected return, 3-6% volatility, for income and diversification
   - **Cash**: 0-4% return (tracks short rates), minimal volatility, liquidity needs

   **Macro-Driven Tactical Tilts**:
   - **Early Expansion**: Overweight financials, industrials, small-cap, value
   - **Mid Expansion**: Overweight technology, growth, momentum
   - **Late Expansion**: Overweight energy, healthcare, utilities, defensive, quality
   - **Recession**: Overweight healthcare, utilities, staples, long-duration bonds

   **Bond Duration Strategy**:
   - **Short Duration (1-3Y)**: When rates rising (early expansion)
   - **Intermediate (5-7Y)**: Neutral stance (mid expansion)
   - **Long Duration (10-30Y)**: When rates falling (late expansion, recession)

   **Rebalancing Rules**:
   - Threshold-based: Rebalance when >5% drift from target
   - Calendar-based: Quarterly review, semi-annual execution
   - Tax-aware: Prioritize tax-advantaged accounts
   - Band width: ±3% tight (risk-intolerant), ±7% wide (taxable accounts)

**Technical Implementation**:

```python
# Atlas agent creation
async def create_atlas_agent() -> StateGraph:
    """Create Atlas investment strategist agent."""
    # Initialize LLM with tools
    llm = ChatAnthropic(model=settings.anthropic_model, ...)

    # Get allocation-focused tools
    tools = macro_tools + treasury_tools + fundamentals_tools + news_tools + file_tools

    # Agent with comprehensive system prompt
    async def call_model(state: AtlasState) -> dict:
        system_msg = """You are Atlas, expert investment strategist...
        - Strategic Asset Allocation across asset classes
        - Risk-Adjusted Optimization (Sharpe ratio)
        - Investment Policy Statement (IPS) development
        - Portfolio Construction and Rebalancing
        """
```

**User Experience**:

1. User switches to Atlas:
   ```
   /atlas
   ✓ Switched to Atlas (Investment Strategist) agent

   You: Design a strategic asset allocation for a 35-year-old with moderate risk tolerance

   Atlas (Investment Strategist):
     → get_key_macro_indicators
     → get_treasury_yield_curve

   [Provides detailed allocation with:
    - Strategic allocation (60/35/5)
    - Tactical adjustments for current macro regime
    - Equity sub-allocation (geography, sector, factor)
    - Bond sub-allocation (duration, credit)
    - Rebalancing guidelines
    - Performance benchmarks]
   ```

**Benefits**:
- ✅ Institutional-grade asset allocation guidance
- ✅ Macro-aware tactical tilts
- ✅ Personalized to risk tolerance and time horizon
- ✅ Complete IPS development support
- ✅ Actionable rebalancing strategies

**Agent Count**: 5 → **6 specialized agents** (Portfolio, Research, Quill, Screen Forge, Macro Lens, Atlas)

## Development Notes

This release completes **Phase 2B** from the agent refactoring plan by implementing Atlas (Investment Strategist), the final remaining item from the original roadmap.

Atlas serves as the **strategic allocation layer** that can:
- Integrate with Quill (bottom-up stock selection)
- Integrate with Macro Lens (top-down regime analysis)
- Guide portfolio construction based on Screen Forge recommendations
- Provide allocation framework for future workflows (tax optimization, risk management)

**Next Steps** (Phase 2C+):
- Extend Investment Analysis Workflow to include Atlas (Quill → Macro Lens → Atlas)
- Build additional multi-agent workflows
- Implement human-in-the-loop checkpoints
- Add workflow state persistence

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.17/
