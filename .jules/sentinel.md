## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2025-02-24 - [Fix XSS in index.html]
**Vulnerability:** XSS vulnerability via unsanitized strings injected directly into innerHTML.
**Learning:** Even internal API responses and simulated LLM output in UI elements can contain malicious script payloads if not sanitized. Specifically strings interpolating dynamically loaded competitor data and simulated multi-agent outputs.
**Prevention:** Always use the `escapeHTML` function when dynamically inserting object properties into DOM element innerHTML properties.
