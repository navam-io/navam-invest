
# 1) Advisory-firm roles → AI agent replacements

| Traditional role               | What they do                                       | Navam agent                                                                                                                                                |
| ------------------------------ | -------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chief Investment Officer (CIO) | Sets strategy, risk guardrails, rebalancing policy | **Policy & Strategy Agent** — encodes IPS (investment policy statement), risk model, drift/rebalance rules; proposes strategy menus and “why” explanations |
| Portfolio Manager              | Allocates across assets, implements tilts          | **Allocator Agent** — turns strategy into target weights by account/tax bucket; simulates scenarios; produces trade lists (no execution)                   |
| Equity/ETF Analyst             | Screens, values, compares securities               | **Fundamentals Analyst Agent** — screeners, factor tilts, DCF/relative valuation, moat & quality scoring                                                   |
| Macro/Quant Research           | Reads macro, rates, cycles, factor regimes         | **Macro & Regime Agent** — pulls FRED/OECD/WB data; classifies regime (growth/inflation/liquidity) and suggests tilts                                      |
| Risk/Compliance                | Monitors concentration, VaR, drawdowns, IPS        | **Risk & Compliance Agent** — limits, alerts, concentration & correlation checks; audit trails                                                             |
| Tax & Rebalancing              | Location, loss harvesting, wash-sale checks        | **Tax Optimizer Agent** — tax-aware rebalancing proposals, TLH suggestions (education only)                                                                |
| Client Advisor                 | Knows goals, constraints, ESG prefs                | **Investor Coach Agent** — asks questions, explains trade-offs Socratically; generates IPS; education library                                              |
| Operations                     | Data hygiene, pricing, corp actions                | **Data Steward Agent** — dedupes identifiers, enriches with FIGI/ISIN, handles splits/dividends metadata                                                   |

> Autonomy: **research, recommend, educate only** (your constraint). All agents produce auditable “explain-like-I'm-5 / expert-mode” memos and never place trades.

---

# 2) Agent specs (Claude Agent SDK + MCP)

Each agent uses: system prompt, tools (MCP), resources (docs/IPS), and a memory namespace (per-investor). Below are concise specs you can paste into SDK configs.

### A. Policy & Strategy Agent

* **Goal:** Convert questionnaire + holdings into a recommended strategy (value/growth/dividend/index/active hybrid) with risk bands and IPS text.
* **Inputs:** Risk tolerance answers, time horizon, liquidity needs, tax brackets, current portfolio.
* **Tools:** `macro.read_series`, `portfolio.metrics`, `screen.funds`, `simulate.backtest`.
* **Outputs:** Strategy spec (targets, tracking index, risk bands), IPS draft, education notes.

### B. Allocator Agent

* **Goal:** Turn strategy into implementable target weights by account (taxable vs IRA) and currency exposure.
* **Tools:** `etf.lookup`, `fx.rates`, `portfolio.optimize` (mean-variance or risk parity), `rebalance.plan`.
* **Outputs:** Target weights, drift report, proposed trades (paper only), location plan.

### C. Fundamentals Analyst Agent

* **Goal:** Find candidates; score on quality, growth, value, dividend safety; build comparative tearsheets.
* **Tools:** `equity.screener`, `equity.fundamentals`, `sec.filings`, `news.search`.
* **Outputs:** Screen tables, factor scores, valuation comps, moat commentary with sources.

### D. Macro & Regime Agent

* **Goal:** Classify current regime; suggest tilts (duration, equity factor, commodities/real assets).
* **Tools:** `macro.read_series` (FRED/OECD/WB), `macro.nowcast`, `scenario.shocks`.
* **Outputs:** One-pager: regime call, leading indicators, suggested tilts + caveats.

### E. Risk & Compliance Agent

* **Goal:** Enforce IPS; monitor exposures, VaR/expected shortfall, sector/country caps.
* **Tools:** `portfolio.risk`, `limits.check`, `alerts.create`.
* **Outputs:** Pass/Fail with explanations; “what changed” diffs.

### F. Tax Optimizer Agent

* **Goal:** TLH candidates, asset location, distribution calendar; wash-sale warnings (educational).
* **Tools:** `tax.lots`, `tax.tlh_scan`, `tax.location_score`.
* **Outputs:** TLH opportunities, projected tax impact tables, documentation.

### G. Investor Coach Agent

* **Goal:** Socratic Q&A; build or revise IPS; explain choices; generate “learning cards.”
* **Tools:** `coach.survey`, `ips.compose`, `explain.with_examples`.
* **Outputs:** Completed questionnaire, IPS v1, tailored learning path.

### H. Data Steward Agent

* **Goal:** Normalize tickers/ISIN/CUSIP, fix splits/dividends, dedupe, cache & backfill.
* **Tools:** `id.resolve` (OpenFIGI), `prices.fetch`, `corpactions.sync`.
* **Outputs:** Cleaned security master, freshness report.

---

# 3) Cross-agent workflows

1. **Onboarding → IPS**

* Coach runs survey → Policy & Strategy drafts IPS → Macro adds current-regime context → Risk checks caps → Coach finalizes IPS.

2. **Quarterly Review**

* Data Steward refresh → Macro regime update → Fundamentals refresh watchlist → Allocator recomputes targets → Risk validates → Coach prepares client memo.

3. **Rebalance Trigger**

* Drift > threshold OR cashflow → Allocator proposes plan (tax-aware via Tax Optimizer) → Risk/Compliance check → Coach explains rationale.

4. **Dividend & Income Plan**

* Fundamentals screens for dividend safety → Allocator builds income sleeve → Risk caps sector/issuer → Coach explains yield vs. risk.

5. **ESG / Preference Overlay**

* Coach collects exclusions → Data Steward tags securities → Screeners apply filters → Allocator rebuilds → Risk checks concentration.

---

# 4) Tools & best free-tier APIs (global scope)

Below is a pragmatic starter bundle with current free-tier notes.

### Market data & fundamentals

* **Alpha Vantage** — broad endpoints; free tier typically **~25 calls/day** (and **~5/min**) on most datasets. Good for indicators and daily prices. ([Alpha Vantage][1])
* **Financial Modeling Prep (FMP)** — strong fundamentals + screeners; free plan **~250 requests/day**; also bandwidth limit note. ([FinancialModelingPrep][2])
* **Polygon.io** — high-quality US equities/opts/forex/crypto; free tier **5 req/min** (paid for more). ([Polygon][3])
* **Tiingo** — clean EOD + news; docs show **~1000 req/day, 50/hr** on basic plans; pricing page outlines caps. (Great Python client.) ([Tiingo][4])
* **SEC EDGAR** — official filings; guideline **≤10 req/sec**; dev portal/rate-limit notes. ([SEC][5])
* **OpenFIGI** — identifier mapping (ISIN/CUSIP→FIGI). *(Add for security master; check their key & terms.)*

### Macro & rates

* **FRED** (St. Louis Fed) — free, API key; vast macro catalog; generous usage (terms, not strict per-day quotas public). ([FRED][6])
* **World Bank Open Data** — free, minimal restrictions; no key needed for most data. ([World Bank Open Data][7])
* **OECD Data API** — rate-limited; guidance shows **~20 downloads/hour** recently. ([OECD][8])

### Crypto (for a complete retail menu)

* **CoinGecko** — free/demo plan commonly **~30 calls/min with ~10k calls/mo** (attribution required). ([CoinGecko][9])
* **CoinMarketCap** — free Basic plan with **~10k calls/month** and **~30 calls/min**, limited endpoints. ([coinmarketcap.com][10])

### News (company & market)

* **NewsAPI.org** — free developer tier **100 requests/day**, 24-hour delay; great for headlines and testing. ([News API][11])
* **FMP news** — also provides news endpoints on free tier (within request limits). ([FinancialModelingPrep][12])
* *(Premium/near-real-time alternatives: Perigon, NewsCatcher, Bing News; many have trials but not long-term free.)* ([NewsCatcher][13])

> Notes: Free tiers change; use the Data Steward agent to **cache aggressively** and respect rate limits. Where ambiguity exists (e.g., vendor pages vs blogs), the conservative limit above is shown with official docs when possible.

---

# 5) MCP tool surface (wrapping the APIs)

Design each tool as a **stateless MCP endpoint** with:

* **name** (e.g., `equity.fundamentals.get`)
* **args schema** (ticker, period, limit…)
* **rate-limit policy** (internal token bucket)
* **auth** (key from Vault/Keychain)
* **output** (normalized Pydantic models)

### Example MCP tools (namespaced)

* `equity.prices.get({ticker, interval, start, end, source})` → Alpha Vantage / Polygon
* `equity.fundamentals.get({ticker, statements:["income","balance","cashflow"], period:"annual|quarter", years})` → FMP/Tiingo
* `equity.screener.run({filters, sort, limit})` → FMP screener
* `sec.filings.search({cikOrTicker, formTypes, startDate, endDate})` → SEC EDGAR
* `macro.read_series({provider:"fred|oecd|wb", series_id, start, end, agg})` → FRED/WB/OECD
* `news.search({q, tickers, from, to, limit})` → NewsAPI/FMP
* `fx.rates.latest({base, quotes})` → Alpha Vantage FX
* `crypto.prices.get({ids, vs_currencies})` → CoinGecko / CMC
* `id.resolve({idType:"isin|cusip|ticker", id})` → OpenFIGI
* Portfolio utilities (internal):

  * `portfolio.metrics({positions})` → returns weights, sector/country mix, factor proxies
  * `portfolio.risk({history, method:"VaR|ES|vol"})`
  * `rebalance.plan({current, targets, min_trade, tax_lots?, constraints})`
  * `tax.tlh_scan({lots, benchmark, lookback})`
  * `limits.check({positions, rules})`

**Implementation tip:** put a thin Python package `navam_mcp_tools/` that exposes MCP JSON-RPC handlers; each handler calls a provider client with retries/backoff and normalizes into your domain models.

---

# 6) Strategy/philosophy menu (with selection logic)

Offer **six base strategies** (any can be blended):

1. **Passive Index Core** (default): global market-cap weighted equity + investment-grade bonds + real assets sleeve.
2. **Quality-Growth Tilt**: add a quality & profitability factor overlay; higher tech/healthcare weight.
3. **Value & Dividend**: value tilt with dividend safety screen; focus on cash flow coverage and payout growth.
4. **Balanced Income**: dividend equities + IG credit ladder + TIPS; target stable cash yield.
5. **Active Satellites**: core index + satellite sleeves (thematics/managed futures/MLP/REITs) with small caps on risk budgets.
6. **Opportunistic (rules-based)**: momentum + risk parity sleeves, explicit drawdown controls.

### Quick decision tree (run by the Coach Agent)

* **Horizon < 3y?** favor short duration bonds + cash equivalents, small equity allocation.
* **Need income now?** prioritize Dividend/Income; else Growth or Passive.
* **Volatility comfort (1–5)?** map to equity band & factor tilts (e.g., value/dividend for lower vol comfort).
* **Complexity appetite?** if low, choose Passive; if medium, add a single factor; if high, add Active Satellites.
* **Tax bracket high?** tilt toward ETFs in taxable, active funds in tax-advantaged; include municipal sleeve where appropriate.

*(Coach Agent asks these and stores answers → Policy Agent finalizes an IPS.)*

---

# 7) Example MCP tool contracts (pseudo-schemas)

```json
// equity.fundamentals.get
{
  "name": "equity.fundamentals.get",
  "args": {
    "ticker": "AAPL",
    "period": "annual",
    "years": 5,
    "source": "fmp"
  },
  "returns": {
    "ticker": "AAPL",
    "financials": {
      "income": [...],
      "balance": [...],
      "cashflow": [...]
    },
    "metadata": {"asOf":"2025-09-30","source":"FMP"}
  }
}
```

```json
// macro.read_series (FRED)
{
  "name": "macro.read_series",
  "args": {"provider":"fred","series_id":"T10Y2Y","start":"2010-01-01"},
  "returns": {"series_id":"T10Y2Y","observations":[["2010-01-04",-2.61],...]}
}
```

```json
// news.search (NewsAPI.org; delayed headlines)
{
  "name": "news.search",
  "args": {"q":"(Tesla OR TSLA) AND earnings","from":"2025-09-01","to":"2025-10-04","limit":50},
  "returns": {"articles":[{"title":"...","url":"...","publishedAt":"...","source":"..."}]}
}
```

---

# 8) Data model & caching (free-tier friendly)

* **Normalization:** FIGI as primary key; map ISIN/CUSIP/Ticker per venue.
* **Cache layers:** `prices:{ticker,interval,date}`; `fundamentals:{ticker,period,year}`; `macro:{series_id,date}` with 24h TTL where appropriate; news cached by URL hash.
* **Backfill jobs:** nightly cron rotates providers (e.g., Polygon intraday for US, AV daily for global) respecting each rate cap (see limits above).
* **Attribution & terms:** attach source and endpoint to every field; comply with display/redistribution clauses (e.g., FMP display licensing). ([FinancialModelingPrep][14])

---

# 9) Guardrails & explainability

* Every recommendation includes: **inputs used → method → data freshness → limitations**.
* Risk checks are **blocking**: e.g., single-name >10% in any account, sector >35%, country >50% (customizable).
* Education: each output has an *ELI5* and an *Analyst* section.

---

# 10) What you can build next (quick wins)

1. **CLI** (`navam invest …`) commands that call MCP tools:

   * `navam coach survey --new`
   * `navam screen quality --min-roic 10 --moat`
   * `navam macro regime`
   * `navam allocate --strategy quality_growth`
   * `navam review --quarterly`
2. **Notebook templates** for tearsheets and IPS PDFs.
3. **Backtests** via `simulate.backtest` using cached daily prices (AV/FMP) and macro filters (FRED/OECD).

---

## Citations for API limits & scope (key items)

* Alpha Vantage free usage (commonly ~25/day, ~5/min). ([Alpha Vantage][1])
* FMP free plan (≈250 requests/day; bandwidth note). ([FinancialModelingPrep][2])
* Polygon free tier (5 requests/min). ([Polygon][3])
* Tiingo caps on basic plans (docs pages). ([Tiingo][4])
* SEC EDGAR fair-use guideline (≤10 r/s) & dev portal. ([SEC][5])
* FRED API docs & key info. ([FRED][6])
* World Bank open data (free/minimal restrictions). ([World Bank Open Data][7])
* OECD API recent throttling guidance. ([OECD][8])
* CoinGecko free/demo rate & monthly cap references. ([CoinGecko][9])
* CoinMarketCap free plan (~10k calls/mo; ~30/min). ([coinmarketcap.com][10])
* NewsAPI.org developer tier (100/day, 24h delay). ([News API][11])
* FMP developer docs (news & fundamentals endpoints). ([FinancialModelingPrep][12])

---

If you want, I can scaffold a **`navam_mcp_tools`** Python package (Typer CLI + MCP handlers + provider clients + Pydantic models) and a **Claude Agent SDK** config set for the eight agents above—ready to run with environment-based keys and local caching.

[1]: https://www.alphavantage.co/support/?utm_source=chatgpt.com "Customer Support"
[2]: https://site.financialmodelingprep.com/faqs?utm_source=chatgpt.com "FAQs - Financial Modeling Prep API | FMP"
[3]: https://polygon.io/knowledge-base/article/what-is-the-request-limit-for-polygons-restful-apis?utm_source=chatgpt.com "What is the request limit for Polygon's RESTful APIs?"
[4]: https://www.tiingo.com/pricing?utm_source=chatgpt.com "Pricing"
[5]: https://www.sec.gov/about/developer-resources?utm_source=chatgpt.com "Developer Resources"
[6]: https://fred.stlouisfed.org/docs/api/fred/?utm_source=chatgpt.com "St. Louis Fed Web Services: FRED® API"
[7]: https://data.worldbank.org/about/get-started?utm_source=chatgpt.com "Get started"
[8]: https://www.oecd.org/en/data/insights/data-explainers/2024/11/Api-best-practices-and-recommendations.html?utm_source=chatgpt.com "API best practices"
[9]: https://www.coingecko.com/en/api/pricing?utm_source=chatgpt.com "Crypto API Pricing Plans"
[10]: https://pro.coinmarketcap.com/api/pricing?utm_source=chatgpt.com "CoinMarketCap API Pricing Plans"
[11]: https://newsapi.org/pricing?utm_source=chatgpt.com "Pricing"
[12]: https://site.financialmodelingprep.com/developer/docs?utm_source=chatgpt.com "Free Stock Market API and Financial Statements API... | FMP"
[13]: https://www.newscatcherapi.com/docs/v3/documentation/get-started/news-api-v3-subscription-plans?utm_source=chatgpt.com "News API v3 subscription plans"
[14]: https://site.financialmodelingprep.com/pricing-plans?utm_source=chatgpt.com "Pricing Plans - Financial Modeling Prep API | FMP"
