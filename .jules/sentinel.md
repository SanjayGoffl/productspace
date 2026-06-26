## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-26 - [XSS via LLM JSON Output Interpolation]
**Vulnerability:** XSS vulnerability through direct interpolation of LLM-generated JSON payload properties (e.g., `persona`, `product_chosen`) into `innerHTML` within the vanilla JS frontend.
**Learning:** Relying purely on JSON parsing and LLM output structure formatting does not inherently mitigate XSS risks when rendering dynamic data to the DOM via vanilla JS. Fields populated by the LLM (like `persona`, `product_chosen`, `quote`, etc.) must still be explicitly sanitized as they can contain malicious scripts disguised as strings.
**Prevention:** Always explicitly sanitize LLM output fields and any other dynamically generated data using `escapeHTML` prior to string interpolation into `innerHTML`, even if the source data is a valid parsed JSON payload.
