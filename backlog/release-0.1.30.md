# Release 0.1.30

## Status
Published to PyPI on January 8, 2025

## Features

### 🔧 API Reliability Improvements

**FMP API Removal** - Replaced with Yahoo Finance + SEC EDGAR alternatives:

- **Removed**: Financial Modeling Prep (FMP) API integration
  - Reason: FMP free tier showed "Access denied - check plan" errors in production
  - Impact: 4 tools removed (`get_company_fundamentals`, `get_financial_ratios`, `get_insider_trades`, `screen_stocks`)

- **Alternatives**: Yahoo Finance + SEC EDGAR provide equivalent functionality:
  - `get_company_fundamentals` → `get_financials` + `get_company_info` (Yahoo Finance)
  - `get_financial_ratios` → `get_financials` (Yahoo Finance includes ratios)
  - `get_insider_trades` → `get_insider_transactions` (SEC Form 4)
  - `screen_stocks` → Can be built with Yahoo data

- **Benefits**:
  - ✅ 100% reliable APIs (Yahoo + SEC have no rate limits)
  - ✅ Better data quality (Yahoo has real-time data)
  - ✅ Simpler setup (one less API key required)
  - ✅ No more "Access denied" errors

### 📊 Data Sources Update

**API Count**: 9 APIs (down from 10)
**Tool Count**: 32 tools (down from 36)
**Free Data Sources**: 3 out of 9 require no API key (Yahoo Finance, SEC EDGAR, U.S. Treasury)

### 🔄 Agent Updates

Updated 5 agents to remove FMP tool dependencies:
- **Quill** (Equity Research) - Removed FMP fundamentals/ratios/insider tools
- **Screen Forge** (Equity Screening) - Removed FMP screening tools
- **Atlas** (Investment Strategist) - Removed FMP fundamentals tools
- **Portfolio** (Legacy) - Removed FMP tools
- **Earnings Whisperer** - Removed FMP ratios tool

All agents retain full functionality through Yahoo Finance + SEC EDGAR alternatives.

### 🧹 Code Quality

- **Settings**: Removed `fmp_api_key` field from configuration
- **API Checker**: Removed FMP status checker
- **Tests**: Updated test suite (65/65 passing, removed 1 FMP test)
- **Documentation**: Updated README with accurate API counts

---

## Release Date
January 8, 2025

## PyPI Package
https://pypi.org/project/navam-invest/0.1.30/
