# Navam Invest Documentation

Welcome to the comprehensive documentation for **Navam Invest** - an AI-powered investment advisory platform for retail investors.

## Quick Links

- 🚀 **[Getting Started](user-guide/getting-started.md)** - Installation, setup, and first queries
- ❓ **[FAQ](faq.md)** - Frequently asked questions covering all features
- 🤖 **[Agents Guide](user-guide/agents.md)** - Complete agent reference
- 🔀 **[Multi-Agent Workflows](user-guide/multi-agent-workflows.md)** - How agents collaborate
- 🛠️ **[API Tools](user-guide/api-tools.md)** - Available data sources and tools
- 🏗️ **[Architecture](architecture/about.md)** - System design and technical overview

---

## Documentation Structure

### User Guide

**For End Users** - How to use Navam Invest effectively

| Document | Description |
|----------|-------------|
| **[Getting Started](user-guide/getting-started.md)** | Quick installation, setup, and first queries |
| **[Agents Guide](user-guide/agents.md)** | Complete reference for all 7 specialized agents |
| **[Multi-Agent Workflows](user-guide/multi-agent-workflows.md)** | Understanding agent collaboration patterns |
| **[API Tools](user-guide/api-tools.md)** | Data sources, API keys, and tool capabilities |

### FAQ

**[Frequently Asked Questions](faq.md)**

Comprehensive Q&A covering:
- First-time user questions (setup, usage, interface)
- Agent behavior (switching, tool calls, error handling)
- Multi-agent workflows (when they trigger, how they work)
- Error handling (tool failures, API issues, recovery)
- Data sources (free vs. paid, which APIs to use)
- Features (all released features through v0.1.32)
- Advanced usage (customization, batch mode, programmatic access)
- Troubleshooting (common issues and solutions)

### Architecture

**For Developers & Power Users** - Technical design and internals

| Document | Description |
|----------|-------------|
| **[About](architecture/about.md)** | Product vision, tech stack, architecture overview |
| **[Agents-Tools Mapping](architecture/agents-tools-mapping.md)** | Which agents use which tools |

### Development

**For Contributors** - Implementation details and release notes

| Document | Description |
|----------|-------------|
| **[API Command Implementation](development/api-command-implementation.md)** | `/api` command design and implementation |
| **[API Status Report](development/api-status-report.md)** | API provider evaluation and selection |
| **[NewsAPI Updates](development/newsapi-updates.md)** | NewsAPI.org vs NewsAPI.ai clarification |
| **[Release v0.1.28](development/release-v0.1.28.md)** | Release summary for v0.1.28 |

---

## Common Workflows

### For First-Time Users

1. **[Install and Setup](user-guide/getting-started.md#quick-installation-3-steps)** (5 minutes)
2. **[Test with `/api`](user-guide/getting-started.md#launch-and-test)** (verify connectivity)
3. **[Try First Query](user-guide/getting-started.md#your-first-queries)** (stock price lookup)
4. **[Explore Agents](user-guide/agents.md)** (learn what each agent does)
5. **[Read FAQ](faq.md)** (understand how everything works)

### For Power Users

1. **[Agent Reference](user-guide/agents.md)** (all 16 planned agents)
2. **[Multi-Agent Patterns](user-guide/multi-agent-workflows.md)** (orchestration strategies)
3. **[Tool Capabilities](user-guide/api-tools.md)** (32 tools across 9 APIs)
4. **[Architecture Deep-Dive](architecture/about.md)** (LangGraph, Claude, Textual)
5. **[Advanced FAQ](faq.md#advanced-usage)** (customization, batch mode, programmatic use)

### For Contributors

1. **[Architecture Overview](architecture/about.md)** (understand the system)
2. **[Development Docs](development/)** (implementation notes)
3. **[CLAUDE.md](../CLAUDE.md)** (AI development guidelines)
4. **[README.md](../README.md)** (project overview)
5. **[Contributing Guide](../CONTRIBUTING.md)** (PR workflow)

---

## Key Features (v0.1.32)

### 7 Specialized AI Agents

- **Quill** - Equity research analyst (36 tools)
- **Earnings Whisperer** - Earnings specialist (14 tools)
- **Screen Forge** - Stock screener (15 tools)
- **Macro Lens** - Market strategist (13 tools)
- **News Sentry** - Event monitor (13 tools) 🆕
- **Portfolio** - General analysis (legacy)
- **Research** - Macro research (legacy)

### Multi-Agent Workflows

- **`/analyze`** - Complete investment analysis (Quill → Macro Lens → Synthesis)
- More workflows coming in future releases

### Data Sources (9 APIs, 32 Tools)

**Always Free (No Keys Needed)**:
- Yahoo Finance (11 tools)
- SEC EDGAR (9 tools)
- U.S. Treasury (4 tools)

**Optional (Free Tiers)**:
- Tiingo, Finnhub, Alpha Vantage, FRED, NewsAPI.org

### Interactive TUI

- Real-time streaming responses
- Tool execution tracking
- Auto-save reports to `reports/`
- Smart input disabling during processing
- Keyboard shortcuts (`Ctrl+C`, `Ctrl+Q`)

---

## API Reference

### Agent Commands

```bash
# Agent switching
/quill         # Equity research
/earnings      # Earnings analysis
/screen        # Stock screening
/macro         # Macro strategy
/news          # Event monitoring
/portfolio     # Portfolio analysis (legacy)
/research      # Market research (legacy)

# Multi-agent workflows
/analyze AAPL  # Complete investment analysis

# System commands
/api           # Check API status
/examples      # Show example prompts
/help          # Show all commands
/clear         # Clear chat (Ctrl+C)
/quit          # Exit app (Ctrl+Q)
```

### Keyboard Shortcuts

```bash
Ctrl+C    # Clear chat history
Ctrl+Q    # Quit application
↑/↓       # Scroll chat
Mouse     # Scroll, select text
```

---

## Version History

### Current Release: v0.1.32 (In Development)

- ✅ **News Sentry Agent**: Real-time event detection
- ✅ **8-K Monitoring**: Material corporate events
- ✅ **Form 4 Tracking**: Insider trading alerts
- ✅ **Breaking News**: Sentiment analysis
- ✅ **Analyst Ratings**: Change tracking

### Recent Releases

- **v0.1.31** (Jan 10, 2025) - Enhanced UX, full responses, auto-save
- **v0.1.30** (Jan 8, 2025) - Removed FMP, improved reliability
- **v0.1.28** (Jan 5, 2025) - `/api` command, self-service diagnostics
- **v0.1.27** (Dec 29, 2024) - Earnings Whisperer agent
- **v0.1.26** (Dec 22, 2024) - Yahoo Finance + enhanced EDGAR

See [backlog/](../backlog/) for complete release notes.

---

## External Resources

### Official Links

- **PyPI**: [pypi.org/project/navam-invest](https://pypi.org/project/navam-invest/)
- **GitHub**: [github.com/navam-io/navam-invest](https://github.com/navam-io/navam-invest)
- **Issues**: [github.com/navam-io/navam-invest/issues](https://github.com/navam-io/navam-invest/issues)
- **Twitter**: [@navam_io](https://twitter.com/navam_io)

### Technology Stack

- **LangGraph**: [langchain-ai.github.io/langgraph](https://langchain-ai.github.io/langgraph/)
- **Anthropic Claude**: [docs.anthropic.com](https://docs.anthropic.com/)
- **Textual TUI**: [textual.textualize.io](https://textual.textualize.io/)
- **Yahoo Finance**: [github.com/ranaroussi/yfinance](https://github.com/ranaroussi/yfinance)
- **SEC EDGAR**: [sec.gov/edgar/sec-api-documentation](https://www.sec.gov/edgar/sec-api-documentation)

### Community

- **Discussions**: [GitHub Discussions](https://github.com/navam-io/navam-invest/discussions)
- **Discord**: Coming soon
- **Email**: contact@navam.io

---

## Contributing

We welcome contributions! See:
- **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines
- **[CLAUDE.md](../CLAUDE.md)** - AI development workflow
- **[Development Docs](development/)** - Implementation notes

---

## License

Navam Invest is licensed under the **MIT License**. See [LICENSE](../LICENSE) for details.

---

**Built with ❤️ for retail investors**

[⬆ Back to Top](#navam-invest-documentation)
