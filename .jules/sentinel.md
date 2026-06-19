## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2024-06-19 - [LLM-generated JSON XSS Prevention]
**Vulnerability:** XSS from unsanitized LLM-generated JSON outputs injected directly into innerHTML.
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends; fields such as persona or product_chosen must still be explicitly sanitized with escapeHTML. When using escapeHTML with a default fallback, apply the fallback inside the function argument (e.g., escapeHTML(data.emoji || '👤')) rather than chaining it outside, to explicitly handle null/undefined inputs before escaping.
**Prevention:** Explicitly sanitize all dynamic fields derived from LLM output (e.g. data.persona, data.product_chosen, data.quote, data.emoji) with escapeHTML before inserting into DOM via innerHTML.
