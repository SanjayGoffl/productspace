## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-05-18 - [Fix XSS in Persona Card Rendering]
**Vulnerability:** XSS vulnerability through lack of input sanitization in LLM output data
**Learning:** JSON parsing of LLM outputs does not prevent malicious script injections in vanilla JS frontends. Fields such as persona name, product chosen, and quote must still be explicitly sanitized with escapeHTML before interpolating into HTML strings.
**Prevention:** Always wrap untrusted data (even if originating from an LLM and parsed via JSON) with escapeHTML before inserting into the DOM. Numeric fields should be explicitly cast to string (e.g., `escapeHTML(String(value))`) to avoid errors.
