## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2025-02-24 - [Avoid `escapeHTML` on explicit DOM properties]
**Vulnerability:** Not a direct vulnerability, but a bug that could be introduced when trying to sanitize DOM property values using `escapeHTML`.
**Learning:** When generating HTML dynamically via string interpolation (e.g., `innerHTML`), attributes derived from untrusted sources must be sanitized using `escapeHTML`. However, direct assignment to DOM object properties (e.g., `element.id = ...`, `element.className = ...`) is inherently safe from XSS and should not use `escapeHTML`, as it is redundant and can introduce bugs (such as parsing ID's with special characters incorrectly).
**Prevention:** Only use `escapeHTML` for template literals that are directly injected into the DOM as innerHTML, not for explicitly assigned properties on created DOM elements.
