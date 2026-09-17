## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-24 - [Unescaped values in index.html passed to innerHTML]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS), even when the data originates from seemingly safe sources like our API or AI backends.
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML, especially when interpolating values into template strings.
