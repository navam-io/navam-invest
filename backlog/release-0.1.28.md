# Release 0.1.28

## Status
Published to PyPI on 2025-10-08

## Features

### `/api` Command - Self-Service API Status Checker ✅ COMPLETED

**Issue Resolution:** Fixed confusion between NewsAPI.org and NewsAPI.ai, created self-testing tools

**What Was Built:**
- Interactive `/api` command in chat interface for checking API connectivity
- Real-time testing of all 10 data providers (Anthropic, FRED, NewsAPI.org, Yahoo Finance, etc.)
- Rich table formatting with color-coded status indicators (✅ ❌ ⚠️ ⚪)
- Actionable troubleshooting tips and error messages
- Comprehensive API testing module (`utils/api_checker.py`)

**User Benefits:**
- **Instant troubleshooting** - Type `/api` to diagnose connectivity issues
- **Setup validation** - Verify `.env` configuration immediately after setup
- **Feature discovery** - See all available data providers at a glance
- **Proactive monitoring** - Check service status during usage

**Technical Implementation:**
- New module: `src/navam_invest/utils/api_checker.py` (242 lines)
- TUI integration: Added `/api` handler in `src/navam_invest/tui/app.py`
- Async HTTP testing with 10-second timeouts
- Parallel execution of all API checks for fast results
- Individual checker functions for each API provider

**Files Created:**
- `src/navam_invest/utils/api_checker.py` - API testing module
- `src/navam_invest/utils/__init__.py` - Utils package
- `scripts/test_api_command.py` - Standalone test script
- `refer/specs/api-status-command.md` - Feature documentation
- `refer/specs/newsapi-comparison.md` - NewsAPI.org vs NewsAPI.ai analysis
- `refer/specs/newsapi-clarification.md` - Service clarification guide
- `API_COMMAND_IMPLEMENTATION.md` - Implementation summary
- `NEWSAPI_DOCUMENTATION_UPDATES.md` - Documentation change log

**Files Modified:**
- `src/navam_invest/tui/app.py` - Added `/api` command handler
- `README.md` - Updated with `/api` documentation
- `.env` - Added clarifying comments for NewsAPI.org
- `.env.example` - Added NewsAPI.org clarification
- `src/navam_invest/tools/newsapi.py` - Updated docstrings to specify NewsAPI.org

**Testing:**
- ✅ Manual testing: All APIs tested successfully
- ✅ TUI integration: Command works in chat interface
- ✅ Live validation: 9/10 APIs working (FMP expected limitation)
- ✅ Comprehensive test suite: `tests/test_api_keys.py`

**Example Output:**
```
> /api

┌─────────────┬──────────┬──────────────────────────┐
│ API         │ Status   │ Details                  │
├─────────────┼──────────┼──────────────────────────┤
│ Anthropic   │ ✅       │ Required - AI model      │
│ FRED        │ ✅       │ Successfully fetched...  │
│ NewsAPI.org │ ✅       │ 1,000 articles available │
│ ...         │ ...      │ ...                      │
└─────────────┴──────────┴──────────────────────────┘

Summary: 9 working • 1 failed • 0 not configured
```

**Documentation:**
- User guide: `refer/specs/api-status-command.md`
- NewsAPI clarification: `refer/specs/newsapi-clarification.md`
- Implementation details: `API_COMMAND_IMPLEMENTATION.md`

### Planned Features (Not Yet Implemented)

- **News Sentry** agent (leverages SEC 8-K material events)
- Enhanced multi-agent workflows
- API caching layer for efficiency
- Options analysis tools (Yahoo Finance options chain)

---

## Release Date
2025-10-08

## PyPI Package
https://pypi.org/project/navam-invest/0.1.28/
