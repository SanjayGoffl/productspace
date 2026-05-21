## 2025-04-15 - FastAPI CORS Configuration
**Vulnerability:** The FastAPI `CORSMiddleware` was using `allow_origins=["*"]`, which allowed cross-origin requests from any domain, exposing the API to potential attacks.
**Learning:** `simulation_server.py` was overly permissive. While fine for local testing, this is a severe vulnerability in production environments or if the API is exposed to the internet.
**Prevention:** Use an environment variable like `ALLOWED_ORIGINS` to configure allowed origins dynamically, with safe defaults for local development (e.g. `http://localhost:8080`, `http://127.0.0.1:8080`).
