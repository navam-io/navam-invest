# Agents-Tools Mapping

This document maps each Navam Invest agent to their system prompts, required tools, and data source APIs.

## Current Implementation Status

✅ **Implemented**
🚧 **Planned**
📋 **Future**

---

## Agent-Tool Matrix

| Agent | Status | System Prompt | Tools | APIs | Notes |
|-------|--------|---------------|-------|------|-------|
| **Portfolio (Current)** | ✅ | Portfolio analysis assistant with comprehensive market data access | `get_stock_price`, `get_stock_overview`, `get_company_fundamentals`, `get_financial_ratios`, `get_insider_trades`, `screen_stocks`, `search_company_by_ticker`, `get_company_filings`, `get_latest_10k`, `get_latest_10q`, `get_institutional_holdings`, `search_market_news`, `get_company_news`, `read_local_file`, `list_local_files` | Alpha Vantage, FMP, SEC EDGAR, NewsAPI | Combines market data, fundamentals, filings, and news |
| **Research (Current)** | ✅ | Market research assistant specializing in macroeconomic analysis and market news | `get_economic_indicator`, `get_key_macro_indicators`, `get_treasury_yield_curve`, `get_treasury_rate`, `get_treasury_yield_spread`, `get_debt_to_gdp`, `search_market_news`, `get_top_financial_headlines`, `get_company_news`, `read_local_file`, `list_local_files` | FRED, U.S. Treasury, NewsAPI | Focuses on macro data and sentiment |
| **Quill** (Equity Research) | 🚧 | Expert fundamental equity analyst doing bottom-up company research, thesis building, and valuation (DCF, comps). Find mispriced quality stocks with live theses including catalysts and risks. | `get_company_fundamentals`, `get_financial_ratios`, `get_latest_10k`, `get_latest_10q`, `get_company_filings`, `search_market_news`, `get_company_news`, `get_insider_trades`, `get_stock_price`, `read_local_file` | FMP, SEC EDGAR, NewsAPI, Alpha Vantage | Deep fundamental analysis |
| **Atlas** (Investment Strategist) | 🚧 | Expert portfolio strategist doing strategic asset allocation, defining target weights, and setting investment policy for long-term risk-adjusted returns. | Portfolio optimization tools (future), `read_local_file`, `list_local_files`, `get_key_macro_indicators`, `get_treasury_yield_curve` | Local optimization libs, FRED, Treasury | Strategic allocation |
| **Macro Lens** | 🚧 | Expert macro strategist doing top-down analysis of rates, inflation, cycles, sectors, and factor regimes to align tilts with macro conditions. | `get_economic_indicator`, `get_key_macro_indicators`, `get_treasury_yield_curve`, `get_treasury_yield_spread`, `get_debt_to_gdp`, `get_top_financial_headlines`, `search_market_news` | FRED, Treasury, NewsAPI, World Bank (future) | Macro regime analysis |
| **Screen Forge** | 🚧 | Expert equity screener doing factor, quality, momentum, and thematic screens to keep refreshed candidate bench. | `screen_stocks`, `get_financial_ratios`, `get_company_fundamentals`, Factor screening tools (future) | FMP, Alpha Vantage, Custom factor libs | Idea generation |
| **News Sentry** | 🚧 | Expert market-news and event-detection analyst filtering news, 8-Ks, downgrades, and unusual volume to surface material time-sensitive items. | `search_market_news`, `get_company_news`, `get_top_financial_headlines`, `get_company_filings`, Volume/price alerts (future) | NewsAPI, SEC EDGAR, Marketaux (future) | Real-time signals |
| **Earnings Whisperer** | 📋 | Expert earnings analyst tracking calendar, digesting transcripts, and analyzing surprises to capture post-earnings drift. | Earnings calendar (future), Transcript analysis (future), `get_company_news`, `get_company_fundamentals` | FMP (earnings), Finnhub (future) | Earnings analysis |
| **Rebalance Bot** | 📋 | Expert rebalancing specialist doing drift detection, tax-aware rebalancing, and cash deployment. | Portfolio drift calculation (future), Rebalancing optimizer (future), `read_local_file` | Local optimization | Portfolio maintenance |
| **Tax Scout** | 📋 | Expert tax-aware specialist doing lot selection, wash-sale checks, and tax-loss harvesting. | Tax lot tracking (future), Wash sale detection (future), `read_local_file` | Local tax engine | Tax optimization |
| **Risk Shield** | 📋 | Expert risk manager doing exposure monitoring, drawdown/VAR checks, and scenario testing. | Risk metrics calculation (future), VaR/CVaR (future), Scenario analysis (future) | Local risk libs | Risk management |
| **Quant Smith** | 📋 | Expert quantitative engineer doing risk/return modeling, factor exposure, and optimization under constraints. | Portfolio optimization (future), Factor analysis (future), `read_local_file` | PyPortfolioOpt, Local quant libs | Quantitative optimization |
| **Factor Scout** | 📋 | Expert factor analyst measuring exposure to value, quality, momentum, size, and low-vol factors. | Factor exposure tools (future), `get_financial_ratios`, `screen_stocks` | Local factor libs, FMP | Style analysis |
| **Compass** (Goal Planning) | 📋 | Expert personal-finance planner doing goal mapping, risk profiling, and cash-flow buffers. | Goal tracking (future), Risk profiling (future), `read_local_file`, `get_treasury_yield_curve` | Local planning tools | Financial planning |
| **Ledger** (Performance) | 📋 | Expert performance analyst doing return calculation, benchmark selection, and multi-period attribution. | Performance calculation (future), Attribution analysis (future), `read_local_file` | Local analytics | Performance reporting |
| **Trader Jane** | 📋 | Expert execution trader doing order slicing, venue selection, and post-trade analysis. | Order routing (future), TCA (future) | Broker APIs (future) | Trade execution |
| **Hedge Smith** | 📋 | Expert options strategist doing collars, covered calls, and protective puts for defined risk. | Options pricing (future), Greeks calculation (future), `get_stock_price` | Options data APIs (future) | Options strategies |
| **Steward** (Cash Management) | 📋 | Expert cash manager doing cash sweeps, T-bill ladders, and dry-powder allocation. | `get_treasury_rate`, `get_treasury_yield_curve`, Cash ladder tools (future) | Treasury, Local cash tools | Cash optimization |
| **Sentinel** (Compliance) | 📋 | Expert compliance guard checking position limits, pattern day-trading, and wash-sale flags. | Compliance rules engine (future), `read_local_file` | Local compliance | Regulatory checks |
| **Notionist** (Knowledge) | 📋 | Expert research librarian organizing theses, notes, and decisions with versioning. | Document management (future), Version control (future), `read_local_file`, `list_local_files` | Local storage, SQLite | Knowledge management |

---

## Tool-to-API Mapping

### Market Data Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `get_stock_price` | Alpha Vantage | 25-500 calls/day | Real-time quotes |
| `get_stock_overview` | Alpha Vantage | 25-500 calls/day | Company overview |

### Fundamental Data Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `get_company_fundamentals` | FMP | 250 req/day | Financial statements |
| `get_financial_ratios` | FMP | 250 req/day | Key ratios |
| `get_insider_trades` | FMP | 250 req/day | Insider activity |
| `screen_stocks` | FMP | 250 req/day | Stock screening |

### Macro Data Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `get_economic_indicator` | FRED | Unlimited with key | Economic data |
| `get_key_macro_indicators` | FRED | Unlimited with key | Macro dashboard |

### Treasury Data Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `get_treasury_yield_curve` | U.S. Treasury | Unlimited, no key | Yield curve |
| `get_treasury_rate` | U.S. Treasury | Unlimited, no key | Specific rates |
| `get_treasury_yield_spread` | U.S. Treasury | Unlimited, no key | Rate spreads |
| `get_debt_to_gdp` | U.S. Treasury | Unlimited, no key | Debt metrics |

### News & Sentiment Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `search_market_news` | NewsAPI.org | 100 req/day | News search |
| `get_top_financial_headlines` | NewsAPI.org | 100 req/day | Top headlines |
| `get_company_news` | NewsAPI.org | 100 req/day | Company news |

### SEC Filings Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `search_company_by_ticker` | SEC EDGAR | 10 req/sec | Company lookup |
| `get_company_filings` | SEC EDGAR | 10 req/sec | All filings |
| `get_latest_10k` | SEC EDGAR | 10 req/sec | Annual report |
| `get_latest_10q` | SEC EDGAR | 10 req/sec | Quarterly report |
| `get_institutional_holdings` | SEC EDGAR | 10 req/sec | 13F filings |

### Local Data Tools
| Tool | API | Free Tier | Purpose |
|------|-----|-----------|---------|
| `read_local_file` | Local filesystem | N/A | Read user files |
| `list_local_files` | Local filesystem | N/A | List available files |

---

## Agent Implementation Priority

### Phase 1 (Completed - v0.1.10)
- ✅ Portfolio Agent - General purpose portfolio analysis
- ✅ Research Agent - Macro and market research

### Phase 2 (Planned - v0.1.11-0.1.15)
- 🚧 Quill (Equity Research) - Deep fundamental analysis
- 🚧 Screen Forge - Systematic idea generation
- 🚧 News Sentry - Real-time signal filtering
- 🚧 Macro Lens - Enhanced macro strategy (upgrade Research)

### Phase 3 (Future - v0.2.x)
- 📋 Atlas - Strategic allocation and IPS
- 📋 Rebalance Bot - Portfolio rebalancing
- 📋 Tax Scout - Tax optimization
- 📋 Risk Shield - Risk management

### Phase 4 (Future - v0.3.x)
- 📋 Quant Smith - Quantitative optimization
- 📋 Factor Scout - Factor analysis
- 📋 Ledger - Performance attribution
- 📋 Compass - Goal-based planning

### Phase 5 (Future - v0.4.x+)
- 📋 Earnings Whisperer - Earnings analysis
- 📋 Trader Jane - Execution (requires broker integration)
- 📋 Hedge Smith - Options strategies
- 📋 Steward - Cash management
- 📋 Sentinel - Compliance checks
- 📋 Notionist - Knowledge management

---

## Tool Gap Analysis

### Missing Tools for Priority Agents

#### Quill (Equity Research) - Ready
- ✅ All fundamental tools available
- ✅ SEC filings access
- ✅ News integration
- ⚠️ Consider: Valuation calculator (DCF, comps) as local tool

#### Screen Forge - Ready
- ✅ Stock screening available
- ✅ Fundamental ratios available
- ⚠️ Consider: Enhanced factor screening (quality, momentum scores)

#### News Sentry - Mostly Ready
- ✅ News search and filtering
- ❌ Missing: Real-time volume/price alerts
- ❌ Missing: Marketaux API (alternative news source)
- ⚠️ Consider: Unusual activity detection

#### Macro Lens - Ready
- ✅ All macro data tools available
- ✅ Treasury data complete
- ⚠️ Consider: World Bank API for international macro

---

## Future Tool Requirements

### Local Computation Tools (Python Libraries)
- **PyPortfolioOpt**: MPT, Black-Litterman, risk parity
- **pandas/numpy**: Risk calculations (VaR, CVaR, beta, volatility)
- **scikit-learn**: Factor modeling, clustering
- **SHAP/LIME**: Explainability for recommendations
- **DuckDB/SQLite**: Local caching and data storage

### Additional API Integrations
- **Finnhub.io**: Earnings data, alternative metrics
- **Marketaux.com**: Alternative news source
- **World Bank Open Data**: International macro indicators
- **OECD API**: Developed markets data
- **CoinGecko**: Crypto market data (diversification)

### Broker Integrations (Future)
- **Alpaca**: Commission-free trading API
- **Interactive Brokers**: Professional platform
- **TD Ameritrade**: ThinkorSwim integration

---

## Notes

1. **Current agents (Portfolio, Research)** are generalist agents with broad tool access
2. **Specialized agents** will have focused tool sets aligned with their specific roles
3. **Multi-agent workflows** will enable agent collaboration (see multi-agents.md)
4. **Local computation tools** will reduce API dependency and enable sophisticated analytics
5. **Free-tier APIs** are prioritized to maintain accessibility for retail investors
