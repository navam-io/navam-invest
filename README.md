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
- Company fundamentals analysis
- Investment insights and recommendations
- Technical indicators

</td>
<td width="50%">

**Market Research Agent**
- Macroeconomic indicators (GDP, CPI, unemployment)
- Federal Reserve data (FRED)
- Economic trend analysis
- Market condition assessment

</td>
</tr>
</table>

### 📊 **Real API Integrations**

| API | Purpose | Cost |
|-----|---------|------|
| **Alpha Vantage** | Stock prices, company fundamentals | Free tier: 25 calls/day |
| **FRED (St. Louis Fed)** | Economic indicators, macro data | Free (unlimited) |
| **Anthropic Claude** | AI reasoning and tool orchestration | Pay-as-you-go |

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

   # Optional (but recommended)
   ALPHA_VANTAGE_API_KEY=your_key_here
   FRED_API_KEY=your_key_here
   ```

3. **Get API Keys** (all free tiers available):
   - **Anthropic**: [console.anthropic.com](https://console.anthropic.com/) (pay-as-you-go)
   - **Alpha Vantage**: [alphavantage.co/support/#api-key](https://www.alphavantage.co/support/#api-key) (free)
   - **FRED**: [fredaccount.stlouisfed.org/apikeys](https://fredaccount.stlouisfed.org/apikeys) (free)

### Usage

#### Launch the Interactive TUI

```bash
navam tui
```

#### Example Interactions

**Portfolio Analysis:**
```
You: What's the current price of AAPL?
Portfolio Agent: [Fetches real-time data and provides formatted response]

You: Show me Apple's fundamentals
Portfolio Agent: [Displays P/E ratio, EPS, market cap, sector info, etc.]
```

**Market Research:**
```
You: /research
You: What's the current GDP?
Research Agent: [Fetches latest GDP data from FRED with date and trend]

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
navam tui       # Launch interactive TUI
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
│   ├── tools/               # 🔧 API integration tools
│   │   ├── alpha_vantage.py #    Stock price & fundamentals
│   │   └── fred.py          #    Economic indicators & macro data
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

**Portfolio Analysis Agent:**
- Tools: `get_stock_price`, `get_stock_overview`
- Use cases: Stock analysis, fundamentals, investment research

**Market Research Agent:**
- Tools: `get_economic_indicator`, `get_key_macro_indicators`
- Use cases: Macro analysis, economic trends, regime detection

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

### v0.2.0 (Planned)
- [ ] Portfolio optimization agent (MPT, Black-Litterman)
- [ ] Tax-loss harvesting agent
- [ ] SEC EDGAR filings integration
- [ ] Conversation persistence with checkpointers
- [ ] TUI panels for portfolio display

### v0.3.0 (Planned)
- [ ] Multi-agent supervisor for coordinated analysis
- [ ] Backtesting framework
- [ ] Risk metrics dashboard
- [ ] Custom screening agents
- [ ] Export to CSV/JSON

### Future
- [ ] Web UI (Streamlit or FastAPI + HTMX)
- [ ] Mobile app (React Native)
- [ ] Cloud deployment option
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
- [FRED](https://fred.stlouisfed.org/) - Economic data from St. Louis Fed

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
