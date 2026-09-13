## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.


## 2024-05-20 - [Fix XSS in Dynamic HTML Generation]
**Vulnerability:** XSS vulnerability through lack of input sanitization in dynamic HTML.
**Learning:** When generating HTML dynamically using string interpolation in JavaScript, all user-provided data must be properly sanitized with an escapeHTML function before insertion.
**Prevention:** Implemented and applied escapeHTML function to sanitize text input before inserting it into innerHTML across the frontend codebase.
