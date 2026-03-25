# How to Run the Test

## Quick Method (Recommended)

The test script now automatically loads the `.env` file. Just run:

```bash
python test_market_setup.py
```

## Alternative Methods

### Method 1: Using run_test.py wrapper
```bash
python run_test.py
```

### Method 2: Set environment variable manually (Windows CMD)
```cmd
set GOOGLE_GEMINI_API_KEY=<YOUR_API_KEY>
python test_market_setup.py
```

### Method 3: Set environment variable manually (Windows PowerShell)
```powershell
$env:GOOGLE_GEMINI_API_KEY="<YOUR_API_KEY>"
python test_market_setup.py
```

### Method 4: Set environment variable manually (Linux/Mac)
```bash
export GOOGLE_GEMINI_API_KEY=<YOUR_API_KEY>
python test_market_setup.py
```

## Expected Output

```
============================================================
TinyTroupe Market Simulation - Setup Verification
============================================================

Testing Configuration
✓ API Type: gemini
✓ Model: models/gemini-2.5-flash
✓ Max Completion Tokens: 128000
✓ Timeout: 240.0

Testing Gemini Setup
✓ API key found: AIzaSyAv4j2rwnB...
✓ GeminiClient initialized successfully
✓ Response received: Hello from Gemini!...

Testing Ollama Setup
⚠ Ollama server not running at http://localhost:11434

============================================================
Summary
============================================================
CONFIG           ✓ PASS
GEMINI           ✓ PASS
OLLAMA           ⚠ SKIPPED

✓ At least one API is configured and working!
```

## Troubleshooting

### "GOOGLE_GEMINI_API_KEY not found"
- Make sure `.env` file exists in the same directory
- Check that the API key line doesn't have extra spaces
- Try running with `python run_test.py` instead

### "Module not found"
- Install dependencies: `pip install -e .`

### "API key invalid"
- Verify your API key at https://ai.google.dev
- Make sure there are no extra spaces or quotes in the `.env` file

## What the Test Checks

1. **Configuration** - Verifies config.ini is properly set
2. **Gemini** - Tests connection to Google Gemini API
3. **Ollama** - Tests connection to local Ollama server (optional)

## Next Steps

Once the test passes:
1. Run examples: `jupyter notebook examples/Interview\ with\ Customer.ipynb`
2. Explore other examples in the `examples/` folder
3. Create your own simulations
