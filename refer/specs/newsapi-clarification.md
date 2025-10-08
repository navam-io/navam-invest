# NewsAPI Service Clarification

**IMPORTANT: This project uses NewsAPI.org, NOT NewsAPI.ai**

## Two Different Services

There are **two completely different** news API services with similar names:

### 1. NewsAPI.org ✅ (What We Use)
- **Website:** https://newsapi.org
- **Registration:** https://newsapi.org/register
- **Account:** https://newsapi.org/account
- **Free Tier:** 1,000 requests/day
- **API Format:** REST API with header-based authentication (`X-Api-Key`)
- **Key Format:** 32-character alphanumeric string (e.g., `370bee2110404ee2944d055ccb4c0af0`)
- **What it provides:** General business and tech news from major publishers
- **Limitations:** 24-hour article delay on free tier

### 2. NewsAPI.ai ❌ (NOT Used)
- **Website:** https://www.newsapi.ai
- **Different service entirely**
- **Different API endpoints and authentication**
- **Keys from NewsAPI.ai will NOT work with our code**

## Why This Matters

If you get a key from NewsAPI.ai and try to use it with this application, you'll get:
```
HTTP error: 401 - {"status":"error","code":"apiKeyInvalid","message":"Your API key is invalid"}
```

This is because the keys are **not interchangeable** - they're from different companies.

## How to Get the Correct Key

1. Go to: https://newsapi.org/register (NOT newsapi.ai)
2. Enter your email and name
3. Receive your API key via email
4. Add to `.env` file:
   ```bash
   NEWSAPI_API_KEY=your_32_character_key_here
   ```

## Verify Your Key Works

```bash
# Activate virtual environment
source .venv/bin/activate

# Run validator
python scripts/validate_newsapi_key.py

# Should see:
# ✅ SUCCESS! Your NewsAPI key is valid and working.
```

## Implementation Details

All NewsAPI.org integration code is in:
- **Tools:** `src/navam_invest/tools/newsapi.py`
- **Tests:** `tests/test_api_keys.py`
- **Validator:** `scripts/validate_newsapi_key.py`

The tools make requests to:
- `https://newsapi.org/v2/everything` (search)
- `https://newsapi.org/v2/top-headlines` (headlines)

Authentication is via HTTP header:
```python
headers={"X-Api-Key": api_key}
```

## Common Mistakes to Avoid

❌ **Wrong:** Getting key from NewsAPI.ai
✅ **Right:** Get key from NewsAPI.org

❌ **Wrong:** Using old/expired key from newsapi.org
✅ **Right:** Generate fresh key from newsapi.org/account

❌ **Wrong:** Expecting real-time news on free tier
✅ **Right:** Free tier has 24-hour delay (still useful for analysis)

## Alternative News Sources

If NewsAPI.org doesn't meet your needs, the application also supports:

1. **Finnhub** - Real-time financial news (finnhub.io)
2. **MarketAux** - Financial news with sentiment (marketaux.com)
3. **Yahoo Finance** - Built-in, no key needed

See `.env.example` for configuration of alternative sources.

## References

- Official NewsAPI.org Docs: https://newsapi.org/docs
- Our implementation: `src/navam_invest/tools/newsapi.py`
- Test suite: `tests/test_api_keys.py::TestNewsAPI`

---

**Last Updated:** 2025-10-08
**Issue Resolution:** Fixed confusion between NewsAPI.org and NewsAPI.ai
