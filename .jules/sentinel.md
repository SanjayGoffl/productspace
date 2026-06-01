## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-01 - [Unsanitized dynamic data in innerHTML]
**Vulnerability:** XSS vulnerability by rendering unescaped dynamic data
**Learning:** Third-party or LLM-generated data can contain malicious script tags if not sanitized before insertion into the DOM via innerHTML.
**Prevention:** Always use the `escapeHTML` function to sanitize dynamic variables (e.g., `c.name`, `c.domain`, `err.message`) before interpolating them into HTML strings.
