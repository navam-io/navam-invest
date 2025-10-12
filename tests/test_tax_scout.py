"""Tests for Tax Scout agent."""

import pytest

from navam_invest.agents.tax_scout import create_tax_scout_agent
from navam_invest.tools import get_tools_for_agent


@pytest.mark.asyncio
async def test_create_tax_scout_agent():
    """Test Tax Scout agent creation."""
    agent = await create_tax_scout_agent()
    assert agent is not None
    assert hasattr(agent, "invoke")


def test_tax_scout_tools():
    """Test that Tax Scout agent has correct tools."""
    tools = get_tools_for_agent("tax_scout")

    # Should have at least 10 tax optimization tools
    assert len(tools) >= 10

    # Key tools for tax-loss harvesting
    tool_names = [tool.name for tool in tools]

    # Portfolio data access
    assert "read_local_file" in tool_names
    assert "list_local_files" in tool_names

    # Market data for loss calculations
    assert "get_quote" in tool_names
    assert "get_stock_price" in tool_names
    assert "get_historical_data" in tool_names

    # Fundamentals for replacement candidates
    assert "get_company_info" in tool_names
    assert "get_financials" in tool_names
    assert "get_stock_overview" in tool_names


def test_tax_scout_agent_capabilities():
    """Test that Tax Scout agent has appropriate tools for each capability."""
    tools = get_tools_for_agent("tax_scout")
    tool_names = [tool.name for tool in tools]

    # Tax-loss harvesting capabilities
    tlh_tools = ["get_quote", "get_historical_data", "get_stock_price"]
    assert all(tool in tool_names for tool in tlh_tools)

    # Wash-sale compliance checking
    wash_sale_tools = ["get_historical_data", "get_historical_fundamentals"]
    assert all(tool in tool_names for tool in wash_sale_tools)

    # Replacement candidate analysis
    replacement_tools = ["get_company_info", "get_financials", "get_stock_overview"]
    assert all(tool in tool_names for tool in replacement_tools)

    # Portfolio access for cost basis and lot-level analysis
    portfolio_tools = ["read_local_file", "list_local_files"]
    assert all(tool in tool_names for tool in portfolio_tools)
