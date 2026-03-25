# TinyTroupe Market Simulation Lab

Complete setup for running TinyTroupe market simulations with **Google Gemini** or **Ollama (Qwen3:8b)**.

## 🚀 Quick Start

Your project is **already configured** with Google Gemini. Just verify it works:

```bash
cd market/TinyTroupe
python test_market_setup.py
```

Then run a simulation:

```bash
jupyter notebook examples/Interview\ with\ Customer.ipynb
```

## 📋 What's Included

### ✓ Gemini API Support (Cloud-based)
- Fast, reliable, no setup needed
- API key already configured
- Ready to use immediately

### ✓ Ollama Support (Local)
- Run models locally (Qwen3:8b, Mistral, Llama2, etc.)
- No API key needed
- Free to use
- Optional - install if you want local inference

### ✓ Pre-configured
- All settings optimized for market simulation
- Easy switching between APIs
- Comprehensive documentation

## 📚 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Get running in 30 seconds
- **[MARKET_SETUP.md](MARKET_SETUP.md)** - Detailed setup guide
- **[CONFIG_REFERENCE.md](CONFIG_REFERENCE.md)** - Configuration options
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical details

## 🎯 Available Examples

### Interview with Customer
Simulate a business consultant interviewing a customer:
```bash
jupyter notebook examples/Interview\ with\ Customer.ipynb
```

### Product Brainstorming
Run a focus group brainstorming session:
```bash
jupyter notebook examples/Product\ Brainstorming.ipynb
```

### Market Research
Conduct market research surveys:
```bash
jupyter notebook examples/Bottled\ Gazpacho\ Market\ Research\ 5.ipynb
```

### Advertisement Evaluation
Evaluate ads with simulated audiences:
```bash
jupyter notebook examples/Advertisement\ for\ TV.ipynb
```

### And More
- AI-enabled Children Story Telling Market Research
- Travel Product Market Research
- Investment Firm Simulation
- Synthetic Data Generation
- Word Processor Tool Usage

## 🔧 Configuration

### Using Gemini (Default)
Already configured! Just run:
```bash
python test_market_setup.py
```

### Using Ollama (Local)
1. Install Ollama: https://ollama.com
2. Run: `ollama serve`
3. Pull model: `ollama pull qwen3:8b`
4. Edit `tinytroupe/config.ini`:
   ```ini
   API_TYPE=ollama
   ```
5. Test: `python test_market_setup.py`

### Using OpenAI (Legacy)
1. Edit `tinytroupe/config.ini`:
   ```ini
   API_TYPE=openai
   ```
2. Set API key:
   ```bash
   export OPENAI_API_KEY=your_key
   ```

## 📊 Performance

| Feature | Gemini | Ollama |
|---------|--------|--------|
| Speed | Fast (cloud) | Moderate (local) |
| Cost | ~$0.075/1M tokens | Free |
| Setup | 1 minute | 10 minutes |
| Internet | Required | Not required |
| Privacy | Cloud-based | Local |

## 🛠️ What Was Added

### New Files
- `tinytroupe/clients/gemini_client.py` - Gemini API client
- `test_market_setup.py` - Setup verification script
- `QUICK_START.md` - Quick start guide
- `MARKET_SETUP.md` - Detailed setup
- `CONFIG_REFERENCE.md` - Configuration reference
- `IMPLEMENTATION_SUMMARY.md` - Technical details
- `README.md` - This file

### Modified Files
- `tinytroupe/clients/__init__.py` - Registered Gemini client
- `tinytroupe/config.ini` - Added Gemini/Ollama config
- `.env` - Added Gemini API key

## ✅ Verification

Run the test script to verify everything:

```bash
cd market/TinyTroupe
python test_market_setup.py
```

Expected output:
```
✓ CONFIG           PASS
✓ GEMINI           PASS
⚠ OLLAMA           SKIPPED (not running)
```

## 🚨 Troubleshooting

### Gemini not working
- Check API key in `.env`
- Verify internet connection
- See [MARKET_SETUP.md](MARKET_SETUP.md#troubleshooting)

### Ollama not working
- Make sure Ollama is running: `ollama serve`
- Pull the model: `ollama pull qwen3:8b`
- See [MARKET_SETUP.md](MARKET_SETUP.md#troubleshooting)

### Import errors
- Install dependencies: `pip install -e .`
- Check Python version: `python --version` (need 3.10+)

## 📖 Learn More

- [TinyTroupe GitHub](https://github.com/microsoft/tinytroupe)
- [TinyTroupe Paper](https://arxiv.org/abs/2507.09788)
- [Google Gemini API](https://ai.google.dev)
- [Ollama](https://ollama.com)

## 🎓 Use Cases

- **Market Research** - Simulate customer surveys and focus groups
- **Product Development** - Get feedback from simulated personas
- **Advertisement Testing** - Evaluate ads before spending money
- **Training Data** - Generate synthetic data for ML models
- **Business Analysis** - Understand customer behavior patterns

## 📝 Next Steps

1. ✓ Verify setup: `python test_market_setup.py`
2. ✓ Run an example: `jupyter notebook examples/Interview\ with\ Customer.ipynb`
3. ✓ Explore other examples
4. ✓ Customize for your use case

## 💡 Tips

- **For speed:** Use Gemini (cloud-based)
- **For privacy:** Use Ollama (local)
- **For cost:** Use Ollama (free)
- **For quality:** Use Gemini Pro or larger Ollama models

## 📞 Support

- Check [MARKET_SETUP.md](MARKET_SETUP.md) for detailed troubleshooting
- Review [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) for configuration options
- See [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) for technical details

---

**Status:** ✓ Ready to Use

Your TinyTroupe market simulation is fully configured and ready to run!
