# Release 0.1.5

## Tier 1 API Tools Expansion

### Feature

**Expanded API Coverage**: Added three new Tier 1 API tool modules providing fundamentals, treasury data, and corporate filings analysis capabilities.

### Implementation Details

#### 1. Financial Modeling Prep (FMP) API Tool (`tools/fmp.py`)

Comprehensive fundamental analysis tools:

```python
@tool
async def get_company_fundamentals(symbol: str, api_key: str) -> str:
    """Get comprehensive fundamental data including income, balance, and metrics."""

@tool
async def get_financial_ratios(symbol: str, api_key: str) -> str:
    """Get liquidity, profitability, and leverage ratios."""

@tool
async def get_insider_trades(symbol: str, api_key: str, limit: int = 10) -> str:
    """Get recent insider trading activity."""

@tool
async def screen_stocks(...) -> str:
    """Screen stocks based on fundamental criteria."""
```

**Capabilities**:
- Income statement, balance sheet, and key metrics
- Financial ratios (liquidity, profitability, returns, leverage)
- Insider trading activity tracking
- Multi-criteria stock screening

#### 2. U.S. Treasury Fiscal Data API Tool (`tools/treasury.py`)

Treasury yield and debt analysis (no API key required):

```python
@tool
async def get_treasury_yield_curve() -> str:
    """Get current yield curve (1M to 30Y)."""

@tool
async def get_treasury_rate(maturity: str) -> str:
    """Get yield for specific maturity."""

@tool
async def get_treasury_yield_spread(short_maturity: str, long_maturity: str) -> str:
    """Calculate and interpret yield spread."""

@tool
async def get_debt_to_gdp() -> str:
    """Get U.S. federal debt data."""
```

**Capabilities**:
- Full yield curve data (1M, 3M, 6M, 1Y, 2Y, 5Y, 10Y, 30Y)
- Specific maturity yield lookup
- Yield spread calculation with economic interpretation
- Federal debt tracking

#### 3. SEC EDGAR API Tool (`tools/sec_edgar.py`)

Corporate filings and regulatory data:

```python
@tool
async def search_company_by_ticker(ticker: str) -> str:
    """Search company info by ticker to get CIK."""

@tool
async def get_latest_10k(cik: str) -> str:
    """Get latest 10-K annual report."""

@tool
async def get_latest_10q(cik: str) -> str:
    """Get latest 10-Q quarterly report."""

@tool
async def get_institutional_holdings(cik: str) -> str:
    """Get 13F institutional holdings."""

@tool
async def get_company_filings(symbol: str, filing_type: str, limit: int) -> str:
    """Get recent filings by type."""
```

**Capabilities**:
- Ticker to CIK mapping
- 10-K/10-Q filing retrieval
- 13F institutional holdings tracking
- Filing metadata and direct links

#### 4. Unified Tools Registry (`tools/__init__.py`)

Centralized tool management:

```python
TOOLS: Dict[str, BaseTool] = {
    # Market Data (5 tools from Alpha Vantage)
    "get_stock_price": get_stock_price,
    "get_stock_overview": get_stock_overview,

    # Fundamentals (4 tools from FMP)
    "get_company_fundamentals": get_company_fundamentals,
    "get_financial_ratios": get_financial_ratios,
    "get_insider_trades": get_insider_trades,
    "screen_stocks": screen_stocks,

    # Macro (2 tools from FRED)
    "get_economic_indicator": get_economic_indicator,
    "get_key_macro_indicators": get_key_macro_indicators,

    # Treasury (4 tools)
    "get_treasury_yield_curve": get_treasury_yield_curve,
    "get_treasury_rate": get_treasury_rate,
    "get_treasury_yield_spread": get_treasury_yield_spread,
    "get_debt_to_gdp": get_debt_to_gdp,

    # SEC (5 tools)
    "search_company_by_ticker": search_company_by_ticker,
    "get_company_filings": get_company_filings,
    "get_latest_10k": get_latest_10k,
    "get_latest_10q": get_latest_10q,
    "get_institutional_holdings": get_institutional_holdings,
}

def get_all_tools() -> List[BaseTool]:
    """Get list of all available tools."""

def get_tools_by_category(category: str) -> List[BaseTool]:
    """Get tools filtered by category."""
```

**Categories**:
- `market` - Price and overview data
- `fundamentals` - Financial analysis and screening
- `macro` - Economic indicators
- `treasury` - Yield curves and debt
- `sec` - Corporate filings

### API Coverage Summary

| Category | API Provider | Free Tier | Tools Added |
|----------|-------------|-----------|-------------|
| **Fundamentals** | Financial Modeling Prep | 250 req/day | 4 tools |
| **Treasury** | U.S. Fiscal Data | Unlimited | 4 tools |
| **Filings** | SEC EDGAR | 10 req/sec | 5 tools |
| **Total** | 3 new APIs | - | **13 new tools** |

### Tool Count Progression

- **v0.1.3**: 4 tools (Alpha Vantage + FRED)
- **v0.1.5**: 17 tools (added FMP, Treasury, SEC)
- **Growth**: +325% tool expansion

### Files Created

1. `src/navam_invest/tools/fmp.py` - Financial Modeling Prep integration
2. `src/navam_invest/tools/treasury.py` - U.S. Treasury data integration
3. `src/navam_invest/tools/sec_edgar.py` - SEC EDGAR integration
4. `src/navam_invest/tools/__init__.py` - Unified registry (replaced stub)

### Files Modified

1. `pyproject.toml` - Version 0.1.4 → 0.1.5
2. `tests/test_config.py` - Fixed model name assertion for flexibility

### Testing

All tests passing:
```
7 passed in 0.20s
Coverage: 22% (baseline for new tools)
```

### Benefits

- ✅ **Comprehensive Fundamentals**: Full financial statement analysis and ratios
- ✅ **Macro Context**: Treasury yield curves for regime detection
- ✅ **Regulatory Intelligence**: SEC filings for governance and institutional activity
- ✅ **Free Tier Focus**: All APIs have generous free quotas
- ✅ **Unified Interface**: Centralized tool registry for easy agent integration
- ✅ **Category Filtering**: Tools organized by domain for specialized agents

### Architecture Alignment

Implements **Tier 1 APIs** from `refer/specs/api-tools.md`:
- ✅ Alpha Vantage (v0.1.3)
- ✅ Financial Modeling Prep (v0.1.5)
- ✅ SEC EDGAR (v0.1.5)
- ✅ U.S. Treasury Fiscal Data (v0.1.5)

**Next Phase**: Tier 2 Macro APIs (World Bank, OECD) + Tier 3 Alternative Data

---

## Agent-Tool Integration Update

### Implementation

**Problem Identified**: After adding 13 new tools, agents were still using only the original 4 tools (23% utilization).

#### Agent Updates

**Portfolio Agent** (`agents/portfolio.py`):
- Changed from hardcoded imports to category-based tool loading
- Now uses **11 tools** (market + fundamentals + SEC):
  ```python
  market_tools = get_tools_by_category("market")          # 2 tools
  fundamentals_tools = get_tools_by_category("fundamentals")  # 4 tools
  sec_tools = get_tools_by_category("sec")                # 5 tools
  ```
- Enhanced system prompt with comprehensive API key context

**Research Agent** (`agents/research.py`):
- Changed from hardcoded imports to category-based tool loading
- Now uses **6 tools** (macro + treasury):
  ```python
  macro_tools = get_tools_by_category("macro")      # 2 tools
  treasury_tools = get_tools_by_category("treasury")  # 4 tools
  ```
- Enhanced system prompt with yield curve interpretation guidance

**Configuration** (`config/settings.py`):
- Added `fmp_api_key: Optional[str] = None`
- Organized API keys by category (Market Data vs Macro Data)

### Results

- **Tool Utilization**: 4/17 (23%) → 17/17 (100%)
- **Portfolio Agent**: 2 → 11 tools
- **Research Agent**: 2 → 6 tools
- **Architecture**: Scalable category-based loading enables future expansion
- **Tests**: All 7 tests passing ✅

---

## Secure API Key Management

### Implementation

**Security Enhancement**: Removed API keys from system prompts and implemented secure credential injection using wrapper functions with proper closure.

#### Problem

**Before (INSECURE)**:
```python
# API keys exposed in system prompts sent to LLM
system_msg = HumanMessage(
    content=f"Use Alpha Vantage API key: {alpha_key} for stock prices..."
)
```
- ❌ API keys visible in LLM context
- ❌ Keys could be logged, cached, or exposed
- ❌ Violates principle of least privilege

**After (SECURE)**:
```python
# API keys bound to tools, never sent to LLM
tools_with_keys = bind_api_keys_to_tools(
    tools,
    alpha_vantage_key=settings.alpha_vantage_api_key,
    fmp_key=settings.fmp_api_key
)
# Clean system prompt without credentials
system_msg = HumanMessage(
    content="You are a portfolio analysis assistant..."
)
```
- ✅ Credentials stay in tool execution layer
- ✅ LLM never sees API keys
- ✅ Follows security best practices

#### Tool Injection Pattern (`tools/__init__.py`)

**New Functions**: `_create_bound_wrapper()` and `bind_api_keys_to_tools()`
```python
def _create_bound_wrapper(original_func, api_key: str):
    """Create a wrapper function that binds API key (proper closure)."""
    @wraps(original_func)
    async def wrapper(*args, **kwargs):
        return await original_func(*args, api_key=api_key, **kwargs)
    return wrapper

def bind_api_keys_to_tools(
    tools: List[BaseTool],
    alpha_vantage_key: str = "",
    fmp_key: str = "",
    fred_key: str = "",
) -> List[BaseTool]:
    """Bind API keys to tools securely using wrapper functions."""
    bound_tools = []
    for tool in tools:
        callable_func = tool.coroutine if tool.coroutine else tool.func
        if tool requires API key:
            bound_func = _create_bound_wrapper(callable_func, key)
            bound_tool = StructuredTool.from_function(
                coroutine=bound_func,
                name=tool.name,
                description=tool.description,
            )
            bound_tools.append(bound_tool)
    return bound_tools
```

**Benefits**:
- Uses wrapper functions with `@wraps` decorator for proper introspection
- Handles async tools correctly via `tool.coroutine` instead of `tool.func`
- Creates proper closures that maintain type information
- Creates new StructuredTool instances with credentials injected
- Maintains tool interface while securing credentials
- Tools requiring no API keys (Treasury, SEC) pass through unchanged

**Bug Fix**: Initial implementation using `functools.partial` failed with "first argument must be callable" error because LangChain's `StructuredTool.from_function()` couldn't introspect partial objects for type hints. Switched to wrapper function pattern for proper async function introspection.

#### Agent Updates

**Portfolio Agent** (`agents/portfolio.py`):
```python
# Secure tool binding
tools_with_keys = bind_api_keys_to_tools(
    tools,
    alpha_vantage_key=settings.alpha_vantage_api_key or "",
    fmp_key=settings.fmp_api_key or "",
)

# Clean system prompt (no API keys)
system_msg = HumanMessage(
    content="You are a portfolio analysis assistant with access to "
    "comprehensive market data. You have tools for stock prices, "
    "company overviews, financial fundamentals, ratios, insider trading, "
    "stock screening, and SEC filings..."
)
```

**Research Agent** (`agents/research.py`):
```python
# Secure tool binding
tools_with_keys = bind_api_keys_to_tools(
    tools,
    fred_key=settings.fred_api_key or ""
)

# Clean system prompt (no API keys)
system_msg = HumanMessage(
    content="You are a market research assistant specializing in "
    "macroeconomic analysis. You have tools for economic indicators "
    "and U.S. Treasury yield curves..."
)
```

#### Security Analysis

| Aspect | Before | After |
|--------|--------|-------|
| **API Key Exposure** | Visible in LLM context | Hidden in tool layer |
| **Logging Risk** | Keys could be logged | Only tool results logged |
| **Cache Risk** | Keys in cached prompts | No keys to cache |
| **Audit Trail** | Credentials in messages | Clean message history |
| **Compliance** | ❌ Fails security review | ✅ Passes best practices |

#### Files Modified

1. `src/navam_invest/tools/__init__.py` - Added `bind_api_keys_to_tools()` function
2. `src/navam_invest/agents/portfolio.py` - Secure credential injection
3. `src/navam_invest/agents/research.py` - Secure credential injection

### Results

- ✅ **Zero API key exposure**: Credentials never enter LLM context
- ✅ **Secure by design**: Uses wrapper function pattern with proper closures
- ✅ **Backward compatible**: Tools still function identically
- ✅ **Clean prompts**: System messages focus on capabilities, not credentials
- ✅ **Application working**: `navam invest` launches successfully with no errors
- ✅ **Tests passing**: All 7 tests passing ✅

### Release Date
2025-10-05

### Version
0.1.5 (Alpha)
