# Release 0.1.16

## Status
Published: October 6, 2025

## Features

### Multi-Agent Workflow: Investment Analysis

**Overview**: Sequential multi-agent workflow that combines bottom-up fundamental analysis (Quill) with top-down macro validation (Macro Lens) to deliver comprehensive investment recommendations.

**Key Components**:

1. **Workflow Module** (`src/navam_invest/workflows/`)
   - New package for multi-agent orchestration
   - `investment_analysis.py`: Sequential workflow implementation
   - `__init__.py`: Public API for workflow creation

2. **Investment Analysis Workflow**
   - **Architecture**: LangGraph StateGraph with 3 nodes
   - **State Management**: Shared InvestmentAnalysisState TypedDict
     - `messages`: Conversation history (Annotated with add_messages)
     - `symbol`: Stock ticker being analyzed
     - `quill_analysis`: Fundamental analysis results
     - `macro_context`: Macro regime validation results

   - **Sequential Flow**:
     1. **Quill Agent** (Node 1): Bottom-up fundamental analysis
        - Business overview and competitive position
        - Financial health: revenue, profitability, cash flow (5-year trends)
        - Valuation: P/E, P/B, DCF-based fair value
        - Investment thesis: bull/bear cases, catalysts
        - Recommendation: BUY/HOLD/SELL with confidence

     2. **Macro Lens Agent** (Node 2): Top-down macro validation
        - Receives Quill's analysis from shared state
        - Assesses current macro regime (expansion/contraction phase)
        - Evaluates sector positioning in current regime
        - Timing assessment: Is now a good entry point?
        - Macro risk factors that could derail thesis

     3. **Synthesis Node** (Node 3): Final recommendation
        - Combines fundamental + macro perspectives
        - Overall rating: BUY/HOLD/SELL (High/Medium/Low confidence)
        - Key reasoning (2-3 sentences)
        - Suggested action for investors
        - Risk warning (most important risk to monitor)

3. **TUI Integration** (`src/navam_invest/tui/app.py`)
   - **New Command**: `/analyze <SYMBOL>` - Multi-agent investment analysis
   - **Workflow Initialization**: Created in `on_mount()` alongside other agents
   - **Real-Time Progress Display**:
     - Agent transitions (📊 Quill → 🌍 Macro Lens → 🎯 Synthesis)
     - Tool calls shown in real-time
     - Final recommendation with markdown formatting

   - **Enhanced `/examples` Command**: Now includes workflow examples
     - Shows 4 random agent-specific examples
     - Plus 4 multi-agent workflow examples

   - **Updated `/help` Command**: Documents `/analyze <SYMBOL>` usage

4. **Example Workflow Prompts**:
   - `/analyze AAPL` - Complete investment analysis (fundamental + macro)
   - `/analyze MSFT` - Should I invest? Get both bottom-up and top-down view
   - `/analyze NVDA` - Multi-agent analysis combining Quill and Macro Lens
   - `/analyze GOOGL` - Comprehensive thesis with macro timing validation

**Technical Implementation**:

```python
# State definition
class InvestmentAnalysisState(TypedDict):
    messages: Annotated[list, add_messages]
    symbol: str
    quill_analysis: str
    macro_context: str

# Workflow graph structure
workflow = StateGraph(InvestmentAnalysisState)
workflow.add_node("quill", quill_agent)
workflow.add_node("macro_lens", macro_lens_agent)
workflow.add_node("synthesize", synthesize_recommendation)

# Sequential execution path
workflow.add_edge(START, "quill")
workflow.add_edge("quill", "macro_lens")
workflow.add_edge("macro_lens", "synthesize")
workflow.add_edge("synthesize", END)
```

**User Experience**:

1. User types: `/analyze AAPL`
2. TUI displays:
   ```
   Investment Analysis Workflow: Starting multi-agent analysis...
   📊 Quill analyzing fundamentals...
     → get_company_fundamentals
     → get_financial_ratios
     → get_dcf_valuation
   🌍 Macro Lens validating timing...
     → get_treasury_yield_curve
     → get_key_macro_indicators
     → search_market_news
   🎯 Synthesizing recommendation...

   Final Recommendation:
   [Markdown-formatted synthesis combining both analyses]
   ```

**Benefits**:
- ✅ Combines bottom-up and top-down analysis automatically
- ✅ Transparent multi-agent execution visible to user
- ✅ Shared state enables agents to reference prior analysis
- ✅ Modular workflow design (can add more agents easily)
- ✅ Real-time streaming shows progress and tool usage
- ✅ Comprehensive investment recommendation in seconds

**Architecture Advantages**:
- **Separation of Concerns**: Each agent focuses on its specialty
- **State Sharing**: Later agents can reference earlier analysis
- **Composability**: Easy to extend workflow with additional agents
- **Transparency**: User sees exactly what each agent is doing
- **Flexibility**: Can modify workflow sequence without changing agents

## Development Notes

This release represents a major milestone in the navam-invest architecture:

1. **Multi-Agent Paradigm**: First implementation of coordinated agent workflows
2. **LangGraph Mastery**: Demonstrates StateGraph, shared state, and sequential orchestration
3. **User Value**: Delivers institutional-grade analysis (fundamental + macro) in a single command
4. **Extensibility**: Pattern can be replicated for other workflows (tax optimization, portfolio rebalancing, etc.)

**Future Enhancements** (Post-v0.1.16):
- Add Atlas agent to workflow for final strategic allocation guidance
- Implement parallel agent execution for independent analyses
- Add human-in-the-loop checkpoints for approval
- Create additional workflows (screening, optimization, tax planning)

---

## Release Date
October 6, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.16/
