## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-18 - XSS in persona card rendering
**Vulnerability:** XSS vulnerability in `index.html` where untrusted data (`data.persona`, `data.emoji`, `data.product_chosen`, `f`, `data.quote`) was directly interpolated into `innerHTML` inside `renderPersonaCard`.
**Learning:** Even structured JSON data from a backend or LLM can contain malicious payloads if the fields are manipulated or hallucinated. Relying solely on JSON structure parsing does not prevent malicious script injections in vanilla JS frontends.
**Prevention:** Always use `escapeHTML` (which should be natively defined or explicitly included) to sanitize all untrusted or dynamic data before concatenating it into strings used for `innerHTML`. Make sure to place fallbacks (e.g. `data.emoji || '👤'`) inside the `escapeHTML` argument.
