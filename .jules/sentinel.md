## 2025-02-27 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI backend used `allow_origins=["*"]` in its `CORSMiddleware` configuration.
**Learning:** This is a wildcard CORS vulnerability that allows any domain to make cross-origin requests to the API. This can lead to unauthorized data access and CSRF attacks.
**Prevention:** Always restrict `allow_origins` to a specific list of trusted domains. Use environment variables (e.g. `ALLOWED_ORIGINS`) to easily manage different environments without hardcoding domains.
