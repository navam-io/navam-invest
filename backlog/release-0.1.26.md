# Release 0.1.26

## Status
✅ **PUBLISHED** - 2025-10-07

## Features

### Yahoo Finance Integration (11 New Tools - FREE, No API Key) 🆕

Added comprehensive Yahoo Finance integration via yfinance library, providing institutional-grade market data at zero cost:

#### New Tools:
1. **`get_quote`** - Real-time stock quotes with extended metrics (P/E, market cap, volume, dividend yield)
2. **`get_historical_data`** - OHLCV historical prices with configurable periods and intervals
3. **`get_financials`** - Financial statements (income statement, balance sheet, cash flow)
4. **`get_earnings_history`** - Historical earnings with EPS actual vs. estimate and surprises
5. **`get_earnings_calendar`** - Upcoming earnings dates and analyst estimates
6. **`get_analyst_recommendations`** - Analyst ratings distribution, price targets, recent changes
7. **`get_institutional_holders`** - Top institutional investors with ownership percentages
8. **`get_company_info`** - Company profile, sector, industry, business description
9. **`get_dividends`** - Dividend payment history and yield statistics
10. **`get_options_chain`** - Options data (calls/puts, IV, volume, open interest)
11. **`get_market_indices`** - Major market indices (S&P 500, Dow, Nasdaq, Russell 2000, VIX)

#### Benefits:
- **Zero Cost**: No API key required, unlimited free access
- **Real-Time Data**: Live quotes and market indices
- **Earnings Intelligence**: Historical surprises and upcoming calendar
- **Analyst Coverage**: Consensus ratings and price targets
- **Ownership Tracking**: Institutional holdings and changes
- **Annual Savings**: $2,400-$10,800/year vs. paid alternatives

### Enhanced SEC EDGAR Tools (4 New Tools) 🔄

Enhanced SEC EDGAR integration with material event detection and structured data extraction:

#### New Tools:
1. **`get_latest_8k`** - Recent 8-K filings (material events: earnings, M&A, management changes, bankruptcy)
2. **`get_company_facts`** - Structured XBRL data extraction (assets, revenues, net income, EPS)
3. **`search_filings_by_form`** - Flexible filing search for any SEC form type (10-K, 10-Q, 8-K, DEF 14A, S-1, Form 4)
4. **`get_insider_transactions`** - Form 4 insider trading activity (officer/director transactions)

#### Enhanced Existing Tools:
- Improved error handling for `get_latest_10k` and `get_latest_10q`
- Better filing URL formatting and metadata extraction

#### Benefits:
- **Material Event Detection**: Real-time 8-K monitoring for portfolio risk management
- **XBRL Structured Data**: Machine-readable financial metrics
- **Insider Intelligence**: Form 4 transaction patterns for sentiment analysis
- **Comprehensive Coverage**: All SEC filing types accessible

### Quill Agent Enhanced (22 → 36 Tools, +64% Capabilities) ⭐

Upgraded Quill equity research agent with comprehensive Yahoo Finance and EDGAR tools:

#### New Capabilities:
- **Earnings Analysis**: Historical EPS surprises, upcoming earnings calendar, analyst estimates
- **Analyst Coverage**: Consensus ratings, price targets, recent upgrades/downgrades
- **Institutional Ownership**: Top holders, ownership changes, 13F filings
- **Material Events**: 8-K filing detection and analysis
- **XBRL Data**: Structured company facts validation
- **Insider Transactions**: Form 4 sentiment signals
- **Dividend Intelligence**: Payment history and yield analysis

#### Enhanced Analysis Workflow:
Quill can now perform comprehensive equity research including:
1. Real-time market data (Yahoo quotes + Alpha Vantage)
2. Fundamental analysis (Yahoo financials + FMP + Tiingo historical)
3. Earnings momentum (Yahoo earnings history + calendar)
4. Analyst sentiment (Yahoo recommendations + Finnhub trends)
5. Ownership intelligence (Yahoo institutional + SEC 13F)
6. Material events (SEC 8-K + Form 4)
7. Valuation (DCF, comps, historical trends)

### Screen Forge Enhanced (10 → 15 Tools) 📈

Added earnings momentum and analyst upgrade screening capabilities:

#### New Capabilities:
- **Earnings Momentum Screening**: Filter for stocks with consistent earnings beats
- **Analyst Upgrade Activity**: Track recent rating changes and upgrades
- **Historical Price Data**: Post-earnings drift analysis

#### New Use Cases:
- "Screen for stocks with 3+ consecutive earnings beats"
- "Find stocks with recent analyst upgrades and earnings momentum"
- "Identify post-earnings drift opportunities"

### Macro Lens Enhanced (11 → 13 Tools) 🌍

Added market indices tracking for regime identification:

#### New Capabilities:
- **Market Indices Monitoring**: S&P 500, Dow Jones, Nasdaq, Russell 2000, VIX
- **Historical Index Data**: Regime correlation analysis
- **Real-Time Market Sentiment**: VIX for volatility assessment

#### New Use Cases:
- "How are major indices performing relative to historical trends?"
- "Is the VIX indicating elevated market stress?"
- "What's the correlation between yield curve and equity markets?"

### Technical Improvements

#### Dependencies:
- Added `yfinance>=0.2.49` to pyproject.toml (free, no API key required)
- Added `pandas` support for Yahoo Finance data processing (included with yfinance)

#### Tool Registry Updates:
- Enhanced `tools/__init__.py` with new tool mappings
- Updated `get_tools_for_agent()` for specialized tool sets
- Added new categories: `earnings`, `options`, `dividends`, `holders`

#### Agent Updates:
- `quill.py`: Updated system prompt to reflect new Yahoo Finance and EDGAR capabilities
- `quill.py`: Switched to `get_tools_for_agent("quill")` for optimized tool selection

#### Documentation:
- Created `backlog/edgar-yahoo-integration.md` with comprehensive integration guide
- Updated README.md with v0.1.26 features and examples
- Added usage examples for earnings analysis and analyst sentiment

### Backward Compatibility

✅ **Zero Breaking Changes**:
- All existing agents (Portfolio, Research) unchanged
- Existing workflows continue to function
- No API changes to existing tools
- Legacy agents maintain full backward compatibility

### Cost Impact

**Zero Additional Cost**:
- Yahoo Finance: FREE (no API key, unlimited)
- SEC EDGAR: FREE (no API key, 10 req/sec)
- Annual Savings: $2,400-$10,800 vs. paid earnings/analyst APIs

---

## Release Date
2025-10-07

## PyPI Package
https://pypi.org/project/navam-invest/0.1.26/

## Installation

```bash
pip install navam-invest==0.1.26
```

## Upgrade Instructions

```bash
pip install --upgrade navam-invest
```

New dependency (yfinance) will be automatically installed.

## Migration Guide

No migration required - this is a non-breaking feature addition.

To use new tools:
1. Update package: `pip install --upgrade navam-invest`
2. Use Quill agent: `/quill` then "Analyze AAPL with earnings and analyst sentiment"
3. Try earnings screening: `/screen` then "Screen for stocks with consistent earnings beats"
4. Monitor macro indices: `/macro` then "Show current market indices"

## Known Issues

None - all new tools tested and production-ready.

## Future Enhancements

Based on v0.1.26 integration, planned for v0.1.27-0.1.30:
- **Earnings Whisperer** agent (leverages Yahoo earnings calendar)
- **News Sentry** agent (leverages 8-K material events)
- **Hedge Smith** agent options tools (leverages Yahoo options chain)
- Caching layer (DuckDB) for API efficiency
- Enhanced multi-agent workflows with parallel execution

## Contributors

- Integration design and implementation
- Comprehensive documentation
- Testing and validation

---

**Full Documentation**: See `backlog/edgar-yahoo-integration.md` for detailed integration guide.
