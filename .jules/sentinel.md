## 2025-05-29 - Fixed DOM-based XSS in index.html
**Vulnerability:** Unescaped variables (e.g. `c.name`, `s.id`) in string template literals assigned to `innerHTML`.
**Learning:** This codebase uses template strings for client-side rendering. There are custom JS functions (`escapeHTML`, `escapeJSString`) which must be used properly, especially to prevent escaping from both JS string arguments and HTML tags in inline handlers (`onclick`).
**Prevention:** Always wrap user-provided variables with `escapeHTML`. For inline event handler string arguments, wrap with `escapeHTML(escapeJSString(data))`.
