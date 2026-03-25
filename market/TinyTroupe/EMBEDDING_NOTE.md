# Embedding Model Configuration Note

## Important: LlamaIndex Compatibility

TinyTroupe uses LlamaIndex for some internal operations, which currently only supports OpenAI embedding models. This means:

### Current Configuration
```ini
# In config.ini
API_TYPE=gemini                          # ✓ Uses Gemini for chat/generation
MODEL=models/gemini-2.5-flash           # ✓ Uses Gemini for responses
REASONING_MODEL=models/gemini-3.1-pro-preview  # ✓ Uses Gemini for reasoning
EMBEDDING_MODEL=text-embedding-3-small  # ⚠ Uses OpenAI for embeddings
```

### Why This Matters

- **Chat/Generation:** Uses Gemini (your configured API)
- **Embeddings:** Uses OpenAI (required by LlamaIndex)

This means you need **both** API keys if you want to use features that require embeddings:
- `GOOGLE_GEMINI_API_KEY` - For chat and generation (main functionality)
- `OPENAI_API_KEY` - For embeddings (used by LlamaIndex internally)

### What Works Without OpenAI Key

Most TinyTroupe features work fine with just Gemini:
- ✓ Agent conversations
- ✓ Simulations
- ✓ Market research
- ✓ Product brainstorming
- ✓ Advertisement evaluation
- ✓ Customer interviews

### What Requires OpenAI Key

Only advanced features that use LlamaIndex embeddings:
- Semantic memory retrieval (if enabled)
- Document similarity search
- Some advanced cognitive features

### Solutions

#### Option 1: Use Gemini Only (Recommended for Most Users)
Just use Gemini. Most examples work fine without embeddings.

```ini
API_TYPE=gemini
MODEL=models/gemini-2.5-flash
EMBEDDING_MODEL=text-embedding-3-small  # Won't be used unless needed
```

Only set `OPENAI_API_KEY` if you encounter errors about embeddings.

#### Option 2: Add OpenAI Key for Full Features
If you need embedding features:

1. Get an OpenAI API key from https://platform.openai.com
2. Add to `.env`:
   ```
   GOOGLE_GEMINI_API_KEY=your_gemini_key
   OPENAI_API_KEY=your_openai_key
   ```

#### Option 3: Use OpenAI for Everything
If you prefer to use OpenAI for all operations:

```ini
API_TYPE=openai
MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
```

Then only set `OPENAI_API_KEY` in `.env`.

#### Option 4: Use Ollama (Local, Free)
For completely free local operation:

```ini
API_TYPE=ollama
MODEL=qwen3:8b
EMBEDDING_MODEL=text-embedding-3-small  # Won't be used
```

No API keys needed, but you need to run Ollama locally.

### Current Setup

Your current setup uses:
- **Gemini** for chat/generation (fast, cloud-based)
- **OpenAI embedding model name** for LlamaIndex compatibility (but won't actually call OpenAI unless needed)

This is the best configuration for most users - you get Gemini's speed and quality, and only need one API key.

### Future

The TinyTroupe team may add support for other embedding providers in the future. For now, this is the recommended configuration.

## Summary

- ✓ **Gemini works great** for 95% of TinyTroupe features
- ✓ **No OpenAI key needed** for most examples
- ⚠ **OpenAI key optional** for advanced embedding features
- ✓ **Current config is optimal** for Gemini-only usage

Just run the examples and enjoy! Only add an OpenAI key if you see embedding-related errors.
