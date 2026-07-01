## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2026-07-01 - [XSS Fix: Unescaped string interpolation in index.html]
**Vulnerability:** XSS vulnerability through unescaped user and LLM-generated data injected into `innerHTML`
**Learning:** Even when using a templating string in client-side code, any interpolated variable derived from untrusted sources (like LLMs or user input) must be sanitized before being used in `innerHTML`.
**Prevention:** Always use `escapeHTML` (with fallback logic inside the function call, e.g., `escapeHTML(var || 'default')`) when dynamically rendering text to the DOM via `innerHTML`.
