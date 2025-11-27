"""
Simple test to verify Anthropic API key works.
"""
import sys
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings

print("Testing Anthropic API Key...")
print(f"Key loaded: {bool(settings.ANTHROPIC_API_KEY)}")

if not settings.ANTHROPIC_API_KEY:
    print("❌ No API key found")
    sys.exit(1)

api_key = settings.ANTHROPIC_API_KEY.strip()
print(f"Key length: {len(api_key)}")
print(f"Key starts with: {api_key[:20]}")

try:
    import anthropic
    print(f"\n✅ Anthropic SDK imported (version: {anthropic.__version__})")
    
    client = anthropic.Anthropic(api_key=api_key)
    print("✅ Client created")
    
    print("\nSending test request...")
    
    # Try all Claude models from official documentation (prioritize 4.5 models)
    models_to_try = [
        getattr(settings, 'ANTHROPIC_MODEL', None),
        # Claude 4.5 Models (Latest - November 2025)
        "claude-sonnet-4-5",  # Official alias for Claude Sonnet 4.5
        "claude-sonnet-4.5",  # Friendly name with dot
        "claude-sonnet-4-5-20250929",  # Full API ID
        "claude-haiku-4-5",  # Official alias for Claude Haiku 4.5
        "claude-haiku-4.5",  # Friendly name
        "claude-haiku-4-5-20251001",  # Full API ID
        "claude-opus-4-5",  # Official alias for Claude Opus 4.5
        "claude-opus-4.5",  # Friendly name
        "claude-opus-4-5-20251101",  # Full API ID
        "claude-opus-4-1",  # Official alias for Claude Opus 4.1
        "claude-opus-4.1",  # Friendly name
        "claude-opus-4-1-20250805",  # Full API ID
        # Legacy models (fallback)
        "claude-3-5-sonnet-20241022",
        "claude-3-opus-20240229",
        "claude-3-sonnet-20240229",
    ]
    
    # Filter out None values
    models_to_try = [m for m in models_to_try if m]
    
    success = False
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}...")
            message = client.messages.create(
                model=model_name,
                max_tokens=20,
                messages=[{"role": "user", "content": "Say hello"}]
            )
            print(f"✅ SUCCESS with model: {model_name}!")
            print(f"Response: {message.content[0].text}")
            print(f"\n💡 Add this to your .env file:")
            print(f"   ANTHROPIC_MODEL={model_name}")
            success = True
            break
        except anthropic.NotFoundError:
            print(f"   ❌ Model not found")
            continue
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}")
            continue
    
    if not success:
        print(f"\n❌ None of the tested models worked.")
        print(f"Check your Anthropic account for available models:")
        print(f"https://console.anthropic.com/")
    
except anthropic.AuthenticationError as e:
    print(f"\n❌ AUTHENTICATION ERROR")
    print(f"Error: {e}")
    print(f"\nPossible causes:")
    print("1. API key is invalid or expired")
    print("2. API key was revoked")
    print("3. Account doesn't have billing/credits set up")
    print("4. Check: https://console.anthropic.com/")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"Message: {e}")
    import traceback
    traceback.print_exc()

