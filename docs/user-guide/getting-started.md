# Getting Started with Navam Invest

Welcome to **Navam Invest** - your AI-powered investment advisory platform! This guide will help you get up and running in minutes.

## Quick Installation (3 Steps)

### 1. Install the Package

```bash
pip install navam-invest
```

### 2. Set Up Your API Key

Create a `.env` file in your working directory:

```bash
# Required - AI reasoning engine
ANTHROPIC_API_KEY=sk-ant-your_key_here
```

> **Get your Anthropic API key** at [console.anthropic.com](https://console.anthropic.com/)
>
> **Cost**: Pay-as-you-go, typically $3-15/month for regular use

### 3. Launch and Test

```bash
navam invest
```

Once the TUI loads, test your setup:

```
You: /api
```

This will show you which APIs are working (✅), failed (❌), or not configured (⚪).

## Your First Queries

### Test Basic Functionality

```
You: /quill
You: What's the current price and overview of AAPL?
```

You'll see Quill (the Equity Research agent) gather data and provide analysis!

### Try Multi-Agent Analysis

```
You: /analyze MSFT
```

This triggers a coordinated workflow where:
1. **Quill** analyzes fundamentals (earnings, valuation, analyst sentiment)
2. **Macro Lens** validates macro timing (economic cycle, yield curve)
3. **Synthesis** combines both perspectives into a final recommendation

### Explore Different Agents

```
# Earnings analysis
/earnings
Analyze NVDA earnings history - is there a post-earnings drift opportunity?

# Stock screening
/screen
Screen for tech stocks with P/E under 20 and market cap over $10B

# Macro analysis
/macro
What's the current macro regime and which sectors should I overweight?
```

## Understanding the Interface

### TUI Layout

```
┌─────────────────────────────────────────────┐
│ Navam Invest                  Agent: Quill │  ← Header (shows current agent)
├─────────────────────────────────────────────┤
│                                             │
│  You: What's the price of AAPL?            │  ← Chat history
│                                             │
│  Quill (Equity Research):                  │
│    → Calling get_quote(symbol=AAPL)        │  ← Tool execution tracking
│    ✓ get_quote completed                   │
│                                             │
│  **AAPL Current Quote**                    │  ← Agent response
│  Price: $185.50 (+1.2%)                    │    (rendered markdown)
│  Market Cap: $2.85T                        │
│                                             │
├─────────────────────────────────────────────┤
│ [Ask about stocks...]                      │  ← Input field
├─────────────────────────────────────────────┤
│ ^C Clear | ^Q Quit                         │  ← Footer (keyboard shortcuts)
└─────────────────────────────────────────────┘
```

### Processing States

**Before Query**:
```
Footer: Agent: Quill | Ready
Input: [Ask about stocks or economic indicators...]
```

**During Processing** (input automatically disabled):
```
Footer: Processing...
Input: [⏳ Processing your request...] ← Grayed out, uneditable
```

**After Completion**:
```
Footer: Agent: Quill | Ready
Input: [Ask about stocks...] ← Auto-focused, ready for next query
```

## Available Commands

### System Commands

| Command | Purpose |
|---------|---------|
| `/help` | Show all available commands |
| `/examples` | Show example prompts for current agent |
| `/api` | Check API connectivity status |
| `/clear` | Clear chat history (or `Ctrl+C`) |
| `/quit` | Exit application (or `Ctrl+Q`) |

### Agent Switching

| Command | Agent | Specialization |
|---------|-------|----------------|
| `/quill` | Quill | Equity research, valuation, thesis building |
| `/earnings` | Earnings Whisperer | Earnings analysis, post-earnings drift |
| `/screen` | Screen Forge | Stock screening, idea generation |
| `/macro` | Macro Lens | Macro analysis, sector allocation |
| `/news` | News Sentry | Real-time event detection, 8-K monitoring |
| `/portfolio` | Portfolio (legacy) | General portfolio analysis |
| `/research` | Research (legacy) | General market research |

### Multi-Agent Workflows

| Command | Workflow | Agents Used |
|---------|----------|-------------|
| `/analyze <SYMBOL>` | Complete investment analysis | Quill → Macro Lens → Synthesis |

## Optional: Add More Data Sources

While **Yahoo Finance**, **SEC EDGAR**, and **U.S. Treasury** work without API keys, you can unlock additional features:

Edit your `.env` file:

```bash
# Already have (required)
ANTHROPIC_API_KEY=sk-ant-...

# Optional - Add any or all of these for enhanced coverage
ALPHA_VANTAGE_API_KEY=your_key     # Stock prices, company overviews
TIINGO_API_KEY=your_key            # Historical fundamentals (5yr)
FINNHUB_API_KEY=your_key           # News/social sentiment, analyst ratings
FRED_API_KEY=your_key              # Economic indicators, macro data
NEWSAPI_API_KEY=your_key           # Market news, headlines

# No keys needed (always free)
# - Yahoo Finance (quotes, earnings, analyst ratings, ownership)
# - SEC EDGAR (10-K, 10-Q, 8-K filings, Form 4 insider trades)
# - U.S. Treasury (yield curves, treasury rates)
```

### Get Free API Keys

| Service | Link | Free Tier |
|---------|------|-----------|
| **Alpha Vantage** | [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key) | 25-500 calls/day |
| **Tiingo** | [tiingo.com](https://www.tiingo.com/) | 50 symbols/hr, 5yr history |
| **Finnhub** | [finnhub.io/register](https://finnhub.io/register) | 60 calls/min |
| **FRED** | [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys) | Unlimited |
| **NewsAPI.org** | [newsapi.org/register](https://newsapi.org/register) | 1,000 calls/day |

After adding keys, restart the app and run `/api` to verify they're working.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Clear chat history |
| `Ctrl+Q` | Quit application |
| `↑/↓` | Scroll through chat history |
| Mouse wheel | Scroll chat log |

## Auto-Saved Reports

All substantial agent responses (>200 characters) are automatically saved to the `reports/` directory:

```
reports/
├── AAPL_analysis_20251008_143022.md
├── MSFT_equity_research_20251008_144530.md
├── NVDA_earnings_20251008_150145.md
└── SCREENER_earnings_beats_20251008_151200.md
```

Reports include:
- Timestamp and query context
- Full agent response in markdown format
- Symbol/ticker for investment reports

## Next Steps

### Learn the Agents

Read [agents.md](agents.md) to understand each agent's capabilities and when to use them.

### Explore Workflows

Check out [multi-agent-workflows.md](multi-agent-workflows.md) to see how agents collaborate.

### Review the FAQ

See [../faq.md](../faq.md) for answers to common questions about agent behavior, error handling, and advanced features.

### Read Release Notes

Check the `backlog/` directory for detailed release notes showing what's new in each version.

## Troubleshooting

### "Error: API key not found"

1. Make sure you created a `.env` file in your working directory
2. Check that it contains `ANTHROPIC_API_KEY=sk-ant-...` (with your actual key)
3. Restart the application

### "Error: Failed to fetch data"

1. Run `/api` to see which APIs are failing
2. Check your internet connection
3. Verify API keys are correct in `.env`
4. Check if you've hit free tier rate limits (wait and try again)

### "Agent not responding"

1. Check footer bar - it should show "Processing..." during work
2. Look for tool execution indicators (→ Calling..., ✓ completed)
3. If frozen, press `Ctrl+C` to clear, then `Ctrl+Q` to restart

### Yahoo Finance vs SEC EDGAR

If optional APIs are failing, **you can still use Navam Invest!**

- **Yahoo Finance** (no key needed): Real-time quotes, earnings, analyst ratings, ownership
- **SEC EDGAR** (no key needed): Corporate filings (10-K, 10-Q, 8-K, Form 4)
- **U.S. Treasury** (no key needed): Yield curves, treasury rates

These three sources provide comprehensive coverage for most investment research needs.

## Need Help?

- 📖 Read the [FAQ](../faq.md)
- 🐛 Report bugs at [github.com/navam-io/navam-invest/issues](https://github.com/navam-io/navam-invest/issues)
- 📚 Check [documentation](../../README.md)
- 💬 Join discussions on GitHub

---

**Ready to analyze your first stock?**

```bash
navam invest
```

```
You: /analyze AAPL
```

Let the multi-agent analysis begin! 🚀
