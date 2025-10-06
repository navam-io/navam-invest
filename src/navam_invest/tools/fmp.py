"""Financial Modeling Prep (FMP) API tools for fundamentals and analytics."""

from typing import Any, Dict, List, Optional

import httpx
from langchain_core.tools import tool


async def _fetch_fmp(
    endpoint: str, api_key: str, **params: Any
) -> Dict[str, Any] | List[Dict[str, Any]]:
    """Fetch data from Financial Modeling Prep API."""
    async with httpx.AsyncClient() as client:
        url = f"https://financialmodelingprep.com/api/v3/{endpoint}"
        params_with_key = {"apikey": api_key, **params}
        response = await client.get(url, params=params_with_key, timeout=30.0)
        response.raise_for_status()
        return response.json()


@tool
async def get_company_fundamentals(symbol: str, api_key: str) -> str:
    """Get comprehensive fundamental data for a company.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        api_key: Financial Modeling Prep API key

    Returns:
        Formatted string with key fundamental metrics
    """
    try:
        # Get income statement (annual)
        income_data = await _fetch_fmp(
            f"income-statement/{symbol}", api_key, period="annual", limit=1
        )

        # Get balance sheet (annual)
        balance_data = await _fetch_fmp(
            f"balance-sheet-statement/{symbol}", api_key, period="annual", limit=1
        )

        # Get key metrics
        metrics_data = await _fetch_fmp(f"key-metrics/{symbol}", api_key, limit=1)

        if not income_data or not balance_data or not metrics_data:
            return f"No fundamental data found for {symbol}"

        income = income_data[0] if isinstance(income_data, list) else income_data
        balance = balance_data[0] if isinstance(balance_data, list) else balance_data
        metrics = metrics_data[0] if isinstance(metrics_data, list) else metrics_data

        # Extract key metrics
        revenue = income.get("revenue", "N/A")
        net_income = income.get("netIncome", "N/A")
        eps = income.get("eps", "N/A")
        total_assets = balance.get("totalAssets", "N/A")
        total_debt = balance.get("totalDebt", "N/A")
        pe_ratio = metrics.get("peRatio", "N/A")
        roe = metrics.get("roe", "N/A")
        debt_to_equity = metrics.get("debtToEquity", "N/A")

        return (
            f"**{symbol} - Fundamental Analysis**\n\n"
            f"**Income Statement:**\n"
            f"Revenue: ${revenue:,.0f}\n"
            f"Net Income: ${net_income:,.0f}\n"
            f"EPS: ${eps}\n\n"
            f"**Balance Sheet:**\n"
            f"Total Assets: ${total_assets:,.0f}\n"
            f"Total Debt: ${total_debt:,.0f}\n\n"
            f"**Key Metrics:**\n"
            f"P/E Ratio: {pe_ratio}\n"
            f"ROE: {roe}\n"
            f"Debt/Equity: {debt_to_equity}"
        )
    except Exception as e:
        return f"Error fetching fundamentals for {symbol}: {str(e)}"


@tool
async def get_financial_ratios(symbol: str, api_key: str) -> str:
    """Get financial ratios and metrics for analysis.

    Args:
        symbol: Stock ticker symbol
        api_key: Financial Modeling Prep API key

    Returns:
        Formatted string with financial ratios
    """
    try:
        data = await _fetch_fmp(f"ratios/{symbol}", api_key, limit=1)

        if not data:
            return f"No ratio data found for {symbol}"

        ratios = data[0] if isinstance(data, list) else data

        # Extract key ratios
        current_ratio = ratios.get("currentRatio", "N/A")
        quick_ratio = ratios.get("quickRatio", "N/A")
        gross_margin = ratios.get("grossProfitMargin", "N/A")
        operating_margin = ratios.get("operatingProfitMargin", "N/A")
        net_margin = ratios.get("netProfitMargin", "N/A")
        roe = ratios.get("returnOnEquity", "N/A")
        roa = ratios.get("returnOnAssets", "N/A")
        debt_ratio = ratios.get("debtRatio", "N/A")

        return (
            f"**{symbol} - Financial Ratios**\n\n"
            f"**Liquidity:**\n"
            f"Current Ratio: {current_ratio}\n"
            f"Quick Ratio: {quick_ratio}\n\n"
            f"**Profitability:**\n"
            f"Gross Margin: {gross_margin}\n"
            f"Operating Margin: {operating_margin}\n"
            f"Net Margin: {net_margin}\n\n"
            f"**Returns:**\n"
            f"ROE: {roe}\n"
            f"ROA: {roa}\n\n"
            f"**Leverage:**\n"
            f"Debt Ratio: {debt_ratio}"
        )
    except Exception as e:
        return f"Error fetching ratios for {symbol}: {str(e)}"


@tool
async def get_insider_trades(symbol: str, api_key: str, limit: int = 10) -> str:
    """Get recent insider trading activity.

    Args:
        symbol: Stock ticker symbol
        api_key: Financial Modeling Prep API key
        limit: Number of recent trades to return (default: 10)

    Returns:
        Formatted string with insider trading data
    """
    try:
        data = await _fetch_fmp(
            f"insider-trading", api_key, symbol=symbol, limit=limit
        )

        if not data:
            return f"No insider trading data found for {symbol}"

        trades = data if isinstance(data, list) else [data]

        result = [f"**{symbol} - Recent Insider Trades**\n"]

        for trade in trades[:limit]:
            filing_date = trade.get("filingDate", "N/A")
            transaction_date = trade.get("transactionDate", "N/A")
            reporter = trade.get("reportingName", "Unknown")
            transaction_type = trade.get("transactionType", "N/A")
            shares = trade.get("securitiesTransacted", "N/A")
            price = trade.get("price", "N/A")

            result.append(
                f"\n**{filing_date}** - {reporter}\n"
                f"Type: {transaction_type}\n"
                f"Shares: {shares:,} @ ${price}\n"
                f"Transaction Date: {transaction_date}"
            )

        return "\n".join(result)
    except Exception as e:
        return f"Error fetching insider trades for {symbol}: {str(e)}"


@tool
async def screen_stocks(
    api_key: str,
    market_cap_more_than: Optional[int] = None,
    beta_more_than: Optional[float] = None,
    volume_more_than: Optional[int] = None,
    dividend_more_than: Optional[float] = None,
    limit: int = 20,
) -> str:
    """Screen stocks based on fundamental criteria.

    Args:
        api_key: Financial Modeling Prep API key
        market_cap_more_than: Minimum market cap
        beta_more_than: Minimum beta
        volume_more_than: Minimum trading volume
        dividend_more_than: Minimum dividend yield
        limit: Maximum results to return (default: 20)

    Returns:
        List of stocks matching criteria
    """
    try:
        params: Dict[str, Any] = {"limit": limit}

        if market_cap_more_than is not None:
            params["marketCapMoreThan"] = market_cap_more_than
        if beta_more_than is not None:
            params["betaMoreThan"] = beta_more_than
        if volume_more_than is not None:
            params["volumeMoreThan"] = volume_more_than
        if dividend_more_than is not None:
            params["dividendMoreThan"] = dividend_more_than

        data = await _fetch_fmp("stock-screener", api_key, **params)

        if not data:
            return "No stocks found matching criteria"

        stocks = data if isinstance(data, list) else [data]

        result = ["**Stock Screener Results**\n"]

        for stock in stocks[:limit]:
            symbol = stock.get("symbol", "N/A")
            name = stock.get("companyName", "Unknown")
            price = stock.get("price", "N/A")
            market_cap = stock.get("marketCap", "N/A")
            volume = stock.get("volume", "N/A")

            result.append(
                f"\n**{symbol}** - {name}\n"
                f"Price: ${price} | Market Cap: ${market_cap:,} | Volume: {volume:,}"
            )

        return "\n".join(result)
    except Exception as e:
        return f"Error running stock screener: {str(e)}"
