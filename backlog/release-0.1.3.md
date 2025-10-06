# Release 0.1.3

## CLI Command Improvement

### Feature

**Improved User Experience**: Replaced CLI command `navam tui` with `navam invest` for more intuitive usage.

### Implementation Details

#### 1. Command Replacement (`cli.py`)
Replaced `tui` command with `invest` command:
```python
@app.command()
def invest() -> None:
    """Launch the interactive investment advisor chat interface."""
    console.print("[bold green]Launching Navam Invest...[/bold green]")
    asyncio.run(run_tui())
```

#### 2. Updated Documentation
- Updated CLI help messages to show `navam invest` as primary command
- Updated README.md with new command in all examples
- Updated TUI error messages to reference new command
- Updated main callback help text

### User Experience Changes

**Before**:
```bash
navam tui       # Launch interactive TUI
```

**After**:
```bash
navam invest    # Launch interactive chat interface
```

### Files Modified
1. `src/navam_invest/cli.py` - Replaced `tui` command with `invest`, updated help text
2. `src/navam_invest/tui/app.py` - Updated error message to reference `navam invest`
3. `README.md` - Updated all command references to use `navam invest`
4. `pyproject.toml` - Incremented version 0.1.2 → 0.1.3

### Benefits
- ✅ More intuitive command name ("invest" vs "tui")
- ✅ Better reflects the application's purpose
- ✅ Cleaner CLI interface with single launch command
- ✅ Consistent documentation across all files

### Testing
- Verified `navam invest` launches correctly
- Verified `navam --help` shows only `invest` and `version` commands
- Verified help text updated correctly
- Verified version displays as 0.1.3

### Release Date
2025-10-05

### Version
0.1.3 (Alpha)
