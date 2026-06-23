## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-05-18 - [Missing escapeHTML function usage on LLM JSON outputs]
**Vulnerability:** XSS vulnerability through lack of input sanitization in LLM-generated content
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends. Fields such as persona, product_chosen, emoji, or quotes must still be explicitly sanitized before being rendered.
**Prevention:** Implement and use an escapeHTML function to explicitly sanitize any dynamic text input or LLM generated properties before interpolating it into innerHTML. When using escapeHTML with a default fallback, apply the fallback inside the function argument (e.g., escapeHTML(data.emoji || '👤')).
