## 2025-05-06 - CORS Misconfiguration

**Vulnerability:** The simulation server's API `simulation_server.py` had an overly permissive CORS setup where `allow_origins` was set to `["*"]`.
**Learning:** This is a common oversight during development but it leaves the API open to requests from any domain, making it vulnerable to unauthorized access and possibly CSRF attacks.
**Prevention:** Always use specific trusted domains (like localhost for development) and rely on configuration properties (like environment variables) to add valid production domains explicitly instead of utilizing wildcard tokens.
