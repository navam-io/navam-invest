# API Alternatives Research Report

**Date**: 2025-10-06
**Purpose**: Evaluate free-tier API alternatives to replace or supplement Financial Modeling Prep (FMP) for stock screening and fundamental data

---

## Executive Summary

This report evaluates alternative APIs to address FMP's limited free-tier stock screening capabilities. Based on comprehensive research, **we recommend a multi-API strategy** that leverages the strengths of different providers while maintaining free-tier sustainability.

### Key Findings

1. **No single free API** offers comprehensive stock screening with generous rate limits
2. **FMP remains competitive** for fundamentals (250 req/day) despite screener limitations
3. **Best alternatives** for screening: Alpha Vantage (fundamentals), Finnhub (institutional data), Tiingo (historical fundamentals)
4. **Recommended strategy**: Keep FMP as primary, add Finnhub and Tiingo as supplements

---

## Current FMP Implementation

### Tools Using FMP
- `get_company_fundamentals` - Income statement, balance sheet, key metrics
- `get_financial_ratios` - Financial ratios and profitability metrics
- `get_insider_trades` - Insider trading activity
- `screen_stocks` - Stock screening (LIMITED on free tier)

### FMP Free Tier Limitations
- **250 requests/day** - Reasonable for fundamentals
- **Stock screener access**: ❌ **VERY LIMITED** on free tier
- **403 errors**: Common for screener endpoint on free plans
- **Coverage**: Strong for US stocks, limited international

### FMP Strengths
- Comprehensive fundamental data (income, balance, cash flow)
- Good financial ratios coverage
- Insider trading data
- Institutional holdings (13F)
- Reasonable daily quota (250 requests)

---

## Alternative APIs Evaluated

### 1. Alpha Vantage (CURRENT - Keep)

**Status**: ✅ Already integrated
**Free Tier**: 25-500 calls/day (with demo key)

**Strengths**:
- Best overall stock API for 2025
- Real-time and historical price data
- Fundamentals API with P/E ratios, margins, financial statements
- Technical indicators (50+)
- Excellent for screening data sources

**Limitations**:
- No dedicated stock screener endpoint
- Would need custom screening logic

**Recommendation**: ✅ **Keep as primary market data source**

---

### 2. Finnhub (RECOMMENDED - Add)

**Status**: 🆕 Recommended addition
**Free Tier**: 50-60 calls/minute, generous free plan

**Strengths**:
- Institutional-grade data for retail investors
- Strong alternative data (social sentiment, insider transactions)
- Senate lobbying, government spending data
- Real-time market data from global exchanges
- 10 forex brokers, 15+ crypto exchanges
- Year's worth of historical data per API call

**Limitations**:
- Free tier APIs limited (missing some basic endpoints)
- No dedicated stock screener on free tier
- Would need to build custom screening with fundamental data points

**Use Cases**:
- Alternative data enrichment (sentiment, insider activity)
- Supplement FMP fundamentals
- Institutional holdings analysis
- Enhanced insider trading signals

**Recommendation**: ✅ **Add as supplementary source for alternative data**

---

### 3. Tiingo (RECOMMENDED - Add)

**Status**: 🆕 Recommended addition
**Free Tier**: 50 symbols/hour for EOD data

**Strengths**:
- **5 years of fundamental data** on free tier (vs 15+ on paid)
- 30+ years of historical stock data
- Fast JSON fundamental data access
- Daily fundamental data + quarterly statements
- Various financial metrics and ratios
- Python library available

**Limitations**:
- 50 symbols/hour rate limit (modest but workable)
- Free tier for internal/personal use only
- No dedicated stock screener endpoint

**Use Cases**:
- Historical fundamental analysis (5 years free)
- Quarterly statement tracking
- Supplement FMP fundamentals with longer history
- Custom screening with fundamental ratios

**Recommendation**: ✅ **Add for historical fundamentals and quarterly tracking**

---

### 4. Twelve Data (NOT RECOMMENDED)

**Status**: ❌ Not recommended
**Free Tier**: 8 calls/min, 800/day

**Limitations**:
- No dedicated stock screener
- High credit costs for fundamentals (100 credits per fundamental call)
- Would exhaust 800 daily credits with just 8 fundamental queries
- Limited fundamentals on free tier

**Verdict**: ❌ **Unsuitable - too expensive per call for fundamentals**

---

### 5. EODHD (NOT RECOMMENDED - Paid Only)

**Status**: ❌ Not recommended
**Free Tier**: Trial only

**Limitations**:
- **Stock Screener API NOT available on free tier**
- Requires "All-In-One" or "All World Extended" paid plans
- Each screener request = 5 API calls
- Free trial insufficient for production use

**Verdict**: ❌ **Screener requires paid plan**

---

### 6. Polygon.io (NOT RECOMMENDED)

**Status**: ❌ Not recommended
**Free Tier**: 5 requests/minute

**Limitations**:
- Only 5 requests/minute (too restrictive)
- End-of-day data only on free tier
- Limited real-time capabilities
- U.S. stocks only

**Verdict**: ❌ **Too restrictive for our use case**

---

### 7. IEX Cloud (DISCONTINUED)

**Status**: ❌ Service shut down
**Note**: IEX Cloud shut down in August 2024

**Verdict**: ❌ **No longer available**

---

## Recommended Multi-API Strategy

### Phase 1: Immediate (v0.1.11-0.1.12)

**Add Finnhub integration**:
```python
# New module: src/navam_invest/tools/finnhub.py
- get_alternative_sentiment()  # Social media sentiment
- get_insider_sentiment()      # Aggregated insider activity
- get_lobbying_data()          # Senate lobbying data
- get_institutional_ownership() # Institutional positions
```

**Benefits**:
- Enriches existing fundamental analysis with sentiment
- Provides alternative insider trading perspective
- No overlap with existing FMP/Alpha Vantage coverage
- 50-60 calls/minute very generous

---

### Phase 2: Near-term (v0.1.13-0.1.15)

**Add Tiingo integration**:
```python
# New module: src/navam_invest/tools/tiingo.py
- get_fundamental_history()    # 5 years free historical fundamentals
- get_quarterly_statements()   # Quarterly financial data
- get_daily_fundamentals()     # Daily fundamental metrics
```

**Benefits**:
- Historical fundamental analysis (5 years)
- Quarterly tracking for earnings analysis
- Fallback for FMP fundamental queries
- 50 symbols/hour sufficient for retail use

---

### Phase 3: Custom Screening Logic (v0.2.x)

**Build hybrid screener**:
```python
# New module: src/navam_invest/tools/screener.py
- screen_by_fundamentals()     # Use FMP/Alpha Vantage/Tiingo data
- screen_by_quality()          # Custom quality score
- screen_by_momentum()         # Price momentum + volume
- screen_by_value()            # Valuation ratios
```

**Strategy**:
- Fetch universe of symbols (Alpha Vantage, SEC EDGAR)
- Parallel fetch fundamentals (FMP primary, Tiingo fallback)
- Local computation (pandas/numpy) for filtering
- Cache results (DuckDB/SQLite) to respect rate limits

**Benefits**:
- No dependency on dedicated screener APIs
- Full control over screening criteria
- Cost-effective (compute locally vs API calls)
- Respects free-tier rate limits via caching

---

## Implementation Priorities

### Priority 1: Finnhub Integration (v0.1.11-0.1.12)
**Impact**: High - Adds unique alternative data
**Effort**: Low - Similar to existing FMP integration
**Timeline**: 1-2 days

**Tasks**:
- [ ] Create `src/navam_invest/tools/finnhub.py`
- [ ] Implement 4-5 core Finnhub tools (sentiment, insider, lobbying)
- [ ] Add Finnhub API key to configuration
- [ ] Update agents to leverage alternative data
- [ ] Add tests for Finnhub tools

---

### Priority 2: Tiingo Integration (v0.1.13-0.1.15)
**Impact**: Medium - Historical fundamentals + quarterly tracking
**Effort**: Low-Medium - Similar integration pattern
**Timeline**: 2-3 days

**Tasks**:
- [ ] Create `src/navam_invest/tools/tiingo.py`
- [ ] Implement fundamental history and quarterly tools
- [ ] Add Tiingo API key to configuration
- [ ] Add fallback logic (FMP → Tiingo)
- [ ] Add tests for Tiingo tools

---

### Priority 3: Custom Screening Engine (v0.2.x)
**Impact**: High - Enables full screening without paid APIs
**Effort**: High - Requires local computation + caching
**Timeline**: 1-2 weeks

**Tasks**:
- [ ] Design screener architecture (fetch + compute + cache)
- [ ] Implement local screening logic (pandas/numpy)
- [ ] Add DuckDB caching layer
- [ ] Create screening agents (Screen Forge)
- [ ] Build factor screening (quality, momentum, value)
- [ ] Add comprehensive tests

---

## API Comparison Matrix

| API | Free Tier | Screening | Fundamentals | Alternative Data | Recommendation |
|-----|-----------|-----------|--------------|-----------------|----------------|
| **FMP** | 250/day | ❌ Very Limited | ✅ Strong | ⚠️ Some | ✅ Keep (Primary) |
| **Alpha Vantage** | 25-500/day | ❌ None | ✅ Good | ❌ None | ✅ Keep (Prices) |
| **Finnhub** | 50-60/min | ❌ None | ⚠️ Limited | ✅ Excellent | ✅ Add (Alt Data) |
| **Tiingo** | 50 symbols/hr | ❌ None | ✅ Good (5yr) | ❌ None | ✅ Add (History) |
| **Twelve Data** | 800/day | ❌ None | ⚠️ Expensive | ❌ None | ❌ Skip |
| **EODHD** | Trial only | 💰 Paid Only | ✅ Good | ❌ None | ❌ Skip |
| **Polygon.io** | 5/min | ❌ None | ❌ Limited | ❌ None | ❌ Skip |
| **IEX Cloud** | N/A | N/A | N/A | N/A | ❌ Shut down |

---

## Cost-Benefit Analysis

### Option A: Keep FMP Only + Custom Screener
**Pros**: Minimal new integrations, full control over screening
**Cons**: More engineering effort, no alternative data
**Cost**: $0/month API, high dev time

### Option B: FMP + Finnhub + Custom Screener (RECOMMENDED)
**Pros**: Alternative data, enriched analysis, manageable complexity
**Cons**: Two new integrations
**Cost**: $0/month API, medium dev time

### Option C: FMP + Finnhub + Tiingo + Custom Screener (FUTURE)
**Pros**: Maximum data coverage, historical depth, fallback redundancy
**Cons**: Three integrations to manage
**Cost**: $0/month API, high dev time

---

## Conclusion

### Immediate Action (v0.1.11)
1. ✅ **Keep FMP** as primary fundamentals source
2. ✅ **Keep Alpha Vantage** for market data
3. 🆕 **Add Finnhub** for alternative data (sentiment, insider sentiment, lobbying)

### Near-Term (v0.1.12-0.1.15)
4. 🆕 **Add Tiingo** for historical fundamentals and quarterly tracking
5. 🆕 **Build custom screener** using local computation + caching

### Long-Term (v0.2.x+)
6. 🆕 **Enhance screener** with factor models (quality, momentum, value)
7. 🆕 **Add more alternative data** sources as needed

---

## References

- **FMP Documentation**: https://site.financialmodelingprep.com/developer/docs
- **Finnhub Documentation**: https://finnhub.io/docs/api
- **Tiingo Documentation**: https://app.tiingo.com/data/api
- **Alpha Vantage Documentation**: https://www.alphavantage.co/documentation/
- **Project Specs**: `refer/specs/api-tools.md`, `refer/specs/agents-tools.md`

---

## Next Steps

1. Review this report with stakeholders
2. Approve recommended strategy
3. Implement Finnhub integration (Priority 1)
4. Test alternative data enrichment
5. Plan Tiingo integration (Priority 2)
6. Design custom screener architecture (Priority 3)
