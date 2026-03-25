#!/usr/bin/env python3
"""
Wrapper script to load .env file and run test_market_setup.py
"""

import os
import sys
from pathlib import Path

# Load .env file
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    print(f"Loading environment from {env_file}")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value
                print(f"  Set {key}")
    print()
else:
    print(f"Warning: .env file not found at {env_file}")
    print()

# Now run the test
print("Running test_market_setup.py...")
print()

# Import and run the test
import test_market_setup
sys.exit(test_market_setup.main())
