## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2025-02-14 - Fix LLM Output XSS in Persona Cards
**Vulnerability:** XSS vulnerability in `renderPersonaCard` where dynamic data derived from LLM output (`data.persona`, `data.product_chosen`, `data.emoji`, etc.) was inserted using `innerHTML` without proper sanitization.
**Learning:** Even though LLM outputs are returned in JSON format, the values contained within them are not guaranteed to be safe for direct DOM insertion. Relying solely on JSON structure parsing does not prevent malicious script injections in vanilla JS frontends.
**Prevention:** All dynamic data (including third-party or LLM-generated data) must be explicitly sanitized before being rendered in the DOM via `innerHTML`. In vanilla JS, a robust sanitization function like `escapeHTML` should be applied to variables (e.g., `escapeHTML(data.field || '')`).
