## 2024-03-24 - Missing Connection Pooling for Ollama Backend
**Learning:** The FastAPI `simulation_server.py` creates a new `httpx.AsyncClient` for each Ollama health check and inference request. When simulating 20 personas concurrently, this leads to unnecessary TCP handshake overhead and can quickly exhaust available local ephemeral ports when making many fast requests to a local service.
**Action:** Always instantiate a shared HTTP client (like `httpx.AsyncClient`) at the application/class level rather than creating new clients inside per-request functions to allow connection pooling.
