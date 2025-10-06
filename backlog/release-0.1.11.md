# Release 0.1.11

## Status
IN DEVELOPMENT

## Features

### Agent Architecture Documentation

**Comprehensive multi-agent system specifications**

Created detailed architectural documentation for Navam Invest's multi-agent system:

1. **agents-tools.md** - Agent-Tool-API Mapping
   - Complete mapping of 18 specialized agents to their tools, system prompts, and required APIs
   - Current implementation status (Portfolio, Research agents completed)
   - Tool-to-API mapping table with free tier limits
   - Agent implementation priority across 5 phases (v0.1.11 through v0.4.x+)
   - Tool gap analysis identifying missing capabilities for each priority agent
   - Future requirements for local computation tools and additional API integrations

2. **multi-agents.md** - Multi-Agent Workflows
   - Multi-agent architecture patterns (Supervisor, Hierarchical, Sequential)
   - State schema design for global investment state
   - 6 comprehensive workflows:
     - Workflow 1: Comprehensive Investment Analysis (Quill → Macro Lens → Risk Shield → Atlas)
     - Workflow 2: Portfolio Rebalancing with Tax Optimization (Atlas → Rebalance Bot → Tax Scout → Trader Jane)
     - Workflow 3: Earnings-Driven Position Adjustment (Earnings Whisperer → Quill → Risk Shield → Trader Jane)
     - Workflow 4: News-Triggered Risk Response (News Sentry → Quill → Risk Shield → Hedge Smith)
     - Workflow 5: Systematic Idea Generation Pipeline (Screen Forge → Quill → Atlas → Notionist)
     - Workflow 6: Year-End Tax Planning (Tax Scout → Quill → Rebalance Bot → Trader Jane)
   - Communication protocols (shared state, tagged messages, structured handoffs, event-driven)
   - Supervisor implementations (LLM-based, rule-based, hybrid)
   - Error handling and recovery patterns
   - Testing strategies for multi-agent systems
   - Implementation priority aligned with agent roadmap

These specifications provide the architectural blueprint for building sophisticated multi-agent workflows in future releases.

**Files Created**:
- `refer/specs/agents-tools.md`
- `refer/specs/multi-agents.md`

**Documentation**: Complete architectural reference for multi-agent system development

---

### API Alternatives Research & Strategy

**Comprehensive evaluation of free-tier API alternatives to FMP**

Conducted extensive research on alternative APIs to address FMP's limited free-tier stock screening capabilities. The research evaluated 7+ APIs and produced strategic recommendations for a multi-API approach.

**Key Findings**:

1. **APIs Evaluated**:
   - ✅ Alpha Vantage (keep - already integrated)
   - ✅ Finnhub (recommended - add for alternative data)
   - ✅ Tiingo (recommended - add for historical fundamentals)
   - ❌ Twelve Data (rejected - expensive credit costs)
   - ❌ EODHD (rejected - screener requires paid plan)
   - ❌ Polygon.io (rejected - too restrictive at 5 req/min)
   - ❌ IEX Cloud (service shut down in Aug 2024)

2. **Recommended Multi-API Strategy**:
   - **Keep FMP** as primary fundamentals source (250 req/day)
   - **Keep Alpha Vantage** for market data (25-500 calls/day)
   - **Add Finnhub** for alternative data: sentiment, insider sentiment, lobbying (50-60 calls/min)
   - **Add Tiingo** for historical fundamentals (5 years free) and quarterly tracking (50 symbols/hr)
   - **Build custom screener** using local computation + caching (pandas/numpy + DuckDB)

3. **Implementation Roadmap**:
   - **Phase 1 (v0.1.11-0.1.12)**: Add Finnhub integration for alternative data
   - **Phase 2 (v0.1.13-0.1.15)**: Add Tiingo integration for historical fundamentals
   - **Phase 3 (v0.2.x)**: Build custom hybrid screening engine with local computation

4. **Strategic Benefits**:
   - No single free API offers comprehensive screening with generous limits
   - Multi-API approach leverages strengths of different providers
   - All recommended APIs remain 100% free-tier sustainable
   - Custom screener provides full control without API dependency
   - Alternative data (sentiment, lobbying) enriches fundamental analysis

**Files Created**:
- `refer/specs/api-alternatives-report.md` - Comprehensive 300+ line research report with:
  - Detailed evaluation of 7 APIs with pros/cons/recommendations
  - Free tier limits and capabilities comparison
  - Multi-API integration strategy and priorities
  - Cost-benefit analysis of different approaches
  - Implementation roadmap with specific tasks
  - API comparison matrix

**Next Actions**:
- Implement Finnhub integration (Priority 1) ✅ COMPLETED
- Implement Tiingo integration (Priority 2)
- Design custom screening engine (Priority 3)

**Documentation**: Complete API alternatives analysis with strategic recommendations

---

### Finnhub Integration for Alternative Data

**Implemented institutional-grade sentiment analysis tools**

Integrated Finnhub API to provide alternative data and sentiment analysis capabilities, significantly enriching the Portfolio agent's analytical power.

**Features Implemented**:

1. **Five New Sentiment Tools**:
   - `get_company_news_sentiment` - News sentiment scores, sector averages, bullish/bearish percentages
   - `get_social_sentiment` - Reddit and Twitter sentiment, mentions, positive/negative scores
   - `get_insider_sentiment` - Monthly Share Purchase Ratio (MSPR), insider trading patterns
   - `get_recommendation_trends` - Analyst ratings distribution (strong buy, buy, hold, sell, strong sell)
   - `get_finnhub_company_news` - Company-specific news articles with summaries

2. **Configuration Updates**:
   - Added `finnhub_api_key` to Settings (config/settings.py)
   - Updated `.env.example` with Finnhub configuration
   - Added Finnhub key binding to tools registry

3. **Agent Enhancement**:
   - Portfolio agent now includes sentiment analysis capabilities
   - Updated system prompt to highlight alternative data tools
   - Added "sentiment" category to tools registry

4. **Comprehensive Testing**:
   - 8 unit tests covering all Finnhub tools
   - 76% code coverage for finnhub.py module
   - Tests for success cases, no-data scenarios, and error handling
   - All tests passing with 100% success rate

**Technical Details**:
- Async API wrapper using httpx
- Rate limit: 50-60 calls/minute on free tier
- Graceful error handling for 401, 403, 429 status codes
- Secure API key binding (credentials outside LLM context)

**Impact**:
- Portfolio agent can now analyze sentiment from multiple sources (news, social media, insiders, analysts)
- Institutional-grade alternative data available to retail investors
- Zero API costs (100% free-tier sustainable)
- 23 total tools available (up from 18)

**Files Created**:
- `src/navam_invest/tools/finnhub.py` - Finnhub API tools module
- `tests/test_finnhub.py` - Comprehensive test suite

**Files Modified**:
- `src/navam_invest/tools/__init__.py` - Registry and API key binding
- `src/navam_invest/config/settings.py` - Configuration
- `src/navam_invest/agents/portfolio.py` - Agent enhancement
- `.env.example` - Environment template

**Documentation**: Complete Finnhub integration with sentiment analysis tools

## Release Date
TBD

## PyPI Package
Not yet published
