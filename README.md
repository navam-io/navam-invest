<div align="center">

# 🤖 Navam Invest

**AI-Powered Investment Advisor for Retail Investors**

[![PyPI version](https://badge.fury.io/py/navam-invest.svg)](https://badge.fury.io/py/navam-invest)
[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/navam-invest)](https://pepy.tech/project/navam-invest)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://img.shields.io/badge/mypy-checked-blue)](http://mypy-lang.org/)

[Features](#-features) •
[Quick Start](#-quick-start) •
[Documentation](#-documentation) •
[Contributing](#-contributing)

</div>

---

## 🆕 What's New in v0.1.5

**Tier 1 API Tools Expansion** - Added 13 new tools across 3 major APIs:

- ✨ **Financial Modeling Prep**: Comprehensive fundamentals, ratios, insider trades, stock screening
- ✨ **U.S. Treasury Data**: Full yield curves (1M-30Y), spreads, debt metrics - no API key needed!
- ✨ **SEC EDGAR**: Corporate filings (10-K, 10-Q, 13F) with direct links

**Tool Count**: 4 → 17 tools (+325% growth) | **Full release notes**: [v0.1.5](backlog/release-0.1.5.md)

---

## 📖 Overview

`navam-invest` brings institutional-grade portfolio intelligence to individual retail investors. Built with [LangGraph](https://langchain-ai.github.io/langgraph/) and powered by [Anthropic's Claude](https://www.anthropic.com/claude), it provides specialized AI agents for portfolio analysis, market research, and investment insights—all accessible through an interactive terminal interface.

### Why Navam Invest?

- **🎯 Institutional Intelligence**: Access the same analytical depth once reserved for institutional portfolios
- **🔒 Privacy-First**: Run locally with your own API keys—your data stays yours
- **💡 Transparent**: Full audit trails and explainable AI reasoning
- **🆓 Free Data Sources**: Leverages high-quality public APIs (FRED, Alpha Vantage)
- **🔧 Extensible**: Modular architecture makes it easy to add new agents and data sources

---

## ✨ Features

### 🤖 **AI Agents Powered by LangGraph**

<table>
<tr>
<td width="50%">

**Portfolio Analysis Agent**
- Real-time stock quotes and metrics
- Company fundamentals & financial ratios
- Insider trading activity tracking
- SEC filings (10-K, 10-Q, 13F)
- Multi-criteria stock screening

</td>
<td width="50%">

**Market Research Agent**
- Macroeconomic indicators (GDP, CPI, unemployment)
- Treasury yield curves & spreads
- Federal Reserve data (FRED)
- Economic regime detection
- Debt-to-GDP analysis

</td>
</tr>
</table>

### 📊 **Real API Integrations** (17 Tools Across 5 Data Sources)

| API | Tools | Purpose | Cost |
|-----|-------|---------|------|
| **Alpha Vantage** | 2 | Stock prices, company fundamentals, technical indicators | Free tier: 25 calls/day |
| **Financial Modeling Prep** | 4 | Financial statements, ratios, insider trades, screening | Free tier: 250 calls/day |
| **FRED (St. Louis Fed)** | 2 | Economic indicators, macro data | Free (unlimited) |
| **U.S. Treasury** | 4 | Yield curves, treasury rates, debt data | Free (unlimited) |
| **SEC EDGAR** | 5 | Corporate filings (10-K, 10-Q, 13F) | Free (10 req/sec) |
| **Anthropic Claude** | - | AI reasoning and tool orchestration | Pay-as-you-go |

### 💬 **Interactive Terminal UI**

- **Chat Interface**: Natural language interaction with AI agents
- **Real-time Streaming**: Watch agents think and reason in real-time
- **Markdown Rendering**: Beautiful formatted output with tables and lists
- **Agent Switching**: Seamlessly switch between specialized agents
- **Command Palette**: Quick access to common actions

### 🏗️ **Built on Modern Tech**

```
LangGraph (Agent Orchestration) → LangChain (Tools) → Anthropic Claude (Reasoning)
     ↓
Textual (Terminal UI) + Typer (CLI) + httpx (Async HTTP)
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.9+** (3.13 recommended)
- **pip** or **uv** package manager
- API keys (see [Configuration](#configuration))

### Installation

#### Option 1: Install from PyPI

```bash
pip install navam-invest
```

#### Option 2: Install from Source

```bash
git clone https://github.com/navam-io/navam-invest.git
cd navam-invest
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

### Configuration

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys** to `.env`:
   ```bash
   # Required
   ANTHROPIC_API_KEY=sk-ant-...

   # Optional (but recommended for full functionality)
   ALPHA_VANTAGE_API_KEY=your_key_here
   FRED_API_KEY=your_key_here
   FMP_API_KEY=your_key_here
   ```

3. **Get API Keys** (all free tiers available):
   - **Anthropic**: [console.anthropic.com](https://console.anthropic.com/) (pay-as-you-go)
   - **Alpha Vantage**: [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key) (free)
   - **FRED**: [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys) (free)
   - **FMP**: [financialmodelingprep.com/developer](https://financialmodelingprep.com/developer) (free)
   - **Treasury & SEC**: No API keys required!

### Usage

#### Launch the Interactive Interface

```bash
navam invest
```

#### Example Interactions

**Portfolio Analysis:**
```
You: What's the current price of AAPL?
Portfolio Agent: [Fetches real-time data and provides formatted response]

You: Show me Apple's financial ratios
Portfolio Agent: [Displays liquidity, profitability, leverage ratios]

You: Any recent insider trading at AAPL?
Portfolio Agent: [Shows latest insider buy/sell activity with dates and volumes]

You: Find me the latest 10-K for Apple
Portfolio Agent: [Retrieves SEC filing with direct link to document]
```

**Market Research:**
```
You: /research
You: What's the current GDP?
Research Agent: [Fetches latest GDP data from FRED with date and trend]

You: Show me the Treasury yield curve
Research Agent: [Displays full curve from 1M to 30Y with current rates]

You: What's the 2Y-10Y spread telling us?
Research Agent: [Calculates spread with economic interpretation (normal/inverted/flat)]

You: Give me key economic indicators
Research Agent: [Shows dashboard of GDP, unemployment, CPI, fed funds rate]
```

#### TUI Commands

| Command | Action |
|---------|--------|
| `/portfolio` | Switch to Portfolio Analysis Agent |
| `/research` | Switch to Market Research Agent |
| `/help` | Show help message |
| `Ctrl+C` | Clear chat history |
| `Ctrl+Q` | Quit application |

#### CLI Commands

```bash
navam invest    # Launch interactive chat interface
navam version   # Show version information
navam --help    # Show help
```

---

## 📚 Documentation

### Project Structure

```
navam-invest/
├── src/navam_invest/
│   ├── agents/              # 🤖 LangGraph agent implementations
│   │   ├── portfolio.py     #    Portfolio analysis with ReAct pattern
│   │   └── research.py      #    Market research with macro tools
│   ├── tools/               # 🔧 API integration tools (17 tools total)
│   │   ├── alpha_vantage.py #    Stock price & fundamentals
│   │   ├── fred.py          #    Economic indicators & macro data
│   │   ├── fmp.py           #    Financial statements & ratios
│   │   ├── treasury.py      #    Yield curves & treasury data
│   │   ├── sec_edgar.py     #    Corporate filings (10-K, 10-Q, 13F)
│   │   └── __init__.py      #    Unified tools registry
│   ├── tui/                 # 💬 Textual-based user interface
│   │   └── app.py           #    Chat interface with streaming
│   ├── config/              # ⚙️ Configuration management
│   │   └── settings.py      #    Pydantic settings with .env
│   └── cli.py               # 🖥️ Typer CLI entry point
├── tests/                   # ✅ Test suite (pytest + async)
│   ├── test_config.py
│   └── test_tools.py
├── refer/                   # 📖 Reference documentation
│   ├── langgraph/           #    LangGraph docs & examples
│   └── specs/               #    Project specifications
├── backlog/                 # 📋 Development backlog
│   ├── active.md            #    Current features
│   └── release-*.md         #    Release notes
├── .env.example             # 🔑 Environment template
├── pyproject.toml           # 📦 Package configuration
├── CLAUDE.md                # 🤖 AI assistant guide
└── README.md                # 📄 This file
```

### Architecture

#### Technology Stack

<table>
<tr>
<td><b>AI & Agents</b></td>
<td>

- **LangGraph** 0.2+ - Agent orchestration, stateful workflows
- **LangChain Core** 0.3+ - Tool framework, message handling
- **Anthropic Claude** - Sonnet 4.5 for reasoning & analysis

</td>
</tr>
<tr>
<td><b>User Interface</b></td>
<td>

- **Textual** 1.0+ - Modern terminal UI framework
- **Typer** 0.15+ - CLI framework with type hints
- **Rich** 13+ - Terminal formatting & markdown

</td>
</tr>
<tr>
<td><b>Data & HTTP</b></td>
<td>

- **httpx** 0.28+ - Async HTTP client
- **Pydantic** 2.0+ - Data validation & settings
- **python-dotenv** - Environment management

</td>
</tr>
</table>

#### Agent Design Pattern

Both agents implement the **ReAct (Reasoning + Acting)** pattern:

```
User Query → Agent Reasoning → Tool Selection → Tool Execution → Response Formatting
     ↑                                                                    ↓
     └──────────────────── Streaming Updates ←──────────────────────────┘
```

**Portfolio Analysis Agent (17 tools available):**
- **Market Data**: `get_stock_price`, `get_stock_overview` (Alpha Vantage)
- **Fundamentals**: `get_company_fundamentals`, `get_financial_ratios`, `get_insider_trades`, `screen_stocks` (FMP)
- **Filings**: `search_company_by_ticker`, `get_latest_10k`, `get_latest_10q`, `get_institutional_holdings`, `get_company_filings` (SEC)
- **Use cases**: Stock analysis, fundamental screening, insider tracking, regulatory research

**Market Research Agent (6 tools available):**
- **Macro**: `get_economic_indicator`, `get_key_macro_indicators` (FRED)
- **Treasury**: `get_treasury_yield_curve`, `get_treasury_rate`, `get_treasury_yield_spread`, `get_debt_to_gdp` (Treasury)
- **Use cases**: Macro analysis, yield curve interpretation, regime detection, economic trends

---

## 🛠️ Development

### Setup Development Environment

```bash
# Clone and setup
git clone https://github.com/navam-io/navam-invest.git
cd navam-invest
python3 -m venv .venv
source .venv/bin/activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_tools.py -v

# Run with coverage report
pytest --cov=src/navam_invest --cov-report=term-missing
```

**Current Coverage:** 7/7 tests passing ✅

### Code Quality

```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Type check
mypy src/

# Run all quality checks
black src/ tests/ && ruff check src/ tests/ && mypy src/
```

### Development Tools

- **Black** - Code formatting (88 char line length)
- **Ruff** - Fast Python linter
- **MyPy** - Static type checking
- **pytest** - Testing framework with async support
- **Textual DevTools** - TUI hot-reload (`textual run --dev`)

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **🐛 Report Bugs**: [Open an issue](https://github.com/navam-io/navam-invest/issues)
2. **💡 Suggest Features**: [Start a discussion](https://github.com/navam-io/navam-invest/discussions)
3. **📝 Improve Docs**: Submit PR for documentation improvements
4. **🔧 Submit Code**: Fork, create branch, submit PR

### Development Workflow

```bash
# 1. Create feature branch
git checkout -b feature/your-feature-name

# 2. Make changes and test
pytest

# 3. Format and lint
black src/ tests/
ruff check src/ tests/

# 4. Commit and push
git commit -m "feat: add your feature"
git push origin feature/your-feature-name

# 5. Open Pull Request
```

### Adding New Agents

See `CLAUDE.md` for comprehensive guide on adding new LangGraph agents and tools.

---

## 📋 Roadmap

### ✅ v0.1.5 (Released 2025-10-05)
- [x] Financial Modeling Prep integration (fundamentals, ratios, insider trades, screening)
- [x] U.S. Treasury data integration (yield curves, spreads, debt metrics)
- [x] SEC EDGAR integration (10-K, 10-Q, 13F filings)
- [x] Unified tools registry (17 tools across 5 categories)

### v0.2.0 (Planned)
- [ ] Tier 2 macro APIs (World Bank, OECD)
- [ ] Alternative data (CoinGecko crypto, NewsAPI sentiment)
- [ ] Portfolio optimization agent (MPT, Black-Litterman)
- [ ] Tax-loss harvesting agent
- [ ] Conversation persistence with LangGraph checkpointers
- [ ] Enhanced TUI with portfolio display panels

### v0.3.0 (Planned)
- [ ] Multi-agent supervisor for coordinated analysis
- [ ] Backtesting framework with historical data
- [ ] Risk metrics dashboard (VaR, beta, Sharpe)
- [ ] Custom screening agents
- [ ] Export capabilities (CSV/JSON/PDF)

### Future
- [ ] Web UI (Streamlit or FastAPI + HTMX)
- [ ] Mobile app (React Native)
- [ ] LangGraph Cloud deployment
- [ ] Social trading features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with these amazing open-source projects:

- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration framework
- [LangChain](https://github.com/langchain-ai/langchain) - LLM application framework
- [Anthropic Claude](https://www.anthropic.com/) - AI reasoning engine
- [Textual](https://github.com/Textualize/textual) - Terminal UI framework
- [Typer](https://github.com/tiangolo/typer) - CLI framework

Data sources:
- [Alpha Vantage](https://www.alphavantage.co/) - Stock market data
- [Financial Modeling Prep](https://financialmodelingprep.com/) - Fundamentals & financials
- [FRED](https://fred.stlouisfed.org/) - Economic data from St. Louis Fed
- [U.S. Treasury](https://fiscaldata.treasury.gov/) - Treasury yields & debt data
- [SEC EDGAR](https://www.sec.gov/edgar) - Corporate filings

---

## 🔗 Links

- **Homepage**: [github.com/navam-io/navam-invest](https://github.com/navam-io/navam-invest)
- **Documentation**: [View on GitHub](https://github.com/navam-io/navam-invest/tree/main/refer)
- **Issues**: [Report bugs](https://github.com/navam-io/navam-invest/issues)
- **Discussions**: [Join the conversation](https://github.com/navam-io/navam-invest/discussions)

---

<div align="center">

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ by the Navam team

</div>
