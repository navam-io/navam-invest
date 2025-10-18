Perfect — that’s actually a very smart simplification for an early-stage AI advisory system like **Navam Invest**.
If you’re packaging your **LangGraph-based agent system** as a **single Python package** (`navam_invest`), then MCP servers and discovery layers add unnecessary complexity.
Instead, think in terms of **“builtin tools”** — async Python modules exposing a unified interface your LangGraph nodes (agents) can call directly.

Below is your **curated, free-tier-only API stack**, ranked by *value, coverage, and long-term sustainability*, along with exactly what you can build on top of them.

---

## 🧱 Tier 1 — Core Market & Fundamentals (absolute must-haves)

| Domain                            | API                               | Free-Tier Capabilities                                                                                       | Rate Limits / Notes                            | Recommended Usage                                                    |
| --------------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------- | -------------------------------------------------------------------- |
| **Equities & ETFs**               | **Alpha Vantage**                 | OHLCV prices (daily/intraday), 50+ technical indicators, fundamentals (income/balance/cashflow), FX & crypto | 25 calls/day (default) or ~500/day (demo key)  | Primary data source for equities, FX, and simple technical analysis. |
| **Fundamentals & Screeners**      | **Financial Modeling Prep (FMP)** | Fundamentals, ratios, insider trades, 13F holdings, ESG scores                                               | ~250 requests/day free                         | Rich fundamentals + screeners for quality/value/dividend filters.    |
| **Identifiers / Security Master** | **OpenFIGI (Bloomberg)**          | Universal ID mapping (ISIN ↔ CUSIP ↔ Ticker)                                                                 | Unlimited / Free Forever                       | Normalization layer for multi-source data merging.                   |
| **Corporate Filings**             | **SEC EDGAR**                     | 10-K/Q, 8-K, 13-F, XBRL data since 1993                                                                      | 10 req/sec limit                               | For fundamental analysis and governance screens.                     |

🧩 **Why these:** Cover 90 % of daily research needs (prices + fundamentals + filings + IDs) with sustainable free quotas.

Implement thin async wrappers in `navam_invest.tools.equity` using `httpx.AsyncClient` + `tenacity` for backoff.

---

## 🌍 Tier 2 — Macro & Rates Data (official free sources)

| Domain                   | API                      | Data Coverage                                        | Notes                   |
| ------------------------ | ------------------------ | ---------------------------------------------------- | ----------------------- |
| **U.S. Macro**           | **FRED (St. Louis Fed)** | 800 k time series (GDP, CPI, PCE, employment, rates) | 100 % free with key     |
| **U.S. Treasury Yields** | **U.S. Fiscal Data API** | Daily yield curve 1 M – 30 Y, debt metrics           | No API key needed       |
| **International Macro**  | **World Bank Open Data** | 16 k indicators across 200 + countries               | Free no auth            |
| **Developed Markets**    | **OECD API**             | Rates, CPI, productivity indices                     | Free 20 req/hour limit  |

🧩 **Why:** These are *official and permanent* data feeds — ideal for regime detection, macro dashboards, and economic education agents.

---

## 🪙 Tier 3 — Alternative & Sentiment Data (augment insight)

| Domain                | API             | Free-Tier Highlights                              | Use                                                |
| --------------------- | --------------- | ------------------------------------------------- | -------------------------------------------------- |
| **Crypto Markets**    | **CoinGecko**   | 10 k calls/mo • 30 calls/min • 19 k tokens + NFTs | Diversification sleeve / trend analysis            |
| **Market News**       | **NewsAPI.org** | 100 calls/day • 24 h delay                        | Headlines & sentiment for learning/explain outputs |
| **Alternative Macro** | **BEA API**     | GDP accounts, personal income, regional data      | Free • Great for U.S. macro granularity            |

🧩 **Why:** Adds news context and digital asset data for well-rounded coverage.

---

## 🧩 Tier 4 — Computation & Analytics (Local / Open-Source)

| Function                | Library                           | Reason                                          |
| ----------------------- | --------------------------------- | ----------------------------------------------- |
| Portfolio Optimization  | **PyPortfolioOpt**                | MPT, Black-Litterman, risk parity locally       |
| Factor / Risk Analytics | **numpy + pandas + scikit-learn** | Compute vol, VaR, beta without API cost         |
| Explainability          | **SHAP / LIME**                   | Local XAI for recommendations                   |
| Data Store              | **DuckDB / SQLite**               | Local cache for free-tier rate-limit protection |

🧩 These replace commercial engines while keeping LangGraph nodes self-contained and offline-friendly.

---

## 🧮 Unified Tool Interface Structure

Inside `navam_invest/tools/`:

```python
# tools/market.py
async def get_price(ticker: str, source: str = "alpha_vantage"): ...
async def get_fundamentals(ticker: str, source: str = "fmp"): ...
async def get_macro(series_id: str, provider: str = "fred"): ...
async def get_yield_curve(): ...
async def get_news(query: str, limit: int = 20): ...
```

Use a simple registry dict:

```python
TOOLS = {
  "prices": get_price,
  "fundamentals": get_fundamentals,
  "macro": get_macro,
  ...
}
```

and inject these into LangGraph node context:

```python
from navam_invest.tools import TOOLS
graph.bind_tools(TOOLS)
```

✅ No MCP server needed — agents call local Python functions directly.

---

## 🗺️ Prioritization Roadmap (Free-Only Focus)

| Stage             | Core Goal                      | APIs Used                          | Deliverables                                       |
| ----------------- | ------------------------------ | ---------------------------------- | -------------------------------------------------- |
| **Phase 1 (MLP)** | Portfolio overview + chat UI   | Alpha Vantage, FRED, FMP, OpenFIGI | Onboarding agent, price fetch, basic strategy recs |
| **Phase 2**       | Macro & Regime Analysis        | FRED, Treasury, World Bank         | Macro agent classifies regime + suggests tilts     |
| **Phase 3**       | Research & Education Expansion | SEC EDGAR, NewsAPI, CoinGecko      | Analyst agent + coach agent with explanations      |
| **Phase 4**       | Optimization & XAI Reports     | Local libs (PyPortfolioOpt, SHAP)  | Allocator agent + risk / explain modules           |
| **Phase 5**       | Data Quality & Caching         | DuckDB local cache + OpenFIGI      | Data steward agent handles refresh / dedupe        |

---

## ✅ Summary: Free-Tier API Bundle for Navam Invest

| Category            | Primary API          | Backup                    |
| ------------------- | -------------------- | ------------------------- |
| Prices & Indicators | Alpha Vantage        | Twelve Data (fallback)    |
| Fundamentals        | FMP                  | Tiingo (when free)        |
| Macro Data          | FRED                 | World Bank / OECD         |
| Yields & Rates      | Treasury Fiscal Data | FRED alt series           |
| Identifiers         | OpenFIGI             | None needed               |
| News                | NewsAPI.org          | FMP news endpoint         |
| Filings             | SEC EDGAR            | sec-api.io (limited free) |
| Crypto              | CoinGecko            | CoinMarketCap basic plan  |

---

Would you like me to now **generate the Python scaffold** for these tools — i.e., `navam_invest/tools` package with async wrappers for all the above APIs (all free-tier endpoints, error handling, caching, and LangGraph integration)?
