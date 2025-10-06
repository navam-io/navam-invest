# Release 0.1.6

## Secure API Key Management

### Feature

**Security Enhancement**: Removed API keys from system prompts and implemented secure credential injection using wrapper functions with proper closure.

### Implementation Details

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
- ✅ **Published to PyPI**: Version 0.1.6 available at https://pypi.org/project/navam-invest/0.1.6/

---

## TUI Command Enhancements

### Feature

**UX Improvement**: Added `/quit` and `/clear` slash commands as alternatives to keyboard shortcuts, improving usability in VS Code terminal and other environments where `Ctrl+Q` may be intercepted.

### Implementation Details

#### Problem

**Before**:
- Only keyboard shortcuts available: `Ctrl+Q` (quit) and `Ctrl+C` (clear)
- VS Code terminal intercepts `Ctrl+Q`, preventing users from quitting the app
- No command-line alternatives for these essential operations

**After**:
- Added `/quit` command to exit the application
- Added `/clear` command to clear chat history
- Both keyboard shortcuts and slash commands now available
- Updated welcome message and help text to show all options

#### Changes Made (`tui/app.py`)

**Command Handler Enhancement**:
```python
async def _handle_command(self, command: str, chat_log: RichLog) -> None:
    """Handle slash commands."""
    if command == "/help":
        chat_log.write(
            Markdown(
                "\n**Available Commands:**\n"
                "- `/portfolio` - Switch to portfolio analysis agent\n"
                "- `/research` - Switch to market research agent\n"
                "- `/clear` - Clear chat history\n"
                "- `/quit` - Exit the application\n"
                "- `/help` - Show this help message\n"
            )
        )
    elif command == "/clear":
        self.action_clear()
    elif command == "/quit":
        self.exit()
```

**Updated Welcome Message**:
```markdown
**Commands:**
- `/portfolio` - Switch to portfolio analysis agent
- `/research` - Switch to market research agent
- `/clear` - Clear chat history
- `/quit` - Exit the application
- `/help` - Show all commands

**Keyboard Shortcuts:**
- `Ctrl+C` - Clear chat
- `Ctrl+Q` - Quit
```

**Updated Input Placeholder**:
```python
Input(
    placeholder="Ask about stocks or economic indicators (/help for commands, /quit to exit)...",
    id="user-input",
)
```

#### Benefits

- ✅ **VS Code Compatible**: `/quit` works in VS Code terminal where `Ctrl+Q` is intercepted
- ✅ **Discoverability**: Commands visible in welcome message and help text
- ✅ **Flexibility**: Users can choose between keyboard shortcuts or slash commands
- ✅ **Consistency**: All major actions now have both keyboard and command options
- ✅ **Better UX**: Clear, intuitive commands that match user expectations

#### Files Modified

1. `src/navam_invest/tui/app.py` - Added `/quit` and `/clear` command handlers, updated help text and welcome message

### Results

- ✅ **Slash commands working**: `/quit` exits app, `/clear` clears chat
- ✅ **Keyboard shortcuts preserved**: `Ctrl+Q` and `Ctrl+C` still work
- ✅ **Help updated**: All documentation reflects new commands
- ✅ **Syntax valid**: Python compilation successful
- ✅ **VS Code friendly**: Users can now exit the app in VS Code terminal

---

### Release Date
2025-10-05

### PyPI Package
https://pypi.org/project/navam-invest/0.1.6/
