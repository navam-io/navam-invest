# LangGraph Tools Guide

## Overview

Tools are specialized functions that enable AI models to interact with external systems using structured inputs. They allow models to make precise, actionable requests to APIs, databases, and other systems.

## Tool Calling Mechanism

### How It Works

1. **Model generates tool call request** (doesn't execute directly)
2. **Tool call includes**:
   - Tool name
   - Input arguments
   - Specific input schema
3. **ToolNode or executor runs the tool**
4. **Results returned to model**

### Example Flow

```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
agent = create_react_agent(llm, tools=[multiply])

result = agent.invoke({
    "messages": [{"role": "user", "content": "What is 2 multiplied by 3?"}]
})
# Model calls multiply(2, 3), gets result 6, responds "6"
```

## Creating Custom Tools

### Using @tool Decorator

```python
from langchain_core.tools import tool

@tool
def search_portfolio(symbol: str) -> dict:
    """Search for a stock symbol in the user's portfolio.

    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')

    Returns:
        Portfolio position details including shares and cost basis
    """
    # Tool implementation
    position = database.get_position(symbol)
    return {
        "symbol": symbol,
        "shares": position.shares,
        "cost_basis": position.cost_basis
    }
```

### Using Function Directly

```python
def calculate_roi(initial: float, current: float) -> float:
    """Calculate return on investment percentage.

    Args:
        initial: Initial investment amount
        current: Current value

    Returns:
        ROI as percentage
    """
    return ((current - initial) / initial) * 100

# Pass function directly to agent
agent = create_react_agent(llm, tools=[calculate_roi])
```

### Using BaseTool Class

```python
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

class AnalysisInput(BaseModel):
    symbol: str = Field(description="Stock ticker symbol")
    period: str = Field(description="Analysis period: '1d', '1w', '1m', '1y'")

class StockAnalysisTool(BaseTool):
    name: str = "analyze_stock"
    description: str = "Perform technical analysis on a stock"
    args_schema: type[BaseModel] = AnalysisInput

    def _run(self, symbol: str, period: str) -> dict:
        # Perform analysis
        return analysis_results

    async def _arun(self, symbol: str, period: str) -> dict:
        # Async implementation
        return await async_analysis_results

tool = StockAnalysisTool()
```

## Prebuilt Tool Categories

LangChain provides integrations across various categories:

### Search Tools
```python
from langchain_community.tools import BingSearchRun

search = BingSearchRun(api_key=os.getenv("BING_API_KEY"))
```

### Database Tools
```python
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

db_tool = QuerySQLDataBaseTool(db=sql_database)
```

### API Tools
```python
from langchain_community.tools import OpenWeatherMapQueryRun

weather_tool = OpenWeatherMapQueryRun(api_key=os.getenv("OPENWEATHER_API_KEY"))
```

### Code Execution
```python
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
```

## Using Tools in Agents

### Prebuilt ReAct Agent

```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(
    model=llm,
    tools=[search_portfolio, calculate_roi, analyze_stock]
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Analyze my AAPL position"}]
})
```

### Custom Tool Execution with ToolNode

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from typing import TypedDict, Annotated
from langchain_core.messages import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

def call_model(state: State):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state: State):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# Create tool node
tool_node = ToolNode(tools=[search_portfolio, calculate_roi])

# Build graph
builder = StateGraph(State)
builder.add_node("agent", call_model)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_conditional_edge("agent", should_continue)
builder.add_edge("tools", "agent")

graph = builder.compile()
```

## Tool Error Handling

### Handle Errors in Tools

```python
@tool
def fetch_stock_price(symbol: str) -> dict:
    """Fetch current stock price.

    Args:
        symbol: Stock ticker symbol

    Returns:
        Price data or error message
    """
    try:
        price = api.get_price(symbol)
        return {"symbol": symbol, "price": price, "success": True}
    except APIError as e:
        return {"symbol": symbol, "error": str(e), "success": False}
    except Exception as e:
        return {"symbol": symbol, "error": "Unexpected error", "success": False}
```

### Fallback Handling

```python
@tool
def search_with_fallback(query: str) -> str:
    """Search with fallback to alternative sources."""
    try:
        return primary_search(query)
    except Exception:
        try:
            return secondary_search(query)
        except Exception:
            return "Search unavailable, please try again later"
```

## Tool Best Practices

### 1. Clear Descriptions
```python
@tool
def analyze_portfolio_risk(
    symbols: list[str],
    risk_free_rate: float = 0.02
) -> dict:
    """Analyze portfolio risk metrics including volatility and Sharpe ratio.

    This tool calculates comprehensive risk metrics for a portfolio of stocks.
    It requires historical price data and computes various risk-adjusted returns.

    Args:
        symbols: List of stock ticker symbols in the portfolio (e.g., ['AAPL', 'GOOGL'])
        risk_free_rate: Annual risk-free rate for Sharpe calculation (default: 0.02 = 2%)

    Returns:
        Dictionary containing:
        - portfolio_volatility: Annualized portfolio standard deviation
        - sharpe_ratio: Risk-adjusted return metric
        - max_drawdown: Maximum peak-to-trough decline
    """
    # Implementation
```

### 2. Type Hints
```python
from typing import Literal

@tool
def get_market_data(
    symbol: str,
    data_type: Literal["price", "volume", "fundamentals"]
) -> dict:
    """Fetch market data with specific type constraints."""
    # Implementation
```

### 3. Input Validation
```python
@tool
def set_stop_loss(symbol: str, price: float) -> dict:
    """Set stop loss order.

    Args:
        symbol: Stock ticker
        price: Stop loss price (must be positive)
    """
    if price <= 0:
        return {"error": "Price must be positive"}

    if not validate_symbol(symbol):
        return {"error": "Invalid symbol"}

    return place_order(symbol, price)
```

### 4. Structured Outputs
```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    symbol: str
    recommendation: Literal["buy", "hold", "sell"]
    confidence: float
    reasoning: str

@tool
def analyze_stock(symbol: str) -> AnalysisResult:
    """Analyze stock and return structured recommendation."""
    # Analysis logic
    return AnalysisResult(
        symbol=symbol,
        recommendation="buy",
        confidence=0.85,
        reasoning="Strong fundamentals and technical breakout"
    )
```

## Advanced Patterns

### Tool with Context

```python
from langgraph.prebuilt import InjectedState

@tool
def analyze_with_context(
    symbol: str,
    state: Annotated[dict, InjectedState]
) -> dict:
    """Analyze stock using conversation context.

    Args:
        symbol: Stock ticker
        state: Injected conversation state (automatic)
    """
    user_risk_tolerance = state.get("risk_tolerance", "moderate")
    # Use context in analysis
    return perform_analysis(symbol, user_risk_tolerance)
```

### Conditional Tool Availability

```python
def get_tools_for_user(user_id: str) -> list:
    """Return tools based on user permissions."""
    base_tools = [search_portfolio, calculate_roi]

    if user_has_premium(user_id):
        base_tools.extend([advanced_analysis, realtime_data])

    if user_has_trading_enabled(user_id):
        base_tools.extend([place_order, cancel_order])

    return base_tools

# Create agent with user-specific tools
tools = get_tools_for_user(current_user_id)
agent = create_react_agent(llm, tools=tools)
```

## Complete Example

```python
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_anthropic import ChatAnthropic

# Define tools
@tool
def get_portfolio_value(user_id: str) -> dict:
    """Get total portfolio value for user."""
    positions = db.get_positions(user_id)
    total = sum(p.shares * get_price(p.symbol) for p in positions)
    return {"user_id": user_id, "total_value": total}

@tool
def get_position(user_id: str, symbol: str) -> dict:
    """Get specific position details."""
    position = db.get_position(user_id, symbol)
    current_price = get_price(symbol)
    return {
        "symbol": symbol,
        "shares": position.shares,
        "cost_basis": position.cost_basis,
        "current_value": position.shares * current_price,
        "profit_loss": (position.shares * current_price) - position.cost_basis
    }

@tool
def analyze_stock(symbol: str) -> dict:
    """Perform technical and fundamental analysis."""
    return {
        "symbol": symbol,
        "recommendation": "buy",
        "price_target": 180.00,
        "risk_level": "moderate"
    }

# Create agent
llm = ChatAnthropic(model="claude-3-7-sonnet-latest")
agent = create_react_agent(
    llm,
    tools=[get_portfolio_value, get_position, analyze_stock]
)

# Use agent
result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "What's my AAPL position worth and should I buy more?"
    }]
})

print(result["messages"][-1].content)
```

## Reference

- **Tool Decorators**: `@tool` for simple functions
- **Base Classes**: `BaseTool` for complex tools
- **Execution**: `ToolNode`, `create_react_agent`
- **Type Safety**: Use Pydantic models for inputs/outputs
- **Error Handling**: Return error objects instead of raising exceptions

---

**Note**: Tools enable LLMs to interact with external systems. Always validate inputs and handle errors gracefully.
