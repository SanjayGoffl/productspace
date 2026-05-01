## 2024-05-01 - XSS via innerHTML rendering without sanitization
**Vulnerability:** User inputs and backend LLM responses are rendered directly using `innerHTML` across multiple locations in `index.html` (e.g., product features, competitor grids, chat messages). This allows an attacker to execute arbitrary JavaScript (XSS).
**Learning:** In purely vanilla JS/HTML frontends without frameworks like React that auto-escape, we must manually sanitize inputs before setting `innerHTML`. Memory instructed me to implement `escapeHTML` and `escapeJSString` but they were not present in the code.
**Prevention:** Always implement and use custom escaping functions or DOM element text properties (e.g. `textContent`) when dealing with user-generated or third-party (LLM) data in a vanilla JS setup.
