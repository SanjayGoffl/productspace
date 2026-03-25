#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify Gemini and Ollama setup for TinyTroupe Market Simulation.
"""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Load .env file before importing anything else
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    print(f"Loading environment from {env_file}...")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value
    print()

# Add the project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_gemini_setup():
    """Test Gemini API setup."""
    print("\n" + "="*60)
    print("Testing Gemini Setup")
    print("="*60)
    
    try:
        from tinytroupe.clients import GeminiClient
        from tinytroupe import config_manager
        
        # Check API key
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        if not api_key:
            print("[FAIL] GOOGLE_GEMINI_API_KEY not set in environment")
            return False
        
        print(f"[OK] API key found: {api_key[:20]}...")
        
        # Initialize client
        client = GeminiClient()
        print("[OK] GeminiClient initialized successfully")
        
        # Test a simple message
        test_messages = [
            {"role": "user", "content": "Say 'Hello from Gemini!' in one sentence."}
        ]
        
        print("\nTesting message send...")
        response = client.send_message(
            test_messages,
            model="models/gemini-2.5-flash",
            temperature=0.7,
            max_completion_tokens=100,
            max_attempts=2
        )
        
        if response:
            # Response is a dict with 'content' key
            content = response.get('content', str(response))
            preview = content[:100] if len(content) > 100 else content
            print(f"[OK] Response received: {preview}...")
            return True
        else:
            print("[FAIL] No response from Gemini API")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing Gemini: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_ollama_setup():
    """Test Ollama setup."""
    print("\n" + "="*60)
    print("Testing Ollama Setup")
    print("="*60)
    
    try:
        from tinytroupe.clients import OllamaClient
        from tinytroupe import config_manager
        
        # Check if Ollama is running
        import requests
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                print("[OK] Ollama server is running")
                models = response.json().get("models", [])
                print(f"  Available models: {[m.get('name') for m in models]}")
            else:
                print("[WARN] Ollama server responded but with unexpected status")
        except requests.exceptions.ConnectionError:
            print("[WARN] Ollama server not running at http://localhost:11434")
            print("  To use Ollama, start it with: ollama serve")
            print("  Then pull a model: ollama pull qwen3:8b")
            return None  # Not an error, just not available
        
        # Initialize client
        client = OllamaClient()
        print("[OK] OllamaClient initialized successfully")
        
        # Test a simple message
        test_messages = [
            {"role": "user", "content": "Say 'Hello from Ollama!' in one sentence."}
        ]
        
        print("\nTesting message send...")
        response = client.send_message(
            test_messages,
            model="qwen3:8b",
            temperature=0.7,
            max_attempts=2
        )
        
        if response:
            # Response is a dict with 'content' key
            content = response.get('content', str(response))
            preview = content[:100] if len(content) > 100 else content
            print(f"[OK] Response received: {preview}...")
            return True
        else:
            print("[FAIL] No response from Ollama")
            return False
            
    except Exception as e:
        print(f"[FAIL] Error testing Ollama: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config():
    """Test configuration."""
    print("\n" + "="*60)
    print("Testing Configuration")
    print("="*60)
    
    try:
        from tinytroupe import config_manager
        
        api_type = config_manager.get("api_type")
        model = config_manager.get("model")
        
        print(f"[OK] API Type: {api_type}")
        print(f"[OK] Model: {model}")
        print(f"[OK] Max Completion Tokens: {config_manager.get('max_completion_tokens')}")
        print(f"[OK] Timeout: {config_manager.get('timeout')}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Error testing config: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("TinyTroupe Market Simulation - Setup Verification")
    print("="*60)
    
    results = {}
    
    # Test configuration
    results["config"] = test_config()
    
    # Test Gemini
    results["gemini"] = test_gemini_setup()
    
    # Test Ollama
    results["ollama"] = test_ollama_setup()
    
    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)
    
    for test_name, result in results.items():
        if result is True:
            status = "[PASS]"
        elif result is False:
            status = "[FAIL]"
        else:
            status = "[SKIP]"
        print(f"{test_name.upper():15} {status}")
    
    # Check if at least one API is working
    if results.get("gemini") or results.get("ollama"):
        print("\n[OK] At least one API is configured and working!")
        print("\nYou can now run TinyTroupe examples:")
        print("  jupyter notebook examples/Interview\\ with\\ Customer.ipynb")
        print("  jupyter notebook examples/Product\\ Brainstorming.ipynb")
        return 0
    else:
        print("\n[FAIL] No working API found. Please configure Gemini or Ollama.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
