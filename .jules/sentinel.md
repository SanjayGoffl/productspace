## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-06-09 - [XSS via unescaped variables in innerHTML]
**Vulnerability:** XSS vulnerability through lack of input sanitization in innerHTML template literal.
**Learning:** Dynamic text, such as competitor name, domain, and price, passed directly into `innerHTML` without sanitization can execute arbitrary script if maliciously crafted.
**Prevention:** Use `escapeHTML` to sanitize all variables dynamically injected into `innerHTML` template literals to prevent Cross-Site Scripting (XSS).
