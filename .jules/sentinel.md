## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-24 - [Unescaped Variable Interpolation in Vanilla JS Templates]
**Vulnerability:** Widespread Cross-Site Scripting (XSS) vulnerability due to direct template string interpolation of variables like `${data.persona}` directly into `.innerHTML` assignments in vanilla JS.
**Learning:** Even when reading data directly from APIs or state objects, vanilla JS doesn't automatically escape variables inserted into template literals. If these template literals are later used in `.innerHTML` assignments, any malicious HTML or script tag within the variable payload will be executed in the client's browser.
**Prevention:** Consistently use an explicit `escapeHTML()` wrapper around all dynamic string insertions within template literals that will be assigned to DOM manipulation methods capable of interpreting HTML (e.g., `innerHTML`). Additionally, when using short-circuit fallbacks (e.g. `data.emoji || '👤'`), the fallback logic must be performed *inside* the `escapeHTML` call so that null/undefined isn't passed to the string manipulation functions.
