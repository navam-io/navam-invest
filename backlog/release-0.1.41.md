# Release 0.1.41

## Status
RELEASED - October 14, 2025

## Features

### ✅ Completed Features

**API Caching Layer** - Performance optimization:
- ✅ DuckDB-based caching manager implemented (`src/navam_invest/cache/manager.py` - 596 lines)
- ✅ Intelligent cache invalidation strategies with per-source TTL configuration
- ✅ Cache statistics tracking (hits, misses, hit rates)
- ✅ Configurable cache TTL per data source (real-time: 60s, fundamental: 1h, economic: 24h)
- ✅ `@cached` decorator for easy tool function caching (supports both sync and async functions)
- ✅ Persistent cache storage in user's home directory (`~/.navam-invest/cache/`)
- ✅ Added `duckdb>=1.0.0` dependency
- ✅ Applied caching to **all 42 tool functions** across **9 API sources**:
  - Yahoo Finance: 11 functions (quotes, historical data, financials, earnings, options, etc.)
  - FRED: 2 functions (economic indicators)
  - FMP: 4 functions (fundamentals, ratios, insider trades, screening)
  - Finnhub: 5 functions (news sentiment, social sentiment, insider sentiment, recommendations)
  - Alpha Vantage: 2 functions (stock price, company overview)
  - Tiingo: 4 functions (fundamentals definitions, daily, statements, historical)
  - SEC EDGAR: 9 functions (filings, 10-K, 10-Q, 8-K, Form 4, company facts, search)
  - Treasury: 4 functions (yield curve, rates, spreads, debt-to-GDP)
  - NewsAPI: 3 functions (market news search, top headlines, company news)
- ✅ `/cache` TUI command for viewing cache statistics with Rich tables
- ✅ `/cache clear` command for manual cache invalidation
- ✅ `/cache warm` command for pre-populating cache with common queries
- ✅ Color-coded hit rate indicators (green ≥75%, yellow ≥50%, red <50%)
- ✅ 7-day rolling statistics with detailed per-tool breakdowns
- ✅ Common queries module (`src/navam_invest/cache/common_queries.py`) with predefined warmup queries:
  - Market indices (S&P 500, Dow, Nasdaq, Russell 2000, VIX)
  - Popular stocks (AAPL, MSFT, GOOGL, AMZN, NVDA, META, TSLA)
  - Treasury yield curve
  - Key economic indicators (10Y Treasury, Unemployment, CPI, GDP)

**Technical Implementation:**
- `src/navam_invest/cache/manager.py` - Complete caching manager with DuckDB backend
  - Added `warm_cache()` async method for pre-populating cache
  - Supports both sync and async function execution
  - Returns detailed statistics (total, cached, warmed, failed)
- `src/navam_invest/cache/__init__.py` - Public API exports
- `src/navam_invest/cache/common_queries.py` - Common queries configuration module
  - `get_common_queries()` - Returns list of warmup query dictionaries
  - `get_query_summary()` - Returns human-readable description
- `src/navam_invest/tools/yahoo_finance.py` - All 11 tool functions now use caching
- `src/navam_invest/tools/fred.py` - 2 FRED functions cached
- `src/navam_invest/tools/treasury.py` - 4 Treasury functions cached
- SHA256-based cache key generation from function arguments
- Automatic expiration and cleanup of stale entries
- Statistics recording with daily granularity
- Thread-safe operations
- Cached helper function pattern for compatibility with LangChain `@tool` decorator

**Cached Tool Functions:**
1. `get_quote()` - Real-time stock quotes
2. `get_historical_data()` - Historical OHLCV data
3. `get_financials()` - Financial statements (income, balance sheet, cash flow)
4. `get_earnings_history()` - Historical earnings with surprises
5. `get_earnings_calendar()` - Upcoming earnings dates
6. `get_analyst_recommendations()` - Analyst ratings and price targets
7. `get_institutional_holders()` - Top institutional holders
8. `get_company_info()` - Company profile and business description
9. `get_dividends()` - Dividend payment history
10. `get_options_chain()` - Options chain data (calls/puts)
11. `get_market_indices()` - Major market indices (S&P 500, Dow, Nasdaq, etc.)

### 🚧 Planned Features (for v0.1.42+)

**Workflow Progress Visualization** - Enhanced TUI:
- Enhanced TUI display for multi-agent workflows
- Visual progress indicators for each agent
- Better error recovery and partial completion handling

**Bug Fixes**:
- TUI stability improvements
- Error handling enhancements
- Command processing refinements

---

## Technical Improvements

**Performance Optimization**:
- [x] Implement DuckDB-based caching layer
- [x] Add cache invalidation logic
- [x] Configure per-source TTL settings
- [x] Add cache statistics tracking
- [x] Apply caching decorators to all 42 tool functions across 9 API sources
- [x] Support both sync and async functions in `@cached` decorator
- [x] Add `/cache` TUI command for statistics viewing
- [x] Add `/cache clear` command for manual cache invalidation
- [x] Implement cache warming for common queries
- [x] Add `/cache warm` TUI command
- [x] Create common queries configuration module

**TUI Enhancements**:
- [ ] Enhanced workflow progress visualization
- [ ] Multi-agent status indicators
- [ ] Better error recovery UI
- [ ] Partial completion handling

**Documentation Updates**:
- [ ] Update `docs/user-guide/multi-agent-workflows.md` - New workflows
- [ ] Update `docs/user-guide/getting-started.md` - Workflow examples
- [ ] Create `docs/architecture/workflows.md` - Workflow design patterns

---

## Breaking Changes

None planned for this release.

---

## Release Date
October 14, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.41/
