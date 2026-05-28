## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2026-05-28 - [Unescaped Variable Interpolation in index.html]
**Vulnerability:** Multiple components rendered using innerHTML contained unsanitized object properties (e.g. `c.name`, `c.domain`), causing an XSS vulnerability when users add custom inputs manually.
**Learning:** Even internal helper methods rendering table bodies, chat boxes, and competitor grids are vulnerable to injection attacks if object properties representing user input are directly injected via template literals.
**Prevention:** Apply `escapeHTML()` string conversion proactively on all dynamically generated variables embedded inside `innerHTML` template strings.
