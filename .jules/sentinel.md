## 2025-04-11 - XSS Vulnerability in innerHTML rendering and Inline Event Handlers
**Vulnerability:** Found unescaped variables (e.g. `state.product.features`, `c.name`) directly rendered using `innerHTML` and inline event handlers (`onclick`) in `index.html`.
**Learning:** Browsers decode HTML entities before JavaScript execution for inline event handlers, so injecting user inputs into attributes like `onclick="..."` requires escaping both for JavaScript and HTML (double escaping: `escapeHTML(escapeJSString(val))`). Regular text content passed into `innerHTML` needs `escapeHTML(val)`.
**Prevention:** Always use appropriate escaping functions (`escapeHTML` and `escapeJSString`) when dynamically generating HTML strings and rendering them via `innerHTML`.
