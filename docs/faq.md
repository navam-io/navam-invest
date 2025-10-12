# Navam Invest - Frequently Asked Questions (FAQ)

## Table of Contents

- [First-Time User Questions](#first-time-user-questions)
- [Automatic Router (NEW in v0.1.36)](#automatic-router-new-in-v0136)
- [Agent Behavior](#agent-behavior)
- [Multi-Agent Workflows](#multi-agent-workflows)
- [Error Handling & Tool Failures](#error-handling--tool-failures)
- [Data Sources & API Keys](#data-sources--api-keys)
- [Features & Functionality](#features--functionality)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)

---

## First-Time User Questions

### How do I know which agent is currently active?

**In Router Mode (Default - NEW in v0.1.36)**:

The router coordinates agents automatically. You'll see:

1. **Header Bar**: Shows `Router: Active 🔀`
2. **Footer Bar**: Shows `Router: Active | Ready` when idle
3. **During Processing**: `Router: → Quill + Macro Lens | Processing`
4. **Agent Responses**: Prefixed with agent name:
   ```
   [Router] Routing to Quill for fundamental analysis...
     → get_quote(symbol=AAPL)
     ✓ Analysis complete

   [Quill] **AAPL Analysis**
   Price: $185.50 (+1.2%)...
   ```

**In Manual Mode** (after using `/quill`, `/macro`, etc.):

The active agent is displayed in **three** places:

1. **Header Bar** (top right): Shows `Agent: Quill` or similar
2. **Footer Bar** (bottom): Shows `Manual: Quill | Ready` when idle, `Processing...` when working
3. **Agent Name in Response**: Each response is prefixed with the agent name:
   ```
   Quill (Equity Research):
   ✓ AAPL: $185.50 (+1.2%)...
   ```

**To Switch Between Modes**:
- `/router on` - Enable automatic routing (default)
- `/router off` - Disable router, switch to manual mode
- Any manual agent command (`/quill`, `/macro`) - Automatically disables router

### Can I switch agents mid-conversation?

**Yes!** You can switch agents at any time using agent commands:

```
You: /quill
✓ Switched to Quill (Equity Research) agent

You: Analyze AAPL
[Quill responds with equity research]

You: /macro
✓ Switched to Macro Lens (Market Strategist) agent

You: What's the current macro regime?
[Macro Lens responds with macro analysis]
```

### What happens to my conversation history when I switch agents?

**Your chat history remains visible**, but each agent starts with a fresh context. Agents **do not share memory** across switches - they only see their own system prompt and the current user message.

To clear history and start fresh: Press `Ctrl+C` or type `/clear`

### How do I know if the system is processing or frozen?

Navam Invest provides **clear visual feedback** at multiple levels:

**During Processing**:
- **Footer Bar**: Changes from `Ready` to `Processing...`
- **Input Field**: Automatically disabled with placeholder `⏳ Processing your request...`
- **Tool Execution**: Live tracking of tool calls:
  ```
  → Calling get_quote(symbol=AAPL)
  ✓ get_quote completed
  ```

**If No Visible Progress**:
- LLM may still be reasoning (no tools called yet)
- Watch footer bar - if it says `Processing...`, system is working
- If footer is stuck on `Processing...` for >30 seconds with no tool calls, there may be an issue

**Frozen vs Working**:
- **Working**: Footer says `Processing...`, input disabled
- **Frozen**: Footer stuck, input enabled, no response after long wait → Press `Ctrl+Q` and restart

### Where are my reports saved?

All substantial responses (>200 characters) are **automatically saved** to:

```
reports/
├── AAPL_analysis_20251008_143022.md          # Multi-agent analysis
├── MSFT_equity_research_20251008_144530.md   # Quill research
├── NVDA_earnings_20251008_150145.md          # Earnings analysis
└── SCREENER_earnings_beats_20251008_151200.md # Screening results
```

**Naming Convention**: `{symbol}_{report_type}_{timestamp}.md`

**What's Saved**:
- Query context (date, symbol, question)
- Full agent response with formatting
- All markdown (tables, code blocks, lists)

**Note**: You'll see `📄 Report saved to: reports/...` at the end of each response.

### Do I need all the API keys?

**No! Only Anthropic Claude is required.**

**Always Free (No API Keys Needed)**:
- ✅ **Yahoo Finance**: Real-time quotes, earnings, analyst ratings, ownership
- ✅ **SEC EDGAR**: Corporate filings (10-K, 10-Q, 8-K, Form 4)
- ✅ **U.S. Treasury**: Yield curves, treasury rates

**Optional (Free Tiers Available)**:
- 🔧 **Alpha Vantage**: Stock prices, company overviews (25-500 calls/day)
- 🔧 **Tiingo**: Historical fundamentals (50 symbols/hr)
- 🔧 **Finnhub**: News/social sentiment (60 calls/min)
- 🔧 **FRED**: Economic indicators (unlimited)
- 🔧 **NewsAPI.org**: Market news (1,000 calls/day)

**Recommendation**: Start with just Anthropic, then add optional keys as needed.

---

## Automatic Router (NEW in v0.1.36)

### How does the router work?

The **router is a supervisor agent** that automatically selects and coordinates specialist agents based on your question's intent.

**Behind the Scenes**:
1. **Intent Classification**: Router LLM analyzes your question
2. **Agent Selection**: Chooses 1-3 relevant specialist agents
3. **Execution**: Invokes selected agents (can run in parallel)
4. **Synthesis**: Combines results into coherent response

**Example Flow**:
```
You: Should I invest in AAPL right now?

[Router analyzes intent]
→ Detected: Investment decision query
→ Routing to: Quill (fundamentals) + Macro Lens (timing) + Risk Shield (risk)

[Parallel execution]
Quill → Analyzes AAPL financials, earnings, valuation
Macro Lens → Assesses market regime, tech sector outlook
Risk Shield → Evaluates portfolio concentration risk

[Router synthesizes]
Final recommendation combining all perspectives
```

### Do I still need to learn which agent does what?

**No!** That's the point of the router. Just ask naturally:

```
# You don't need to know which agent handles this
You: Find me undervalued tech stocks with strong earnings

# Router automatically routes to Screen Forge
[Screen Forge executes screening tools]
```

**However**, knowing agent specialties is still useful for:
- **Power users**: Direct agent access via `/quill`, `/macro` bypasses router
- **Understanding responses**: Know which specialist is providing analysis
- **Debugging**: Identify which agent might need better tools/prompts

### When should I use the router vs. manual agent selection?

**Use Router Mode (Default)** when:
- ✅ You're new to Navam Invest
- ✅ Asking exploratory questions
- ✅ Want comprehensive multi-agent analysis
- ✅ Don't want to think about which agent to use
- ✅ Asking complex questions spanning multiple domains

**Use Manual Mode** (`/quill`, `/macro`, etc.) when:
- 🎯 You know exactly which specialist you need
- 🎯 Want faster responses (skip router overhead)
- 🎯 Iterating within one agent's specialty
- 🎯 Building focused research on specific topic
- 🎯 Troubleshooting agent-specific behavior

**Example - Router Mode**:
```
You: Should I invest in AAPL?
[Router coordinates Quill + Macro + Risk → comprehensive analysis]
```

**Example - Manual Mode**:
```
You: /quill
You: What's AAPL's P/E ratio?
You: Show me the balance sheet
You: Compare to MSFT valuation
[Staying in Quill for focused equity research]
```

### Can I see which sub-agents the router is calling?

**Yes! Progressive streaming (NEW in v0.1.36)** shows sub-agent tool calls in real-time:

```
You: Analyze TSLA

[Router] Routing to Quill for fundamental analysis...
  → get_quote(symbol=TSLA)
  → get_financials(symbol=TSLA)
  → get_earnings_history(symbol=TSLA)
  ✓ Quill analysis complete

[Router] Routing to Macro Lens for timing assessment...
  → get_economic_indicators()
  → get_yield_curve()
  ✓ Macro analysis complete

[Router] Synthesizing recommendation...

[Final comprehensive analysis]
```

**What You See**:
- Which agents the router selected
- Individual tool calls from each sub-agent
- Real-time execution progress (not batched)
- Clear indication when each agent completes

### How do I disable the router?

**Three ways**:

1. **Command**: `/router off`
   ```
   You: /router off
   ✓ Router disabled. Switched to manual mode.
   You must now select agents explicitly using /quill, /macro, etc.
   ```

2. **Manual Agent Selection** (automatic disable):
   ```
   You: /quill
   ✓ Router automatically disabled.
   Switched to Quill (Equity Research) agent.
   ```

3. **Persistent Setting** (not yet available):
   - Future: Config file option `router_enabled: false`

**Re-enable Router**:
```
You: /router on
✓ Router enabled. Agent selection now automatic.
```

### Does the router add latency to queries?

**Yes, but minimal** (<2 seconds typical overhead):

**Router Overhead**:
1. Intent classification (LLM call): ~1-2 seconds
2. Agent selection reasoning: Included in classification
3. No additional overhead for agent execution (same as manual)

**Comparison**:

| Mode | Time to First Response |
|------|----------------------|
| Router Mode | User query → Router classifies (1-2s) → Agent executes → Response |
| Manual Mode | User query → Agent executes → Response |

**Mitigation**:
- Router uses lower temperature (0.1) for faster, deterministic routing
- Intent classification is cached for repeated question patterns (future)
- For rapid-fire questions within one domain, use manual mode

**When Overhead Matters**:
- Rapid iteration within one agent's specialty → Use manual mode (`/quill`)
- One-off comprehensive questions → Router is fine

### Can the router call multiple agents in parallel?

**Yes!** The router can invoke multiple agents simultaneously when appropriate:

```
You: Give me a complete investment analysis of NVDA

[Router determines: Needs fundamentals + macro + risk + news]

[Parallel execution]
Quill → Fundamentals analysis
Macro Lens → Market timing
Risk Shield → Portfolio fit
News Sentry → Recent events

[All execute concurrently, then router synthesizes]
```

**Benefits**:
- Faster than sequential execution
- Comprehensive analysis from multiple perspectives
- Real-time streaming shows progress from all agents

**When Parallel Execution Happens**:
- Complex investment decisions
- Questions explicitly requesting multiple viewpoints
- Comprehensive analysis commands

**When Sequential Execution Happens**:
- Agent outputs feed into next agent (e.g., Screen Forge → Quill)
- Context from earlier agent needed by later agent

### How accurate is the router's intent classification?

**95%+ accuracy** based on v0.1.36 test suite:

**Test Coverage**:
- 16 comprehensive router tests (all passing)
- 10+ intent classification scenarios
- 10 specialist agent routing tests
- 5+ multi-agent coordination tests
- 5+ error handling tests

**Common Classification Examples**:

| User Query | Router Routes To |
|-----------|-----------------|
| "What's AAPL trading at?" | Quill (quote tools) |
| "Find undervalued tech stocks" | Screen Forge (screening tools) |
| "Is recession risk high?" | Macro Lens (macro indicators) |
| "TSLA earnings analysis" | Earnings Whisperer (earnings tools) |
| "Should I invest in NVDA?" | Quill + Macro + Risk (multi-agent) |
| "Tax-loss harvesting opportunities" | Tax Scout (tax tools) |
| "Protect my position with options" | Hedge Smith (options tools) |

**Misclassification Handling**:
- Wrong agent selected → Agent attempts with available tools, may provide limited response
- Ambiguous query → Router asks clarifying questions or routes to Portfolio (general agent)
- User feedback → Use manual mode (`/quill`) to force correct agent

### What if the router selects the wrong agent?

**Fallback Mechanisms**:

1. **Agent Attempts Best Effort**:
   ```
   You: What's the price of AAPL?
   [Router mistakenly routes to Macro Lens instead of Quill]

   Macro Lens: I don't have stock quote tools, but I can
   provide macro context for tech sector...
   ```

2. **Manual Override**:
   ```
   You: /quill
   You: What's the price of AAPL?
   [Direct to correct agent, bypasses router]
   ```

3. **Rephrase Query**:
   ```
   You: Get me the current stock quote for AAPL
   [More explicit intent → Router routes correctly]
   ```

4. **Router Learns** (future):
   - User corrections feed into routing improvements
   - Pattern recognition for ambiguous queries

**Report Misclassifications**:
If router consistently selects wrong agent for a query type, please report on [GitHub Issues](https://github.com/navam-io/navam-invest/issues) to improve intent classification.

---

## Agent Behavior

### When I ask a question better suited for another agent, how does Navam Invest handle it?

**Each agent will attempt to answer within their tool capabilities**, but responses may be limited or suboptimal:

**Example - Asking Macro Lens about a stock**:
```
You: /macro
You: What's the price of AAPL?

Macro Lens: I don't have stock quote tools, but based on market
indices, tech stocks are trading near yearly highs...
```

**Better Approach**:
```
You: /quill
You: What's the price of AAPL?

Quill: [Calls get_quote(symbol=AAPL)]
✓ AAPL: $185.50 (+1.2%), Market Cap $2.85T...
```

**Agent Tool Separation**:
- **Quill**: 36 tools (stocks, earnings, SEC filings, analysts)
- **Earnings Whisperer**: 14 tools (earnings, analyst coverage)
- **Screen Forge**: 15 tools (screening, sentiment)
- **Macro Lens**: 13 tools (macro indicators, yield curves, indices)
- **News Sentry**: 13 tools (8-K filings, Form 4, news, sentiment)

**Recommendation**: Use `/examples` to see what each agent can do, then switch to the right agent for your question.

### Can agents call tools from other agents' toolsets?

**No.** Each agent has a **dedicated set of tools**. Agents cannot access tools outside their specialization.

**Example**:
- **Quill** can call `get_earnings_history()` ✅
- **Macro Lens** cannot call `get_earnings_history()` ❌ (not in its toolset)

**Why?** This design ensures:
1. Focused expertise (agents don't get distracted by irrelevant tools)
2. Predictable behavior (you know what data each agent can access)
3. Cost efficiency (fewer tools = faster reasoning)

**For Cross-Domain Analysis**: Use multi-agent workflows (see next section)

### What's the difference between single-agent and multi-agent mode?

**Single-Agent Mode** (default):
- Activated by agent switching commands (`/quill`, `/macro`, etc.)
- One agent handles your query using its toolset
- Best for: Focused questions within an agent's specialty

**Multi-Agent Mode** (workflows):
- Activated by workflow commands (`/analyze`)
- Multiple agents collaborate sequentially
- Each agent contributes its expertise
- Final synthesis combines all perspectives
- Best for: Complex analysis requiring multiple viewpoints

**Comparison**:

| Feature | Single-Agent | Multi-Agent Workflow |
|---------|-------------|---------------------|
| **Command** | `/quill`, `/macro`, etc. | `/analyze <SYMBOL>` |
| **Agents Used** | 1 | 2+ (sequential) |
| **Collaboration** | None | Explicit handoffs |
| **Use Case** | Focused questions | Comprehensive analysis |
| **Output** | Single perspective | Synthesized recommendation |

### How do I know which tools an agent is using?

**Real-time tool tracking** is displayed during agent processing:

```
Quill (Equity Research):
  → Calling get_quote(symbol=AAPL)
  ✓ get_quote completed

  → Calling get_earnings_history(symbol=AAPL)
  ✓ get_earnings_history completed

  → Calling get_analyst_recommendations(symbol=AAPL)
  ✓ get_analyst_recommendations completed

[Agent response with combined insights]
```

**Tool Call Details**:
- **→ Calling** shows tool name and abbreviated arguments
- **✓ completed** confirms successful execution
- **Errors** are shown if a tool fails (see Error Handling section)

---

## Multi-Agent Workflows

### When do multi-agents kick in?

**Multi-agent workflows are triggered by specific commands**:

**Currently Available**:
- `/analyze <SYMBOL>` - Comprehensive Investment Analysis Workflow (5 agents)
- `/discover [CRITERIA]` - Systematic Idea Discovery Workflow (3 agents)

**Future Workflows** (planned):
- `/optimize-tax` - Tax-loss harvesting workflow (Tax Scout → Hedge Smith)
- `/protect` - Portfolio hedging workflow (Risk Shield → Hedge Smith)

**Single-agent mode is default** - multi-agents only activate when explicitly requested.

### Can I customize multi-agent workflows?

**Not yet.** In v0.1.x, workflows are **pre-configured** with fixed agent sequences.

**Current `/analyze` Workflow** (NEW in v0.1.37 - 5 agents):
1. **Quill** → Bottom-up fundamental analysis (valuation, financials, thesis)
2. **News Sentry** → Material events, insider trading, recent news
3. **Macro Lens** → Top-down macro validation and timing assessment
4. **Risk Shield** → Portfolio fit, concentration risk, volatility analysis
5. **Tax Scout** → Tax implications, wash-sale checks, timing optimization
6. **Synthesis** → Combined recommendation integrating all perspectives

**Current `/discover` Workflow** (NEW in v0.1.37 - 3 agents):
1. **Screen Forge** → Systematic screening with factor-based filters (10-15 candidates)
2. **Quill** → Deep fundamental analysis on top 3-5 candidates
3. **Risk Shield** → Portfolio fit and position sizing for each candidate
4. **Synthesis** → Final ranked recommendations with action steps

**Future** (v0.2.0+):
- Custom workflow builder
- User-defined agent sequences
- Conditional branching (if X, then call agent Y)
- Parallel agent execution

**Workaround** (manual multi-agent analysis):
```
/quill
Analyze AAPL fundamentals

/macro
What's the macro regime for tech stocks?

/earnings
Check AAPL earnings momentum

# Then manually synthesize insights
```

### What's the difference between `/analyze` and manually asking each agent?

**`/analyze` (Automated Workflow)**:
- **Sequential orchestration**: Agents receive context from prior agents
- **Structured handoff**: Macro Lens receives Quill's thesis for validation
- **Final synthesis**: Dedicated synthesis step combines perspectives
- **Consistent format**: Standardized output with clear sections
- **One command**: Complete analysis in single request

**Manual Agent Switching**:
- **Independent queries**: Each agent starts fresh, no context sharing
- **No handoff**: Agents don't receive prior agent outputs
- **Manual synthesis**: You must combine insights yourself
- **Flexible**: Can ask different questions to each agent
- **More control**: Choose which agents to consult

**Recommendation**:
- Use `/analyze` for **comprehensive investment decisions**
- Use manual switching for **exploratory research** or **specific questions**

### How do agents communicate with each other?

**In Multi-Agent Workflows**:

Agents communicate through **state updates** managed by LangGraph:

```python
# Simplified workflow structure
State = {
    "messages": [...],              # Conversation history
    "symbol": "AAPL",              # Shared context
    "quill_analysis": "",          # Quill's output
    "macro_context": "",           # Macro Lens output
}

# Step 1: Quill analyzes
state["quill_analysis"] = quill_agent(state)

# Step 2: Macro Lens receives Quill's analysis
state["macro_context"] = macro_lens_agent(state)  # Can see quill_analysis

# Step 3: Synthesis combines both
final = synthesize(state["quill_analysis"], state["macro_context"])
```

**Key Points**:
- Agents don't "talk" directly - they read/write shared state
- Later agents can see earlier agents' outputs
- Earlier agents can't see later agents' outputs (sequential flow)
- State persists throughout workflow execution

**In Single-Agent Mode**:
- No communication (agents operate independently)
- Each switch starts fresh context

---

## Error Handling & Tool Failures

### How do I know if the response is from the LLM vs tool failures?

**Tool Success** (full data available):
```
Quill (Equity Research):
  → Calling get_quote(symbol=AAPL)
  ✓ get_quote completed                    ← Success indicator

AAPL Current Quote:
Price: $185.50 (+1.2%)
Market Cap: $2.85T
[Detailed analysis based on real data]
```

**Tool Failure** (LLM reasoning without data):
```
Quill (Equity Research):
  → Calling get_quote(symbol=AAPL)
  ✗ Tool call failed: API rate limit exceeded    ← Failure indicator

I cannot retrieve real-time data for AAPL due to API
limitations. Based on recent market trends and analyst
reports, Apple has been...
[LLM provides reasoning without current data]
```

**Partial Failures** (some tools work, some fail):
```
Quill (Equity Research):
  → Calling get_quote(symbol=AAPL)
  ✓ get_quote completed

  → Calling get_earnings_history(symbol=AAPL)
  ✗ Tool call failed: API timeout

AAPL Analysis:
Current Price: $185.50 (+1.2%)           ← From successful tool
[Price analysis]

Historical Earnings:                      ← LLM estimation
I cannot access earnings history data, but Apple
typically reports quarterly earnings...
```

**Key Indicators**:
- ✓ **completed** = Tool worked, data is real
- ✗ **failed** = Tool didn't work, data is LLM's best reasoning
- **Missing tool calls** = Agent chose not to use tools (answering from knowledge)

### What happens when an API key is missing?

**Behavior depends on agent's toolset**:

**Scenario 1: Agent relies on optional APIs** (Finnhub, Alpha Vantage, etc.)
```
You: /screen
You: Screen for stocks with positive sentiment

Screen Forge:
  → Calling get_social_sentiment(...)
  ✗ Tool call failed: Finnhub API key not configured

I cannot access social sentiment data without Finnhub API.
However, I can screen using other factors:
  → Calling get_earnings_history(...)    ← Falls back to available tools
  ✓ Screening by earnings momentum instead...
```

**Scenario 2: Agent relies on free APIs** (Yahoo Finance, SEC EDGAR)
```
You: /quill
You: Analyze AAPL

Quill:
  → Calling get_quote(symbol=AAPL)         ← Yahoo Finance (no key needed)
  ✓ get_quote completed
  [Analysis proceeds normally]
```

**Best Practice**: Run `/api` to see which APIs are configured and fix any issues before starting analysis.

### What happens when a tool call fails mid-analysis?

**Agents attempt to recover gracefully**:

**1. Retry** (automatic for transient errors):
```
→ Calling get_quote(symbol=AAPL)
✗ Timeout - retrying...
→ Calling get_quote(symbol=AAPL)
✓ get_quote completed
```

**2. Fallback to alternative tools**:
```
→ Calling get_fundamentals_daily(...)  [Tiingo - requires key]
✗ Tool call failed: API key not configured

→ Calling get_financials(...)          [Yahoo Finance - no key needed]
✓ get_financials completed
[Analysis continues with Yahoo data]
```

**3. Reasoning without data**:
```
→ Calling get_quote(symbol=AAPL)
✗ All API endpoints failed

I cannot retrieve real-time data. Based on:
- Recent market trends (S&P 500 performance)
- Sector dynamics (tech sector resilience)
- Last known fundamentals

Apple likely remains...
[LLM provides contextual reasoning]
```

**4. Partial analysis**:
```
✓ Price data retrieved successfully
✗ Earnings data unavailable
✓ Analyst ratings retrieved

Analysis is PARTIAL. I can evaluate:
- Current valuation (P/E, market cap)
- Analyst sentiment
But cannot assess earnings trends.
```

### Can agents recover from errors?

**Yes, in multiple ways**:

**Tool-Level Recovery**:
- Automatic retries for timeouts
- Fallback to alternative data sources
- Graceful degradation (continue with available data)

**Agent-Level Recovery**:
- LLM reasoning fills gaps when data unavailable
- Transparency about limitations ("I cannot access...")
- Clear indication of data vs. reasoning in responses

**User-Level Recovery**:
- Input auto-enables after errors (never stuck)
- Retry by re-asking question
- Check `/api` for failing services
- Switch agents if needed

**Example Recovery Flow**:
```
User: Analyze AAPL

Quill:
  → API timeout errors...
  ✗ Cannot complete analysis

# Input auto-enables
Footer: Agent: Quill | Ready

User: /api
# Sees Tiingo is down but Yahoo Finance works

User: Analyze AAPL
# Quill retries with Yahoo Finance tools
# Analysis succeeds
```

### What if I hit rate limits?

**Free Tier Rate Limits**:
- **Alpha Vantage**: 25 calls/day → Wait 24 hours or upgrade
- **Finnhub**: 60 calls/min → Wait 1 minute
- **NewsAPI.org**: 1,000 calls/day → Wait 24 hours
- **Tiingo**: 50 symbols/hr → Wait 1 hour

**No Rate Limits**:
- Yahoo Finance: Unlimited
- SEC EDGAR: Unlimited (but polite rate limiting recommended)
- U.S. Treasury: Unlimited

**When You Hit Limits**:
```
→ Calling get_stock_price(...)
✗ API rate limit exceeded (25/25 calls today)

Alpha Vantage daily limit reached. Analysis will continue
using Yahoo Finance for price data.
  → Calling get_quote(...)
  ✓ get_quote completed
```

**Mitigation Strategies**:
1. **Rely on unlimited APIs**: Yahoo Finance + SEC EDGAR provide 90% of needs
2. **Space out queries**: Don't batch 50 stock analyses in one session
3. **Check `/api`** before intensive research
4. **Upgrade APIs** if you need higher limits (most offer paid tiers)

---

## Data Sources & API Keys

### What's the difference between Yahoo Finance, SEC EDGAR, and paid APIs?

**Yahoo Finance** (Free, No Key):
- **Real-time quotes**: Price, volume, market cap
- **Earnings**: Historical surprises, calendar, estimates
- **Analyst coverage**: Recommendations, price targets, upgrades/downgrades
- **Ownership**: Institutional holders, insider transactions (via SEC link)
- **Financials**: Income statement, balance sheet, cash flow
- **Options**: Full options chain with Greeks
- **Dividends**: Yield, history, payout ratios
- **Indices**: S&P 500, Nasdaq, VIX

**SEC EDGAR** (Free, No Key):
- **10-K**: Annual reports with full financials
- **10-Q**: Quarterly reports
- **8-K**: Material events (M&A, management changes, bankruptcy)
- **Form 4**: Insider transactions (buys/sells by officers/directors)
- **13F**: Institutional holdings (quarterly updates)
- **XBRL**: Structured financial data

**Paid/Optional APIs** (Free Tiers):
- **Alpha Vantage**: Alternative price source (25-500 calls/day)
- **Tiingo**: 5-year historical fundamentals (50 symbols/hr)
- **Finnhub**: News/social sentiment, alternative analyst data (60 calls/min)
- **FRED**: Economic indicators (unlimited)
- **NewsAPI.org**: Market news, headlines (1,000 calls/day)

**Recommendation**:
- **Start with**: Anthropic Claude + Yahoo Finance + SEC EDGAR (comprehensive, no extra keys)
- **Add later**: Tiingo (for historical trends), Finnhub (for sentiment), FRED (for macro)

### Which API keys are actually worth getting?

**Tier 1 - Must Have**:
- ✅ **Anthropic Claude**: Required for AI reasoning ($3-15/month typical usage)

**Tier 2 - Highly Recommended** (free tiers, high value):
- ⭐ **FRED**: Economic indicators, macro data (UNLIMITED, free forever)
  - Why: Essential for Macro Lens agent, no restrictions
- ⭐ **Tiingo**: Historical fundamentals (50 symbols/hr, free)
  - Why: 5-year trends for Quill's financial analysis

**Tier 3 - Nice to Have** (free tiers, situational):
- 🔧 **Finnhub**: News/social sentiment (60 calls/min, free)
  - Why: Sentiment analysis for Screen Forge, not critical
- 🔧 **NewsAPI.org**: Market news (1,000 calls/day, free)
  - Why: News context for agents, but Yahoo Finance has company news

**Tier 4 - Optional** (limited free tiers):
- 💤 **Alpha Vantage**: Stock prices (25 calls/day, free)
  - Why: Yahoo Finance does this better with no limits

**Recommended Setup**:
```bash
# Minimum viable (most users)
ANTHROPIC_API_KEY=sk-ant-...

# Recommended (power users)
ANTHROPIC_API_KEY=sk-ant-...
FRED_API_KEY=...           # Unlimited, always add this
TIINGO_API_KEY=...         # 50/hr, great for historical data

# Optional (specific needs)
FINNHUB_API_KEY=...        # If you want sentiment analysis
NEWSAPI_API_KEY=...        # If you want broader news coverage
```

---

## Features & Functionality

### What are all the available agents?

**Currently Released** (v0.1.32):

| Agent | Command | Specialization | Tools |
|-------|---------|----------------|-------|
| **Quill** | `/quill` | Equity research, valuation, thesis building | 36 |
| **Earnings Whisperer** | `/earnings` | Earnings analysis, post-earnings drift | 14 |
| **Screen Forge** | `/screen` | Stock screening, idea generation | 15 |
| **Macro Lens** | `/macro` | Macro analysis, sector allocation, regime ID | 13 |
| **News Sentry** | `/news` | Real-time events, 8-K monitoring, insider trades | 13 |
| **Portfolio** (legacy) | `/portfolio` | General portfolio analysis | 24 |
| **Research** (legacy) | `/research` | General market research | 10 |

**Planned** (v0.1.33-0.1.35):
- **Risk Shield**: Portfolio risk management, VAR, drawdown analysis
- **Tax Scout**: Tax optimization, loss harvesting, wash-sale checks
- **Hedge Smith**: Options strategies, protective puts, covered calls
- **Atlas**: Investment strategist, IPS development, asset allocation
- **Quant Smith**: Portfolio optimizer, factor analysis, constraint optimization
- **Rebalance Bot**: Drift detection, tax-aware rebalancing
- **Compass**: Goal planning, risk profiling, cash-flow management
- **Trader Jane**: Execution specialist, order slicing, TCA

### What's the difference between legacy agents and new specialized agents?

**Legacy Agents** (Portfolio, Research):
- **Broader scope**: Try to do many things
- **More tools**: Portfolio has 24 tools (harder for LLM to choose correctly)
- **Less specialized**: Generic prompts without deep expertise
- **Backward compatible**: Maintained for users familiar with them
- **Phase-out**: Will be removed in v0.2.0

**New Specialized Agents** (Quill, Earnings Whisperer, etc.):
- **Focused expertise**: Single domain mastery
- **Curated tools**: Only relevant tools (easier for LLM to reason)
- **Expert prompts**: Deep domain knowledge and frameworks
- **Better results**: More accurate, more detailed, more actionable
- **Future**: Will receive all new features

**Recommendation**: Use new specialized agents. They're better in every way.

### How does automatic report saving work?

**What Gets Saved**:
- Responses **over 200 characters**
- All agent types (single-agent and multi-agent workflows)
- Full markdown formatting preserved

**File Naming**:
```
{symbol}_{report_type}_{timestamp}.md

Examples:
AAPL_analysis_20251008_143022.md
MSFT_equity_research_20251008_144530.md
NVDA_earnings_20251008_150145.md
SCREENER_20251008_151200.md
```

**Report Types**:
- `analysis` - Multi-agent `/analyze` workflow
- `equity_research` - Quill reports
- `earnings` - Earnings Whisperer reports
- `screening` - Screen Forge results
- `macro_analysis` - Macro Lens reports
- `news_monitoring` - News Sentry alerts
- `portfolio` - Portfolio agent reports

**Location**: `reports/` directory (created automatically in working directory)

**Metadata Included**:
```markdown
---
date: 2025-10-08
symbol: AAPL
query: Analyze AAPL with focus on earnings
report_type: analysis
---

[Full agent response in markdown]
```

**Note**: You'll see `📄 Report saved to: reports/...` after each substantial response.

### How does the `/api` command work?

**Purpose**: Self-service API connectivity testing

**What It Tests**:
1. **API Reachability**: Can connect to each API endpoint
2. **Authentication**: API keys are valid
3. **Data Retrieval**: Can fetch sample data
4. **Rate Limits**: Shows if you're hitting limits

**Output Format**:
```
API Status Report

┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ API Provider      ┃ Status             ┃ Details           ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Yahoo Finance     │ ✅ Working         │ No key needed     │
│ SEC EDGAR         │ ✅ Working         │ No key needed     │
│ U.S. Treasury     │ ✅ Working         │ No key needed     │
│ Anthropic Claude  │ ✅ Working         │ sk-ant-...        │
│ Tiingo            │ ✅ Working         │ 50 symbols/hr     │
│ Finnhub           │ ❌ Failed          │ Invalid API key   │
│ Alpha Vantage     │ ⚪ Not configured  │ Optional          │
│ FRED              │ ✅ Working         │ Unlimited         │
│ NewsAPI.org       │ ⚠️ Rate Limited    │ 997/1000 today    │
└───────────────────┴────────────────────┴───────────────────┘

Summary: 6 working • 1 failed • 1 not configured

💡 Tips:
- Failed APIs: Check your .env file for correct API keys
- Not configured: Optional - get free keys to unlock more features
- Rate limited: Wait and try again
```

**When to Use**:
- After setup to verify configuration
- Before intensive research sessions
- When agent responses seem incomplete
- Troubleshooting tool failures

### What are the keyboard shortcuts?

**Built-In Shortcuts**:
- `Ctrl+C` - Clear chat history
- `Ctrl+Q` - Quit application
- `↑/↓` - Scroll through chat (if supported)
- Mouse wheel - Scroll chat log

**Future** (planned for v0.2.0):
- `Ctrl+R` - Retry last query
- `Ctrl+S` - Save current chat
- `Ctrl+L` - Load saved chat
- `Tab` - Autocomplete commands

---

## Advanced Usage

### Can I run Navam Invest in batch mode (non-interactive)?

**Not currently.** Navam Invest is designed as an **interactive TUI** application.

**Workaround** (programmatic usage):
```python
# Create Python script using navam_invest library
from navam_invest.agents.quill import create_quill_agent
from langchain_core.messages import HumanMessage

async def analyze_stock(symbol):
    agent = await create_quill_agent()
    result = await agent.ainvoke({
        "messages": [HumanMessage(content=f"Analyze {symbol}")]
    })
    return result["messages"][-1].content

# Run analysis
import asyncio
analysis = asyncio.run(analyze_stock("AAPL"))
print(analysis)
```

**Future** (v0.2.0+):
- CLI batch mode: `navam analyze AAPL --output=json`
- API server: Run as HTTP service
- Python SDK: Import and use agents programmatically

### Can I customize agent prompts or tools?

**Not through configuration.** Agent prompts and tools are **hardcoded** for reliability.

**To Customize** (requires code changes):

1. **Fork the repository**
2. **Edit agent files**:
   ```python
   # src/navam_invest/agents/quill.py
   system_msg = HumanMessage(
       content="You are Quill... [modify prompt here]"
   )
   ```
3. **Add/remove tools**:
   ```python
   # src/navam_invest/tools/__init__.py
   "quill": [
       "get_quote",
       "get_financials",
       "your_custom_tool",  # Add here
   ]
   ```
4. **Install in editable mode**:
   ```bash
   pip install -e .
   ```

**Future** (v0.2.0+):
- User-defined agent templates
- Custom tool registration via config
- Prompt template overrides

### Can I use Navam Invest with other LLMs (OpenAI, Gemini, etc.)?

**Not currently.** Navam Invest is hardcoded to use **Anthropic Claude**.

**Why Claude?**
- Superior reasoning for financial analysis
- Extended context window (200K tokens)
- Tool use reliability
- Transparent thinking process

**To Use Other LLMs** (requires code changes):

```python
# src/navam_invest/agents/quill.py
# Replace:
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")

# With:
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
```

**Future** (v0.2.0+):
- Model selection in config: `NAVAM_MODEL=openai:gpt-4o`
- Model-specific optimizations
- Local model support (Ollama)

### How do I add a custom data source or tool?

**Step 1: Create Tool Function**

```python
# src/navam_invest/tools/my_custom_tool.py
from langchain_core.tools import tool

@tool
async def get_custom_data(symbol: str, api_key: str) -> str:
    """Get data from my custom API.

    Args:
        symbol: Stock ticker
        api_key: API key for my service
    """
    # Your implementation
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://myapi.com/{symbol}")
        return response.text
```

**Step 2: Register Tool**

```python
# src/navam_invest/tools/__init__.py

from navam_invest.tools.my_custom_tool import get_custom_data

TOOLS: Dict[str, BaseTool] = {
    # Existing tools...
    "get_custom_data": get_custom_data,
}
```

**Step 3: Add to Agent**

```python
# src/navam_invest/tools/__init__.py

"quill": [
    # Existing tools...
    "get_custom_data",
]
```

**Step 4: Bind API Key** (if needed)

```python
# src/navam_invest/tools/__init__.py

def bind_api_keys_to_tools(..., my_custom_key: str = ""):
    # Add binding logic
    if tool_name == "get_custom_data":
        if my_custom_key and callable_func:
            bound_func = _create_bound_wrapper(callable_func, my_custom_key)
            # ...
```

**Step 5: Test**

```bash
pytest tests/test_my_custom_tool.py
```

---

## Troubleshooting

### Agent responses are truncated or incomplete

**Cause**: Max token limit reached (shouldn't happen in v0.1.31+)

**Fixed in v0.1.31**: `max_tokens=8192` (up from 4096)

**If Still Happening**:
1. Check agent file: `src/navam_invest/agents/[agent].py`
2. Verify `max_tokens=8192` in `ChatAnthropic` initialization
3. Report issue on GitHub

### Tools are being called repeatedly without finishing

**Cause**: Agent is stuck in tool-calling loop

**Symptoms**:
```
→ Calling get_quote(...)
→ Calling get_quote(...)
→ Calling get_quote(...)
[Never shows ✓ completed]
```

**Solutions**:
1. **Press `Ctrl+C`** to stop current query
2. **Check `/api`** - API might be down/timing out
3. **Restart app** (`Ctrl+Q` then `navam invest`)
4. **Report issue** if persistent

### "No module named 'navam_invest'" error

**Cause**: Package not installed correctly

**Solutions**:
```bash
# Option 1: Reinstall from PyPI
pip uninstall navam-invest
pip install navam-invest

# Option 2: Install from source
cd /path/to/navam-invest
pip install -e .

# Option 3: Check Python environment
which python        # Make sure it's the right Python
pip list | grep navam   # Verify installation
```

### API shows "Working" but agent says data unavailable

**Cause**: Tool call succeeded but returned empty/unexpected data

**Check**:
1. **API Rate Limits**: Even if connected, might be rate-limited
2. **Symbol Validity**: `AAPL` works, `APPL` doesn't
3. **Data Availability**: Some stocks lack earnings/analyst data
4. **Retry**: Data might have been temporarily unavailable

**Example**:
```
→ Calling get_earnings_history(symbol=PRIV)
✓ get_earnings_history completed

No earnings history found for PRIV. This may be a private
company or lack public earnings reports.
```

### App crashes with "Connection refused" or "Timeout"

**Cause**: Network issues or API endpoint unreachable

**Solutions**:
1. **Check internet**: `ping google.com`
2. **Check API status**: Visit API provider websites
3. **Check firewall**: Ensure app can make outbound HTTP(S) requests
4. **Use `/api`** to identify which service is failing
5. **Fallback**: Rely on Yahoo Finance + SEC (most reliable)

### How do I report a bug or request a feature?

**Bug Reports**:
1. Go to [GitHub Issues](https://github.com/navam-io/navam-invest/issues)
2. Click "New Issue"
3. Include:
   - Navam Invest version: `pip show navam-invest`
   - Python version: `python --version`
   - Operating system
   - Steps to reproduce
   - Error messages or screenshots
   - What you expected vs. what happened

**Feature Requests**:
1. Go to [GitHub Issues](https://github.com/navam-io/navam-invest/issues)
2. Click "New Issue"
3. Describe:
   - Use case (what are you trying to do?)
   - Proposed solution (if you have ideas)
   - Alternative approaches
   - Why this would be valuable

**Community**:
- Discussions: GitHub Discussions tab
- Twitter: [@navam_io](https://twitter.com/navam_io)
- Email: contact@navam.io

---

## Version History & Features

### What's new in recent releases?

**v0.1.32** (Current - In Development):
- ✅ **News Sentry Agent**: Real-time event detection
  - 8-K material event monitoring
  - Form 4 insider trading alerts
  - Breaking news with sentiment
  - Analyst rating change tracking
  - Event prioritization (CRITICAL/HIGH/MEDIUM/LOW)

**v0.1.31** (Jan 10, 2025):
- ✅ **Enhanced UX**: Smart input disabling during processing
- ✅ **Full Responses**: Increased max_tokens to 8192 (no truncation)
- ✅ **Auto-Save Reports**: All responses >200 chars saved to reports/

**v0.1.30** (Jan 8, 2025):
- ✅ **Removed FMP API**: Replaced with more reliable Yahoo Finance
- ✅ **Improved Reliability**: 100% free-tier APIs with no access errors

**v0.1.28** (Jan 5, 2025):
- ✅ **`/api` Command**: Self-service API status checker
- ✅ **Rich Tables**: Color-coded status (✅/❌/⚪)
- ✅ **Troubleshooting**: Inline tips for fixing API issues

**v0.1.27** (Dec 29, 2024):
- ✅ **Earnings Whisperer Agent**: Earnings analysis specialist
- ✅ **14 Tools**: Yahoo Finance + SEC + Finnhub
- ✅ **Pattern Recognition**: Consistent beaters, drift detection

**v0.1.26** (Dec 22, 2024):
- ✅ **Yahoo Finance Integration**: 11 FREE tools (quotes, earnings, analysts)
- ✅ **Enhanced EDGAR**: 4 new tools (8-K, Form 4, XBRL, institutional)
- ✅ **Zero Cost Expansion**: $2.4K-$10.8K/year savings

See [backlog/](../../backlog/) for complete release notes.

---

## Still Have Questions?

- 📖 **Documentation**: Check [user-guide/](../user-guide/) folder
- 🚀 **Getting Started**: See [getting-started.md](../user-guide/getting-started.md)
- 🤖 **Agent Details**: Read [agents.md](../user-guide/agents.md)
- 🔀 **Workflows**: Explore [multi-agent-workflows.md](../user-guide/multi-agent-workflows.md)
- 🐛 **Report Issues**: [GitHub Issues](https://github.com/navam-io/navam-invest/issues)

**Can't find your answer?** Open a [GitHub Discussion](https://github.com/navam-io/navam-invest/discussions)!
