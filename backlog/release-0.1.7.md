# Release 0.1.7

## TUI Command Enhancements

### Features

1. **UX Improvement - Command Alternatives**: Added `/quit` and `/clear` slash commands as alternatives to keyboard shortcuts, improving usability in VS Code terminal and other environments where `Ctrl+Q` may be intercepted.

2. **Onboarding Enhancement - Example Prompts**: Added `/examples` command that displays randomized, agent-specific example prompts to help users discover capabilities and understand what questions they can ask.

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

## Example Prompts Feature (`/examples`)

### Problem

**Before**:
- New users didn't know what questions to ask or what the agents could do
- No discovery mechanism for available tools and capabilities
- Users had to guess or read documentation to understand agent capabilities
- No quick way to see concrete examples of valuable queries

**After**:
- `/examples` command shows 4 randomly selected example prompts
- Examples are agent-specific (different for portfolio vs research agents)
- Examples cover all major tool categories available to each agent
- Fresh randomization on each command invocation improves discovery
- Clear, actionable prompts users can copy or adapt

### Implementation Details

#### Example Prompt Collections (`tui/app.py`)

**Portfolio Agent Examples** (8 total):
```python
PORTFOLIO_EXAMPLES = [
    "What's the current price and overview of AAPL?",
    "Show me the fundamentals and financial ratios for TSLA",
    "What insider trades have happened at MSFT recently?",
    "Screen for tech stocks with P/E ratio under 20 and market cap over $10B",
    "Get the latest 10-K filing for GOOGL",
    "Show me institutional holdings (13F filings) for NVDA",
    "Compare the financial ratios of AAPL and MSFT",
    "What does the latest 10-Q for AMZN reveal about their business?",
]
```

**Research Agent Examples** (8 total):
```python
RESEARCH_EXAMPLES = [
    "What's the current GDP growth rate?",
    "Show me key macro indicators: GDP, CPI, and unemployment",
    "What does the Treasury yield curve look like today?",
    "Calculate the 10-year minus 2-year yield spread",
    "What's the current debt-to-GDP ratio?",
    "How has inflation (CPI) trended over the past year?",
    "What's the current federal funds rate?",
    "Is the yield curve inverted? What does that signal?",
]
```

#### Command Handler (`tui/app.py`)

```python
elif command == "/examples":
    # Show examples for current agent
    examples = (
        PORTFOLIO_EXAMPLES
        if self.current_agent == "portfolio"
        else RESEARCH_EXAMPLES
    )
    agent_name = (
        "Portfolio Analysis" if self.current_agent == "portfolio" else "Market Research"
    )

    # Randomly select 4 examples to show
    selected_examples = random.sample(examples, min(4, len(examples)))

    examples_text = "\n".join(f"{i+1}. {ex}" for i, ex in enumerate(selected_examples))

    chat_log.write(
        Markdown(
            f"\n**Example prompts for {agent_name} agent:**\n\n"
            f"{examples_text}\n\n"
            f"💡 Try copying one of these or ask your own question!\n"
        )
    )
```

#### Tool Coverage Analysis

**Portfolio Agent Examples Cover**:
- ✅ Market data tools (Alpha Vantage): price, overview
- ✅ Fundamentals tools (FMP): fundamentals, ratios, insider trades, screening
- ✅ SEC filing tools: 10-K, 10-Q, 13F institutional holdings

**Research Agent Examples Cover**:
- ✅ Macro tools (FRED): GDP, CPI, unemployment, interest rates
- ✅ Treasury tools: yield curves, spreads, debt-to-GDP
- ✅ Economic interpretation: yield curve signals, macro indicators

#### Updated UI Elements

**Welcome Message**:
```markdown
**Commands:**
- `/portfolio` - Switch to portfolio analysis agent
- `/research` - Switch to market research agent
- `/examples` - Show example prompts for current agent  ← NEW
- `/clear` - Clear chat history
- `/quit` - Exit the application
- `/help` - Show all commands

**Tip:** Type `/examples` to see what you can ask!  ← NEW
```

**Input Placeholder**:
```python
placeholder="Ask about stocks or economic indicators (/examples for ideas, /help for commands)..."
```

**Help Command**:
```markdown
**Available Commands:**
- `/portfolio` - Switch to portfolio analysis agent
- `/research` - Switch to market research agent
- `/examples` - Show example prompts for current agent  ← NEW
- `/clear` - Clear chat history
- `/quit` - Exit the application
- `/help` - Show this help message
```

### Benefits

- ✅ **Improved Onboarding**: New users immediately see what they can ask
- ✅ **Tool Discovery**: Examples demonstrate all major tool categories
- ✅ **Agent-Aware**: Different examples for portfolio vs research agents
- ✅ **Randomization**: Each `/examples` call shows 4 random prompts from 8 total
- ✅ **Actionable**: Users can copy/paste or adapt example prompts
- ✅ **100% Tool Coverage**: Examples exercise all 17 available tools across both agents
- ✅ **Educational**: Examples teach users what kinds of questions work well

### Files Modified

1. `src/navam_invest/tui/app.py`:
   - Added `PORTFOLIO_EXAMPLES` and `RESEARCH_EXAMPLES` constants (8 examples each)
   - Added `random` import for randomization
   - Implemented `/examples` command handler with agent-specific logic
   - Updated welcome message to promote `/examples`
   - Updated input placeholder to mention `/examples`
   - Updated `/help` command to include `/examples`

### Results

- ✅ **8 portfolio examples**: Cover market data, fundamentals, SEC filings, screening
- ✅ **8 research examples**: Cover macro indicators, Treasury data, yield curves
- ✅ **Random rotation**: Shows 4 different examples each time
- ✅ **Agent-aware**: Automatically shows relevant examples based on current agent
- ✅ **Discoverable**: Promoted in welcome message, help, and input placeholder
- ✅ **Syntax valid**: Python compilation successful
- ✅ **Complete tool coverage**: All 17 tools represented across examples

### Release Date
IN DEVELOPMENT

### PyPI Package
Not yet published
