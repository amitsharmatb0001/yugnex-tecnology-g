"""
Find which Claude model name works with your API key.
Tests all Claude 4.5 models from official Anthropic documentation.
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
    
    print("=" * 70)
    print("🔍 FINDING WORKING CLAUDE MODEL NAME")
    print("Based on official Anthropic documentation")
    print("=" * 70)
    print()
    
    # All Claude models from official documentation
    models_to_test = [
        # Claude 4.5 Models (Latest - November 2025)
        ("claude-sonnet-4-5", "Claude Sonnet 4.5 (Official alias)"),
        ("claude-sonnet-4.5", "Claude Sonnet 4.5 (Friendly name)"),
        ("claude-sonnet-4-5-20250929", "Claude Sonnet 4.5 (Full API ID)"),
        
        ("claude-haiku-4-5", "Claude Haiku 4.5 (Official alias)"),
        ("claude-haiku-4.5", "Claude Haiku 4.5 (Friendly name)"),
        ("claude-haiku-4-5-20251001", "Claude Haiku 4.5 (Full API ID)"),
        
        ("claude-opus-4-5", "Claude Opus 4.5 (Official alias)"),
        ("claude-opus-4.5", "Claude Opus 4.5 (Friendly name)"),
        ("claude-opus-4-5-20251101", "Claude Opus 4.5 (Full API ID)"),
        
        ("claude-opus-4-1", "Claude Opus 4.1 (Official alias)"),
        ("claude-opus-4.1", "Claude Opus 4.1 (Friendly name)"),
        ("claude-opus-4-1-20250805", "Claude Opus 4.1 (Full API ID)"),
        
        # Legacy Claude 3.5 Models
        ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet (Legacy)"),
        ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku (Legacy)"),
        
        # Legacy Claude 3.0 Models
        ("claude-3-opus-20240229", "Claude 3 Opus (Legacy)"),
        ("claude-3-sonnet-20240229", "Claude 3 Sonnet (Legacy)"),
        ("claude-3-haiku-20240307", "Claude 3 Haiku (Legacy)"),
    ]
    
    print(f"Testing {len(models_to_test)} model names...\n")
    print("-" * 70)
    
    working_models = []
    
    for i, (model_name, description) in enumerate(models_to_test, 1):
        try:
            print(f"[{i}/{len(models_to_test)}] {description}")
            print(f"    Model: {model_name:<40}", end=" ")
            
            message = client.messages.create(
                model=model_name,
                max_tokens=5,
                messages=[{"role": "user", "content": "Hi"}]
            )
            
            print(f"✅ WORKS!")
            working_models.append((model_name, description))
            print(f"    Response: {message.content[0].text[:50]}")
            print()
            
        except anthropic.NotFoundError:
            print("❌ Not found")
        except anthropic.AuthenticationError as e:
            print(f"❌ Auth error: {e}")
            break  # Stop if auth fails
        except Exception as e:
            print(f"❌ {type(e).__name__}")
    
    print("-" * 70)
    print()
    
    if working_models:
        print("=" * 70)
        print("✅ WORKING MODELS FOUND:")
        print("=" * 70)
        for model_name, description in working_models:
            print(f"   • {model_name:<35} - {description}")
        print()
        print("💡 Recommended model (first working):")
        print(f"   ANTHROPIC_MODEL={working_models[0][0]}")
        print()
        print("Add this to your .env file:")
        print(f"   ANTHROPIC_MODEL={working_models[0][0]}")
    else:
        print("=" * 70)
        print("❌ NO WORKING MODELS FOUND")
        print("=" * 70)
        print("\nPossible issues:")
        print("1. API key doesn't have access to Claude models")
        print("2. Account needs billing/credits setup")
        print("3. Check: https://console.anthropic.com/")
        print("4. Model names may have changed - check Anthropic docs")
    
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

