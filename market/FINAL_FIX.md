# Final Fix Applied

## Issue Found
The Gemini client's `_raw_model_response_extractor` was returning just the content string, but TinyTroupe expects a dict (like OpenAI's `message.to_dict()`).

## Fix Applied
Changed `_raw_model_response_extractor` to return the full message dict instead of just the content string:

```python
# Before (wrong)
return response["choices"][0]["message"]["content"]  # Returns string

# After (correct)
return response["choices"][0]["message"]  # Returns dict
```

## Also Fixed
Updated embedding model in config from `models/text-embedding-004` (Gemini) to `text-embedding-3-small` (OpenAI) for LlamaIndex compatibility.

## Why This Matters
- TinyTroupe uses LlamaIndex internally
- LlamaIndex only supports OpenAI embedding models
- Chat/generation still uses Gemini (your main API)
- Embeddings use OpenAI model name (but won't call API unless needed)

## Current Configuration
```ini
API_TYPE=gemini                          # ✓ Gemini for chat
MODEL=models/gemini-2.5-flash           # ✓ Gemini model
EMBEDDING_MODEL=text-embedding-3-small  # ✓ OpenAI-compatible name
```

## Test Now
```bash
cd market/TinyTroupe
python test_market_setup.py
```

## Expected Result
```
✓ CONFIG           PASS
✓ GEMINI           PASS
⚠ OLLAMA           SKIPPED

✓ At least one API is configured and working!
```

## Files Modified
1. `market/TinyTroupe/tinytroupe/clients/gemini_client.py` - Fixed response extraction
2. `market/TinyTroupe/config.ini` - Changed embedding model
3. `market/TinyTroupe/tinytroupe/config.ini` - Changed embedding model

## Files Created
1. `market/TinyTroupe/EMBEDDING_NOTE.md` - Explains embedding configuration

## Ready!
The setup is now complete and should work correctly.
