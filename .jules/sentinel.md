## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2026-09-04 - [Missing escapeHTML usage in Persona Card]
**Vulnerability:** XSS vulnerability through lack of sanitization of AI-generated inputs in innerHTML (Specifically in persona result rendering).
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends; fields such as persona or product_chosen must still be explicitly sanitized with escapeHTML when interpolating strings into innerHTML.
**Prevention:** Always explicitly wrap dynamic string concatenations with escapeHTML when assigning to innerHTML.
