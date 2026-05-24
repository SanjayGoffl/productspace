## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.
## 2024-05-24 - Fix XSS in index.html innerHTML injections
**Vulnerability:** User-supplied strings (like product name, persona traits, competitor details) were injected directly into the DOM using `innerHTML` without HTML escaping in `index.html`.
**Learning:** This is a classic XSS vulnerability pattern where dynamic, externally-controlled strings are interpolated straight into HTML templates. Even if data seems safe, if it touches `innerHTML`, it must be escaped to prevent execution of arbitrary JS.
**Prevention:** Always use the provided `escapeHTML()` function (or standard native methods like `.textContent`) when injecting dynamic strings into `innerHTML` blocks.
