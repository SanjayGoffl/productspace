## 2026-05-19 - Secure CORS Configuration
**Vulnerability:** Overly permissive CORS configuration (`allow_origins=["*"]`) allowed any domain to make requests to the FastAPI application.
**Learning:** This could expose the simulation API to cross-site request forgery or unauthorized cross-origin data access.
**Prevention:** Use an environment variable to specify allowed origins, with a secure fallback default to explicit local development URLs rather than a wildcard.
