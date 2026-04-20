## 2024-05-15 - [XSS Vulnerability in Inline Event Handlers]
**Vulnerability:** XSS through unsanitized user inputs interpolated into inline event handlers in `index.html` via `innerHTML` (e.g., `<button onclick="removeFeature('${f}')">`).
**Learning:** Browsers decode HTML entities before executing JavaScript in inline event handlers. Simple HTML escaping is insufficient to prevent XSS in this context because an attacker can break out of the string literal if the input contains quotes that are only HTML-escaped.
**Prevention:** Always double-escape user input embedded in inline event handlers using both JS string escaping and HTML escaping (e.g., `escapeHTML(escapeJSString(input))`). Alternatively, avoid inline event handlers and use `addEventListener` with `data-` attributes.
