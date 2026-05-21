## 2024-05-10 - Overly Permissive CORS Configuration
**Vulnerability:** Found a wildcard CORS configuration (`allow_origins=["*"]`) in `simulation_server.py`.
**Learning:** Hardcoding wildcard origins in FastAPI applications exposes them to Cross-Origin Resource Sharing vulnerabilities, allowing malicious websites to make cross-origin requests.
**Prevention:** Use environment variables (e.g., `ALLOWED_ORIGINS`) to configure CORS, falling back to secure localhost defaults for development.
