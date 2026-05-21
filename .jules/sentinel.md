## 2025-04-28 - Fix DOM XSS in index.html feature chips
**Vulnerability:** A direct DOM-based XSS existed in `index.html` where user input for product features was interpolated directly into `innerHTML` and inline `onclick` handler strings.
**Learning:** Browsers first decode HTML entities before parsing JavaScript in event handlers. Thus, inputs in `onclick="..."` attributes need to be first JS-escaped, and then HTML-escaped (`escapeHTML(escapeJSString(val))`) to prevent double-injection attacks where quotes break out of the JS string or out of the HTML attribute.
**Prevention:** Always use utility functions `escapeHTML` and `escapeJSString` to sanitize any user-controlled input before inserting it into the DOM via `innerHTML`, especially for inline event handlers.
