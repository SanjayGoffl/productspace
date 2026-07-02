## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-05-18 - [Missing escapeHTML for synthetic persona data]
**Vulnerability:** XSS vulnerability through lack of input sanitization in synthetic persona evaluation results
**Learning:** LLM-generated output injected into HTML via `innerHTML` can introduce Cross-Site Scripting (XSS). Relying solely on JSON structure parsing does not prevent malicious script injections in vanilla JS frontends.
**Prevention:** Always apply the `escapeHTML` function to explicitly sanitize LLM outputs (e.g., persona names, quotes, product chosen) before injecting them into the DOM, even with safe fallbacks.
