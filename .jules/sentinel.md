## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-18 - [LLM JSON to DOM XSS]
**Vulnerability:** XSS vulnerability by rendering raw JSON response values from an LLM directly into the DOM (e.g. innerHTML, attribute templates).
**Learning:** Even though the LLM response is expected to be a structured JSON object and not HTML, malicious user input (e.g. via prompt injection) could cause the LLM to output script tags in fields like `persona`, `product_chosen`, or `quote`.
**Prevention:** Relying solely on JSON structure parsing does not prevent DOM injection vulnerabilities. Fields derived from untrusted sources, including LLMs, must be explicitly sanitized using `escapeHTML` before string interpolation or innerHTML assignment.
