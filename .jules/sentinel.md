## 2024-05-24 - Overly Permissive CORS Configuration

**Vulnerability:** The FastAPI backend in `simulation_server.py` had a wildcard CORS configuration (`allow_origins=["*"]`), which allows any domain to make cross-origin requests to the application. This could expose sensitive endpoints to Cross-Site Request Forgery (CSRF) or allow malicious sites to interact with the backend API.

**Learning:** During rapid prototyping, particularly for simulation applications spanning a backend and a separate static frontend served on an arbitrary port, developers often use `allow_origins=["*"]` to quickly bypass CORS errors. This configuration frequently gets committed and leaks into production or shared environments.

**Prevention:** Ensure `CORSMiddleware` specifically targets the required frontend origin. Use environment variables (e.g., `ALLOWED_ORIGINS`) to easily manage origins across different environments, falling back to local development defaults (e.g., `http://localhost:8080`, `http://127.0.0.1:8080`) rather than a wildcard.
