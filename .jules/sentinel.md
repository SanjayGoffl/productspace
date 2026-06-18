## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-18 - [Missing escapeHTML on LLM JSON Output]
**Vulnerability:** XSS vulnerability through lack of input sanitization on LLM output.
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends; fields such as `persona`, `emoji`, `quote`, or `product_chosen` must still be explicitly sanitized.
**Prevention:** Always use explicit `escapeHTML` sanitization before interpolating any dynamic content (including structured LLM outputs) into `innerHTML` or DOM attributes.
