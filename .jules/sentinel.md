## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-15 - Fixed DOM XSS in ProductScope Frontend
**Vulnerability:** Several parts of `index.html` were constructing HTML strings dynamically using template literals and directly appending them to the DOM via `innerHTML` without sanitizing variables. This exposed the application to Stored and Reflected DOM XSS via malicious product names, competitor names, domains, and personas.
**Learning:** Even internal toolings or simple vanilla JS applications are highly vulnerable if `innerHTML` is used for rendering untrusted strings. The provided custom `escapeHTML` function is a great utility but must be consistently applied wherever dynamic interpolations exist in HTML templates.
**Prevention:** Avoid `innerHTML` whenever possible, preferring `textContent` or `document.createElement`. When `innerHTML` is necessary (e.g. template rows), wrap every variable interpolation in a sanitization function like `escapeHTML`.
