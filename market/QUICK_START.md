# Quick Start - TinyTroupe Market Simulation

## 30-Second Setup

### Already Configured with Gemini ✓

Your project is **already set up** with Google Gemini API. Just run:

```bash
cd market/TinyTroupe
python test_market_setup.py
```

If you see ✓ PASS for Gemini, you're ready to go!

## Run Your First Simulation

```bash
cd market/TinyTroupe
jupyter notebook examples/Interview\ with\ Customer.ipynb
```

This will open a Jupyter notebook where you can:
- Interview a simulated customer
- Ask them about their needs
- Get realistic responses powered by Gemini

## Other Examples to Try

```bash
# Product brainstorming with a focus group
jupyter notebook examples/Product\ Brainstorming.ipynb

# Market research survey
jupyter notebook examples/Bottled\ Gazpacho\ Market\ Research\ 5.ipynb

# Advertisement evaluation
jupyter notebook examples/Advertisement\ for\ TV.ipynb
```

## Want to Use Ollama Instead?

If you want to run models locally without API keys:

1. **Install Ollama:** https://ollama.com
2. **Start Ollama:** `ollama serve`
3. **Pull model:** `ollama pull qwen3:8b`
4. **Edit config:**
   ```bash
   # Edit market/TinyTroupe/tinytroupe/config.ini
   # Change: API_TYPE=gemini
   # To:     API_TYPE=ollama
   ```
5. **Run test:** `python test_market_setup.py`

## Troubleshooting

**"GOOGLE_GEMINI_API_KEY not set"**
- The API key is already in `.env` file
- Make sure you're in the right directory

**"Module not found"**
- Install dependencies: `pip install -e .`

**"Connection error"**
- Check internet connection (Gemini needs it)
- Or switch to Ollama (local, no internet needed)

## What's Configured

✓ **Gemini API** - Cloud-based, fast, no setup needed
✓ **Ollama Support** - Local models, free, no API key needed
✓ **Config Files** - Everything pre-configured
✓ **Test Script** - Verify setup with one command

## Next Steps

1. Run `python test_market_setup.py` to verify
2. Open a Jupyter notebook example
3. Explore the simulation
4. Customize for your use case

See `MARKET_SETUP.md` for detailed configuration options.
