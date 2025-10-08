#!/usr/bin/env python3
"""Validate and test NewsAPI.org API key."""

import asyncio
import sys

import httpx


async def validate_newsapi_key(api_key: str) -> dict:
    """Validate NewsAPI key by making a simple test request.

    Args:
        api_key: NewsAPI.org API key to validate

    Returns:
        Dictionary with validation results
    """
    print(f"\n🔍 Validating NewsAPI key: {api_key[:10]}...\n")

    # Test 1: Check key format
    print("1️⃣  Checking key format...")
    if not api_key or len(api_key) < 20:
        return {
            "valid": False,
            "error": "API key too short. NewsAPI keys are typically 32 characters.",
        }

    # Test 2: Make actual API request
    print("2️⃣  Testing API request...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://newsapi.org/v2/top-headlines",
                params={"country": "us", "category": "business", "pageSize": 1},
                headers={"X-Api-Key": api_key},
                timeout=10.0,
            )

            print(f"   Status Code: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "ok":
                    total = data.get("totalResults", 0)
                    print(f"   ✅ API key is VALID! ({total} articles available)")
                    return {
                        "valid": True,
                        "totalResults": total,
                        "response": data,
                    }
                else:
                    error_msg = data.get("message", "Unknown error")
                    print(f"   ❌ API returned error: {error_msg}")
                    return {"valid": False, "error": error_msg}

            elif response.status_code == 401:
                data = response.json()
                error_code = data.get("code", "")
                error_msg = data.get("message", "")
                print(f"   ❌ Authentication failed!")
                print(f"   Error Code: {error_code}")
                print(f"   Message: {error_msg}")
                return {"valid": False, "error": f"{error_code}: {error_msg}"}

            elif response.status_code == 429:
                print(f"   ⚠️  Rate limit exceeded. Key may be valid but exhausted.")
                return {"valid": False, "error": "Rate limit exceeded"}

            else:
                print(f"   ❌ Unexpected status code: {response.status_code}")
                return {
                    "valid": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                }

    except httpx.TimeoutException:
        print(f"   ❌ Request timed out")
        return {"valid": False, "error": "Request timeout"}
    except Exception as e:
        print(f"   ❌ Request failed: {str(e)}")
        return {"valid": False, "error": str(e)}


async def main():
    """Main validation script."""
    print("=" * 60)
    print("NewsAPI.org Key Validator")
    print("=" * 60)

    # Try to load from .env file
    try:
        from navam_invest.config.settings import get_settings

        settings = get_settings()
        api_key = settings.newsapi_api_key

        if not api_key:
            print("\n❌ No NEWSAPI_API_KEY found in .env file")
            print("\n📝 To get a FREE NewsAPI key:")
            print("   1. Go to: https://newsapi.org/register")
            print("   2. Sign up with your email")
            print("   3. Get your API key (free tier: 1000 requests/day)")
            print("   4. Add to .env file: NEWSAPI_API_KEY=your_key_here")
            sys.exit(1)

        print(f"\n✅ Found NEWSAPI_API_KEY in .env file")

    except Exception as e:
        print(f"\n❌ Error loading settings: {e}")
        sys.exit(1)

    # Validate the key
    result = await validate_newsapi_key(api_key)

    print("\n" + "=" * 60)
    print("Validation Results")
    print("=" * 60)

    if result["valid"]:
        print("\n✅ SUCCESS! Your NewsAPI key is valid and working.")
        print(f"   Total articles available: {result.get('totalResults', 0)}")
    else:
        print("\n❌ FAILED! Your NewsAPI key is invalid or expired.")
        print(f"\n🔴 Error: {result['error']}")
        print("\n📝 How to fix:")
        print("   1. Go to: https://newsapi.org/account")
        print("   2. Check if your API key is active")
        print("   3. If expired or invalid, generate a new key")
        print("   4. Update your .env file with: NEWSAPI_API_KEY=new_key_here")
        print("\n💡 Free tier includes:")
        print("   • 1,000 requests per day")
        print("   • General business and tech news")
        print("   • 24-hour article delay")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
