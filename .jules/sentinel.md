## 2024-05-24 - Double-Escaping for Inline Event Handlers
**Vulnerability:** XSS vulnerabilities in dynamically generated HTML via innerHTML where user input is placed inside inline event handlers (like onclick) and regular HTML text.
**Learning:** Browsers decode HTML entities before executing JavaScript in inline event handlers. Simply escaping HTML is not enough; if input contains single quotes, it can break out of the JS string context. Input must be double-escaped: first escape JavaScript string literal syntax, then escape HTML entities.
**Prevention:** Always use a helper `escapeJSString` and `escapeHTML` when dealing with `onclick="someFunction('input')"` patterns: e.g. `escapeHTML(escapeJSString(val))`. When placing input inside normal elements, use `escapeHTML(val)`.
