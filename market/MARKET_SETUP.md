# TinyTroupe Market Simulation - Setup Guide

This guide explains how to set up and run the TinyTroupe market simulation with either **Google Gemini** or **Ollama (Qwen3:8b)**.

## Quick Start

### Option 1: Using Google Gemini (Recommended - Cloud-based)

**Prerequisites:**
- Python 3.10+
- Google Gemini API key

**Setup:**

1. **Install dependencies:**
   ```bash
   cd market/TinyTroupe
   pip install -e .
   ```

2. **Configure API key:**
   - Edit `market/TinyTroupe/.env` and add your Gemini API key:
     ```
     GOOGLE_GEMINI_API_KEY=your_actual_api_key_here
     ```
   - Or set it as an environment variable:
     ```bash
     export GOOGLE_GEMINI_API_KEY=your_actual_api_key_here
     ```

3. **Verify setup:**
   ```bash
   cd market/TinyTroupe
   python test_market_setup.py
   ```

4. **Run examples:**
   ```bash
   jupyter notebook examples/Interview\ with\ Customer.ipynb
   ```

---

### Option 2: Using Ollama with Qwen3:8b (Local - No API Key Needed)

**Prerequisites:**
- Python 3.10+
- Ollama installed ([download here](https://ollama.com))
- ~8GB RAM for Qwen3:8b model

**Setup:**

1. **Install Ollama:**
   - Download from https://ollama.com
   - Install and start the Ollama service

2. **Pull the Qwen3:8b model:**
   ```bash
   ollama pull qwen3:8b
   ```

3. **Start Ollama server:**
   ```bash
   ollama serve
   ```
   (This runs on `http://localhost:11434` by default)

4. **In a new terminal, install TinyTroupe:**
   ```bash
   cd market/TinyTroupe
   pip install -e .
   ```

5. **Configure for Ollama:**
   - Edit `market/TinyTroupe/tinytroupe/config.ini` and change:
     ```ini
     [OpenAI]
     API_TYPE=ollama
     ```
   - Or edit `.env` and set:
     ```
     OLLAMA_BASE_URL=http://localhost:11434/v1
     OLLAMA_MODEL=qwen3:8b
     ```

6. **Verify setup:**
   ```bash
   cd market/TinyTroupe
   python test_market_setup.py
   ```

7. **Run examples:**
   ```bash
   jupyter notebook examples/Interview\ with\ Customer.ipynb
   ```

---

## Configuration Files

### `.env` File
Located at `market/TinyTroupe/.env`

```dotenv
# For Gemini (Cloud)
GOOGLE_GEMINI_API_KEY=your_key_here

# For Ollama (Local)
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:8b
```

### `config.ini` File
Located at `market/TinyTroupe/tinytroupe/config.ini`

**Key settings:**
```ini
[OpenAI]
# Choose: openai, azure, gemini, or ollama
API_TYPE=gemini

# Model to use
MODEL=models/gemini-2.5-flash

# For Ollama, use:
# API_TYPE=ollama
# MODEL=qwen3:8b
```

---

## Switching Between APIs

### Switch to Gemini:
```bash
# Edit config.ini
API_TYPE=gemini
MODEL=models/gemini-2.5-flash
```

### Switch to Ollama:
```bash
# Edit config.ini
API_TYPE=ollama
MODEL=qwen3:8b

# Make sure Ollama is running:
ollama serve
```

### Switch to OpenAI:
```bash
# Edit config.ini
API_TYPE=openai
MODEL=gpt-4o-mini

# Set environment variable:
export OPENAI_API_KEY=your_key_here
```

---

## Troubleshooting

### Gemini Issues

**Error: "GOOGLE_GEMINI_API_KEY not set"**
- Make sure you've set the API key in `.env` or as an environment variable
- Restart your terminal/IDE after setting the variable

**Error: "Invalid API key"**
- Verify your API key is correct
- Check that you're using the right key from Google AI Studio

**Error: "Rate limit exceeded"**
- Gemini has rate limits. Wait a few seconds and try again
- The library will automatically retry with exponential backoff

### Ollama Issues

**Error: "Connection refused" or "Cannot connect to Ollama"**
- Make sure Ollama is running: `ollama serve`
- Check that it's running on `http://localhost:11434`

**Error: "Model not found: qwen3:8b"**
- Pull the model: `ollama pull qwen3:8b`
- Wait for the download to complete

**Slow responses**
- Qwen3:8b requires significant compute
- Ensure you have enough RAM (8GB minimum)
- Consider using a smaller model like `qwen2:7b` or `mistral:7b`

**Out of memory**
- Reduce model size: `ollama pull qwen2:7b`
- Or use Gemini (cloud-based, no local resources needed)

---

## Available Models

### Gemini Models
- `models/gemini-2.5-flash` - Fast, good for most tasks
- `models/gemini-2.5-pro` - More capable, slower
- `models/gemini-3.1-pro-preview` - Latest, best reasoning

### Ollama Models
- `qwen3:8b` - Recommended (8B parameters)
- `qwen2:7b` - Smaller, faster
- `mistral:7b` - Good general purpose
- `llama2:7b` - Popular open model
- `neural-chat:7b` - Optimized for chat

To use a different model:
```bash
# Pull the model
ollama pull mistral:7b

# Update config.ini
MODEL=mistral:7b
```

---

## Running Examples

### Interview with Customer
```bash
jupyter notebook examples/Interview\ with\ Customer.ipynb
```

### Product Brainstorming
```bash
jupyter notebook examples/Product\ Brainstorming.ipynb
```

### Market Research
```bash
jupyter notebook examples/Bottled\ Gazpacho\ Market\ Research\ 5.ipynb
```

### Advertisement Evaluation
```bash
jupyter notebook examples/Advertisement\ for\ TV.ipynb
```

---

## Performance Tips

### For Gemini:
- Use `models/gemini-2.5-flash` for speed
- Set `CACHE_API_CALLS=True` in config.ini to cache responses
- Reduce `MAX_COMPLETION_TOKENS` if not needed

### For Ollama:
- Use smaller models (7B) for faster responses
- Ensure GPU acceleration is enabled if available
- Run on a machine with at least 8GB RAM
- Consider using `qwen2:7b` instead of `qwen3:8b` for speed

---

## Cost Considerations

### Gemini
- Free tier available with rate limits
- Paid tier: ~$0.075 per 1M input tokens, ~$0.30 per 1M output tokens
- See [Google AI Pricing](https://ai.google.dev/pricing)

### Ollama
- Completely free (runs locally)
- Only costs: electricity and disk space for model storage
- Qwen3:8b requires ~16GB disk space

---

## Next Steps

1. **Verify setup:** Run `python test_market_setup.py`
2. **Run an example:** Start with `Interview with Customer.ipynb`
3. **Explore:** Check out other notebooks in the `examples/` folder
4. **Customize:** Create your own market simulation scenarios

---

## Support

For issues or questions:
- Check the [TinyTroupe GitHub](https://github.com/microsoft/tinytroupe)
- Review the [TinyTroupe Documentation](https://github.com/microsoft/tinytroupe/tree/main/docs)
- Check Ollama docs: https://ollama.com
- Check Gemini docs: https://ai.google.dev

---

## Architecture

The setup includes:

- **GeminiClient** (`tinytroupe/clients/gemini_client.py`) - New client for Gemini API
- **OllamaClient** (`tinytroupe/clients/ollama_client.py`) - Existing client for local models
- **OpenAIClient** (`tinytroupe/clients/openai_client.py`) - Original OpenAI client
- **AzureClient** (`tinytroupe/clients/azure_client.py`) - Azure OpenAI client

All clients implement the same interface, so you can switch between them by changing `API_TYPE` in config.ini.
