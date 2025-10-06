# Release 0.1.10

## Status
Published

## Features

### New Capabilities
- **NewsAPI.org Integration**: Added market news and sentiment analysis tools
  - New tools: `search_market_news`, `get_top_financial_headlines`, `get_company_news`
  - Integrated with Portfolio and Research agents
  - Free tier: 100 requests/day with 24-hour article delay
  - Features:
    - Search market news by keywords (stocks, companies, financial topics)
    - Get top business/financial headlines by country and category
    - Track company-specific news and announcements
    - Support for multiple countries (US, UK, CA, AU, DE, FR)
    - Configurable result limits (up to 20 articles per request)
  - Comprehensive test coverage (9 tests, 38% coverage for newsapi.py)

### Configuration Updates
- Added `NEWSAPI_API_KEY` to settings for optional NewsAPI.org integration
- Updated `.env.example` with NewsAPI configuration

### Agent Enhancements
- **Research Agent**: Now includes news tools for market sentiment analysis
- **Portfolio Agent**: Can analyze company news and market sentiment alongside fundamentals

### Use Cases Enabled
- Track breaking market news and financial headlines
- Monitor company-specific news for portfolio holdings
- Analyze market sentiment from news sources
- Research financial topics with recent news context
- Get news-driven insights for investment decisions

## Release Date
2025-10-06

## PyPI Package
https://pypi.org/project/navam-invest/0.1.10/
