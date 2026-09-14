## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-15 - Relying on JSON structure parsing is insufficient to prevent XSS
**Vulnerability:** XSS vulnerabilities in the vanilla JS frontend due to unescaped rendering of dynamic data from LLM backends (like persona name, chosen product, etc.) directly into `innerHTML`.
**Learning:** Relying solely on JSON structure parsing for LLM outputs does not prevent malicious script injections in vanilla JS frontends. The parsed JSON values can still contain malicious HTML or Javascript payloads.
**Prevention:** Always explicitly sanitize all fields originating from LLM backends (e.g., `persona`, `product_chosen`) with functions like `escapeHTML` before dynamically inserting them into the DOM using methods like `innerHTML`.
