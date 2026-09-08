## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2025-09-08 - [LLM Output Sanitization]
**Vulnerability:** XSS vulnerability through lack of input sanitization for LLM-generated content and external scraped content
**Learning:** Relying purely on JSON structure parsing does not prevent malicious script injections when those fields are eventually inserted into the DOM using innerHTML. Dynamic data returned from LLMs must still be sanitized.
**Prevention:** Always use `escapeHTML` for dynamic fields (such as persona output, product quotes, or scraped competitor data) before they are injected into HTML strings.
