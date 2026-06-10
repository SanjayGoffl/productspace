## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-24 - [Unescaped input in Client-Side Template Literals]
**Vulnerability:** XSS vulnerability through unescaped user inputs injected into `innerHTML` using template literals.
**Learning:** Even when `escapeHTML` and `escapeJSString` helper functions exist, they must be consistently applied to all user-provided data (e.g. `c.name`, `s.product.name`) interpolated into HTML strings that are subsequently assigned to `innerHTML`.
**Prevention:** Audit all usages of `.innerHTML = ` combined with template literals to ensure every interpolation of dynamic/user data is wrapped in `escapeHTML`.
