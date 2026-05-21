## 2024-05-24 - Overly Permissive CORS Configuration
**Vulnerability:** The FastAPI application was configured with `allow_origins=["*"]`, allowing any website to make cross-origin requests to the API.
**Learning:** This is a common misconfiguration that exposes the API to CSRF-like attacks and data exfiltration by malicious sites.
**Prevention:** Always restrict CORS origins to trusted domains using environment variables, with secure defaults (like localhost) for development.