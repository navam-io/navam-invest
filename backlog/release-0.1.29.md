# Release 0.1.29

## Status
IN DEVELOPMENT

## Features

### ✅ Completed Features

#### 📄 Automatic Report Saving (v0.1.29)

**Problem**: Users had no way to save or reference agent-generated analysis after exiting the TUI.

**Solution**: Automatic report saving to `reports/` directory with timestamps and metadata.

**Implementation**:
- **New Module**: `src/navam_invest/utils/report_saver.py` (165 lines)
  - `save_agent_report()` - General-purpose report saving for any agent response
  - `save_investment_report()` - Specialized multi-section report saving for `/analyze` workflow
  - Automatic directory creation
  - Timestamped filenames with context
  - Markdown formatting with metadata headers

- **TUI Integration**: Modified `src/navam_invest/tui/app.py`
  - `/analyze` workflow: Saves complete 3-section report (Quill + Macro Lens + Final Recommendation)
  - All agent responses: Saves substantial responses (>200 chars) automatically
  - User notification: Shows saved file path after each report
  - Error handling: Graceful degradation if save fails

- **Test Suite**: `tests/test_report_saver.py` (5 tests)
  - Basic report saving
  - Report saving with context (symbol, query)
  - Investment analysis multi-section reports
  - Directory creation
  - Minimal report handling

**User Benefits**:
1. **Persistent Analysis**: All investment research automatically preserved
2. **Audit Trail**: Complete history of agent recommendations with timestamps
3. **Easy Sharing**: Markdown reports can be shared with advisors/colleagues
4. **Offline Reference**: Review analysis without re-running queries
5. **No Manual Work**: Fully automatic—user doesn't need to copy/paste

**Technical Details**:
- Report filename format: `{symbol}_{report_type}_{timestamp}.md`
- Example: `AAPL_analysis_20251008_143022.md`
- Metadata includes: generation date, symbol, query text
- Content includes agent responses + footer
- Minimum length threshold: 200 characters (filters out trivial responses)

**Usage Example**:
```
> /analyze AAPL
📊 Quill analyzing fundamentals...
🌍 Macro Lens validating timing...
🎯 Final Recommendation: BUY - High Confidence
📄 Report saved to: /path/to/reports/AAPL_analysis_20251008_143022.md
```

**Files Changed**:
- NEW: `src/navam_invest/utils/report_saver.py`
- NEW: `tests/test_report_saver.py`
- Modified: `src/navam_invest/utils/__init__.py`
- Modified: `src/navam_invest/tui/app.py`
- Modified: `README.md` (new documentation section)

**Tests**: 66/66 passing (5 new tests for report saving)

---

### 🚧 Planned Features

Based on v0.1.28 foundation:
- **News Sentry** agent (leverages SEC 8-K material events and real-time news filtering)
- Enhanced multi-agent workflows (extend `/analyze` workflow)
- API caching layer for efficiency (DuckDB-based caching)
- Options analysis tools (Yahoo Finance options chain integration)
- Risk management enhancements

---

## Release Date
TBD

## PyPI Package
TBD
