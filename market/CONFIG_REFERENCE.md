# Configuration Reference

## API Type Selection

### In `tinytroupe/config.ini`

```ini
[OpenAI]
API_TYPE=gemini  # Options: openai, azure, gemini, ollama
```

## Gemini Configuration

### Environment Variables (`.env`)
```dotenv
GOOGLE_GEMINI_API_KEY=your_api_key_here
```

### Config File (`config.ini`)
```ini
[OpenAI]
API_TYPE=gemini
MODEL=models/gemini-2.5-flash
REASONING_MODEL=models/gemini-3.1-pro-preview
EMBEDDING_MODEL=models/text-embedding-004
```

### Available Gemini Models
- `models/gemini-2.5-flash` - Fast, recommended for most tasks
- `models/gemini-2.5-pro` - More capable, slower
- `models/gemini-3.1-pro-preview` - Latest, best reasoning

### Gemini Parameters
```ini
MAX_COMPLETION_TOKENS=128000  # Max output tokens
TIMEOUT=480                    # Request timeout in seconds
MAX_ATTEMPTS=5                 # Retry attempts
WAITING_TIME=1                 # Wait between retries (seconds)
EXPONENTIAL_BACKOFF_FACTOR=5   # Backoff multiplier
```

## Ollama Configuration

### Environment Variables (`.env`)
```dotenv
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:8b
```

### Config File (`config.ini`)
```ini
[OpenAI]
API_TYPE=ollama
MODEL=qwen3:8b

[Ollama]
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:8b
OLLAMA_TIMEOUT=300
```

### Available Ollama Models
- `qwen3:8b` - Recommended (8B parameters)
- `qwen2:7b` - Smaller, faster
- `mistral:7b` - Good general purpose
- `llama2:7b` - Popular open model
- `neural-chat:7b` - Optimized for chat

### Ollama Parameters
```ini
OLLAMA_TIMEOUT=300  # Request timeout in seconds
```

## OpenAI Configuration (Legacy)

### Environment Variables (`.env`)
```dotenv
OPENAI_API_KEY=your_api_key_here
```

### Config File (`config.ini`)
```ini
[OpenAI]
API_TYPE=openai
MODEL=gpt-4o-mini
```

## Azure OpenAI Configuration (Legacy)

### Environment Variables (`.env`)
```dotenv
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
```

### Config File (`config.ini`)
```ini
[OpenAI]
API_TYPE=azure
AZURE_API_VERSION=2024-12-01-preview
```

## Common Parameters (All APIs)

```ini
[OpenAI]
# Model parameters
MAX_COMPLETION_TOKENS=128000  # Maximum tokens to generate
TIMEOUT=480                    # Request timeout (seconds)
MAX_ATTEMPTS=5                 # Number of retry attempts
WAITING_TIME=1                 # Initial wait between retries (seconds)
EXPONENTIAL_BACKOFF_FACTOR=5   # Backoff multiplier for retries

# Concurrency
MAX_CONCURRENT_MODEL_CALLS=4   # Max parallel API calls (0 = unlimited)

# Caching
CACHE_API_CALLS=False          # Cache API responses
CACHE_FILE_NAME=openai_api_cache.pickle  # Cache file name

# Other
MAX_CONTENT_DISPLAY_LENGTH=4000  # Max chars to display in logs
```

## Simulation Parameters

```ini
[Simulation]
PARALLEL_AGENT_GENERATION=True  # Generate agents in parallel
PARALLEL_AGENT_ACTIONS=True     # Run agent actions in parallel

# Responsible AI
RAI_HARMFUL_CONTENT_PREVENTION=True
RAI_COPYRIGHT_INFRINGEMENT_PREVENTION=True
```

## Cognition Parameters

```ini
[Cognition]
ENABLE_MEMORY_CONSOLIDATION=True
ENABLE_CONTINUOUS_CONTEXTUAL_SEMANTIC_MEMORY_RETRIEVAL=True

MIN_EPISODE_LENGTH=10
MAX_EPISODE_LENGTH=15

EPISODIC_MEMORY_FIXED_PREFIX_LENGTH=10
EPISODIC_MEMORY_LOOKBACK_LENGTH=20
```

## Action Generator Parameters

```ini
[ActionGenerator]
MAX_ATTEMPTS=2

# Quality checks
ENABLE_QUALITY_CHECKS=False
ENABLE_REGENERATION=True
ENABLE_DIRECT_CORRECTION=False

ENABLE_QUALITY_CHECK_FOR_PERSONA_ADHERENCE=True
ENABLE_QUALITY_CHECK_FOR_SELFCONSISTENCY=False
ENABLE_QUALITY_CHECK_FOR_FLUENCY=False
ENABLE_QUALITY_CHECK_FOR_SUITABILITY=False
ENABLE_QUALITY_CHECK_FOR_SIMILARITY=False

CONTINUE_ON_FAILURE=True
QUALITY_THRESHOLD=5  # 0-9 scale
```

## Logging Configuration

```ini
[Logging]
# Default log level
LOGLEVEL=ERROR

# Per-target overrides
LOGLEVEL_CONSOLE=INFO
LOGLEVEL_FILE=DEBUG

# Include thread IDs in logs
LOG_INCLUDE_THREAD_ID=True
```

## How Configuration is Loaded

1. **Default values** in code
2. **`config.ini`** file (overrides defaults)
3. **Environment variables** (overrides config.ini)
4. **Function parameters** (overrides everything)

## Switching APIs

### From Gemini to Ollama
```bash
# 1. Edit config.ini
API_TYPE=ollama

# 2. Make sure Ollama is running
ollama serve

# 3. Test
python test_market_setup.py
```

### From Ollama to Gemini
```bash
# 1. Edit config.ini
API_TYPE=gemini

# 2. Test
python test_market_setup.py
```

### From Gemini to OpenAI
```bash
# 1. Edit config.ini
API_TYPE=openai

# 2. Set API key
export OPENAI_API_KEY=your_key

# 3. Test
python test_market_setup.py
```

## Performance Tuning

### For Speed (Gemini)
```ini
MODEL=models/gemini-2.5-flash
MAX_COMPLETION_TOKENS=1000  # Reduce if not needed
CACHE_API_CALLS=True        # Cache responses
MAX_CONCURRENT_MODEL_CALLS=8  # Increase parallelism
```

### For Quality (Gemini)
```ini
MODEL=models/gemini-2.5-pro
MAX_COMPLETION_TOKENS=128000
REASONING_EFFORT=high
```

### For Speed (Ollama)
```ini
OLLAMA_MODEL=qwen2:7b  # Smaller model
MAX_COMPLETION_TOKENS=1000
MAX_CONCURRENT_MODEL_CALLS=4
```

### For Quality (Ollama)
```ini
OLLAMA_MODEL=qwen3:8b  # Larger model
MAX_COMPLETION_TOKENS=4000
```

## Debugging

### Enable Debug Logging
```ini
[Logging]
LOGLEVEL=DEBUG
LOGLEVEL_CONSOLE=DEBUG
LOGLEVEL_FILE=DEBUG
```

### Disable Caching (for testing)
```ini
CACHE_API_CALLS=False
```

### Reduce Concurrency (for stability)
```ini
MAX_CONCURRENT_MODEL_CALLS=1
```

## Cost Optimization

### Gemini
- Use `gemini-2.5-flash` (cheaper than pro)
- Enable caching: `CACHE_API_CALLS=True`
- Reduce `MAX_COMPLETION_TOKENS` if possible
- Monitor usage at https://ai.google.dev/pricing

### Ollama
- No API costs (local)
- Use smaller models for speed: `qwen2:7b`
- Larger models for quality: `qwen3:8b`

## Troubleshooting Configuration

### "API type not supported"
- Check `API_TYPE` value in config.ini
- Valid values: openai, azure, gemini, ollama

### "Model not found"
- Verify model name is correct
- For Ollama: run `ollama pull model_name`
- For Gemini: check available models in docs

### "API key not set"
- Check `.env` file for correct key name
- Verify environment variable is exported
- Restart terminal/IDE after setting

### "Connection timeout"
- Increase `TIMEOUT` value
- Check internet connection (for cloud APIs)
- Check Ollama is running (for local)

## File Locations

- **Config file:** `market/TinyTroupe/tinytroupe/config.ini`
- **Environment file:** `market/TinyTroupe/.env`
- **Cache file:** `market/TinyTroupe/openai_api_cache.pickle` (or custom name)
- **Log file:** `market/TinyTroupe/tinytroupe.<timestamp>.log`

## See Also

- `QUICK_START.md` - Get started in 30 seconds
- `MARKET_SETUP.md` - Detailed setup guide
- `IMPLEMENTATION_SUMMARY.md` - Technical details
