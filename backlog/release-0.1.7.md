# Release 0.1.7

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

### Release Date
TBD (in development)

### PyPI Package
Not yet published
