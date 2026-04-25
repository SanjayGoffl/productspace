## 2026-04-25 - Overly Permissive CORS Configuration
**Vulnerability:** FastAPI `CORSMiddleware` in `simulation_server.py` was using `allow_origins=["*"]`, allowing requests from any domain.
**Learning:** Hardcoded permissive CORS configurations are a common pattern in rapid prototyping that can easily slip into production. The application requires dynamic configuration based on environments.
**Prevention:** Always use environment variables (e.g., `ALLOWED_ORIGINS`) to configure CORS settings, with safe fallback defaults for local development (e.g., `http://localhost:8080`).
