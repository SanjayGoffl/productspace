## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2025-10-24 - [XSS vulnerabilities via innerHTML]
**Vulnerability:** XSS vulnerability through lack of input sanitization in client-side HTML generation using innerHTML.
**Learning:** Even internal API responses or generated data like persona names and quotes need to be sanitized because they can contain unexpected characters or malicious payloads.
**Prevention:** Always use the escapeHTML function to sanitize any text input/variables before inserting them into DOM elements via innerHTML.
