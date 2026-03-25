# Verification Checklist

Use this checklist to verify that everything is properly configured.

## ✓ Installation & Setup

- [ ] Python 3.10+ installed
  ```bash
  python --version
  ```

- [ ] TinyTroupe installed
  ```bash
  cd market/TinyTroupe
  pip install -e .
  ```

- [ ] Dependencies installed
  ```bash
  pip list | grep -E "google-generativeai|ollama|requests"
  ```

## ✓ Gemini Configuration

- [ ] `.env` file exists
  ```bash
  ls -la market/TinyTroupe/.env
  ```

- [ ] API key is set
  ```bash
  grep GOOGLE_GEMINI_API_KEY market/TinyTroupe/.env
  ```

- [ ] API key is valid (not just "....") 
  ```bash
  cat market/TinyTroupe/.env | grep GOOGLE_GEMINI_API_KEY
  ```

- [ ] `config.ini` has Gemini as default
  ```bash
  grep "API_TYPE=gemini" market/TinyTroupe/tinytroupe/config.ini
  ```

- [ ] Gemini client file exists
  ```bash
  ls -la market/TinyTroupe/tinytroupe/clients/gemini_client.py
  ```

- [ ] Gemini client is registered
  ```bash
  grep "register_client.*gemini" market/TinyTroupe/tinytroupe/clients/__init__.py
  ```

## ✓ Ollama Configuration (Optional)

- [ ] Ollama installed (if using local models)
  ```bash
  ollama --version
  ```

- [ ] Ollama server running
  ```bash
  curl http://localhost:11434/api/tags
  ```

- [ ] Qwen3:8b model pulled
  ```bash
  ollama list | grep qwen3
  ```

- [ ] Ollama config in `config.ini`
  ```bash
  grep -A 3 "\[Ollama\]" market/TinyTroupe/tinytroupe/config.ini
  ```

## ✓ Test Verification

- [ ] Test script exists
  ```bash
  ls -la market/TinyTroupe/test_market_setup.py
  ```

- [ ] Test script runs without errors
  ```bash
  cd market/TinyTroupe
  python test_market_setup.py
  ```

- [ ] Configuration test passes
  ```
  CONFIG           ✓ PASS
  ```

- [ ] Gemini test passes
  ```
  GEMINI           ✓ PASS
  ```

- [ ] At least one API is working
  ```
  ✓ At least one API is configured and working!
  ```

## ✓ Documentation

- [ ] README.md exists
  ```bash
  ls -la market/README.md
  ```

- [ ] QUICK_START.md exists
  ```bash
  ls -la market/QUICK_START.md
  ```

- [ ] MARKET_SETUP.md exists
  ```bash
  ls -la market/MARKET_SETUP.md
  ```

- [ ] CONFIG_REFERENCE.md exists
  ```bash
  ls -la market/CONFIG_REFERENCE.md
  ```

- [ ] IMPLEMENTATION_SUMMARY.md exists
  ```bash
  ls -la market/IMPLEMENTATION_SUMMARY.md
  ```

## ✓ Examples

- [ ] Examples folder exists
  ```bash
  ls -la market/TinyTroupe/examples/
  ```

- [ ] Interview example exists
  ```bash
  ls -la market/TinyTroupe/examples/Interview\ with\ Customer.ipynb
  ```

- [ ] Product Brainstorming example exists
  ```bash
  ls -la market/TinyTroupe/examples/Product\ Brainstorming.ipynb
  ```

- [ ] Market Research example exists
  ```bash
  ls -la market/TinyTroupe/examples/Bottled\ Gazpacho\ Market\ Research\ 5.ipynb
  ```

## ✓ Functionality Tests

### Test 1: Import Gemini Client
```bash
cd market/TinyTroupe
python -c "from tinytroupe.clients import GeminiClient; print('✓ GeminiClient imported')"
```
Expected: `✓ GeminiClient imported`

### Test 2: Get Client
```bash
python -c "from tinytroupe.clients import client; c = client(); print(f'✓ Client type: {type(c).__name__}')"
```
Expected: `✓ Client type: GeminiClient`

### Test 3: Config Values
```bash
python -c "from tinytroupe import config_manager; print(f'API Type: {config_manager.get(\"api_type\")}'); print(f'Model: {config_manager.get(\"model\")}')"
```
Expected:
```
API Type: gemini
Model: models/gemini-2.5-flash
```

### Test 4: Run Full Test Suite
```bash
cd market/TinyTroupe
python test_market_setup.py
```
Expected: All tests pass or skip appropriately

## ✓ Jupyter Notebook Test

- [ ] Jupyter installed
  ```bash
  jupyter --version
  ```

- [ ] Can start Jupyter
  ```bash
  cd market/TinyTroupe
  jupyter notebook --version
  ```

- [ ] Can open example notebook
  ```bash
  jupyter notebook examples/Interview\ with\ Customer.ipynb
  ```

## ✓ API Connectivity

### Gemini
- [ ] Internet connection available
  ```bash
  ping -c 1 8.8.8.8
  ```

- [ ] Can reach Gemini API
  ```bash
  curl -s https://generativelanguage.googleapis.com/v1beta/models?key=test | head -c 100
  ```

- [ ] API key is valid (test in notebook)

### Ollama (if using)
- [ ] Ollama server is running
  ```bash
  curl http://localhost:11434/api/tags
  ```

- [ ] Model is available
  ```bash
  ollama list
  ```

## ✓ File Structure

```
market/
├── README.md                          ✓
├── QUICK_START.md                     ✓
├── MARKET_SETUP.md                    ✓
├── CONFIG_REFERENCE.md                ✓
├── IMPLEMENTATION_SUMMARY.md          ✓
├── VERIFICATION_CHECKLIST.md          ✓
└── TinyTroupe/
    ├── .env                           ✓ (with API key)
    ├── tinytroupe/
    │   ├── clients/
    │   │   ├── __init__.py            ✓ (Gemini registered)
    │   │   ├── gemini_client.py       ✓ (NEW)
    │   │   ├── openai_client.py       ✓
    │   │   ├── azure_client.py        ✓
    │   │   └── ollama_client.py       ✓
    │   ├── config.ini                 ✓ (Gemini default)
    │   └── ...
    ├── test_market_setup.py           ✓ (NEW)
    ├── examples/
    │   ├── Interview with Customer.ipynb
    │   ├── Product Brainstorming.ipynb
    │   └── ...
    └── ...
```

## ✓ Quick Verification Command

Run this single command to verify everything:

```bash
cd market/TinyTroupe && \
echo "=== Python Version ===" && python --version && \
echo "=== Gemini Client ===" && python -c "from tinytroupe.clients import GeminiClient; print('✓ Imported')" && \
echo "=== Config ===" && python -c "from tinytroupe import config_manager; print(f'API: {config_manager.get(\"api_type\")}'); print(f'Model: {config_manager.get(\"model\")}')" && \
echo "=== Test Script ===" && python test_market_setup.py
```

## ✓ Troubleshooting

If any check fails, see:
- [QUICK_START.md](QUICK_START.md) - Quick fixes
- [MARKET_SETUP.md](MARKET_SETUP.md#troubleshooting) - Detailed troubleshooting
- [CONFIG_REFERENCE.md](CONFIG_REFERENCE.md) - Configuration help

## ✓ Success Criteria

All of the following should be true:

1. ✓ Python 3.10+ installed
2. ✓ TinyTroupe installed with `pip install -e .`
3. ✓ Gemini API key in `.env` file
4. ✓ `config.ini` has `API_TYPE=gemini`
5. ✓ `test_market_setup.py` shows ✓ PASS for Gemini
6. ✓ Can import `GeminiClient`
7. ✓ Can run `jupyter notebook`
8. ✓ Can open and run example notebooks

## ✓ Next Steps

Once all checks pass:

1. Run: `python test_market_setup.py`
2. Open: `jupyter notebook examples/Interview\ with\ Customer.ipynb`
3. Explore: Try other examples
4. Customize: Create your own simulations

---

**Last Updated:** 2026-03-01
**Status:** Ready for Use ✓
