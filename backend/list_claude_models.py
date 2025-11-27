"""
List available Claude models for your API key.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings

if not settings.ANTHROPIC_API_KEY:
    print("❌ ANTHROPIC_API_KEY not found")
    sys.exit(1)

api_key = settings.ANTHROPIC_API_KEY.strip()

try:
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)
    
    print("=" * 60)
    print("🔍 Testing Common Claude Model Names")
    print("=" * 60)
    print()
    
    # Common model names to test
    models_to_test = [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-latest",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
        "claude-3-haiku-20240307",
        "claude-sonnet-4.5",
        "claude-3-5-sonnet",
    ]
    
    print("Testing model names...\n")
    
    for model_name in models_to_test:
        try:
            print(f"Testing: {model_name}...", end=" ")
            message = client.messages.create(
                model=model_name,
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}]
            )
            print(f"✅ WORKS! Response: {message.content[0].text[:30]}")
            print(f"   ⭐ Use this model: {model_name}\n")
            break
        except anthropic.NotFoundError:
            print(f"❌ Not found")
        except Exception as e:
            print(f"❌ Error: {type(e).__name__}")
    
    print("\n" + "=" * 60)
    print("💡 If none work, check:")
    print("   1. Your API key has access to Claude models")
    print("   2. Your account has billing/credits set up")
    print("   3. Visit: https://console.anthropic.com/")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

