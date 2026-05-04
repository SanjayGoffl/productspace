## 2024-05-04 - Overly Permissive CORS Configuration
**Vulnerability:** Found `allow_origins=["*"]` wildcard setting in `CORSMiddleware` configuration in `simulation_server.py`.
**Learning:** This wildcard CORS setting allows any origin to request resources from the API, which can lead to cross-origin data exposure or misuse of endpoints. A secure implementation should restrict `allow_origins` strictly to trusted domains.
**Prevention:** Configured `allow_origins` to parse the `ALLOWED_ORIGINS` environment variable, falling back to local development URLs (`http://localhost:8080`, `http://127.0.0.1:8080`), ensuring no wildcard CORS vulnerabilities exist in production.
