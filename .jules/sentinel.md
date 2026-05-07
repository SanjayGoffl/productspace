## 2025-05-07 - Overly Permissive CORS Configuration

**Vulnerability:** The `simulation_server.py` FastAPI app used an overly permissive CORS configuration (`allow_origins=["*"]`), which allowed any website to make cross-origin requests to the API. This could lead to Cross-Site Request Forgery (CSRF) or unintended data exposure if users are authenticated or if the API is internal.
**Learning:** Hardcoding wildcard origins in a CORS configuration is an anti-pattern. Applications should read allowed origins from environment variables to securely adapt to different deployment environments.
**Prevention:** Avoid `allow_origins=["*"]` unless explicitly creating a public API that has no authentication. Instead, use an environment variable (e.g., `ALLOWED_ORIGINS`) to load permitted origins and fallback to safe defaults (like localhost) for development environments.
