## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-14 - [XSS via unsanitized LLM output in dynamic HTML]
**Vulnerability:** XSS vulnerability through unsanitized LLM-generated output when creating DOM elements
**Learning:** Even LLM-generated outputs (like those passed into `innerHTML` or `id` attributes) can be vectors for XSS and DOM injection if untrusted or manipulated. Relying solely on JSON structure parsing does not prevent malicious script injections in fields like `persona`, `product_chosen`, or `quote`.
**Prevention:** Always wrap variables representing dynamic data, including LLM outputs, in `escapeHTML()` when interpolating them into HTML templates. Ensure fallbacks are applied inside the `escapeHTML` argument (e.g. `escapeHTML(data.emoji || '👤')`).
