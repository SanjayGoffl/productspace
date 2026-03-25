import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# The user might have named it GOOGLE_GEMINI_API_KEY or GOOGLE_GEMINI_API_KEY0
api_key = os.getenv("GOOGLE_GEMINI_API_KEY") or os.getenv("GOOGLE_GEMINI_API_KEY0") or os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: Could not find GOOGLE_GEMINI_API_KEY in .env file.")
    exit(1)

genai.configure(api_key=api_key)

try:
    print("Fetching available Gemini models...\n")
    models = genai.list_models()
    for m in models:
        # We generally only care about models that can generate content
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error accessing Gemini API: {e}")
