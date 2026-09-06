## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2025-02-28 - [Incomplete XSS mitigations with escapeHTML]
**Vulnerability:** XSS vulnerability through incomplete usage of `escapeHTML` on dynamic variables embedded via `innerHTML`.
**Learning:** `escapeHTML` was defined natively but not applied to all dynamic strings rendered using `innerHTML`, exposing components such as the persona grid, the chat history, and the tables. Relying solely on JSON structure does not stop XSS inside vanilla JS templates.
**Prevention:** Always wrap dynamically generated external or untrusted fields (like `persona`, `product_chosen`, `quote`, `emoji`, `text`) using `escapeHTML` before embedding them into `innerHTML`.
