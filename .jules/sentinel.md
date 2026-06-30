## 2026-05-18 - [Missing escapeHTML function]
**Vulnerability:** XSS vulnerability through lack of input sanitization
**Learning:** We need to sanitize user input when generating dynamic HTML directly in client-side code to prevent Cross-Site Scripting (XSS).
**Prevention:** Implement and use an escapeHTML function to sanitize text input before inserting it into innerHTML.

## 2024-05-18 - [Missing escapeHTML definition in simulation rendering]
**Vulnerability:** XSS vulnerability through direct interpolation of unescaped variables using string templates and assignment to `innerHTML`.
**Learning:** `escapeHTML` works correctly when defined locally, but modifying DOM properties (like `element.id`) instead of `innerHTML` is inherently safe from XSS. However, explicitly injecting numbers (like `total` or `share`) as escaped strings doesn't provide significant benefit over directly using DOM properties, but it acts as defense-in-depth.
**Prevention:** Avoid assigning unescaped variables to `innerHTML`. Wrap them with an `escapeHTML` function or set properties like `textContent` explicitly.
