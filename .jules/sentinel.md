## 2024-05-24 - Cross-Site Scripting (XSS) in Client-Side Templating

**Vulnerability:** XSS vulnerability found in `index.html` where user input and LLM responses were directly interpolated into DOM elements using `innerHTML` without sanitization.

**Learning:** It existed because there was no native escaping mechanism utilized when mapping data to HTML strings.

**Prevention:** Always use a utility function like `escapeHTML` to sanitize external or user-provided strings before inserting them into the DOM via `innerHTML` or similar properties. Avoid using `innerHTML` with untrusted data when possible.