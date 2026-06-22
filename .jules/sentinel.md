## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-06-22 - [Persona Card XSS via innerHTML]
**Vulnerability:** DOM-based Cross-Site Scripting (XSS) in `index.html` via `innerHTML` injection of unsanitized LLM-generated data during persona card generation.
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends; fields such as `persona` or `product_chosen` must still be explicitly sanitized with `escapeHTML`. When using the custom `escapeHTML` function to sanitize data with a default fallback, apply the fallback inside the function argument (e.g., `escapeHTML(data.emoji || '👤')`) rather than chaining it outside, to explicitly handle null/undefined inputs before escaping.
**Prevention:** Always use `escapeHTML` for dynamic data bound to the DOM when generating HTML directly. Do not assume LLM outputs are "safe" text.
