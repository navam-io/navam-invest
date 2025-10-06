# Release 0.1.12

## Status
IN DEVELOPMENT

## Features

### Tiingo Integration for Historical Fundamentals

**Implemented 5-year historical fundamental analysis capabilities**

Integrated Tiingo API to provide long-term fundamental analysis, quarterly tracking, and historical trend analysis, complementing existing FMP fundamentals with deeper historical data.

**Features Implemented**:

1. **Four New Fundamental Tools**:
   - `get_fundamentals_daily` - Daily-updated metrics (market cap, P/E, P/B ratios) with 90-day default range
   - `get_fundamentals_statements` - Quarterly financial statements (income, balance sheet, cash flow)
   - `get_fundamentals_definitions` - Metadata and field definitions for fundamental metrics
   - `get_historical_fundamentals` - Multi-year trend analysis with CAGR calculations (up to 5 years)

2. **Configuration Updates**:
   - Added `tiingo_api_key` to Settings (config/settings.py)
   - Updated `.env.example` with Tiingo configuration
   - Added Tiingo key binding to tools registry

3. **Agent Enhancement**:
   - Portfolio agent now includes historical fundamental analysis capabilities
   - Updated system prompt to highlight 5-year historical data access
   - Added "Historical Fundamentals" category to tools registry

4. **Comprehensive Testing**:
   - 12 unit tests covering all Tiingo tools
   - 86% code coverage for tiingo.py module
   - Tests for success cases, no-data scenarios, error handling, and free-tier limits
   - All tests passing (48 total project tests)

**Technical Details**:
- Async API wrapper using httpx
- Rate limit: 50 symbols/hour, 1000 requests/day on free tier
- Free tier provides 5 years of historical data (vs 15+ on paid)
- Supports both as-reported and corrected financial statement data
- Graceful error handling for 401, 403, 404, 429 status codes

**Strategic Value**:
- Complements FMP fundamentals with longer historical perspective
- Enables long-term trend analysis and CAGR calculations
- Quarterly statement tracking for earnings analysis
- Free-tier sustainable (50 symbols/hour sufficient for retail investors)
- 27 total tools available (up from 23)

**Files Created**:
- `src/navam_invest/tools/tiingo.py` - Tiingo API tools module (229 lines)
- `tests/test_tiingo.py` - Comprehensive test suite (12 tests, 86% coverage)

**Files Modified**:
- `src/navam_invest/tools/__init__.py` - Registry and API key binding
- `src/navam_invest/config/settings.py` - Configuration
- `src/navam_invest/agents/portfolio.py` - Agent enhancement
- `.env.example` - Environment template

**Use Cases**:
- Long-term fundamental trend analysis (5-year CAGR)
- Quarterly earnings tracking and progression
- Historical P/E ratio and valuation trends
- Balance sheet strength over time
- Free cash flow generation history

**Documentation**: Complete Tiingo integration with historical fundamental analysis

## Release Date
TBD

## PyPI Package
TBD
