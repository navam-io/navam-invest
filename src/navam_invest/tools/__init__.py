"""Unified tools registry for navam-invest agents."""

from typing import Dict, List

from langchain_core.tools import BaseTool

# Alpha Vantage tools
from navam_invest.tools.alpha_vantage import get_stock_overview, get_stock_price

# FRED tools
from navam_invest.tools.fred import get_economic_indicator, get_key_macro_indicators

# Financial Modeling Prep tools
from navam_invest.tools.fmp import (
    get_company_fundamentals,
    get_financial_ratios,
    get_insider_trades,
    screen_stocks,
)

# SEC EDGAR tools
from navam_invest.tools.sec_edgar import (
    get_company_filings,
    get_institutional_holdings,
    get_latest_10k,
    get_latest_10q,
    search_company_by_ticker,
)

# Treasury tools
from navam_invest.tools.treasury import (
    get_debt_to_gdp,
    get_treasury_rate,
    get_treasury_yield_curve,
    get_treasury_yield_spread,
)

# Unified tools registry
TOOLS: Dict[str, BaseTool] = {
    # Market Data (Alpha Vantage)
    "get_stock_price": get_stock_price,
    "get_stock_overview": get_stock_overview,
    # Fundamentals (FMP)
    "get_company_fundamentals": get_company_fundamentals,
    "get_financial_ratios": get_financial_ratios,
    "get_insider_trades": get_insider_trades,
    "screen_stocks": screen_stocks,
    # Macro Data (FRED)
    "get_economic_indicator": get_economic_indicator,
    "get_key_macro_indicators": get_key_macro_indicators,
    # Treasury Data
    "get_treasury_yield_curve": get_treasury_yield_curve,
    "get_treasury_rate": get_treasury_rate,
    "get_treasury_yield_spread": get_treasury_yield_spread,
    "get_debt_to_gdp": get_debt_to_gdp,
    # SEC Filings
    "search_company_by_ticker": search_company_by_ticker,
    "get_company_filings": get_company_filings,
    "get_latest_10k": get_latest_10k,
    "get_latest_10q": get_latest_10q,
    "get_institutional_holdings": get_institutional_holdings,
}


def get_all_tools() -> List[BaseTool]:
    """Get list of all available tools."""
    return list(TOOLS.values())


def get_tools_by_category(category: str) -> List[BaseTool]:
    """Get tools filtered by category.

    Args:
        category: One of 'market', 'fundamentals', 'macro', 'treasury', 'sec'

    Returns:
        List of tools in the specified category
    """
    category_map = {
        "market": ["get_stock_price", "get_stock_overview"],
        "fundamentals": [
            "get_company_fundamentals",
            "get_financial_ratios",
            "get_insider_trades",
            "screen_stocks",
        ],
        "macro": ["get_economic_indicator", "get_key_macro_indicators"],
        "treasury": [
            "get_treasury_yield_curve",
            "get_treasury_rate",
            "get_treasury_yield_spread",
            "get_debt_to_gdp",
        ],
        "sec": [
            "search_company_by_ticker",
            "get_company_filings",
            "get_latest_10k",
            "get_latest_10q",
            "get_institutional_holdings",
        ],
    }

    if category not in category_map:
        return []

    return [TOOLS[name] for name in category_map[category] if name in TOOLS]


__all__ = [
    "TOOLS",
    "get_all_tools",
    "get_tools_by_category",
    # Alpha Vantage
    "get_stock_price",
    "get_stock_overview",
    # FMP
    "get_company_fundamentals",
    "get_financial_ratios",
    "get_insider_trades",
    "screen_stocks",
    # FRED
    "get_economic_indicator",
    "get_key_macro_indicators",
    # Treasury
    "get_treasury_yield_curve",
    "get_treasury_rate",
    "get_treasury_yield_spread",
    "get_debt_to_gdp",
    # SEC
    "search_company_by_ticker",
    "get_company_filings",
    "get_latest_10k",
    "get_latest_10q",
    "get_institutional_holdings",
]
