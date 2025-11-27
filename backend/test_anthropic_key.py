"""
FILE: test_anthropic_key.py
PATH: backend/test_anthropic_key.py
PURPOSE: Test Anthropic API key directly to verify it works.
USAGE: python test_anthropic_key.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings

print("=" * 60)
print("🧪 TESTING ANTHROPIC API KEY")
print("=" * 60)
print()

if not settings.ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not found in settings")
    sys.exit(1)

api_key = settings.ANTHROPIC_API_KEY.strip()
print(f"✅ Key loaded: {api_key[:20]}...{api_key[-10:]}")
print(f"   Length: {len(api_key)} characters")
print()

# Test 1: Direct Anthropic SDK
print("Test 1: Direct Anthropic SDK...")
try:
    import anthropic
    print(f"   Using anthropic SDK version: {anthropic.__version__ if hasattr(anthropic, '__version__') else 'unknown'}")
    client = anthropic.Anthropic(api_key=api_key)
    
    # Test with Claude Sonnet 4.5 (official alias)
    print(f"   Testing model: claude-sonnet-4-5 (Claude Sonnet 4.5)")
    message = client.messages.create(
        model="claude-sonnet-4-5",  # Official Claude 4.5 alias
        max_tokens=10,
        messages=[{"role": "user", "content": "Say 'test'"}]
    )
    print(f"   ✅ SUCCESS! Response: {message.content[0].text[:50]}")
except ImportError as e:
    print(f"   ❌ Import Error: {e}")
    print(f"   Install with: pip install anthropic")
except anthropic.AuthenticationError as e:
    print(f"   ❌ AUTHENTICATION ERROR: {e}")
    print(f"   This means the API key is invalid, expired, or revoked.")
    print(f"   Check: https://console.anthropic.com/")
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print(f"   Full traceback:")
    traceback.print_exc()

print()

# Test 2: LangChain ChatAnthropic
print("Test 2: LangChain ChatAnthropic...")
try:
    from langchain_anthropic import ChatAnthropic
    import langchain_anthropic
    
    print(f"   Using langchain-anthropic version: {langchain_anthropic.__version__ if hasattr(langchain_anthropic, '__version__') else 'unknown'}")
    
    # Set environment variable
    os.environ["ANTHROPIC_API_KEY"] = api_key
    print(f"   ✅ Set ANTHROPIC_API_KEY environment variable")
    
    chat = ChatAnthropic(
        model="claude-sonnet-4-5",  # Official Claude 4.5 alias
        temperature=0,
        max_tokens=10,
        api_key=api_key
    )
    print(f"   ✅ Created ChatAnthropic instance")
    
    # Test invoke
    print(f"   Attempting to invoke...")
    response = chat.invoke("Say 'test'")
    print(f"   ✅ SUCCESS! Response: {response.content[:50]}")
except ImportError as e:
    print(f"   ❌ Import Error: {e}")
    print(f"   Install with: pip install langchain-anthropic")
except Exception as e:
    print(f"   ❌ FAILED: {e}")
    print(f"   Error type: {type(e).__name__}")
    import traceback
    print(f"   Full traceback:")
    traceback.print_exc()

print()
print("=" * 60)
print("💡 If both tests fail, your API key may be:")
print("   1. Invalid or expired")
print("   2. Revoked in Anthropic console")
print("   3. Not activated (check your Anthropic account)")
print("=" * 60)

