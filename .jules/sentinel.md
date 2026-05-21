## 2024-05-24 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI backend used a wildcard `allow_origins=["*"]` in its `CORSMiddleware` configuration.
**Learning:** Hardcoded wildcard CORS allows any domain to make cross-origin requests to the API, potentially leading to unauthorized data access or CSRF-like attacks if the API uses cookie-based authentication or if the endpoints are sensitive.
**Prevention:** Always configure `allow_origins` securely. Use environment variables (like `ALLOWED_ORIGINS`) to define allowed domains per environment (dev, staging, prod), and provide safe default fallbacks (e.g., `localhost` ports) if the environment variable is not set. Never use `*` in production for endpoints handling sensitive data.
