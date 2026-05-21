
## 2026-04-23 - Cross-Site Scripting (XSS) Vulnerability in `index.html`

**Vulnerability:** Found widespread use of `innerHTML` assignments injecting unescaped user-provided and LLM-generated strings directly into the DOM across various phases (features, competitors, matrix, chat history, etc.).

**Learning:** The application heavily relies on dynamic DOM updates via string interpolation into `innerHTML`, but lacked centralized or local HTML escaping mechanisms, leading to potential arbitrary JavaScript execution if malicious input were processed.

**Prevention:** To avoid this next time, always enforce robust escaping on strings prior to using `innerHTML`. Global utility functions like `escapeHTML` and `escapeJSString` should be used consistently. For inline event handlers, double-escaping (`escapeHTML(escapeJSString(val))`) is necessary to prevent breakout from quotes and HTML tags.
