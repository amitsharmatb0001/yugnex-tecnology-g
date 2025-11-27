"""
FILE: check_api_keys.py
PATH: backend/check_api_keys.py
PURPOSE: Diagnostic script to verify API keys are loaded correctly.
USAGE: python check_api_keys.py
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import settings

print("=" * 60)
print("🔍 API KEY DIAGNOSTIC TOOL")
print("=" * 60)
print()

# Check .env file location
env_file = Path(__file__).parent / ".env"
print(f"📁 .env file location: {env_file}")
print(f"   Exists: {env_file.exists()}")
print()

# Check Anthropic Key
print("🔑 ANTHROPIC API KEY:")
if settings.ANTHROPIC_API_KEY:
    key = settings.ANTHROPIC_API_KEY.strip()
    print(f"   ✅ Key is loaded")
    print(f"   Length: {len(key)} characters")
    print(f"   Starts with: {key[:15]}...")
    print(f"   Ends with: ...{key[-10:]}")
    
    # Validate format
    if key.startswith("sk-ant-"):
        print(f"   ✅ Format looks correct (starts with 'sk-ant-')")
    else:
        print(f"   ⚠️  WARNING: Key doesn't start with 'sk-ant-'")
        print(f"   Expected format: sk-ant-api03-...")
    
    # Check for common issues
    if len(key) < 50:
        print(f"   ⚠️  WARNING: Key seems too short (expected ~100+ chars)")
    if " " in key:
        print(f"   ⚠️  WARNING: Key contains spaces (should be removed)")
    if "\n" in key or "\r" in key:
        print(f"   ⚠️  WARNING: Key contains line breaks (should be removed)")
else:
    print(f"   ❌ Key is NOT loaded")
    print(f"   Check your .env file has: ANTHROPIC_API_KEY=sk-ant-...")

print()

# Check Google Key
print("🔑 GOOGLE API KEY:")
google_key = settings.GOOGLE_AI_STUDIO_KEY or settings.GOOGLE_API_KEY
if google_key:
    key = google_key.strip()
    print(f"   ✅ Key is loaded ({'GOOGLE_AI_STUDIO_KEY' if settings.GOOGLE_AI_STUDIO_KEY else 'GOOGLE_API_KEY'})")
    print(f"   Length: {len(key)} characters")
    print(f"   Starts with: {key[:15]}...")
    print(f"   Ends with: ...{key[-10:]}")
    
    # Validate format
    if key.startswith("AIza"):
        print(f"   ✅ Format looks correct (starts with 'AIza')")
    else:
        print(f"   ⚠️  WARNING: Key doesn't start with 'AIza'")
    
    # Check for common issues
    if len(key) < 30:
        print(f"   ⚠️  WARNING: Key seems too short")
    if " " in key:
        print(f"   ⚠️  WARNING: Key contains spaces (should be removed)")
else:
    print(f"   ❌ Key is NOT loaded")
    print(f"   Check your .env file has: GOOGLE_AI_STUDIO_KEY=AIza...")

print()
print("=" * 60)
print("💡 TIPS:")
print("   1. Keys should have NO spaces around the = sign")
print("   2. Keys should be on a single line (no line breaks)")
print("   3. Remove any quotes around the key value")
print("   4. Anthropic keys start with: sk-ant-api03-")
print("   5. Google keys start with: AIza")
print("=" * 60)

