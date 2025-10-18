# `/api` Command - API Status Checker

## Overview

The `/api` command provides users with a convenient way to self-test their API connectivity directly from the chat interface. This helps diagnose configuration issues without requiring command-line knowledge or running Python scripts.

## Usage

In the Navam Invest chat interface, simply type:

```
/api
```

The command will:
1. Check all configured API keys from your `.env` file
2. Test actual connectivity to each API provider
3. Display results in a formatted table
4. Provide actionable guidance for failed APIs

## Features

### Real-Time Testing
- Tests actual API connectivity (not just key presence)
- Detects rate limiting and access issues
- Shows which APIs are working vs failing

### Visual Status Indicators
- ✅ **Working** - API is configured and responding correctly
- ❌ **Failed** - API key invalid, expired, or access denied
- ⚠️ **Rate Limited** - API temporarily unavailable (retry later)
- ⚪ **Not Configured** - Optional API not set up (no key in `.env`)
- 🔵 **Built-in** - Free APIs requiring no configuration

### Comprehensive Coverage
Tests all supported APIs:
- **Anthropic** - AI model provider (required)
- **Alpha Vantage** - Stock quotes
- **FRED** - Economic data
- **NewsAPI.org** - News articles
- **FMP** - Fundamentals
- **Finnhub** - Alternative data
- **Tiingo** - Historical data
- **Yahoo Finance** - Built-in (no key needed)
- **SEC EDGAR** - Built-in (no key needed)
- **U.S. Treasury** - Built-in (no key needed)

### Actionable Summary
Provides:
- Count of working/failed/unconfigured APIs
- Troubleshooting tips for common issues
- Links to validation scripts for specific APIs

## Example Output

```
Checking API Status...
Testing connectivity to all configured APIs...

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ API Provider  ┃ Status       ┃ Details                          ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Anthropic     │ ✅ Configured│ Required - AI model provider     │
│ Alpha Vantage │ ✅ Working   │ Successfully fetched quote data  │
│ FRED          │ ✅ Working   │ Successfully fetched economic data│
│ NewsAPI.org   │ ✅ Working   │ 1,000 articles available         │
│ FMP           │ ❌ Failed    │ Access denied - check plan       │
│ Finnhub       │ ✅ Working   │ Successfully fetched quote       │
│ Tiingo        │ ✅ Working   │ Successfully fetched data        │
│ Yahoo Finance │ ✅ Built-in  │ Free - No API key required       │
│ SEC EDGAR     │ ✅ Built-in  │ Free - No API key required       │
│ U.S. Treasury │ ✅ Built-in  │ Free - No API key required       │
└───────────────┴──────────────┴──────────────────────────────────┘

Summary: 9 working • 1 failed • 0 not configured

💡 Tips:
- Failed APIs: Check your .env file for correct API keys
- Not configured: Optional - get free keys to unlock more features
- Rate limited: Wait a few minutes and try again

Run `python scripts/validate_newsapi_key.py` to validate NewsAPI.org specifically.
```

## Implementation Details

### Architecture

```
User types /api in TUI
    ↓
ChatUI._handle_command()
    ↓
check_all_apis() in utils/api_checker.py
    ↓
Parallel async HTTP requests to each API
    ↓
Rich Table formatting in TUI
    ↓
Display results + summary
```

### Code Location

- **Command Handler:** `src/navam_invest/tui/app.py` (lines ~395-453)
- **API Checker:** `src/navam_invest/utils/api_checker.py`
- **Test Script:** `scripts/test_api_command.py`

### API Testing Logic

Each API has a dedicated checker function:
- `check_alpha_vantage()` - Fetches AAPL quote
- `check_fred()` - Fetches GDP series
- `check_newsapi()` - Fetches top headlines
- `check_fmp()` - Fetches AAPL fundamentals
- `check_finnhub()` - Fetches AAPL quote
- `check_tiingo()` - Fetches AAPL daily data

All checks:
1. Make actual API request (not just validation)
2. Parse response for success/error
3. Return status + details
4. Handle timeouts and network errors gracefully

### Error Handling

The command handles:
- **Network timeouts** - 10-second timeout per API
- **Invalid keys** - Clear "Invalid API key" message
- **Rate limits** - Distinguishes rate limiting from failures
- **Access denied** - Shows when plan upgrade needed
- **Unknown errors** - Graceful degradation with error message

## User Benefits

### 1. **Self-Service Diagnostics**
Users can troubleshoot API issues without:
- Running Python scripts
- Reading documentation
- Understanding technical details
- Contacting support

### 2. **Configuration Validation**
Immediately after setting up `.env` file, users can:
- Verify all keys are correct
- Confirm connectivity works
- Identify misconfigured APIs
- See which features are available

### 3. **Proactive Monitoring**
During usage, users can:
- Check if API failures are on their end
- Detect rate limit exhaustion
- Verify service availability
- Diagnose connectivity issues

### 4. **Educational Context**
Shows users:
- Which APIs are required vs optional
- What each API provides
- Free tier limitations
- Where to get API keys

## Common Use Cases

### Scenario 1: Initial Setup
**User:** Just created `.env` file with API keys
**Action:** Type `/api` to validate configuration
**Result:** See which keys work, fix any that fail

### Scenario 2: Troubleshooting Errors
**User:** Agent says "Failed to fetch news"
**Action:** Type `/api` to diagnose
**Result:** See NewsAPI is rate limited or key invalid

### Scenario 3: Feature Discovery
**User:** Wondering what data sources are available
**Action:** Type `/api` to see all providers
**Result:** Learn about optional APIs to enable

### Scenario 4: Performance Issues
**User:** Queries seem slow or failing
**Action:** Type `/api` to check service status
**Result:** Identify rate-limited or down APIs

## Integration with Other Tools

### Complementary Scripts

The `/api` command complements standalone scripts:

**In Chat Interface:**
```
/api  # Quick overview of all APIs
```

**In Terminal:**
```bash
# Detailed NewsAPI validation
python scripts/validate_newsapi_key.py

# Comprehensive test suite
pytest tests/test_api_keys.py -v
```

### When to Use Each

| Tool | When to Use |
|------|-------------|
| **`/api` command** | Quick check during normal usage |
| **`validate_newsapi_key.py`** | Detailed NewsAPI debugging |
| **`test_api_keys.py`** | Development/CI testing |
| **`test_api_command.py`** | Command-line status check |

## Future Enhancements

### Potential Additions

1. **Rate Limit Tracking**
   - Show remaining API calls
   - Display reset time
   - Warn before exhaustion

2. **Historical Status**
   - Track API uptime
   - Show failure patterns
   - Alert on degraded service

3. **Auto-Retry Logic**
   - Retry failed APIs
   - Exponential backoff
   - Success notification

4. **Detailed Error Messages**
   - HTTP response details
   - Suggested fixes
   - Documentation links

5. **API Key Management**
   - Mask sensitive keys
   - Rotate expired keys
   - Test new keys before saving

## Developer Notes

### Adding New API Checks

To add a new API checker:

1. **Create checker function** in `utils/api_checker.py`:
```python
async def check_new_api(api_key: str) -> Dict[str, Any]:
    """Test NewAPI API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.newapi.com/test",
                headers={"Authorization": f"Bearer {api_key}"},
                timeout=10.0,
            )
            if response.status_code == 200:
                return {"status": "✅ Working", "details": "API responding"}
            else:
                return {"status": "❌ Failed", "details": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"status": "❌ Failed", "details": str(e)[:50]}
```

2. **Add to `check_all_apis()`**:
```python
if settings.new_api_key:
    result = await check_new_api(settings.new_api_key)
    results.append({"api": "NewAPI", **result})
else:
    results.append({
        "api": "NewAPI",
        "status": "⚪ Not Configured",
        "details": "Optional - description",
    })
```

3. **Update settings** in `config/settings.py`:
```python
new_api_key: Optional[str] = None
```

### Testing

```bash
# Test API checker module
python scripts/test_api_command.py

# Test in TUI
navam invest
> /api

# Run unit tests
pytest tests/test_api_keys.py -v
```

## Documentation References

- **User Guide:** See README.md for `/api` command usage
- **API Keys Setup:** See README.md "Get API Keys" section
- **NewsAPI Guide:** See `refer/specs/newsapi-clarification.md`
- **Test Suite:** See `tests/test_api_keys.py`

---

**Status:** ✅ Implemented in v0.1.27+
**Location:** Available in chat interface via `/api` command
**Dependencies:** httpx, rich, textual
