## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-10-24 - [LLM Output XSS in Persona Cards]
**Vulnerability:** XSS vulnerability through lack of input sanitization for LLM-generated JSON fields in `renderPersonaCard`.
**Learning:** LLM outputs, even when parsed as JSON, should be treated as untrusted user input. In this codebase, string properties like `data.persona`, `data.product_chosen`, and `data.quote` were being injected directly into `innerHTML` without sanitization.
**Prevention:** Always use the `escapeHTML` function on string fields originating from LLM responses before inserting them into `innerHTML`. Furthermore, as per the rules, apply fallbacks inside the function argument: `escapeHTML(data.emoji || '👤')`.
